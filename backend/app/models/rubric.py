from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, JSONType, TimestampMixin


class Rubric(TimestampMixin, Base):
    """Configurable scoring rubric. `dimensions` is a list of {name, weight}
    whose weights must sum to 100 (enforced in the schema and the bootstrap)."""

    __tablename__ = "rubrics"

    key: Mapped[str] = mapped_column(String(40), primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    dimensions: Mapped[list] = mapped_column(JSONType)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
