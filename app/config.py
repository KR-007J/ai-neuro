"""
Configuration Management
Loads settings from environment variables with sensible defaults
"""

from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""

    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 10000
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # CORS - comma-separated string so Render env var works correctly
    ALLOWED_ORIGINS: str = "http://localhost:5500,http://127.0.0.1:5500,http://localhost:3000"

    @property
    def cors_origins(self) -> List[str]:
        """Parse comma-separated origins into a list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]

    # Database
    DATABASE_URL: str = "sqlite:///./neuro_learning.db"

    # Model Configuration
    MODEL_PATH: str = "app/models/"
    LEARNING_STYLE_MODEL: str = "learning_style.pkl"
    ENGAGEMENT_MODEL: str = "engagement_model.pkl"
    DIFFICULTY_MODEL: str = "difficulty_predictor.pkl"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Cognitive Profiling Parameters
    VARK_THRESHOLD: float = 0.6
    COGNITIVE_LOAD_MAX: int = 10
    ADAPTATION_SENSITIVITY: float = 0.7

    # Engagement Tracking
    ENGAGEMENT_WINDOW: int = 5
    MIN_ENGAGEMENT_SCORE: float = 0.3

    # Content Difficulty Levels
    DIFFICULTY_LEVELS: List[str] = ["beginner", "intermediate", "advanced", "expert"]

    # Recommendation System
    MIN_RECOMMENDATIONS: int = 3
    MAX_RECOMMENDATIONS: int = 10

    # API Rate Limiting (requests per minute)
    RATE_LIMIT: int = 100

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Global settings instance
settings = get_settings()