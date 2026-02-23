"""
Adaptation API Routes
Endpoints for adaptive learning and content recommendations
"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Optional
from pydantic import BaseModel
from app.schemas.response_schema import (
    StandardResponse, ContentRecommendation, AdaptationResponse, LearningPath
)
from app.core.adaptation_engine import AdaptationEngine
from app.core.recommendation_engine import RecommendationEngine
from app.services.gemini_service import generate_lesson_content, generate_quiz_feedback
from datetime import datetime
import uuid

router = APIRouter()

adaptation_engine    = AdaptationEngine()
recommendation_engine = RecommendationEngine()

MOCK_CONTENT = [
    {
        "content_id": "c001",
        "title": "Introduction to Python Programming",
        "description": "Learn Python basics with hands-on exercises",
        "content_type": "interactive",
        "difficulty_level": "beginner",
        "duration_minutes": 45,
        "primary_modality": "kinesthetic",
        "complexity_rating": 3,
        "learning_objectives": ["Variables", "Data Types", "Control Flow"],
        "prerequisites": []
    },
    {
        "content_id": "c002",
        "title": "Data Structures in Python",
        "description": "Master lists, dictionaries, and sets",
        "content_type": "video",
        "difficulty_level": "intermediate",
        "duration_minutes": 60,
        "primary_modality": "visual",
        "complexity_rating": 5,
        "learning_objectives": ["Lists", "Dictionaries", "Sets", "Tuples"],
        "prerequisites": ["c001"]
    },
    {
        "content_id": "c003",
        "title": "Object-Oriented Programming",
        "description": "Deep dive into OOP concepts",
        "content_type": "text",
        "difficulty_level": "intermediate",
        "duration_minutes": 90,
        "primary_modality": "reading_writing",
        "complexity_rating": 6,
        "learning_objectives": ["Classes", "Objects", "Inheritance", "Polymorphism"],
        "prerequisites": ["c002"]
    },
    {
        "content_id": "c004",
        "title": "Advanced Algorithms",
        "description": "Complex algorithmic problem solving",
        "content_type": "interactive",
        "difficulty_level": "advanced",
        "duration_minutes": 120,
        "primary_modality": "multimodal",
        "complexity_rating": 8,
        "learning_objectives": ["Dynamic Programming", "Graph Algorithms", "Greedy Algorithms"],
        "prerequisites": ["c003"]
    }
]


# ========================================
# Pydantic Request Models
# ========================================

class RecommendationRequest(BaseModel):
    user_id: str
    user_profile: Dict
    performance_history: List[float]
    completed_content: List[str] = []


class NextLessonRequest(BaseModel):
    user_id: str


class DifficultyAdjustRequest(BaseModel):
    user_id: str
    current_difficulty: str
    performance_history: List[float]
    engagement_history: List[float]
    error_rates: List[float] = []


class EngagementRequest(BaseModel):
    time_on_task: int
    interaction_count: int
    completion_rate: float
    focus_level: float
    error_rate: float


class CognitiveLoadRequest(BaseModel):
    task_complexity: int
    user_capacity: float
    time_pressure: float


class LessonRequest(BaseModel):
    user_id: str
    topic: str
    learning_style: str = "visual"
    difficulty: str = "intermediate"
    user_name: str = "Student"
    cognitive_capacity: float = 7.0


class QuizFeedbackRequest(BaseModel):
    question: str
    user_answer: int
    correct_answer: int
    explanation: str
    learning_style: str = "visual"


# ========================================
# Endpoints
# ========================================

@router.post("/recommend-content", response_model=StandardResponse)
async def recommend_content(request: RecommendationRequest):
    """Get personalized content recommendations"""
    try:
        recommendations = recommendation_engine.generate_recommendations(
            user_profile=request.user_profile,
            available_content=MOCK_CONTENT,
            performance_history=request.performance_history,
            completed_content=request.completed_content
        )

        return StandardResponse(
            success=True,
            message=f"Generated {len(recommendations)} recommendations",
            data=[rec.dict() for rec in recommendations]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recommendations: {str(e)}"
        )


@router.post("/next-lesson")
async def get_next_lesson(request: NextLessonRequest):
    """Get next recommended lesson for user"""
    return {
        "user_id": request.user_id,
        "lesson_id": "lesson_004",
        "lesson_title": "Dictionary Methods & Comprehensions",
        "module": "Data Structures",
        "estimated_duration": 45,
        "difficulty": "intermediate"
    }


@router.post("/adjust-difficulty", response_model=StandardResponse)
async def adjust_difficulty(request: DifficultyAdjustRequest):
    """Adjust content difficulty based on performance"""
    try:
        new_difficulty, reasoning = adaptation_engine.adjust_difficulty(
            current_difficulty=request.current_difficulty,
            performance_history=request.performance_history,
            engagement_history=request.engagement_history,
            error_rates=request.error_rates
        )

        mock_profile = {
            "user_id": request.user_id,
            "learning_style": "multimodal",
            "cognitive_load_capacity": 6.0,
            "current_difficulty": new_difficulty
        }

        recommendations = recommendation_engine.generate_recommendations(
            user_profile=mock_profile,
            available_content=MOCK_CONTENT,
            performance_history=request.performance_history,
            completed_content=[]
        )

        adaptation_recommendations = adaptation_engine.generate_adaptation_recommendations(
            user_profile=mock_profile,
            performance_data={
                "error_rate": request.error_rates[-1] if request.error_rates else 0.0,
                "completion_rate": 0.8,
                "focus_level": request.engagement_history[-1] if request.engagement_history else 0.7
            }
        )

        response = AdaptationResponse(
            user_id=request.user_id,
            current_difficulty=request.current_difficulty,
            recommended_difficulty=new_difficulty,
            difficulty_changed=(new_difficulty != request.current_difficulty),
            reasoning=reasoning,
            recommendations=recommendations,
            next_steps=adaptation_recommendations
        )

        return StandardResponse(
            success=True,
            message="Difficulty adjustment completed",
            data=response.dict()
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to adjust difficulty: {str(e)}"
        )


@router.get("/learning-path/{user_id}", response_model=StandardResponse)
async def get_learning_path(user_id: str, learning_goal: str = "Python Programming"):
    """Get personalized learning path"""
    try:
        mock_profile = {
            "user_id": user_id,
            "learning_style": "multimodal",
            "cognitive_load_capacity": 6.0
        }

        path_modules = recommendation_engine.generate_learning_path(
            user_profile=mock_profile,
            learning_goal=learning_goal,
            available_modules=MOCK_CONTENT
        )

        learning_path = LearningPath(
            path_id=str(uuid.uuid4()),
            user_id=user_id,
            title=f"Path to {learning_goal}",
            description=f"Personalized learning path for mastering {learning_goal}",
            total_modules=len(path_modules),
            estimated_completion_hours=sum(
                m.get("duration_minutes", 0) for m in path_modules) // 60,
            current_module=0,
            completion_percentage=0.0,
            modules=path_modules,
            created_at=datetime.now(),
            last_updated=datetime.now()
        )

        return StandardResponse(
            success=True,
            message="Learning path generated successfully",
            data=learning_path.dict()
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate learning path: {str(e)}"
        )


@router.post("/calculate-engagement", response_model=StandardResponse)
async def calculate_engagement(request: EngagementRequest):
    """Calculate engagement score from metrics"""
    from app.schemas.assessment_schema import LearningAnalytics

    analytics = LearningAnalytics(
        user_id="temp",
        session_id="temp",
        engagement_score=0.0,
        focus_level=request.focus_level,
        interaction_count=request.interaction_count,
        time_on_task_minutes=request.time_on_task,
        completion_rate=request.completion_rate,
        error_rate=request.error_rate,
        help_requests=0
    )

    engagement_score = adaptation_engine.calculate_engagement_score(analytics)

    return StandardResponse(
        success=True,
        message="Engagement score calculated",
        data={
            "engagement_score": round(engagement_score, 3),
            "interpretation": (
                "High engagement"   if engagement_score > 0.7 else
                "Medium engagement" if engagement_score > 0.4 else
                "Low engagement"
            ),
            "recommendations": adaptation_engine.generate_adaptation_recommendations(
                user_profile={"learning_style": "multimodal"},
                performance_data={
                    "error_rate":      request.error_rate,
                    "completion_rate": request.completion_rate,
                    "focus_level":     request.focus_level
                }
            )
        }
    )


@router.post("/cognitive-load", response_model=StandardResponse)
async def calculate_cognitive_load(request: CognitiveLoadRequest):
    """Calculate cognitive load for a task"""
    load = adaptation_engine.calculate_cognitive_load(
        task_complexity=request.task_complexity,
        user_capacity=request.user_capacity,
        time_pressure=request.time_pressure
    )

    return StandardResponse(
        success=True,
        message="Cognitive load calculated",
        data={
            "cognitive_load": round(load, 2),
            "interpretation": (
                "High load - consider reducing complexity" if load > 7 else
                "Moderate load - appropriate challenge"    if load > 4 else
                "Low load - consider increasing complexity"
            ),
            "recommended_action": (
                "Reduce task complexity or time pressure" if load > 7 else
                "Maintain current difficulty"             if load > 4 else
                "Increase challenge level"
            )
        }
    )


@router.get("/content-library", response_model=StandardResponse)
async def get_content_library(
    difficulty_level: Optional[str] = None,
    content_type: Optional[str] = None
):
    """Get available content library"""
    filtered_content = MOCK_CONTENT

    if difficulty_level:
        filtered_content = [
            c for c in filtered_content
            if c["difficulty_level"] == difficulty_level
        ]

    if content_type:
        filtered_content = [
            c for c in filtered_content
            if c["content_type"] == content_type
        ]

    return StandardResponse(
        success=True,
        message=f"Retrieved {len(filtered_content)} content items",
        data=filtered_content
    )


# ========================================
# Gemini AI Lesson Generation
# ========================================

@router.post("/generate-lesson", response_model=StandardResponse)
async def generate_lesson(request: LessonRequest):
    """Generate AI-powered personalized lesson using Gemini 2.5 Flash"""
    try:
        lesson = await generate_lesson_content(
            topic=request.topic,
            learning_style=request.learning_style,
            difficulty=request.difficulty,
            user_name=request.user_name,
            cognitive_capacity=request.cognitive_capacity
        )

        return StandardResponse(
            success=True,
            message="Lesson generated successfully",
            data=lesson
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lesson generation failed: {str(e)}"
        )


@router.post("/quiz-feedback", response_model=StandardResponse)
async def get_quiz_feedback(request: QuizFeedbackRequest):
    """Get AI-generated personalized feedback on quiz answer"""
    try:
        feedback = await generate_quiz_feedback(
            question=request.question,
            user_answer=request.user_answer,
            correct_answer=request.correct_answer,
            explanation=request.explanation,
            learning_style=request.learning_style
        )

        return StandardResponse(
            success=True,
            message="Feedback generated",
            data={"feedback": feedback}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Feedback generation failed: {str(e)}"
        )