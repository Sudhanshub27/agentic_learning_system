"""
SQLAlchemy ORM Models - Knowledge State

Tracks a user's mastery of each topic.
This is the core of the adaptive learning system —
the mastery_score drives all agent decisions.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class KnowledgeState(Base):
    """
    Per-user, per-topic mastery tracking.
    mastery_score (0.0 to 1.0) is updated after every test using
    an exponential moving average for smooth progression.
    """
    __tablename__ = "knowledge_states"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    topic_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )

    # Core mastery score: 0.0 (no knowledge) to 1.0 (fully mastered)
    mastery_score: Mapped[float] = mapped_column(Float, default=0.0)

    # Tracking attempts for learning curve analysis
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    successes: Mapped[int] = mapped_column(Integer, default=0)

    # Current streak (consecutive correct answers)
    streak: Mapped[int] = mapped_column(Integer, default=0)

    # Learning status
    status: Mapped[str] = mapped_column(
        String(20), default="not_started"
        # not_started | learning | reviewing | mastered
    )

    last_tested: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="knowledge_states")
    topic: Mapped["Topic"] = relationship(back_populates="knowledge_states")

    def __repr__(self) -> str:
        return (
            f"<KnowledgeState(user={self.user_id}, topic={self.topic_id}, "
            f"mastery={self.mastery_score:.2f}, status={self.status})>"
        )
