"""Inner Monologue endpoint."""

from fastapi import APIRouter, Depends, HTTPException

from dostoevsky_ai.config import get_settings
from dostoevsky_ai.schemas.inner_monologue import (
    InnerMonologueRequest,
    InnerMonologueResponse,
)
from dostoevsky_ai.services.inner_monologue import (
    EmptyMonologueOutputError,
    InnerMonologueService,
)
from dostoevsky_ai.services.ollama_client import (
    OllamaRequestError,
    OllamaTimeoutError,
    OllamaUnavailableError,
)

router = APIRouter()


def get_inner_monologue_service() -> InnerMonologueService:
    return InnerMonologueService()


@router.post(
    "/features/inner-monologue",
    response_model=InnerMonologueResponse,
)
def create_inner_monologue(
    request: InnerMonologueRequest,
    service: InnerMonologueService = Depends(get_inner_monologue_service),
) -> InnerMonologueResponse:
    try:
        (
            generated_text,
            word_count,
            within_requested_range,
            warnings,
        ) = service.generate(
            scenario=request.scenario,
            perspective=request.perspective,
            min_words=request.min_words,
            max_words=request.max_words,
        )
    except OllamaTimeoutError:
        raise HTTPException(
            status_code=504,
            detail="The local model took too long to write the monologue. Please try again.",
        ) from None
    except OllamaUnavailableError:
        raise HTTPException(
            status_code=503,
            detail="The local Ollama service is unavailable. Check that Ollama is running and try again.",
        ) from None
    except OllamaRequestError:
        raise HTTPException(
            status_code=502,
            detail="The local model could not complete the monologue. Please try again.",
        ) from None
    except EmptyMonologueOutputError:
        raise HTTPException(
            status_code=502,
            detail="The local model returned an empty monologue. Please try again.",
        ) from None

    return InnerMonologueResponse(
        scenario=request.scenario,
        generated_text=generated_text,
        word_count=word_count,
        requested_min_words=request.min_words,
        requested_max_words=request.max_words,
        within_requested_range=within_requested_range,
        model=get_settings().ollama_model,
        validation_warnings=warnings,
    )
