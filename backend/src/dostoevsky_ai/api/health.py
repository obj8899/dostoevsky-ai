"""Application and local Ollama health endpoint."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from dostoevsky_ai.services.ollama_client import (
    OllamaClient,
    OllamaConnectivity,
)

router = APIRouter()


class HealthResponse(BaseModel):
    """Health of the API process and its optional local model service."""

    status: str
    ollama: OllamaConnectivity


def get_ollama_client() -> OllamaClient:
    """Dependency provider kept replaceable for tests."""
    return OllamaClient()


@router.get("/health", response_model=HealthResponse)
def read_health(
    ollama_client: OllamaClient = Depends(get_ollama_client),
) -> HealthResponse:
    connectivity = ollama_client.check_connectivity()
    service_ready = (
        connectivity.status == "connected"
        and connectivity.model_available is True
    )
    return HealthResponse(
        status="ok" if service_ready else "degraded",
        ollama=connectivity,
    )

