import uuid
from sqlalchemy import Boolean, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, JSONType, TimestampMixin


class UserResume(TimestampMixin, Base):
    """User-uploaded resume, parsed metadata, analysis, and targeted interview questions."""

    __tablename__ = "user_resumes"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    filename: Mapped[str] = mapped_column(String(255))
    file_type: Mapped[str] = mapped_column(String(20), default="pdf")
    file_size_bytes: Mapped[int] = mapped_column(Integer, default=0)
    raw_text: Mapped[str] = mapped_column(Text)
    target_role: Mapped[str | None] = mapped_column(String(120))
    
    # Parsed structure: skills, projects, experience, education
    parsed_data: Mapped[dict] = mapped_column(JSONType, default=dict)
    
    # Analysis & Questions: ATS score, strengths, flagged risks, focus areas, generated questions
    analysis: Mapped[dict] = mapped_column(JSONType, default=dict)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user = relationship("User", back_populates="resumes")
