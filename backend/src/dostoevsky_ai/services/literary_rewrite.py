"""Validation and orchestration for Literary Rewrite generation."""

from dostoevsky_ai.config import Settings, get_settings
from dostoevsky_ai.prompts.literary_rewrite import (
    LITERARY_REWRITE_SYSTEM_PROMPT,
    build_literary_rewrite_prompt,
)
from dostoevsky_ai.services.ollama_client import OllamaClient


class EmptyModelOutputError(Exception):
    """The model returned no usable prose."""


def validate_generated_output(
    text: str,
    *,
    done: bool,
    done_reason: str | None,
) -> tuple[str, int, list[str]]:
    """Normalize output, count whitespace-delimited words, and flag likely truncation."""
    rewritten_text = text.strip()
    if not rewritten_text:
        raise EmptyModelOutputError

    word_count = len(rewritten_text.split())
    reason = (done_reason or "").casefold()
    warnings = []
    if not done or any(
        marker in reason for marker in ("length", "token", "limit", "max")
    ):
        warnings.append(
            "The response may be incomplete because generation stopped at a limit."
        )
    return rewritten_text, word_count, warnings


class LiteraryRewriteService:
    """Connects the feature prompt to the configured local Ollama client."""

    def __init__(
        self,
        *,
        settings: Settings | None = None,
        ollama_client: OllamaClient | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.ollama_client = ollama_client or OllamaClient(self.settings)

    def rewrite(self, source_text: str) -> tuple[str, int, list[str]]:
        generated = self.ollama_client.generate(
            prompt=build_literary_rewrite_prompt(source_text),
            system=LITERARY_REWRITE_SYSTEM_PROMPT,
        )
        return validate_generated_output(
            generated.response,
            done=generated.done,
            done_reason=generated.done_reason,
        )
