import hashlib
import re

from sqlalchemy import Boolean, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, JSONType, TimestampMixin


def question_fingerprint(text: str) -> str:
    """Stable hash of a normalised question, used to block exact duplicates."""
    normalised = re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()
    return hashlib.sha256(normalised.encode("utf-8")).hexdigest()


class Question(TimestampMixin, Base):
    __tablename__ = "questions"

    # Human-readable stable ID from the seed file, e.g. "hr-001".
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    question: Mapped[str] = mapped_column(Text)
    question_hash: Mapped[str] = mapped_column(String(64), unique=True)
    category: Mapped[str] = mapped_column(String(40), index=True)
    subcategory: Mapped[str] = mapped_column(String(120), index=True)
    difficulty: Mapped[str] = mapped_column(String(20), index=True)
    question_type: Mapped[str] = mapped_column(String(16), default="technical")
    target_roles: Mapped[list] = mapped_column(JSONType, default=list)
    interview_stage: Mapped[list] = mapped_column(JSONType, default=list)
    reference_answer: Mapped[str] = mapped_column(Text)
    key_points: Mapped[list] = mapped_column(JSONType, default=list)
    evaluation_criteria: Mapped[list] = mapped_column(JSONType, default=list)
    common_mistakes: Mapped[list] = mapped_column(JSONType, default=list)
    follow_up_questions: Mapped[list] = mapped_column(JSONType, default=list)
    tags: Mapped[list] = mapped_column(JSONType, default=list)
    # Optional per-question rubric override (key of a row in `rubrics`).
    rubric_key: Mapped[str | None] = mapped_column(String(40))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)

    __table_args__ = (Index("ix_questions_category_difficulty", "category", "difficulty"),)
