"""Literary Rewrite endpoint and request/response schemas."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator

from dostoevsky_ai.config import Settings, get_settings
from dostoevsky_ai.prompts.literary_rewrite import (
    LITERARY_REWRITE_SYSTEM_PROMPT,
    build_literary_rewrite_prompt,
)
from dostoevsky_ai.services.literary_rewrite import (
    EmptyModelOutputError,
    LiteraryRewriteService,
)
from dostoevsky_ai.services.ollama_client import (
    OllamaClient,
    OllamaRequestError,
    OllamaTimeoutError,
    OllamaUnavailableError,
)

router = APIRouter()
MAX_INPUT_LENGTH = 5000


class LiteraryRewriteRequest(BaseModel):
    """Source prose submitted for transformation."""

    text: str = Field(min_length=1, max_length=MAX_INPUT_LENGTH)

    @field_validator("text")
    @classmethod
    def require_non_whitespace_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Text must contain at least one non-whitespace character.")
        return value


class LiteraryRewriteResponse(BaseModel):
    """Transformed prose and transparent output metadata."""

    original_text: str
    rewritten_text: str
    word_count: int
    model: str
    validation_warnings: list[str]


def get_literary_rewrite_service() -> LiteraryRewriteService:
    return LiteraryRewriteService(settings=get_settings())


@router.post(
    "/features/literary-rewrite",
    response_model=LiteraryRewriteResponse,
)
def rewrite_literary_text(
    request: LiteraryRewriteRequest,
    service: LiteraryRewriteService = Depends(get_literary_rewrite_service),
) -> LiteraryRewriteResponse:
    try:
        rewritten_text, word_count, warnings = service.rewrite(request.text)
    except OllamaTimeoutError:
        raise HTTPException(
            status_code=504,
            detail="The local model took too long to complete the rewrite. Please try again.",
        ) from None
    except OllamaUnavailableError:
        raise HTTPException(
            status_code=503,
            detail="The local Ollama service is unavailable. Check that Ollama is running and try again.",
        ) from None
    except OllamaRequestError:
        raise HTTPException(
            status_code=502,
            detail="The local model could not complete the rewrite. Please try again.",
        ) from None
    except EmptyModelOutputError:
        raise HTTPException(
            status_code=502,
            detail="The local model returned an empty response. Please try again.",
        ) from None

    settings: Settings = get_settings()
    return LiteraryRewriteResponse(
        original_text=request.text,
        rewritten_text=rewritten_text,
        word_count=word_count,
        model=settings.ollama_model,
        validation_warnings=warnings,
    )
