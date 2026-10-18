import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    Boolean,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, JSONType, TimestampMixin
from app.models.enums import SessionStatus, TurnStatus


class InterviewSession(TimestampMixin, Base):
    """One mock interview. State lives here so a refresh never loses progress."""

    __tablename__ = "interview_sessions"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    status: Mapped[str] = mapped_column(
        String(20), default=SessionStatus.IN_PROGRESS.value, index=True
    )
    # role, company, stage, difficulty, duration, question count, mode, source, preset
    config: Mapped[dict] = mapped_column(JSONType, default=dict)
    # Adaptive-difficulty bookkeeping (running level, vagueness streak, ...).
    adaptive_state: Mapped[dict] = mapped_column(JSONType, default=dict)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    final_score: Mapped[float | None] = mapped_column(Float)
    report: Mapped[dict | None] = mapped_column(JSONType)

    turns: Mapped[list["InterviewTurn"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="InterviewTurn.sequence",
    )


class InterviewTurn(TimestampMixin, Base):
    """A question, the candidate's answer, and its evaluation."""

    __tablename__ = "interview_turns"
    __table_args__ = (UniqueConstraint("session_id", "sequence", name="uq_turn_sequence"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("interview_sessions.id", ondelete="CASCADE"), index=True
    )
    sequence: Mapped[int] = mapped_column(Integer)
    question_id: Mapped[str | None] = mapped_column(
        ForeignKey("questions.id", ondelete="SET NULL")
    )  # NULL for AI-generated and follow-up questions
    parent_turn_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("interview_turns.id", ondelete="SET NULL")
    )
    question_text: Mapped[str] = mapped_column(Text)
    is_follow_up: Mapped[bool] = mapped_column(Boolean, default=False)
    rubric_key: Mapped[str | None] = mapped_column(String(40))
    difficulty: Mapped[str | None] = mapped_column(String(20))
    topic: Mapped[str | None] = mapped_column(String(120))

    answer_text: Mapped[str | None] = mapped_column(Text)
    answered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    status: Mapped[str] = mapped_column(String(24), default=TurnStatus.ASKED.value)
    evaluation: Mapped[dict | None] = mapped_column(JSONType)
    overall_score: Mapped[float | None] = mapped_column(Float, index=True)

    # Observability. Error text only, never the candidate's answer.
    eval_model: Mapped[str | None] = mapped_column(String(80))
    eval_latency_ms: Mapped[int | None] = mapped_column(Integer)
    eval_prompt_tokens: Mapped[int | None] = mapped_column(Integer)
    eval_completion_tokens: Mapped[int | None] = mapped_column(Integer)
    eval_attempts: Mapped[int] = mapped_column(Integer, default=0)
    eval_error: Mapped[str | None] = mapped_column(String(500))

    session: Mapped[InterviewSession] = relationship(back_populates="turns")


class HRAnswerDraft(TimestampMixin, Base):
    """Personal answer builder: the user's own facts and their edited answer."""

    __tablename__ = "hr_answer_drafts"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    topic: Mapped[str] = mapped_column(String(120))
    facts: Mapped[dict] = mapped_column(JSONType, default=dict)  # user-supplied only
    generated_answer: Mapped[str | None] = mapped_column(Text)
    final_answer: Mapped[str | None] = mapped_column(Text)
