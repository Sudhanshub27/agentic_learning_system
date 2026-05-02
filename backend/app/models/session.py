"""
SQLAlchemy ORM Models - Session

Represents a single learning session. A session contains
one or more iterations of the PLAN→TEACH→TEST→ANALYZE→ADAPT loop.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, DateTime, JSON, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Session(Base):
    """
    A learning session — one continuous period of study.
    Tracks which topics were covered and overall performance.
    """
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # Session timing
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    ended_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # How many loop iterations completed
    loop_count: Mapped[int] = mapped_column(Integer, default=0)

    # Current phase in the loop (for resuming interrupted sessions)
    current_phase: Mapped[str] = mapped_column(
        String(20), default="plan"
        # plan | teach | test | analyze | adapt | memory_update | completed
    )

    # Summary data
    topics_covered: Mapped[list] = mapped_column(JSON, default=list)
    performance_summary: Mapped[dict] = mapped_column(JSON, default=dict)

    # Session status
    status: Mapped[str] = mapped_column(
        String(20), default="active"  # active | paused | completed
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="sessions")
    test_results: Mapped[list["TestResult"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"<Session(id={self.id}, user={self.user_id}, "
            f"phase={self.current_phase}, loops={self.loop_count})>"
        )
