"""
API Tests
Basic tests for API endpoints
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "online"
        assert "docs" in data
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestUserEndpoints:
    """Test user management endpoints"""
    
    def test_register_user(self):
        """Test user registration"""
        user_data = {
            "email": "test@example.com",
            "full_name": "Test User",
            "age": 25,
            "education_level": "Bachelor's",
            "password": "securepass123"
        }
        response = client.post("/api/v1/users/register", json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert "data" in data
    
    def test_register_duplicate_email(self):
        """Test registration with duplicate email"""
        user_data = {
            "email": "duplicate@example.com",
            "full_name": "User One",
            "age": 30,
            "password": "password123"
        }
        # First registration
        client.post("/api/v1/users/register", json=user_data)
        # Duplicate registration
        response = client.post("/api/v1/users/register", json=user_data)
        assert response.status_code == 400


class TestAssessmentEndpoints:
    """Test assessment endpoints"""
    
    def test_vark_assessment(self):
        """Test VARK learning style assessment"""
        responses = [
            {"preferred_modality": "visual"},
            {"preferred_modality": "visual"},
            {"preferred_modality": "auditory"}
        ]
        response = client.post(
            "/api/v1/assessment/vark-assessment",
            params={"user_id": "test_user_123"},
            json=responses
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "dominant_style" in data["data"]


class TestAdaptationEndpoints:
    """Test adaptation endpoints"""
    
    def test_calculate_engagement(self):
        """Test engagement score calculation"""
        metrics = {
            "time_on_task": 25,
            "interaction_count": 15,
            "completion_rate": 0.8,
            "focus_level": 0.75,
            "error_rate": 0.2
        }
        response = client.post("/api/v1/adaptation/calculate-engagement", json=metrics)
        assert response.status_code == 200
        data = response.json()
        assert "engagement_score" in data["data"]
        assert 0 <= data["data"]["engagement_score"] <= 1
    
    def test_cognitive_load_calculation(self):
        """Test cognitive load calculation"""
        params = {
            "task_complexity": 7,
            "user_capacity": 6.5,
            "time_pressure": 0.5
        }
        response = client.post("/api/v1/adaptation/cognitive-load", json=params)
        assert response.status_code == 200
        data = response.json()
        assert "cognitive_load" in data["data"]


# Run tests with: pytest tests/test_api.py -v
