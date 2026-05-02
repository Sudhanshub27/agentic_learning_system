"""
SQLAlchemy ORM Models - Learning Path

An ordered sequence of topics for a user within a subject.
Created by the Planner Agent, tracks progress through the curriculum.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, JSON, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class LearningPath(Base):
    """
    A user's personalized learning path through a subject.
    Contains an ordered list of topic IDs and tracks current position.
    """
    __tablename__ = "learning_paths"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    subject_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False
    )

    # Ordered list of topic IDs to learn
    topic_order: Mapped[list] = mapped_column(JSON, default=list)

    # Current position in the topic_order list
    current_index: Mapped[int] = mapped_column(Integer, default=0)

    # Path status
    status: Mapped[str] = mapped_column(
        String(20), default="active"  # active | completed | paused
    )

    # Strategy metadata from the Strategy Agent
    # e.g., {"difficulty_mode": "adaptive", "review_frequency": "every_3_topics"}
    strategy_config: Mapped[dict] = mapped_column(JSON, default=dict)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="learning_paths")
    subject: Mapped["Subject"] = relationship(back_populates="learning_paths")

    def __repr__(self) -> str:
        return (
            f"<LearningPath(user={self.user_id}, subject={self.subject_id}, "
            f"progress={self.current_index}/{len(self.topic_order)})>"
        )
