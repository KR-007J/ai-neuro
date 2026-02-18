"""
Response Schemas
Standard API response models
"""

from pydantic import BaseModel
from typing import Optional, Any, List, Dict
from datetime import datetime


class StandardResponse(BaseModel):
    """Standard API response wrapper"""
    success: bool
    message: str
    data: Optional[Any] = None
    timestamp: datetime = datetime.now()


class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = False
    error: str
    error_code: Optional[str] = None
    details: Optional[Any] = None
    timestamp: datetime = datetime.now()


class ContentRecommendation(BaseModel):
    """Recommended learning content"""
    content_id: str
    title: str
    description: str
    content_type: str  # "video", "text", "interactive", "quiz"
    difficulty_level: str
    estimated_duration_minutes: int
    relevance_score: float
    learning_objectives: List[str] = []
    prerequisites: List[str] = []


class AdaptationResponse(BaseModel):
    """Response from adaptation engine"""
    user_id: str
    current_difficulty: str
    recommended_difficulty: str
    difficulty_changed: bool
    reasoning: str
    recommendations: List[ContentRecommendation]
    next_steps: List[str] = []


class LearningPath(BaseModel):
    """Personalized learning path"""
    path_id: str
    user_id: str
    title: str
    description: str
    total_modules: int
    estimated_completion_hours: int
    current_module: int
    completion_percentage: float
    modules: List[Dict[str, Any]]
    created_at: datetime
    last_updated: datetime
