"""Word Cabinet API and output validation tests."""

import json

import httpx
import pytest
from fastapi.testclient import TestClient

from dostoevsky_ai.main import app
from dostoevsky_ai.schemas.word_cabinet import WordCabinetGeneration


def make_entry(word: str = "ambivalence") -> dict[str, object]:
    return {
        "word": word,
        "part_of_speech": "noun",
        "definition": "The coexistence of opposing feelings.",
        "connotation": "Often suggests unresolved emotional tension.",
        "intensity": 3,
        "distinction": "Unlike uncertainty, it involves two simultaneous attitudes.",
        "example": "Her ambivalence about leaving made the final goodbye slow.",
    }


def mock_ollama(monkeypatch, output: object) -> list[dict[str, object]]:
    requests: list[dict[str, object]] = []

    class FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return {
                "response": json.dumps(output),
                "done": True,
                "done_reason": "stop",
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


def post_context(text: str = "A conflicted feeling", count: int = 3):
    return TestClient(app).post(
        "/api/features/word-cabinet",
        json={"context": text, "count": count},
    )


def test_word_cabinet_returns_structured_response_and_requests_json_schema(
    monkeypatch,
) -> None:
    requests = mock_ollama(monkeypatch, {"words": [make_entry()]})

    response = post_context(count=3)

    assert response.status_code == 200
    assert response.json()["context"] == "A conflicted feeling"
    assert response.json()["model"] == "dostoevsky-baseline:latest"
    assert response.json()["words"] == [make_entry()]
    assert response.json()["validation_warnings"] == [
        "The model returned 1 usable entry; 3 requested."
    ]
    assert requests[0]["url"] == "http://localhost:11434/api/generate"
    assert requests[0]["model"] == "dostoevsky-baseline:latest"
    assert requests[0]["stream"] is False
    json_schema = requests[0]["format"]
    assert isinstance(json_schema, dict)
    assert json_schema == WordCabinetGeneration.model_json_schema()
    assert requests[0]["options"] == {"num_predict": 1400}
    assert "A conflicted feeling" in str(requests[0]["prompt"])


@pytest.mark.parametrize("context", ["", "   \t\n"])
def test_word_cabinet_rejects_empty_context(context: str) -> None:
    response = TestClient(app).post(
        "/api/features/word-cabinet",
        json={"context": context},
    )

    assert response.status_code == 422


def test_word_cabinet_rejects_context_above_maximum() -> None:
    response = TestClient(app).post(
        "/api/features/word-cabinet",
        json={"context": "x" * 2001},
    )

    assert response.status_code == 422


@pytest.mark.parametrize("count", [2, 9, 3.5])
def test_word_cabinet_rejects_invalid_count(count: object) -> None:
    response = TestClient(app).post(
        "/api/features/word-cabinet",
        json={"context": "A difficult emotion", "count": count},
    )

    assert response.status_code == 422


def test_word_cabinet_defaults_to_six_entries(monkeypatch) -> None:
    requests = mock_ollama(monkeypatch, {"words": [make_entry()]})
    response = TestClient(app).post(
        "/api/features/word-cabinet",
        json={"context": "A difficult emotion"},
    )

    assert response.status_code == 200
    assert '"requested_count": 6' in str(requests[0]["prompt"])


def test_word_cabinet_rejects_malformed_json_without_logging_output(
    monkeypatch,
    caplog,
) -> None:
    class FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return {
                "response": '{"words": [',
                "done": True,
                "done_reason": "stop",
            }

    class FakeClient:
        def __init__(self, *, timeout: httpx.Timeout) -> None:
            pass

        def __enter__(self) -> "FakeClient":
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def post(self, url: str, *, json: dict[str, object]) -> FakeResponse:
            return FakeResponse()

    monkeypatch.setattr(httpx, "Client", FakeClient)
    response = post_context()

    assert response.status_code == 502
    assert "invalid vocabulary response" in response.json()["detail"]
    assert '{"words": [' not in response.text
    assert "category=json_parse_failed" in caplog.text
    assert "A conflicted feeling" not in caplog.text
    assert '{"words": [' not in caplog.text


def test_word_cabinet_discards_entries_with_missing_fields(monkeypatch) -> None:
    invalid = {"word": "regret", "part_of_speech": "noun"}
    mock_ollama(monkeypatch, {"words": [make_entry(), invalid]})

    response = post_context()

    assert response.status_code == 200
    assert len(response.json()["words"]) == 1
    assert any("1 invalid vocabulary entry was discarded" in warning for warning in response.json()["validation_warnings"])


def test_word_cabinet_discards_invalid_intensity(monkeypatch) -> None:
    invalid_intensity = make_entry("anguish")
    invalid_intensity["intensity"] = 6
    mock_ollama(monkeypatch, {"words": [make_entry(), invalid_intensity]})

    response = post_context()

    assert response.status_code == 200
    assert [word["word"] for word in response.json()["words"]] == ["ambivalence"]
    assert any("invalid vocabulary entry was discarded" in warning for warning in response.json()["validation_warnings"])


def test_word_cabinet_discards_case_insensitive_duplicate_entries(monkeypatch) -> None:
    mock_ollama(
        monkeypatch,
        {"words": [make_entry("Remorse"), make_entry("remorse")]},
    )

    response = post_context(count=3)

    assert response.status_code == 200
    assert len(response.json()["words"]) == 1
    assert any("1 duplicate vocabulary entry was discarded" in warning for warning in response.json()["validation_warnings"])


def test_word_cabinet_returns_warning_when_fewer_entries_than_requested(
    monkeypatch,
) -> None:
    mock_ollama(monkeypatch, {"words": [make_entry(), make_entry("guilt")]})

    response = post_context(count=3)

    assert response.status_code == 200
    assert len(response.json()["words"]) == 2
    assert "The model returned 2 usable entries; 3 requested." in response.json()["validation_warnings"]


def test_word_cabinet_excludes_entries_above_requested_count(monkeypatch) -> None:
    mock_ollama(
        monkeypatch,
        {
            "words": [
                make_entry("remorse"),
                make_entry("regret"),
                make_entry("contrition"),
                make_entry("guilt"),
            ]
        },
    )

    response = post_context(count=3)

    assert response.status_code == 200
    assert [word["word"] for word in response.json()["words"]] == [
        "remorse",
        "regret",
        "contrition",
    ]
    assert "1 extra vocabulary entry was excluded." in response.json()["validation_warnings"]


def test_word_cabinet_reports_ollama_unavailable(monkeypatch) -> None:
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
    response = post_context()

    assert response.status_code == 503
    assert "private connection detail" not in response.text


def test_word_cabinet_reports_ollama_timeout(monkeypatch) -> None:
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
    response = post_context()

    assert response.status_code == 504
    assert "private timeout detail" not in response.text


def test_word_cabinet_returns_empty_words_array_when_model_returns_empty_words_list(
    monkeypatch,
) -> None:
    mock_ollama(monkeypatch, {"words": []})

    response = post_context(count=3)

    assert response.status_code == 200
    assert response.json()["words"] == []
    assert response.json()["validation_warnings"] == [
        "The model returned 0 usable entries; 3 requested."
    ]


def test_word_cabinet_returns_empty_words_array_when_all_entries_invalid(
    monkeypatch,
) -> None:
    invalid1 = {"word": "regret", "part_of_speech": "noun"}
    invalid2 = {"invalid": "shape"}
    mock_ollama(monkeypatch, {"words": [invalid1, invalid2]})

    response = post_context(count=3)

    assert response.status_code == 200
    assert response.json()["words"] == []
    warnings = response.json()["validation_warnings"]
    assert any("2 invalid vocabulary entries were discarded" in w for w in warnings)
    assert any("The model returned 0 usable entries; 3 requested." in w for w in warnings)


def test_word_cabinet_rejects_truncated_output_with_zero_entries(
    monkeypatch,
    caplog,
) -> None:
    class TruncatedZeroClient:
        def __init__(self, *, timeout: httpx.Timeout) -> None:
            pass

        def __enter__(self) -> "TruncatedZeroClient":
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def post(self, url: str, *, json: dict[str, object]):
            class FakeResponse:
                def raise_for_status(self) -> None:
                    return None

                def json(self) -> dict[str, object]:
                    return {
                        "response": '{"words": []}',
                        "done": False,
                        "done_reason": "length",
                    }

            return FakeResponse()

    monkeypatch.setattr(httpx, "Client", TruncatedZeroClient)
    response = post_context(count=3)

    assert response.status_code == 502
    assert "invalid vocabulary response" in response.json()["detail"]
    assert "category=truncated_no_entries" in caplog.text


def test_word_cabinet_preserves_partial_entries_when_truncated(
    monkeypatch,
) -> None:
    import json as _json

    class TruncatedPartialClient:
        def __init__(self, *, timeout: httpx.Timeout) -> None:
            pass

        def __enter__(self) -> "TruncatedPartialClient":
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def post(self, url: str, *, json: dict[str, object]):
            class FakeResponse:
                def raise_for_status(self) -> None:
                    return None

                def json(self) -> dict[str, object]:
                    return {
                        "response": _json.dumps({"words": [make_entry("dread")]}),
                        "done": False,
                        "done_reason": "length",
                    }

            return FakeResponse()

    monkeypatch.setattr(httpx, "Client", TruncatedPartialClient)
    response = post_context(count=3)

    assert response.status_code == 200
    assert len(response.json()["words"]) == 1
    assert response.json()["words"][0]["word"] == "dread"
    warnings = response.json()["validation_warnings"]
    assert any("The model returned 1 usable entry; 3 requested." in w for w in warnings)
    assert any("generation stopped at a limit" in w for w in warnings)
