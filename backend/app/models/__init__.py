"""
Models Package - Import all models here for Alembic and Base.metadata.create_all()

All models must be imported here so SQLAlchemy registers them
with Base.metadata before table creation.
"""

from app.models.user import User
from app.models.subject import Subject
from app.models.topic import Topic
from app.models.knowledge_state import KnowledgeState
from app.models.learning_path import LearningPath
from app.models.session import Session
from app.models.test_result import TestResult
from app.models.weakness import WeaknessMap

__all__ = [
    "User",
    "Subject",
    "Topic",
    "KnowledgeState",
    "LearningPath",
    "Session",
    "TestResult",
    "WeaknessMap",
]
