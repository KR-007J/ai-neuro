"""
Adaptation Engine
Dynamic difficulty adjustment and content personalization
"""

import numpy as np
from typing import List, Dict, Tuple
from app.schemas.assessment_schema import DifficultyLevel, LearningAnalytics
from app.config import settings


class AdaptationEngine:
    """
    Engine for adaptive difficulty adjustment and content selection
    based on user performance and engagement
    """
    
    def __init__(self):
        self.adaptation_sensitivity = settings.ADAPTATION_SENSITIVITY
        self.difficulty_levels = settings.DIFFICULTY_LEVELS
        self.min_engagement = settings.MIN_ENGAGEMENT_SCORE
        
    def calculate_performance_score(self, 
                                   correct_answers: int,
                                   total_questions: int,
                                   avg_response_time: float,
                                   optimal_time: float) -> float:
        """
        Calculate overall performance score
        
        Args:
            correct_answers: Number of correct answers
            total_questions: Total number of questions
            avg_response_time: Average time taken per question
            optimal_time: Optimal time for questions at current difficulty
            
        Returns:
            Performance score (0-1)
        """
        if total_questions == 0:
            return 0.5
        
        # Accuracy component (60% weight)
        accuracy = correct_answers / total_questions
        
        # Time efficiency component (40% weight)
        if optimal_time > 0:
            time_ratio = min(optimal_time / avg_response_time, 1.5)
            time_score = min(time_ratio / 1.5, 1.0)
        else:
            time_score = 0.5
        
        performance = (accuracy * 0.6) + (time_score * 0.4)
        return performance
    
    def should_increase_difficulty(self, 
                                  performance_score: float,
                                  engagement_score: float,
                                  current_difficulty: str) -> bool:
        """
        Determine if difficulty should be increased
        
        Args:
            performance_score: Current performance score (0-1)
            engagement_score: Current engagement score (0-1)
            current_difficulty: Current difficulty level
            
        Returns:
            True if difficulty should increase
        """
        # Don't increase if already at max difficulty
        if current_difficulty == self.difficulty_levels[-1]:
            return False
        
        # Increase if performing well and engaged
        threshold = 0.75 + (1 - self.adaptation_sensitivity) * 0.2
        
        return (performance_score > threshold and 
                engagement_score > self.min_engagement)
    
    def should_decrease_difficulty(self,
                                  performance_score: float,
                                  engagement_score: float,
                                  error_rate: float,
                                  current_difficulty: str) -> bool:
        """
        Determine if difficulty should be decreased
        
        Args:
            performance_score: Current performance score (0-1)
            engagement_score: Current engagement score (0-1)
            error_rate: Current error rate (0-1)
            current_difficulty: Current difficulty level
            
        Returns:
            True if difficulty should decrease
        """
        # Don't decrease if already at min difficulty
        if current_difficulty == self.difficulty_levels[0]:
            return False
        
        # Decrease if struggling or disengaged
        performance_threshold = 0.5 - (self.adaptation_sensitivity * 0.2)
        engagement_threshold = self.min_engagement
        
        return (performance_score < performance_threshold or 
                engagement_score < engagement_threshold or
                error_rate > 0.5)
    
    def adjust_difficulty(self,
                         current_difficulty: str,
                         performance_history: List[float],
                         engagement_history: List[float],
                         error_rates: List[float]) -> Tuple[str, str]:
        """
        Adjust difficulty level based on performance metrics
        
        Args:
            current_difficulty: Current difficulty level
            performance_history: Recent performance scores
            engagement_history: Recent engagement scores
            error_rates: Recent error rates
            
        Returns:
            Tuple of (new_difficulty, reasoning)
        """
        if not performance_history or not engagement_history:
            return current_difficulty, "Insufficient data for adjustment"
        
        # Calculate moving averages
        avg_performance = np.mean(performance_history[-settings.ENGAGEMENT_WINDOW:])
        avg_engagement = np.mean(engagement_history[-settings.ENGAGEMENT_WINDOW:])
        avg_error_rate = np.mean(error_rates[-settings.ENGAGEMENT_WINDOW:]) if error_rates else 0.0
        
        current_idx = self.difficulty_levels.index(current_difficulty)
        
        # Check for increase
        if self.should_increase_difficulty(avg_performance, avg_engagement, current_difficulty):
            new_difficulty = self.difficulty_levels[current_idx + 1]
            reasoning = f"Performance ({avg_performance:.2f}) and engagement ({avg_engagement:.2f}) are high - increasing difficulty"
            return new_difficulty, reasoning
        
        # Check for decrease
        if self.should_decrease_difficulty(avg_performance, avg_engagement, avg_error_rate, current_difficulty):
            new_difficulty = self.difficulty_levels[current_idx - 1]
            reasoning = f"Performance ({avg_performance:.2f}) or engagement ({avg_engagement:.2f}) needs support - decreasing difficulty"
            return new_difficulty, reasoning
        
        # Maintain current level
        return current_difficulty, "Current difficulty level is appropriate"
    
    def calculate_cognitive_load(self,
                                task_complexity: int,
                                user_capacity: float,
                                time_pressure: float) -> float:
        """
        Calculate cognitive load for a task
        
        Args:
            task_complexity: Complexity rating (1-10)
            user_capacity: User's cognitive capacity (1-10)
            time_pressure: Time pressure factor (0-1)
            
        Returns:
            Cognitive load score (0-10)
        """
        # Base load from task complexity
        base_load = task_complexity
        
        # Adjust for user capacity (higher capacity = lower experienced load)
        capacity_factor = 10 / max(user_capacity, 1)
        adjusted_load = base_load * capacity_factor
        
        # Add time pressure component
        time_load = time_pressure * 3  # Max 3 points from time pressure
        
        total_load = min(adjusted_load + time_load, 10)
        return total_load
    
    def recommend_content_difficulty(self,
                                    cognitive_profile: Dict,
                                    recent_performance: List[float],
                                    learning_goals: List[str]) -> str:
        """
        Recommend optimal content difficulty based on profile and goals
        
        Args:
            cognitive_profile: User's cognitive profile
            recent_performance: Recent performance scores
            learning_goals: User's learning objectives
            
        Returns:
            Recommended difficulty level
        """
        # Base recommendation on cognitive capacity
        cognitive_load = cognitive_profile.get("cognitive_load_capacity", 5.0)
        
        if cognitive_load >= 7.5:
            base_difficulty = "advanced"
        elif cognitive_load >= 5:
            base_difficulty = "intermediate"
        else:
            base_difficulty = "beginner"
        
        # Adjust based on recent performance
        if recent_performance:
            avg_performance = np.mean(recent_performance[-5:])
            
            base_idx = self.difficulty_levels.index(base_difficulty)
            
            # Strong performance: move up
            if avg_performance > 0.8 and base_idx < len(self.difficulty_levels) - 1:
                base_difficulty = self.difficulty_levels[base_idx + 1]
            # Weak performance: move down
            elif avg_performance < 0.4 and base_idx > 0:
                base_difficulty = self.difficulty_levels[base_idx - 1]
        
        # Consider learning goals
        goal_keywords = {
            "master": "advanced",
            "expert": "expert",
            "learn": "intermediate",
            "introduction": "beginner",
            "basics": "beginner"
        }
        
        for goal in learning_goals:
            for keyword, difficulty in goal_keywords.items():
                if keyword in goal.lower():
                    # Prefer goal-based difficulty if specified
                    return difficulty
        
        return base_difficulty
    
    def calculate_engagement_score(self, analytics: LearningAnalytics) -> float:
        """
        Calculate engagement score from learning analytics
        
        Args:
            analytics: LearningAnalytics object
            
        Returns:
            Engagement score (0-1)
        """
        # Weight different engagement factors
        factors = {
            "completion_rate": (analytics.completion_rate, 0.3),
            "time_on_task": (min(analytics.time_on_task_minutes / 30, 1.0), 0.2),
            "interaction_count": (min(analytics.interaction_count / 20, 1.0), 0.2),
            "focus_level": (analytics.focus_level, 0.2),
            "low_error_rate": (1 - analytics.error_rate, 0.1)
        }
        
        engagement = sum(score * weight for score, weight in factors.values())
        return min(max(engagement, 0.0), 1.0)
    
    def generate_adaptation_recommendations(self,
                                          user_profile: Dict,
                                          performance_data: Dict) -> List[str]:
        """
        Generate specific recommendations for content adaptation
        
        Args:
            user_profile: User's cognitive profile
            performance_data: Recent performance metrics
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        learning_style = user_profile.get("learning_style", "multimodal")
        
        # Style-specific recommendations
        if learning_style == "visual":
            recommendations.append("Incorporate more diagrams, charts, and visual aids")
        elif learning_style == "auditory":
            recommendations.append("Add audio explanations and verbal instructions")
        elif learning_style == "kinesthetic":
            recommendations.append("Include hands-on activities and practical exercises")
        elif learning_style == "reading_writing":
            recommendations.append("Provide detailed text explanations and note-taking opportunities")
        
        # Performance-based recommendations
        error_rate = performance_data.get("error_rate", 0)
        if error_rate > 0.3:
            recommendations.append("Provide additional scaffolding and guided practice")
            recommendations.append("Break complex concepts into smaller chunks")
        
        completion_rate = performance_data.get("completion_rate", 1.0)
        if completion_rate < 0.6:
            recommendations.append("Reduce content length or complexity")
            recommendations.append("Add progress checkpoints and breaks")
        
        focus_level = performance_data.get("focus_level", 1.0)
        if focus_level < 0.5:
            recommendations.append("Incorporate more interactive elements")
            recommendations.append("Add gamification or rewards")
        
        return recommendations
