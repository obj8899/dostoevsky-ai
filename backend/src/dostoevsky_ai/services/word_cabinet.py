"""Structured Word Cabinet generation and output validation."""

import json
from typing import Any

from pydantic import ValidationError

from dostoevsky_ai.prompts.word_cabinet import (
    WORD_CABINET_SYSTEM_PROMPT,
    build_word_cabinet_prompt,
)
from dostoevsky_ai.schemas.word_cabinet import (
    WordCabinetEntry,
    WordCabinetGeneration,
)
from dostoevsky_ai.services.ollama_client import OllamaClient

WORD_CABINET_NUM_PREDICT = 1400


class WordCabinetOutputError(Exception):
    """The model did not return usable structured vocabulary."""

    def __init__(
        self,
        category: str,
        *,
        response_chars: int,
        done_reason: str | None,
    ) -> None:
        super().__init__(category)
        self.category = category
        self.response_chars = response_chars
        self.done_reason = done_reason


def parse_word_cabinet_output(
    response_text: str,
    *,
    requested_count: int,
    done: bool,
    done_reason: str | None,
) -> tuple[list[WordCabinetEntry], list[str]]:
    """Parse JSON, retain valid unique entries, and explain any output issues."""
    try:
        payload: Any = json.loads(response_text)
    except json.JSONDecodeError:
        raise WordCabinetOutputError(
            "json_parse_failed",
            response_chars=len(response_text),
            done_reason=done_reason,
        ) from None

    if not isinstance(payload, dict) or not isinstance(payload.get("words"), list):
        raise WordCabinetOutputError(
            "invalid_root_schema",
            response_chars=len(response_text),
            done_reason=done_reason,
        )

    entries: list[WordCabinetEntry] = []
    seen_words: set[str] = set()
    discarded_invalid = 0
    discarded_duplicate = 0

    for raw_entry in payload["words"]:
        try:
            entry = WordCabinetEntry.model_validate(raw_entry)
        except (ValidationError, TypeError):
            discarded_invalid += 1
            continue

        normalized_word = entry.word.casefold()
        if normalized_word in seen_words:
            discarded_duplicate += 1
            continue
        seen_words.add(normalized_word)
        entries.append(entry)

    reason = (done_reason or "").casefold()
    is_truncated = (not done) or any(
        marker in reason for marker in ("length", "token", "limit", "max")
    )

    if not entries and is_truncated:
        raise WordCabinetOutputError(
            "truncated_no_entries",
            response_chars=len(response_text),
            done_reason=done_reason,
        )

    warnings: list[str] = []
    if len(entries) > requested_count:
        extra_count = len(entries) - requested_count
        entries = entries[:requested_count]
        warnings.append(
            f"{extra_count} extra vocabulary "
            f"{'entry was' if extra_count == 1 else 'entries were'} excluded."
        )
    if discarded_invalid:
        warnings.append(
            f"{discarded_invalid} invalid vocabulary "
            f"{'entry was' if discarded_invalid == 1 else 'entries were'} discarded."
        )
    if discarded_duplicate:
        warnings.append(
            f"{discarded_duplicate} duplicate vocabulary "
            f"{'entry was' if discarded_duplicate == 1 else 'entries were'} discarded."
        )
    if len(entries) < requested_count:
        warnings.append(
            f"The model returned {len(entries)} usable "
            f"{'entry' if len(entries) == 1 else 'entries'}; "
            f"{requested_count} requested."
        )

    if is_truncated:
        warnings.append(
            "The response may be incomplete because generation stopped at a limit."
        )

    return entries, warnings


class WordCabinetService:
    """Generates structured vocabulary using the configured Ollama model."""

    def __init__(self, ollama_client: OllamaClient | None = None) -> None:
        self.ollama_client = ollama_client or OllamaClient()

    def suggest(
        self,
        *,
        context: str,
        count: int,
    ) -> tuple[list[WordCabinetEntry], list[str]]:
        generated = self.ollama_client.generate(
            prompt=build_word_cabinet_prompt(context, count),
            system=WORD_CABINET_SYSTEM_PROMPT,
            format=WordCabinetGeneration.model_json_schema(),
            num_predict=WORD_CABINET_NUM_PREDICT,
        )
        return parse_word_cabinet_output(
            generated.response,
            requested_count=count,
            done=generated.done,
            done_reason=generated.done_reason,
        )
