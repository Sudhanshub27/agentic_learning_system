"""
Pydantic Schemas - Session & Learning

Request/response models for sessions and learning interactions.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SessionCreate(BaseModel):
    """Schema for starting a new learning session."""
    user_id: str = Field(..., description="ID of the user starting the session")
    subject_id: Optional[str] = Field(
        None, description="Optional: specific subject to focus on"
    )


class SessionResponse(BaseModel):
    """Schema for session API responses."""
    id: str
    user_id: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    loop_count: int
    current_phase: str
    topics_covered: list
    performance_summary: dict
    status: str

    model_config = {"from_attributes": True}


class SubjectCreate(BaseModel):
    """Schema for requesting a new subject to learn."""
    name: str = Field(
        ..., min_length=1, max_length=200,
        description="What you want to learn, e.g., 'Constitutional Law', 'Python', 'Organic Chemistry'"
    )
    description: str = Field(
        default="",
        description="Optional details about what aspects to focus on"
    )
    current_knowledge: str = Field(
        default="none",
        description="Current knowledge: none | basic | intermediate | advanced"
    )
    goal: str = Field(
        default="",
        description="Specific goal, e.g., 'prepare for exam', 'build projects'"
    )


class SubjectResponse(BaseModel):
    """Schema for subject API responses."""
    id: str
    name: str
    description: str
    domain: str
    category: str
    is_generated: bool
    topic_count: int = 0
    created_at: datetime

    model_config = {"from_attributes": True}


class TopicResponse(BaseModel):
    """Schema for topic API responses."""
    id: str
    subject_id: str
    name: str
    description: str
    difficulty_level: int
    order_index: int
    content_type: str
    learning_objectives: list
    estimated_minutes: int

    model_config = {"from_attributes": True}


class AnswerSubmission(BaseModel):
    """Schema for submitting an answer during TEST phase."""
    session_id: str
    question_id: str
    answer: str | dict = Field(
        ..., description="User's answer — string for text, dict for structured"
    )
    time_taken_seconds: Optional[int] = Field(
        None, description="How long the user took to answer"
    )


class ProgressResponse(BaseModel):
    """Schema for user progress dashboard."""
    user_id: str
    total_subjects: int
    total_topics_mastered: int
    total_topics_in_progress: int
    overall_mastery: float  # Average across all topics
    total_sessions: int
    total_study_time_minutes: int
    weaknesses: list[dict]
    strengths: list[dict]
    recent_activity: list[dict]
