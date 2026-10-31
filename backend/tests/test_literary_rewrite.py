"""Literary Rewrite endpoint and output validation tests."""

import httpx
import pytest
from fastapi.testclient import TestClient

from dostoevsky_ai.api.features.literary_rewrite import (
    MAX_INPUT_LENGTH,
)
from dostoevsky_ai.main import app
from dostoevsky_ai.prompts.literary_rewrite import (
    LITERARY_REWRITE_SYSTEM_PROMPT,
)
from dostoevsky_ai.services.literary_rewrite import validate_generated_output


def mock_ollama(monkeypatch, payload: object) -> list[dict[str, object]]:
    requests: list[dict[str, object]] = []

    class FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> object:
            return payload

    class FakeClient:
        def __init__(self, *, timeout: httpx.Timeout) -> None:
            assert timeout.connect == 5.0
            assert timeout.read == 180.0

        def __enter__(self) -> "FakeClient":
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def post(self, url: str, *, json: dict[str, object]) -> FakeResponse:
            requests.append({"url": url, **json})
            return FakeResponse()

    monkeypatch.setattr(httpx, "Client", FakeClient)
    return requests


def test_rewrite_returns_output_and_uses_configured_ollama_request(
    monkeypatch,
) -> None:
    requests = mock_ollama(
        monkeypatch,
        {"response": "He paused, ashamed of his certainty.", "done": True},
    )

    response = TestClient(app).post(
        "/api/features/literary-rewrite",
        json={"text": "He was sure he had done the right thing."},
    )

    assert response.status_code == 200
    assert response.json() == {
        "original_text": "He was sure he had done the right thing.",
        "rewritten_text": "He paused, ashamed of his certainty.",
        "word_count": 6,
        "model": "dostoevsky-baseline:latest",
        "validation_warnings": [],
    }
    assert requests[0]["url"] == "http://localhost:11434/api/generate"
    assert requests[0]["model"] == "dostoevsky-baseline:latest"
    assert requests[0]["stream"] is False
    assert "He was sure he had done the right thing." in str(requests[0]["prompt"])
    assert requests[0]["system"] == LITERARY_REWRITE_SYSTEM_PROMPT


@pytest.mark.parametrize("text", ["", "   \t\n"])
def test_rewrite_rejects_empty_or_whitespace_input(text: str) -> None:
    response = TestClient(app).post(
        "/api/features/literary-rewrite",
        json={"text": text},
    )

    assert response.status_code == 422


def test_rewrite_rejects_input_above_maximum_length() -> None:
    response = TestClient(app).post(
        "/api/features/literary-rewrite",
        json={"text": "x" * (MAX_INPUT_LENGTH + 1)},
    )

    assert response.status_code == 422


def test_rewrite_reports_ollama_unavailable(monkeypatch) -> None:
    class UnavailableClient:
        def __init__(self, *, timeout: httpx.Timeout) -> None:
            pass

        def __enter__(self) -> "UnavailableClient":
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def post(self, url: str, *, json: dict[str, object]) -> None:
            request = httpx.Request("POST", url)
            raise httpx.ConnectError("private connection detail", request=request)

    monkeypatch.setattr(httpx, "Client", UnavailableClient)
    response = TestClient(app).post(
        "/api/features/literary-rewrite",
        json={"text": "The room was quiet."},
    )

    assert response.status_code == 503
    assert "private connection detail" not in response.text


def test_rewrite_reports_ollama_http_failure(monkeypatch) -> None:
    class FailedResponse:
        def raise_for_status(self) -> None:
            request = httpx.Request("POST", "http://localhost:11434/api/generate")
            response = httpx.Response(500, request=request)
            raise httpx.HTTPStatusError(
                "private server detail",
                request=request,
                response=response,
            )

    class FailedClient:
        def __init__(self, *, timeout: httpx.Timeout) -> None:
            pass

        def __enter__(self) -> "FailedClient":
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def post(self, url: str, *, json: dict[str, object]) -> FailedResponse:
            return FailedResponse()

    monkeypatch.setattr(httpx, "Client", FailedClient)
    response = TestClient(app).post(
        "/api/features/literary-rewrite",
        json={"text": "The room was quiet."},
    )

    assert response.status_code == 502
    assert "private server detail" not in response.text


def test_rewrite_reports_ollama_timeout(monkeypatch) -> None:
    class TimedOutClient:
        def __init__(self, *, timeout: httpx.Timeout) -> None:
            assert timeout.read == 180.0

        def __enter__(self) -> "TimedOutClient":
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def post(self, url: str, *, json: dict[str, object]) -> None:
            request = httpx.Request("POST", url)
            raise httpx.ReadTimeout("private timeout detail", request=request)

    monkeypatch.setattr(httpx, "Client", TimedOutClient)
    response = TestClient(app).post(
        "/api/features/literary-rewrite",
        json={"text": "The room was quiet."},
    )

    assert response.status_code == 504
    assert "private timeout detail" not in response.text


def test_rewrite_reports_invalid_ollama_json(monkeypatch) -> None:
    class InvalidJsonResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> object:
            raise ValueError("private response detail")

    class InvalidJsonClient:
        def __init__(self, *, timeout: httpx.Timeout) -> None:
            pass

        def __enter__(self) -> "InvalidJsonClient":
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def post(
            self,
            url: str,
            *,
            json: dict[str, object],
        ) -> InvalidJsonResponse:
            return InvalidJsonResponse()

    monkeypatch.setattr(httpx, "Client", InvalidJsonClient)
    response = TestClient(app).post(
        "/api/features/literary-rewrite",
        json={"text": "The room was quiet."},
    )

    assert response.status_code == 502
    assert "private response detail" not in response.text


def test_rewrite_rejects_empty_model_response(monkeypatch) -> None:
    mock_ollama(monkeypatch, {"response": " \n ", "done": True})

    response = TestClient(app).post(
        "/api/features/literary-rewrite",
        json={"text": "The room was quiet."},
    )

    assert response.status_code == 502
    assert "empty response" in response.json()["detail"]


def test_rewrite_warns_when_generation_stops_at_length_limit(monkeypatch) -> None:
    mock_ollama(
        monkeypatch,
        {
            "response": "He began to explain, but the thought",
            "done": True,
            "done_reason": "length",
        },
    )

    response = TestClient(app).post(
        "/api/features/literary-rewrite",
        json={"text": "He began to explain."},
    )

    assert response.status_code == 200
    assert response.json()["validation_warnings"] == [
        "The response may be incomplete because generation stopped at a limit."
    ]


def test_word_count_uses_whitespace_delimited_tokens() -> None:
    result = validate_generated_output(
        "  One\tquiet\nthought.  ",
        done=True,
        done_reason="stop",
    )

    assert result == ("One\tquiet\nthought.", 3, [])


def test_rewrite_flags_unfinished_generation() -> None:
    result = validate_generated_output(
        "The unfinished sentence",
        done=False,
        done_reason=None,
    )

    assert result[1] == 3
    assert result[2]
