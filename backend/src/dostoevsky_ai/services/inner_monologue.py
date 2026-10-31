"""Inner Monologue generation and output validation."""

from dostoevsky_ai.config import Settings, get_settings
from dostoevsky_ai.prompts.inner_monologue import (
    INNER_MONOLOGUE_SYSTEM_PROMPT,
    build_inner_monologue_prompt,
)
from dostoevsky_ai.schemas.inner_monologue import (
    Perspective,
)
from dostoevsky_ai.services.ollama_client import OllamaClient

# 500 English words commonly need well under 1,000 output tokens, but tokenization
# varies; 1,400 leaves headroom for punctuation and prose without changing the model.
INNER_MONOLOGUE_NUM_PREDICT = 1400


class EmptyMonologueOutputError(Exception):
    """The model returned no usable monologue text."""


def validate_monologue_output(
    text: str,
    *,
    min_words: int,
    max_words: int,
    done: bool,
    done_reason: str | None,
) -> tuple[str, int, bool, list[str]]:
    """Count whitespace-delimited words and report length/completion deviations."""
    generated_text = text.strip()
    if not generated_text:
        raise EmptyMonologueOutputError

    word_count = len(generated_text.split())
    within_requested_range = min_words <= word_count <= max_words
    warnings: list[str] = []
    if word_count < min_words:
        warnings.append(
            f"The response contains {word_count} whitespace-delimited words; "
            f"the requested minimum is {min_words}."
        )
    elif word_count > max_words:
        warnings.append(
            f"The response contains {word_count} whitespace-delimited words; "
            f"the requested maximum is {max_words}."
        )

    reason = (done_reason or "").casefold()
    if not done or any(
        marker in reason for marker in ("length", "token", "limit", "max")
    ):
        warnings.append(
            "The response may be incomplete because generation stopped at a limit."
        )
    return generated_text, word_count, within_requested_range, warnings


class InnerMonologueService:
    """Generates a monologue with the configured local Ollama model."""

    def __init__(
        self,
        *,
        settings: Settings | None = None,
        ollama_client: OllamaClient | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.ollama_client = ollama_client or OllamaClient(self.settings)

    def generate(
        self,
        *,
        scenario: str,
        perspective: Perspective,
        min_words: int,
        max_words: int,
    ) -> tuple[str, int, bool, list[str]]:
        generated = self.ollama_client.generate(
            prompt=build_inner_monologue_prompt(
                scenario,
                perspective=perspective,
                min_words=min_words,
                max_words=max_words,
            ),
            system=INNER_MONOLOGUE_SYSTEM_PROMPT,
            num_predict=INNER_MONOLOGUE_NUM_PREDICT,
        )
        return validate_monologue_output(
            generated.response,
            min_words=min_words,
            max_words=max_words,
            done=generated.done,
            done_reason=generated.done_reason,
        )
