"""
SQLAlchemy ORM Models - Weakness Map

Tracks specific areas where a user struggles.
Goes deeper than KnowledgeState — identifies *what kind*
of weakness (conceptual, application, syntax, etc.)
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class WeaknessMap(Base):
    """
    Identifies specific weaknesses for a user on a topic.
    e.g., "User understands list syntax but struggles with
    list comprehension with conditionals"
    """
    __tablename__ = "weakness_maps"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    topic_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )

    # Type of weakness detected by the Analyzer Agent
    weakness_type: Mapped[str] = mapped_column(
        String(30), default="conceptual"
        # conceptual | application | syntax | reasoning | recall
    )

    # Detailed description from the Analyzer Agent
    description: Mapped[str] = mapped_column(Text, default="")

    # How many times this weakness has been detected
    occurrence_count: Mapped[int] = mapped_column(Integer, default=1)

    # Whether this weakness has been resolved
    is_resolved: Mapped[bool] = mapped_column(default=False)

    first_detected: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    last_detected: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="weaknesses")
    topic: Mapped["Topic"] = relationship(back_populates="weaknesses")

    def __repr__(self) -> str:
        return (
            f"<WeaknessMap(user={self.user_id}, topic={self.topic_id}, "
            f"type={self.weakness_type}, count={self.occurrence_count})>"
        )
