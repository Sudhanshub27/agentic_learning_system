"""
Pydantic Schemas - User

Request/response models for user-related API endpoints.
Separated from SQLAlchemy models for clean API contracts.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    name: str = Field(..., min_length=1, max_length=100, description="User's display name")
    email: Optional[str] = Field(None, description="Optional email for persistence")
    goals: list[str] = Field(
        default_factory=list,
        description="Learning goals, e.g., ['Master Python', 'Learn ML']"
    )
    current_level: str = Field(
        default="beginner",
        description="Self-assessed level: beginner | intermediate | advanced"
    )
    preferences: dict = Field(
        default_factory=dict,
        description="Learning preferences, e.g., {'pace': 'moderate'}"
    )


class UserResponse(BaseModel):
    """Schema for user API responses."""
    id: str
    name: str
    email: Optional[str] = None
    goals: dict
    preferences: dict
    current_level: str
    is_active: bool
    created_at: datetime
    last_active: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    """Schema for updating user profile."""
    name: Optional[str] = None
    goals: Optional[list[str]] = None
    current_level: Optional[str] = None
    preferences: Optional[dict] = None
