"""Inner Monologue API and output validation tests."""

import httpx
import pytest
from fastapi.testclient import TestClient

from dostoevsky_ai.main import app
from dostoevsky_ai.prompts.inner_monologue import (
    INNER_MONOLOGUE_SYSTEM_PROMPT,
)
from dostoevsky_ai.services.inner_monologue import (
    INNER_MONOLOGUE_NUM_PREDICT,
    validate_monologue_output,
)


def make_words(count: int) -> str:
    return " ".join(f"word{index}" for index in range(count))


def mock_ollama(monkeypatch, text: str, *, done: bool = True, reason: str = "stop"):
    requests: list[dict[str, object]] = []

    class FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return {
                "response": text,
                "done": done,
                "done_reason": reason,
            }

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


def post_monologue(
    *,
    scenario: str = "A student feels guilty about a small success.",
    perspective: str = "first_person",
    min_words: int = 50,
    max_words: int = 80,
):
    return TestClient(app).post(
        "/api/features/inner-monologue",
        json={
            "scenario": scenario,
            "perspective": perspective,
            "min_words": min_words,
            "max_words": max_words,
        },
    )


def test_inner_monologue_generates_first_person_with_configured_model_and_budget(
    monkeypatch,
) -> None:
    generated_text = "I " + make_words(54)
    requests = mock_ollama(monkeypatch, generated_text)

    response = post_monologue(
        perspective="first_person",
        min_words=50,
        max_words=60,
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["generated_text"] == generated_text
    assert payload["word_count"] == 55
    assert payload["within_requested_range"] is True
    assert payload["requested_min_words"] == 50
    assert payload["requested_max_words"] == 60
    assert payload["model"] == "dostoevsky-baseline:latest"
    assert payload["validation_warnings"] == []
    request = requests[0]
    assert request["url"] == "http://localhost:11434/api/generate"
    assert request["model"] == "dostoevsky-baseline:latest"
    assert request["stream"] is False
    assert request["options"] == {"num_predict": INNER_MONOLOGUE_NUM_PREDICT}
    assert "first-person narration" in str(request["prompt"])
    assert "preserve" in str(request["system"]).lower()
    assert request["system"] == INNER_MONOLOGUE_SYSTEM_PROMPT


def test_inner_monologue_generates_third_person(monkeypatch) -> None:
    generated_text = "She " + make_words(52)
    requests = mock_ollama(monkeypatch, generated_text)

    response = post_monologue(
        perspective="third_person",
        min_words=50,
        max_words=60,
    )

    assert response.status_code == 200
    assert response.json()["within_requested_range"] is True
    assert "third-person narration" in str(requests[0]["prompt"])


@pytest.mark.parametrize("scenario", ["", " \t\n"])
def test_inner_monologue_rejects_blank_scenario(scenario: str) -> None:
    response = TestClient(app).post(
        "/api/features/inner-monologue",
        json={"scenario": scenario},
    )

    assert response.status_code == 422


def test_inner_monologue_rejects_oversized_scenario() -> None:
    response = TestClient(app).post(
        "/api/features/inner-monologue",
        json={"scenario": "x" * 2001},
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    ("min_words", "max_words"),
    [(49, 100), (100, 49), (50, 501), (501, 501), (50.5, 100)],
)
def test_inner_monologue_rejects_invalid_word_ranges(
    min_words: object,
    max_words: object,
) -> None:
    response = TestClient(app).post(
        "/api/features/inner-monologue",
        json={
            "scenario": "A student considers whether to apologize.",
            "min_words": min_words,
            "max_words": max_words,
        },
    )

    assert response.status_code == 422


def test_inner_monologue_defaults_to_first_person_and_180_to_250_words(
    monkeypatch,
) -> None:
    generated_text = "I " + make_words(179)
    requests = mock_ollama(monkeypatch, generated_text)
    response = TestClient(app).post(
        "/api/features/inner-monologue",
        json={"scenario": "A person debates whether to apologize."},
    )

    assert response.status_code == 200
    assert response.json()["requested_min_words"] == 180
    assert response.json()["requested_max_words"] == 250
    assert "first-person narration" in str(requests[0]["prompt"])


def test_inner_monologue_rejects_empty_model_response(monkeypatch) -> None:
    mock_ollama(monkeypatch, "  \n ")

    response = post_monologue()

    assert response.status_code == 502
    assert "empty monologue" in response.json()["detail"]


def test_inner_monologue_returns_actual_below_minimum_with_warning(
    monkeypatch,
) -> None:
    generated_text = make_words(52)
    mock_ollama(monkeypatch, generated_text)

    response = post_monologue(min_words=60, max_words=80)

    assert response.status_code == 200
    payload = response.json()
    assert payload["generated_text"] == generated_text
    assert payload["word_count"] == 52
    assert payload["within_requested_range"] is False
    assert any("requested minimum is 60" in warning for warning in payload["validation_warnings"])


def test_inner_monologue_returns_actual_above_maximum_with_warning(
    monkeypatch,
) -> None:
    generated_text = make_words(52)
    mock_ollama(monkeypatch, generated_text)

    response = post_monologue(min_words=50, max_words=51)

    assert response.status_code == 200
    payload = response.json()
    assert payload["generated_text"] == generated_text
    assert payload["word_count"] == 52
    assert payload["within_requested_range"] is False
    assert any("requested maximum is 51" in warning for warning in payload["validation_warnings"])


def test_inner_monologue_warns_for_length_limited_generation(monkeypatch) -> None:
    generated_text = make_words(55)
    mock_ollama(monkeypatch, generated_text, reason="length")

    response = post_monologue()

    assert response.status_code == 200
    assert any(
        "generation stopped at a limit" in warning
        for warning in response.json()["validation_warnings"]
    )


def test_inner_monologue_counts_whitespace_delimited_words() -> None:
    text = "  One\tquiet\nthought.  "
    generated, count, within_range, warnings = validate_monologue_output(
        text,
        min_words=3,
        max_words=3,
        done=True,
        done_reason="stop",
    )

    assert generated == "One\tquiet\nthought."
    assert count == 3
    assert within_range is True
    assert warnings == []


def test_inner_monologue_reports_ollama_unavailable_without_details(
    monkeypatch,
) -> None:
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
    response = post_monologue()

    assert response.status_code == 503
    assert "private connection detail" not in response.text


def test_inner_monologue_reports_ollama_timeout(monkeypatch) -> None:
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
    response = post_monologue()

    assert response.status_code == 504
    assert "private timeout detail" not in response.text


def test_inner_monologue_reports_generation_http_failure(monkeypatch) -> None:
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
    response = post_monologue()

    assert response.status_code == 502
    assert "private server detail" not in response.text
