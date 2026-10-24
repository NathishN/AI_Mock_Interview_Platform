import uuid
from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field


class ResumeQuestionOut(BaseModel):
    id: str
    question: str
    category: str = "Resume & Projects"
    topic: str
    difficulty: str = "Intermediate"
    rubric_key: str = "technical"
    interviewer_context: str | None = None
    key_points: list[str] = Field(default_factory=list)
    ideal_answer_outline: str | None = None


class ResumeAnalysisOut(BaseModel):
    overview_summary: str
    ats_score: int
    ats_breakdown: dict[str, int] = Field(default_factory=dict)
    strengths: list[str] = Field(default_factory=list)
    flagged_risks: list[str] = Field(default_factory=list)
    recommended_focus_areas: list[str] = Field(default_factory=list)
    generated_questions: list[ResumeQuestionOut] = Field(default_factory=list)


class ResumeParsedDataOut(BaseModel):
    candidate_name: str | None = "Candidate"
    skills: dict[str, list[str]] = Field(default_factory=dict)
    projects: list[dict[str, Any]] = Field(default_factory=list)
    experience: list[dict[str, Any]] = Field(default_factory=list)
    education: list[dict[str, Any]] = Field(default_factory=list)


class ResumeDetailOut(BaseModel):
    id: uuid.UUID
    filename: str
    file_type: str
    file_size_bytes: int
    raw_text: str
    target_role: str | None = None
    parsed_data: ResumeParsedDataOut
    analysis: ResumeAnalysisOut
    is_active: bool = True
    created_at: datetime

    class Config:
        from_attributes = True


class ResumeSummaryOut(BaseModel):
    id: uuid.UUID
    filename: str
    file_type: str
    file_size_bytes: int
    target_role: str | None = None
    ats_score: int | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class ResumeTextUploadIn(BaseModel):
    raw_text: str
    filename: str = "pasted_resume.txt"
    target_role: str = "Software Development Engineer"


class StartResumeInterviewIn(BaseModel):
    num_questions: int = 5
    target_role: str = "Software Development Engineer"
    company: str = "Target Tech Company"


class EvaluateResumeQuestionIn(BaseModel):
    question_id: str
    question_text: str
    answer_text: str
    target_role: str | None = None
    rubric_key: str = "technical"
