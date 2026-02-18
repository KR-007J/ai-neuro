"""
Assessment Schemas
Pydantic models for cognitive assessments and evaluations
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum


class QuestionType(str, Enum):
    """Types of assessment questions"""
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    OPEN_ENDED = "open_ended"
    MATCHING = "matching"
    PRACTICAL = "practical"


class DifficultyLevel(str, Enum):
    """Content difficulty levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class AssessmentQuestion(BaseModel):
    """Individual assessment question"""
    question_id: str
    question_text: str
    question_type: QuestionType
    options: Optional[List[str]] = None
    correct_answer: Optional[str] = None  # For validation purposes
    difficulty: DifficultyLevel
    cognitive_domain: str  # e.g., "memory", "comprehension", "application"
    time_limit_seconds: Optional[int] = None


class AssessmentResponse(BaseModel):
    """User's response to an assessment question"""
    question_id: str
    user_answer: str
    time_taken_seconds: int
    confidence_level: Optional[int] = Field(None, ge=1, le=5)
    timestamp: datetime = Field(default_factory=datetime.now)


class AssessmentSubmission(BaseModel):
    """Complete assessment submission"""
    user_id: str
    assessment_id: str
    responses: List[AssessmentResponse]
    total_time_seconds: int
    submitted_at: datetime = Field(default_factory=datetime.now)


class AssessmentResult(BaseModel):
    """Assessment evaluation results"""
    assessment_id: str
    user_id: str
    score: float = Field(..., ge=0, le=100)
    correct_answers: int
    total_questions: int
    time_taken_seconds: int
    difficulty_level: DifficultyLevel
    cognitive_load_score: float = Field(..., ge=0, le=10)
    areas_of_strength: List[str] = []
    areas_for_improvement: List[str] = []
    recommended_next_level: Optional[DifficultyLevel] = None


class CognitiveProfile(BaseModel):
    """Comprehensive cognitive profile"""
    user_id: str
    learning_style: str  # VARK result
    learning_style_scores: Dict[str, float]  # Individual VARK scores
    cognitive_load_capacity: float = Field(..., ge=0, le=10)
    attention_span_minutes: int
    preferred_modality: str
    processing_speed: str  # "slow", "medium", "fast"
    working_memory_capacity: str  # "low", "medium", "high"
    strengths: List[str] = []
    weaknesses: List[str] = []
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)


class VARKAssessment(BaseModel):
    """VARK Learning Style Assessment"""
    user_id: str
    visual_score: float = Field(..., ge=0, le=1)
    auditory_score: float = Field(..., ge=0, le=1)
    reading_writing_score: float = Field(..., ge=0, le=1)
    kinesthetic_score: float = Field(..., ge=0, le=1)
    dominant_style: str
    secondary_style: Optional[str] = None
    is_multimodal: bool = False


class LearningAnalytics(BaseModel):
    """Real-time learning analytics"""
    user_id: str
    session_id: str
    engagement_score: float = Field(..., ge=0, le=1)
    focus_level: float = Field(..., ge=0, le=1)
    interaction_count: int = 0
    time_on_task_minutes: int = 0
    completion_rate: float = Field(..., ge=0, le=1)
    error_rate: float = Field(..., ge=0, le=1)
    help_requests: int = 0
    timestamp: datetime = Field(default_factory=datetime.now)
