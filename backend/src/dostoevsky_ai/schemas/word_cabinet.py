"""Validated Word Cabinet request and response schemas."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


PartOfSpeech = Literal["noun", "verb", "adjective", "adverb", "phrase"]


class WordCabinetEntry(BaseModel):
    """One structured vocabulary suggestion."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    word: str = Field(min_length=1, max_length=80)
    part_of_speech: PartOfSpeech
    definition: str = Field(min_length=1, max_length=500)
    connotation: str = Field(min_length=1, max_length=500)
    intensity: int = Field(strict=True, ge=1, le=5)
    distinction: str = Field(min_length=1, max_length=500)
    example: str = Field(min_length=1, max_length=500)

    @field_validator("word", "definition", "connotation", "distinction", "example")
    @classmethod
    def require_non_whitespace_value(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("This field must contain non-whitespace text.")
        return value


class WordCabinetGeneration(BaseModel):
    """Schema requested from Ollama for JSON-constrained generation."""

    words: list[WordCabinetEntry]


class WordCabinetRequest(BaseModel):
    """Context and requested number of vocabulary suggestions."""

    context: str = Field(min_length=1, max_length=2000)
    count: int = Field(default=6, strict=True, ge=3, le=8)

    @field_validator("context")
    @classmethod
    def require_non_whitespace_context(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Context must contain at least one non-whitespace character.")
        return value


class WordCabinetResponse(BaseModel):
    """Structured vocabulary response with generation metadata."""

    context: str
    words: list[WordCabinetEntry]
    model: str
    validation_warnings: list[str]
