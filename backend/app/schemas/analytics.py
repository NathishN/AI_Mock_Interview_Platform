from pydantic import BaseModel, Field


class AnalyticsOverview(BaseModel):
    total_sessions: int
    completed_sessions: int
    total_questions_answered: int
    average_score: float
    readiness_score: float = Field(ge=0.0, le=100.0)
    current_streak_days: int
    performance_band: str


class SkillScore(BaseModel):
    category: str
    score: float
    total_evaluated: int


class ScoreHistoryPoint(BaseModel):
    session_id: str
    date: str
    role: str
    score: float


class WeakAreaItem(BaseModel):
    topic: str
    category: str
    frequency: int
    average_score: float
    recommendation: str
