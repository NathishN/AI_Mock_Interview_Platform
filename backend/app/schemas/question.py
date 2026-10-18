import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.enums import Difficulty, InterviewStage, QuestionCategory, QuestionType

ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_-]{2,63}$")

_DEFAULT_TYPE = {
    QuestionCategory.HR: QuestionType.HR,
    QuestionCategory.BEHAVIORAL: QuestionType.HR,
    QuestionCategory.COMPANY_WORKPLACE: QuestionType.HR,
    QuestionCategory.CODING: QuestionType.CODING,
}


def _clean_required_list(values: list[str], field: str) -> list[str]:
    cleaned = [v.strip() for v in values if v and v.strip()]
    if not cleaned:
        raise ValueError(f"{field} must contain at least one non-empty item")
    return cleaned


def _clean_optional_list(values: list[str]) -> list[str]:
    return [v.strip() for v in values if v and v.strip()]


class QuestionBase(BaseModel):
    question: str = Field(min_length=10, max_length=1000)
    category: QuestionCategory
    subcategory: str = Field(min_length=2, max_length=120)
    difficulty: Difficulty
    question_type: QuestionType | None = None
    target_roles: list[str]
    interview_stage: list[InterviewStage]
    reference_answer: str = Field(min_length=50)
    key_points: list[str]
    evaluation_criteria: list[str]
    common_mistakes: list[str] = []
    follow_up_questions: list[str] = []
    tags: list[str] = []
    rubric_key: str | None = Field(default=None, max_length=40)

    @field_validator("question", "subcategory", "reference_answer")
    @classmethod
    def _strip(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Must not be blank")
        return v

    @field_validator("target_roles")
    @classmethod
    def _roles(cls, v):
        return _clean_required_list(v, "target_roles")

    @field_validator("key_points")
    @classmethod
    def _key_points(cls, v):
        return _clean_required_list(v, "key_points")

    @field_validator("evaluation_criteria")
    @classmethod
    def _criteria(cls, v):
        return _clean_required_list(v, "evaluation_criteria")

    @field_validator("interview_stage")
    @classmethod
    def _stages(cls, v):
        if not v:
            raise ValueError("interview_stage must contain at least one stage")
        return list(dict.fromkeys(v))

    @field_validator("common_mistakes", "follow_up_questions")
    @classmethod
    def _optional_lists(cls, v):
        return _clean_optional_list(v)

    @field_validator("tags")
    @classmethod
    def _tags(cls, v):
        return list(dict.fromkeys(t.strip().lower() for t in v if t and t.strip()))

    @model_validator(mode="after")
    def _default_type(self):
        if self.question_type is None:
            self.question_type = _DEFAULT_TYPE.get(self.category, QuestionType.TECHNICAL)
        return self


class QuestionCreate(QuestionBase):
    id: str

    @field_validator("id")
    @classmethod
    def _id(cls, v: str) -> str:
        v = v.strip().lower()
        if not ID_PATTERN.match(v):
            raise ValueError("id must be 3-64 chars of a-z, 0-9, '-' or '_'")
        return v


class QuestionUpdate(BaseModel):
    """Partial update; validated by re-running QuestionBase on the merged record."""

    model_config = ConfigDict(extra="forbid")

    question: str | None = None
    category: QuestionCategory | None = None
    subcategory: str | None = None
    difficulty: Difficulty | None = None
    question_type: QuestionType | None = None
    target_roles: list[str] | None = None
    interview_stage: list[InterviewStage] | None = None
    reference_answer: str | None = None
    key_points: list[str] | None = None
    evaluation_criteria: list[str] | None = None
    common_mistakes: list[str] | None = None
    follow_up_questions: list[str] | None = None
    tags: list[str] | None = None
    rubric_key: str | None = None
    is_active: bool | None = None


class QuestionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    question: str
    category: str
    subcategory: str
    difficulty: str
    question_type: str
    target_roles: list[str]
    interview_stage: list[str]
    reference_answer: str
    key_points: list[str]
    evaluation_criteria: list[str]
    common_mistakes: list[str]
    follow_up_questions: list[str]
    tags: list[str]
    rubric_key: str | None
    is_active: bool
    updated_at: datetime


class QuestionPage(BaseModel):
    items: list[QuestionOut]
    total: int
    page: int
    page_size: int


class QuestionSummary(BaseModel):
    total: int
    by_category: dict[str, int]
    by_difficulty: dict[str, int]


class ImportError_(BaseModel):
    index: int
    id: str | None
    errors: list[str]


class ImportResult(BaseModel):
    ok: bool
    created: int = 0
    updated: int = 0
    skipped: int = 0
    total_in_file: int = 0
    errors: list[ImportError_] = []


class ImportRequest(BaseModel):
    questions: list[dict] = Field(min_length=1, max_length=1000)
