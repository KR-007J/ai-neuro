"""
User API Routes
Endpoints for user management and profile operations
"""

from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.user_schema import (
    UserCreate, UserResponse, UserUpdate, UserStats, UserPreferences
)
from app.schemas.response_schema import StandardResponse
from datetime import datetime
import uuid

router = APIRouter()

# In-memory storage (replace with database in production)
users_db = {}


@router.post("/register", response_model=StandardResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    """
    Register a new user
    
    Creates a new user account with basic profile information.
    """
    # Check if email already exists
    if any(u.get("email") == user.email for u in users_db.values()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user_id = str(uuid.uuid4())
    user_data = {
        "user_id": user_id,
        "email": user.email,
        "full_name": user.full_name,
        "age": user.age,
        "education_level": user.education_level,
        "learning_style": None,
        "cognitive_profile": None,
        "preferences": UserPreferences().dict(),
        "created_at": datetime.now(),
        "last_active": datetime.now()
    }
    
    users_db[user_id] = user_data
    
    # Create response
    user_response = UserResponse(**user_data)
    
    return StandardResponse(
        success=True,
        message="User registered successfully",
        data=user_response.dict()
    )


@router.get("/{user_id}", response_model=StandardResponse)
async def get_user(user_id: str):
    """
    Get user profile information
    
    Retrieves detailed profile information for a specific user.
    """
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user_data = users_db[user_id]
    user_response = UserResponse(**user_data)
    
    return StandardResponse(
        success=True,
        message="User retrieved successfully",
        data=user_response.dict()
    )


@router.put("/{user_id}", response_model=StandardResponse)
async def update_user(user_id: str, user_update: UserUpdate):
    """
    Update user profile
    
    Updates user information and preferences.
    """
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user_data = users_db[user_id]
    
    # Update fields if provided
    update_data = user_update.dict(exclude_unset=True)
    user_data.update(update_data)
    user_data["last_active"] = datetime.now()
    
    users_db[user_id] = user_data
    
    user_response = UserResponse(**user_data)
    
    return StandardResponse(
        success=True,
        message="User updated successfully",
        data=user_response.dict()
    )


@router.put("/{user_id}/preferences", response_model=StandardResponse)
async def update_preferences(user_id: str, preferences: UserPreferences):
    """
    Update user learning preferences
    
    Updates user-specific learning preferences and settings.
    """
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user_data = users_db[user_id]
    user_data["preferences"] = preferences.dict()
    user_data["last_active"] = datetime.now()
    
    users_db[user_id] = user_data
    
    return StandardResponse(
        success=True,
        message="Preferences updated successfully",
        data=preferences.dict()
    )


@router.get("/{user_id}/stats", response_model=StandardResponse)
async def get_user_stats(user_id: str):
    """
    Get user learning statistics
    
    Retrieves comprehensive learning statistics and progress metrics.
    """
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # In production, calculate from actual data
    stats = UserStats(
        user_id=user_id,
        total_sessions=15,
        total_time_minutes=450,
        completed_modules=8,
        average_score=78.5,
        engagement_score=0.82,
        learning_streak_days=7,
        achievements=["First Module", "Week Warrior", "High Achiever"]
    )
    
    return StandardResponse(
        success=True,
        message="User statistics retrieved successfully",
        data=stats.dict()
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    """
    Delete user account
    
    Permanently deletes a user account and all associated data.
    """
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    del users_db[user_id]
    return None


@router.get("/", response_model=StandardResponse)
async def list_users(skip: int = 0, limit: int = 10):
    """
    List all users (admin only in production)
    
    Returns a paginated list of users.
    """
    users_list = list(users_db.values())[skip:skip + limit]
    user_responses = [UserResponse(**user) for user in users_list]
    
    return StandardResponse(
        success=True,
        message=f"Retrieved {len(user_responses)} users",
        data=[user.dict() for user in user_responses]
    )
