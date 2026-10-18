from pydantic import BaseModel, Field


class CompanyRoundInfo(BaseModel):
    round_number: int
    name: str
    stage: str
    duration_minutes: int
    description: str
    focus_areas: list[str]


class CompanyOverview(BaseModel):
    id: str
    name: str
    slug: str
    logo_letter: str
    category: str  # Product, IT Services, FinTech, Global Capability Center
    difficulty: str
    hiring_rounds: int
    description: str
    rounds: list[CompanyRoundInfo] = Field(default_factory=list)
    key_tips: list[str] = Field(default_factory=list)
    recommended_question_categories: list[str] = Field(default_factory=list)
