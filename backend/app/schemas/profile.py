import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.enums import TargetRole


def _clean_list(values: list[str] | None, max_items: int, max_len: int) -> list[str] | None:
    if values is None:
        return None
    seen: list[str] = []
    for item in values:
        item = item.strip()
        if not item:
            continue
        if len(item) > max_len:
            raise ValueError(f"Items must be at most {max_len} characters")
        if item not in seen:
            seen.append(item)
    if len(seen) > max_items:
        raise ValueError(f"At most {max_items} items allowed")
    return seen


class ProfileUpdate(BaseModel):
    """Every field optional; only fields actually sent are changed."""

    degree: str | None = Field(default=None, max_length=120)
    branch: str | None = Field(default=None, max_length=120)
    graduation_year: int | None = Field(default=None, ge=2000, le=2100)
    target_role: TargetRole | None = None
    preferred_companies: list[str] | None = None
    interview_experience: str | None = Field(default=None, max_length=40)
    weak_areas: list[str] | None = None
    preferred_language: str | None = Field(default=None, max_length=40)
    daily_prep_minutes: int | None = Field(default=None, ge=5, le=600)
    interview_goals: str | None = Field(default=None, max_length=2000)
    full_name: str | None = Field(default=None, min_length=1, max_length=120)

    @field_validator("preferred_companies")
    @classmethod
    def _companies(cls, v):
        return _clean_list(v, 20, 80)

    @field_validator("weak_areas")
    @classmethod
    def _weak(cls, v):
        return _clean_list(v, 20, 80)


class ProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    full_name: str = ""
    degree: str | None
    branch: str | None
    graduation_year: int | None
    target_role: str | None
    preferred_companies: list[str]
    interview_experience: str | None
    weak_areas: list[str]
    preferred_language: str | None
    daily_prep_minutes: int | None
    interview_goals: str | None
    onboarding_completed: bool
    updated_at: datetime
