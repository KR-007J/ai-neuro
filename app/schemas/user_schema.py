"""
User Schemas
Pydantic models for user-related data validation
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, List
from datetime import datetime
from enum import Enum


class LearningStyle(str, Enum):
    """VARK Learning Styles"""
    VISUAL = "visual"
    AUDITORY = "auditory"
    READING_WRITING = "reading_writing"
    KINESTHETIC = "kinesthetic"
    MULTIMODAL = "multimodal"


class UserPreferences(BaseModel):
    """User learning preferences"""
    preferred_time_of_day: Optional[str] = None
    session_duration: Optional[int] = 30  # minutes
    notification_enabled: bool = True
    difficulty_preference: Optional[str] = "adaptive"


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    full_name: str
    age: Optional[int] = Field(None, ge=5, le=120)
    education_level: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=8)


class UserResponse(UserBase):
    """Schema for user response"""
    user_id: str
    learning_style: Optional[LearningStyle] = None
    cognitive_profile: Optional[Dict] = None
    preferences: Optional[UserPreferences] = None
    created_at: datetime
    last_active: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Schema for updating user information"""
    full_name: Optional[str] = None
    age: Optional[int] = Field(None, ge=5, le=120)
    education_level: Optional[str] = None
    preferences: Optional[UserPreferences] = None


class UserStats(BaseModel):
    """User learning statistics"""
    user_id: str
    total_sessions: int = 0
    total_time_minutes: int = 0
    completed_modules: int = 0
    average_score: float = 0.0
    engagement_score: float = 0.0
    learning_streak_days: int = 0
    achievements: List[str] = []
