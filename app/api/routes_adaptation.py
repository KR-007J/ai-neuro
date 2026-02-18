"""
Adaptation API Routes
Endpoints for adaptive learning and content recommendations
"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Optional
from app.schemas.response_schema import (
    StandardResponse, ContentRecommendation, AdaptationResponse, LearningPath
)
from app.core.adaptation_engine import AdaptationEngine
from app.core.recommendation_engine import RecommendationEngine
from datetime import datetime
import uuid

router = APIRouter()

# Initialize engines
adaptation_engine = AdaptationEngine()
recommendation_engine = RecommendationEngine()

# Mock content database
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


@router.post("/recommend-content", response_model=StandardResponse)
async def recommend_content(
    user_id: str,
    user_profile: Dict,
    performance_history: List[float],
    completed_content: List[str] = []
):
    """
    Get personalized content recommendations
    
    Returns a list of recommended learning content based on user profile,
    performance history, and learning goals.
    """
    try:
        recommendations = recommendation_engine.generate_recommendations(
            user_profile=user_profile,
            available_content=MOCK_CONTENT,
            performance_history=performance_history,
            completed_content=completed_content
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


@router.post("/adjust-difficulty", response_model=StandardResponse)
async def adjust_difficulty(
    user_id: str,
    current_difficulty: str,
    performance_history: List[float],
    engagement_history: List[float],
    error_rates: List[float] = []
):
    """
    Adjust content difficulty based on performance
    
    Dynamically adjusts difficulty level based on user performance metrics.
    """
    try:
        new_difficulty, reasoning = adaptation_engine.adjust_difficulty(
            current_difficulty=current_difficulty,
            performance_history=performance_history,
            engagement_history=engagement_history,
            error_rates=error_rates
        )
        
        # Get recommendations for new difficulty
        mock_profile = {
            "user_id": user_id,
            "learning_style": "multimodal",
            "cognitive_load_capacity": 6.0,
            "current_difficulty": new_difficulty
        }
        
        recommendations = recommendation_engine.generate_recommendations(
            user_profile=mock_profile,
            available_content=MOCK_CONTENT,
            performance_history=performance_history,
            completed_content=[]
        )
        
        adaptation_recommendations = adaptation_engine.generate_adaptation_recommendations(
            user_profile=mock_profile,
            performance_data={
                "error_rate": error_rates[-1] if error_rates else 0.0,
                "completion_rate": 0.8,
                "focus_level": engagement_history[-1] if engagement_history else 0.7
            }
        )
        
        response = AdaptationResponse(
            user_id=user_id,
            current_difficulty=current_difficulty,
            recommended_difficulty=new_difficulty,
            difficulty_changed=(new_difficulty != current_difficulty),
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
async def get_learning_path(
    user_id: str,
    learning_goal: str = "Python Programming"
):
    """
    Get personalized learning path
    
    Generates an optimal sequence of learning modules to achieve the goal.
    """
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
            estimated_completion_hours=sum(m.get("duration_minutes", 0) for m in path_modules) // 60,
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
async def calculate_engagement(
    time_on_task: int,
    interaction_count: int,
    completion_rate: float,
    focus_level: float,
    error_rate: float
):
    """
    Calculate engagement score from metrics
    
    Computes overall engagement score from various learning metrics.
    """
    from app.schemas.assessment_schema import LearningAnalytics
    
    analytics = LearningAnalytics(
        user_id="temp",
        session_id="temp",
        engagement_score=0.0,  # Will be calculated
        focus_level=focus_level,
        interaction_count=interaction_count,
        time_on_task_minutes=time_on_task,
        completion_rate=completion_rate,
        error_rate=error_rate,
        help_requests=0
    )
    
    engagement_score = adaptation_engine.calculate_engagement_score(analytics)
    
    return StandardResponse(
        success=True,
        message="Engagement score calculated",
        data={
            "engagement_score": round(engagement_score, 3),
            "interpretation": (
                "High engagement" if engagement_score > 0.7
                else "Medium engagement" if engagement_score > 0.4
                else "Low engagement"
            ),
            "recommendations": adaptation_engine.generate_adaptation_recommendations(
                user_profile={"learning_style": "multimodal"},
                performance_data={
                    "error_rate": error_rate,
                    "completion_rate": completion_rate,
                    "focus_level": focus_level
                }
            )
        }
    )


@router.post("/cognitive-load", response_model=StandardResponse)
async def calculate_cognitive_load(
    task_complexity: int,
    user_capacity: float,
    time_pressure: float
):
    """
    Calculate cognitive load for a task
    
    Estimates cognitive load based on task complexity and user capacity.
    """
    load = adaptation_engine.calculate_cognitive_load(
        task_complexity=task_complexity,
        user_capacity=user_capacity,
        time_pressure=time_pressure
    )
    
    return StandardResponse(
        success=True,
        message="Cognitive load calculated",
        data={
            "cognitive_load": round(load, 2),
            "interpretation": (
                "High load - consider reducing complexity" if load > 7
                else "Moderate load - appropriate challenge" if load > 4
                else "Low load - consider increasing complexity"
            ),
            "recommended_action": (
                "Reduce task complexity or time pressure" if load > 7
                else "Maintain current difficulty" if load > 4
                else "Increase challenge level"
            )
        }
    )


@router.get("/content-library", response_model=StandardResponse)
async def get_content_library(
    difficulty_level: Optional[str] = None,
    content_type: Optional[str] = None
):
    """
    Get available content library
    
    Returns filtered content based on criteria.
    """
    filtered_content = MOCK_CONTENT
    
    if difficulty_level:
        filtered_content = [c for c in filtered_content if c["difficulty_level"] == difficulty_level]
    
    if content_type:
        filtered_content = [c for c in filtered_content if c["content_type"] == content_type]
    
    return StandardResponse(
        success=True,
        message=f"Retrieved {len(filtered_content)} content items",
        data=filtered_content
    )
