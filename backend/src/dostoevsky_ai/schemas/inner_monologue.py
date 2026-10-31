"""Validated Inner Monologue request and response schemas."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


Perspective = Literal["first_person", "third_person"]


class InnerMonologueRequest(BaseModel):
    """Scenario and length/perspective controls for monologue generation."""

    scenario: str = Field(min_length=1, max_length=2000)
    perspective: Perspective = "first_person"
    min_words: int = Field(default=180, strict=True, ge=50, le=500)
    max_words: int = Field(default=250, strict=True, ge=50, le=500)

    @field_validator("scenario")
    @classmethod
    def require_non_whitespace_scenario(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Scenario must contain at least one non-whitespace character.")
        return value

    @model_validator(mode="after")
    def require_valid_word_range(self) -> "InnerMonologueRequest":
        if self.max_words < self.min_words:
            raise ValueError("max_words must be greater than or equal to min_words.")
        return self


class InnerMonologueResponse(BaseModel):
    """Generated monologue and measurable length/completion metadata."""

    scenario: str
    generated_text: str
    word_count: int
    requested_min_words: int
    requested_max_words: int
    within_requested_range: bool
    model: str
    validation_warnings: list[str]
