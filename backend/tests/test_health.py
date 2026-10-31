"""Health endpoint tests using mocked Ollama HTTP responses."""

import httpx
from fastapi.testclient import TestClient

from dostoevsky_ai.main import app


def test_health_reports_ollama_and_configured_model(monkeypatch) -> None:
    class FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, list[dict[str, str]]]:
            return {"models": [{"name": "dostoevsky-baseline:latest"}]}

    class FakeClient:
        def __init__(self, *, timeout: httpx.Timeout) -> None:
            assert timeout.connect is not None

        def __enter__(self) -> "FakeClient":
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def get(self, url: str) -> FakeResponse:
            assert url == "http://localhost:11434/api/tags"
            return FakeResponse()

    monkeypatch.setattr(httpx, "Client", FakeClient)

    response = TestClient(app).get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "ollama": {
            "status": "connected",
            "model": "dostoevsky-baseline:latest",
            "model_available": True,
            "error": None,
        },
    }


def test_health_degrades_when_ollama_is_unavailable(monkeypatch) -> None:
    class FakeClient:
        def __init__(self, *, timeout: httpx.Timeout) -> None:
            assert timeout.connect is not None

        def __enter__(self) -> "FakeClient":
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def get(self, url: str) -> httpx.Response:
            request = httpx.Request("GET", url)
            raise httpx.ConnectError("connection refused", request=request)

    monkeypatch.setattr(httpx, "Client", FakeClient)

    response = TestClient(app).get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "degraded",
        "ollama": {
            "status": "unavailable",
            "model": "dostoevsky-baseline:latest",
            "model_available": None,
            "error": "Could not connect to the local Ollama service.",
        },
    }



def test_cors_allows_localhost_origin() -> None:
    client = TestClient(app)
    response = client.get(
        "/api/health",
        headers={"Origin": "http://localhost:5173"},
    )
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"


def test_cors_allows_127_0_0_1_origin() -> None:
    client = TestClient(app)
    response = client.get(
        "/api/health",
        headers={"Origin": "http://127.0.0.1:5173"},
    )
    assert response.headers.get("access-control-allow-origin") == "http://127.0.0.1:5173"


def test_cors_rejects_unapproved_origin() -> None:
    client = TestClient(app)
    response = client.get(
        "/api/health",
        headers={"Origin": "http://unapproved.example.com"},
    )
    assert "access-control-allow-origin" not in response.headers


def test_cors_preflight_options_for_features() -> None:
    client = TestClient(app)
    for origin in ("http://localhost:5173", "http://127.0.0.1:5173"):
        response = client.options(
            "/api/features/literary-rewrite",
            headers={
                "Origin": origin,
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type",
            },
        )
        assert response.status_code == 200
        assert response.headers.get("access-control-allow-origin") == origin
        assert "POST" in response.headers.get("access-control-allow-methods", "")
