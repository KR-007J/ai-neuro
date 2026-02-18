"""
Assessment API Routes
Endpoints for cognitive assessments and profiling
"""

from fastapi import APIRouter, HTTPException, status
from typing import Dict, List
from app.schemas.assessment_schema import (
    AssessmentSubmission, AssessmentResult, CognitiveProfile,
    VARKAssessment, LearningAnalytics
)
from app.schemas.response_schema import StandardResponse
from app.core.cognitive_model import CognitiveProfiler
from datetime import datetime
import uuid

router = APIRouter()

# Initialize cognitive profiler
profiler = CognitiveProfiler()

# In-memory storage
profiles_db = {}
assessments_db = {}


@router.post("/cognitive-profile", response_model=StandardResponse, status_code=status.HTTP_201_CREATED)
async def create_cognitive_profile(user_id: str, assessment_data: Dict):
    """
    Create cognitive profile from assessment data
    
    Analyzes user responses to create a comprehensive cognitive profile
    including VARK learning style, cognitive load capacity, and more.
    """
    try:
        # Create cognitive profile
        profile = profiler.create_cognitive_profile(user_id, assessment_data)
        
        # Store profile
        profiles_db[user_id] = profile.dict()
        
        return StandardResponse(
            success=True,
            message="Cognitive profile created successfully",
            data=profile.dict()
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create profile: {str(e)}"
        )


@router.get("/profile/{user_id}", response_model=StandardResponse)
async def get_cognitive_profile(user_id: str):
    """
    Get user's cognitive profile
    
    Retrieves the complete cognitive profile for a user.
    """
    if user_id not in profiles_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cognitive profile not found. Please complete assessment first."
        )
    
    profile = profiles_db[user_id]
    
    return StandardResponse(
        success=True,
        message="Cognitive profile retrieved successfully",
        data=profile
    )


@router.post("/vark-assessment", response_model=StandardResponse)
async def assess_vark_learning_style(user_id: str, responses: List[Dict]):
    """
    Assess VARK learning style
    
    Analyzes responses to determine dominant learning style
    (Visual, Auditory, Reading/Writing, Kinesthetic).
    """
    try:
        # Calculate VARK scores
        scores = profiler.calculate_vark_scores(responses)
        dominant, secondary, is_multimodal = profiler.determine_learning_style(scores)
        
        # Create VARK assessment result
        vark_result = VARKAssessment(
            user_id=user_id,
            visual_score=scores.get("visual", 0.0),
            auditory_score=scores.get("auditory", 0.0),
            reading_writing_score=scores.get("reading_writing", 0.0),
            kinesthetic_score=scores.get("kinesthetic", 0.0),
            dominant_style=dominant,
            secondary_style=secondary,
            is_multimodal=is_multimodal
        )
        
        return StandardResponse(
            success=True,
            message="VARK assessment completed successfully",
            data=vark_result.dict()
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Assessment failed: {str(e)}"
        )


@router.post("/submit-response", response_model=StandardResponse)
async def submit_assessment_response(submission: AssessmentSubmission):
    """
    Submit assessment responses for evaluation
    
    Processes and evaluates user responses to assessment questions.
    """
    assessment_id = str(uuid.uuid4())
    
    # Calculate results (simplified version)
    total_questions = len(submission.responses)
    correct_answers = int(total_questions * 0.75)  # Mock calculation
    score = (correct_answers / total_questions) * 100
    
    result = AssessmentResult(
        assessment_id=assessment_id,
        user_id=submission.user_id,
        score=score,
        correct_answers=correct_answers,
        total_questions=total_questions,
        time_taken_seconds=submission.total_time_seconds,
        difficulty_level="intermediate",
        cognitive_load_score=6.5,
        areas_of_strength=["Problem Solving", "Critical Thinking"],
        areas_for_improvement=["Time Management"],
        recommended_next_level="advanced" if score > 80 else "intermediate"
    )
    
    # Store result
    assessments_db[assessment_id] = result.dict()
    
    return StandardResponse(
        success=True,
        message="Assessment submitted and evaluated successfully",
        data=result.dict()
    )


@router.get("/results/{assessment_id}", response_model=StandardResponse)
async def get_assessment_results(assessment_id: str):
    """
    Get assessment results
    
    Retrieves detailed results for a specific assessment.
    """
    if assessment_id not in assessments_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment results not found"
        )
    
    result = assessments_db[assessment_id]
    
    return StandardResponse(
        success=True,
        message="Assessment results retrieved successfully",
        data=result
    )


@router.post("/analytics", response_model=StandardResponse)
async def track_learning_analytics(analytics: LearningAnalytics):
    """
    Track real-time learning analytics
    
    Records engagement and performance metrics during learning sessions.
    """
    # Store analytics (in production, this would go to a time-series database)
    analytics_id = str(uuid.uuid4())
    
    analytics_data = analytics.dict()
    analytics_data["analytics_id"] = analytics_id
    
    return StandardResponse(
        success=True,
        message="Learning analytics tracked successfully",
        data=analytics_data
    )


@router.get("/user-assessments/{user_id}", response_model=StandardResponse)
async def get_user_assessments(user_id: str):
    """
    Get all assessments for a user
    
    Retrieves assessment history for a specific user.
    """
    user_assessments = [
        assessment for assessment in assessments_db.values()
        if assessment.get("user_id") == user_id
    ]
    
    return StandardResponse(
        success=True,
        message=f"Retrieved {len(user_assessments)} assessments",
        data=user_assessments
    )


@router.put("/profile/{user_id}/update", response_model=StandardResponse)
async def update_cognitive_profile(user_id: str, profile_updates: Dict):
    """
    Update cognitive profile
    
    Updates specific fields in the user's cognitive profile based on new data.
    """
    if user_id not in profiles_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cognitive profile not found"
        )
    
    profile = profiles_db[user_id]
    profile.update(profile_updates)
    profile["last_updated"] = datetime.now().isoformat()
    
    profiles_db[user_id] = profile
    
    return StandardResponse(
        success=True,
        message="Cognitive profile updated successfully",
        data=profile
    )
