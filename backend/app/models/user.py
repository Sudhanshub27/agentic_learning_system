"""
SQLAlchemy ORM Models - User

Represents a learner in the system. Stores profile info, goals,
preferences, and timestamps for activity tracking.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, DateTime, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class User(Base):
    """
    Core user model. Each learner has a profile with their goals,
    current skill assessment, and learning preferences.
    """
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True)

    # What the user wants to achieve (e.g., ["master Python", "learn ML basics"])
    goals: Mapped[dict] = mapped_column(JSON, default=dict)

    # Learning preferences (e.g., {"style": "visual", "pace": "moderate"})
    preferences: Mapped[dict] = mapped_column(JSON, default=dict)

    # Self-reported initial skill level
    current_level: Mapped[str] = mapped_column(
        String(20), default="beginner"  # beginner | intermediate | advanced
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    last_active: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    knowledge_states: Mapped[list["KnowledgeState"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    learning_paths: Mapped[list["LearningPath"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    sessions: Mapped[list["Session"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    weaknesses: Mapped[list["WeaknessMap"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name={self.name}, level={self.current_level})>"
