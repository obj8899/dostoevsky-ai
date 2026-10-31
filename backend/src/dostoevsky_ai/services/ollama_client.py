"""Small, non-generative Ollama connectivity check."""

from typing import Literal

import httpx
from pydantic import BaseModel

from dostoevsky_ai.config import Settings, get_settings


class OllamaConnectivity(BaseModel):
    """Connectivity and configured-model availability reported by Ollama."""

    status: Literal["connected", "unavailable"]
    model: str
    model_available: bool | None = None
    error: str | None = None


class OllamaGeneration(BaseModel):
    """Generated text and completion metadata returned by Ollama."""

    response: str
    done: bool
    done_reason: str | None = None


class OllamaUnavailableError(Exception):
    """The local Ollama service could not be reached."""


class OllamaTimeoutError(Exception):
    """Ollama did not finish within the configured generation timeout."""


class OllamaRequestError(Exception):
    """Ollama returned an invalid response or generation error."""


class OllamaClient:
    """Isolates the Ollama HTTP API from request handlers."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    def check_connectivity(self) -> OllamaConnectivity:
        """Read model tags without loading a model or generating text."""
        base_url = self.settings.ollama_base_url.rstrip("/")
        timeout = httpx.Timeout(self.settings.ollama_timeout_seconds)

        try:
            with httpx.Client(timeout=timeout) as client:
                response = client.get(f"{base_url}/api/tags")
                response.raise_for_status()
                payload = response.json()
        except httpx.TimeoutException:
            return OllamaConnectivity(
                status="unavailable",
                model=self.settings.ollama_model,
                error="Timed out while checking the local Ollama service.",
            )
        except httpx.HTTPError:
            return OllamaConnectivity(
                status="unavailable",
                model=self.settings.ollama_model,
                error="Could not connect to the local Ollama service.",
            )
        except ValueError:
            return OllamaConnectivity(
                status="unavailable",
                model=self.settings.ollama_model,
                error="Ollama returned an invalid tags response.",
            )

        models = payload.get("models") if isinstance(payload, dict) else None
        if not isinstance(models, list):
            return OllamaConnectivity(
                status="unavailable",
                model=self.settings.ollama_model,
                error="Ollama returned an unexpected tags response.",
            )

        model_available = any(
            isinstance(item, dict)
            and item.get("name") == self.settings.ollama_model
            for item in models
        )
        return OllamaConnectivity(
            status="connected",
            model=self.settings.ollama_model,
            model_available=model_available,
        )

    def generate(
        self,
        *,
        prompt: str,
        system: str,
        format: str | dict[str, object] | None = None,
        num_predict: int | None = None,
    ) -> OllamaGeneration:
        """Generate one non-streamed response using the configured local model."""
        timeout = httpx.Timeout(
            self.settings.ollama_generation_timeout_seconds,
            connect=5.0,
            write=10.0,
            pool=5.0,
        )
        base_url = self.settings.ollama_base_url.rstrip("/")

        try:
            with httpx.Client(timeout=timeout) as client:
                request_payload: dict[str, object] = {
                    "model": self.settings.ollama_model,
                    "prompt": prompt,
                    "system": system,
                    "stream": False,
                }
                if format is not None:
                    request_payload["format"] = format
                if num_predict is not None:
                    request_payload["options"] = {"num_predict": num_predict}
                response = client.post(
                    f"{base_url}/api/generate",
                    json=request_payload,
                )
                response.raise_for_status()
                payload = response.json()
        except httpx.TimeoutException:
            raise OllamaTimeoutError from None
        except httpx.ConnectError:
            raise OllamaUnavailableError from None
        except httpx.HTTPStatusError as error:
            if error.response.status_code == 404:
                raise OllamaUnavailableError from None
            raise OllamaRequestError from None
        except httpx.HTTPError:
            raise OllamaUnavailableError from None
        except ValueError:
            raise OllamaRequestError from None

        if not isinstance(payload, dict):
            raise OllamaRequestError

        generated_text = payload.get("response")
        done = payload.get("done")
        done_reason = payload.get("done_reason")
        if (
            not isinstance(generated_text, str)
            or not isinstance(done, bool)
            or (done_reason is not None and not isinstance(done_reason, str))
        ):
            raise OllamaRequestError

        return OllamaGeneration(
            response=generated_text,
            done=done,
            done_reason=done_reason,
        )
