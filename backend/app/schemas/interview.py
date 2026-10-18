import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class DimensionScore(BaseModel):
    name: str
    score: float = Field(ge=0.0, le=10.0)
    weight: float = Field(ge=0.0, le=100.0)
    justification: str


class EvaluationResult(BaseModel):
    overall_score: float = Field(ge=0.0, le=100.0)
    performance_band: str
    dimension_scores: list[DimensionScore]
    strengths: list[str] = Field(default_factory=list)
    missing_points: list[str] = Field(default_factory=list)
    mistakes: list[str] = Field(default_factory=list)
    clarity_feedback: str = ""
    ideal_answer: str = ""
    improved_answer: str = ""
    follow_up_question: str | None = None
    practice_recommendations: list[str] = Field(default_factory=list)


class InterviewTurnOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    session_id: uuid.UUID
    sequence: int
    question_id: str | None = None
    parent_turn_id: uuid.UUID | None = None
    question_text: str
    is_follow_up: bool = False
    rubric_key: str | None = None
    difficulty: str | None = None
    topic: str | None = None
    answer_text: str | None = None
    answered_at: datetime | None = None
    status: str
    evaluation: dict | None = None
    overall_score: float | None = None
    eval_latency_ms: int | None = None
    eval_error: str | None = None


class InterviewSessionCreate(BaseModel):
    target_role: str = "Software Development Engineer"
    company: str | None = None
    interview_stage: str = "Technical"
    difficulty: str = "Intermediate"
    duration_minutes: int = Field(default=30, ge=5, le=90)
    num_questions: int = Field(default=5, ge=1, le=15)
    mode: str = "mixed"  # technical, hr, behavioral, coding, mixed
    preset: str | None = None  # hr_round, final_interview, technical_interview, full_mock, weakness_improvement


class InterviewSessionSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    status: str
    config: dict
    started_at: datetime | None = None
    ended_at: datetime | None = None
    final_score: float | None = None
    created_at: datetime


class InterviewSessionDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    status: str
    config: dict
    adaptive_state: dict
    started_at: datetime | None = None
    ended_at: datetime | None = None
    final_score: float | None = None
    report: dict | None = None
    turns: list[InterviewTurnOut] = Field(default_factory=list)
    created_at: datetime


class AnswerSubmitIn(BaseModel):
    answer_text: str = Field(min_length=2, max_length=5000)


class ReportOut(BaseModel):
    session_id: uuid.UUID
    status: str
    final_score: float
    performance_band: str
    total_questions: int
    dimension_breakdown: list[dict]
    strengths: list[str]
    areas_for_improvement: list[str]
    practice_recommendations: list[str]
    turns: list[InterviewTurnOut]
