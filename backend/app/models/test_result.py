"""
SQLAlchemy ORM Models - Test Result

Stores every question asked, answer given, and score received.
This granular data feeds the Analyzer Agent for pattern detection.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, DateTime, JSON, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class TestResult(Base):
    """
    A single test question and its result.
    Stores the full question, user answer, correct answer,
    score, and detailed feedback for learning analytics.
    """
    __tablename__ = "test_results"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    session_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    topic_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )

    # Question type determines how it's graded
    question_type: Mapped[str] = mapped_column(
        String(20), default="mcq"  # mcq | short_answer | coding | true_false
    )

    # Full question content (including options for MCQ)
    question: Mapped[dict] = mapped_column(JSON, default=dict)

    # What the user answered
    user_answer: Mapped[dict] = mapped_column(JSON, default=dict)

    # The correct answer (for reference and feedback)
    correct_answer: Mapped[dict] = mapped_column(JSON, default=dict)

    # Score from 0.0 to 1.0
    score: Mapped[float] = mapped_column(Float, default=0.0)

    # Is this answer correct? (simplified boolean for quick queries)
    is_correct: Mapped[bool] = mapped_column(default=False)

    # Detailed feedback from the Evaluator Agent
    feedback: Mapped[dict] = mapped_column(JSON, default=dict)

    # Time taken to answer (in seconds, for analysis)
    time_taken_seconds: Mapped[Optional[int]] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    session: Mapped["Session"] = relationship(back_populates="test_results")
    topic: Mapped["Topic"] = relationship(back_populates="test_results")

    def __repr__(self) -> str:
        return (
            f"<TestResult(topic={self.topic_id}, type={self.question_type}, "
            f"score={self.score:.2f}, correct={self.is_correct})>"
        )
