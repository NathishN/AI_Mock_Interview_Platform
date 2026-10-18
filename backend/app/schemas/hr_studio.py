import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class HRTopicInfo(BaseModel):
    id: str
    title: str
    framework: str  # e.g., "Present -> Skills -> Projects -> Strengths -> Goals" or "STAR"
    description: str
    prompt_fields: list[dict]  # list of fields user should provide facts for


class HRStudioGenerateIn(BaseModel):
    topic: str
    facts: dict = Field(..., description="User's real facts key-value map")


class HRStudioAnalyzeIn(BaseModel):
    topic: str
    answer_text: str = Field(min_length=10, max_length=5000)


class HRAnalysisOut(BaseModel):
    score: float = Field(ge=0.0, le=100.0)
    strengths: list[str]
    vague_phrases: list[str]
    unsupported_claims: list[str]
    structure_feedback: str
    coaching_tips: list[str]


class HRDraftIn(BaseModel):
    topic: str
    facts: dict = Field(default_factory=dict)
    generated_answer: str | None = None
    final_answer: str = Field(min_length=1)


class HRDraftOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    topic: str
    facts: dict
    generated_answer: str | None = None
    final_answer: str | None = None
    created_at: datetime
    updated_at: datetime
