"""Word Cabinet endpoint."""

import logging

from fastapi import APIRouter, Depends, HTTPException

from dostoevsky_ai.config import get_settings
from dostoevsky_ai.schemas.word_cabinet import (
    WordCabinetRequest,
    WordCabinetResponse,
)
from dostoevsky_ai.services.ollama_client import (
    OllamaRequestError,
    OllamaTimeoutError,
    OllamaUnavailableError,
)
from dostoevsky_ai.services.word_cabinet import (
    WordCabinetOutputError,
    WordCabinetService,
)

router = APIRouter()
logger = logging.getLogger(__name__)


def get_word_cabinet_service() -> WordCabinetService:
    return WordCabinetService()


@router.post(
    "/features/word-cabinet",
    response_model=WordCabinetResponse,
)
def open_word_cabinet(
    request: WordCabinetRequest,
    service: WordCabinetService = Depends(get_word_cabinet_service),
) -> WordCabinetResponse:
    try:
        words, warnings = service.suggest(
            context=request.context,
            count=request.count,
        )
    except OllamaTimeoutError:
        raise HTTPException(
            status_code=504,
            detail="The local model took too long to prepare vocabulary. Please try again.",
        ) from None
    except OllamaUnavailableError:
        raise HTTPException(
            status_code=503,
            detail="The local Ollama service is unavailable. Check that Ollama is running and try again.",
        ) from None
    except OllamaRequestError:
        raise HTTPException(
            status_code=502,
            detail="The local model returned an invalid vocabulary response. Please try again.",
        ) from None
    except WordCabinetOutputError as error:
        done_reason = (
            error.done_reason
            if error.done_reason in {"stop", "length"}
            else "other" if error.done_reason else "unknown"
        )
        logger.warning(
            "Word Cabinet output rejected: category=%s response_chars=%d "
            "done_reason=%s",
            error.category,
            error.response_chars,
            done_reason,
        )
        raise HTTPException(
            status_code=502,
            detail="The local model returned an invalid vocabulary response. Please try again.",
        ) from None

    return WordCabinetResponse(
        context=request.context,
        words=words,
        model=get_settings().ollama_model,
        validation_warnings=warnings,
    )
