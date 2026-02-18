"""
Cognitive Model
Implements cognitive profiling and VARK learning style assessment
"""

import numpy as np
from typing import Dict, List, Tuple
from app.schemas.assessment_schema import VARKAssessment, CognitiveProfile
from app.config import settings


class CognitiveProfiler:
    """
    Cognitive profiling engine that identifies learning styles
    and cognitive capabilities
    """
    
    def __init__(self):
        self.vark_threshold = settings.VARK_THRESHOLD
        
    def calculate_vark_scores(self, responses: List[Dict]) -> Dict[str, float]:
        """
        Calculate VARK learning style scores from assessment responses
        
        Args:
            responses: List of user responses to VARK questionnaire
            
        Returns:
            Dictionary with scores for each learning style
        """
        scores = {
            "visual": 0.0,
            "auditory": 0.0,
            "reading_writing": 0.0,
            "kinesthetic": 0.0
        }
        
        # Process each response
        for response in responses:
            modality = response.get("preferred_modality", "").lower()
            if modality in scores:
                scores[modality] += 1
        
        # Normalize scores
        total = sum(scores.values())
        if total > 0:
            scores = {k: v / total for k, v in scores.items()}
        
        return scores
    
    def determine_learning_style(self, scores: Dict[str, float]) -> Tuple[str, str, bool]:
        """
        Determine dominant learning style from VARK scores
        
        Args:
            scores: Dictionary of VARK scores
            
        Returns:
            Tuple of (dominant_style, secondary_style, is_multimodal)
        """
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        dominant_style = sorted_scores[0][0]
        secondary_style = sorted_scores[1][0] if len(sorted_scores) > 1 else None
        
        # Check if multimodal (multiple high scores)
        high_scores = [k for k, v in scores.items() if v >= self.vark_threshold]
        is_multimodal = len(high_scores) > 1
        
        return dominant_style, secondary_style, is_multimodal
    
    def assess_cognitive_load_capacity(self, 
                                      response_times: List[int],
                                      error_rates: List[float],
                                      task_complexity: List[int]) -> float:
        """
        Assess user's cognitive load capacity based on performance metrics
        
        Args:
            response_times: List of response times in seconds
            error_rates: List of error rates for each task
            task_complexity: Complexity rating for each task (1-10)
            
        Returns:
            Cognitive load capacity score (0-10)
        """
        if not response_times or not error_rates:
            return 5.0  # Default medium capacity
        
        # Normalize response times
        avg_response_time = np.mean(response_times)
        normalized_time = 1 / (1 + np.log1p(avg_response_time))
        
        # Calculate error-based score
        avg_error_rate = np.mean(error_rates)
        error_score = 1 - avg_error_rate
        
        # Consider task complexity
        avg_complexity = np.mean(task_complexity)
        complexity_factor = avg_complexity / 10.0
        
        # Combine factors
        capacity = (normalized_time * 0.3 + error_score * 0.5 + complexity_factor * 0.2) * 10
        
        return min(max(capacity, 0.0), 10.0)
    
    def estimate_attention_span(self, 
                               session_durations: List[int],
                               focus_scores: List[float]) -> int:
        """
        Estimate user's attention span in minutes
        
        Args:
            session_durations: List of session durations in minutes
            focus_scores: Focus level scores (0-1) for each session
            
        Returns:
            Estimated attention span in minutes
        """
        if not session_durations or not focus_scores:
            return 30  # Default 30 minutes
        
        # Find sessions with high focus (>0.7)
        high_focus_durations = [
            duration for duration, focus in zip(session_durations, focus_scores)
            if focus > 0.7
        ]
        
        if high_focus_durations:
            return int(np.mean(high_focus_durations))
        else:
            return int(np.mean(session_durations))
    
    def classify_processing_speed(self, response_times: List[int]) -> str:
        """
        Classify processing speed as slow, medium, or fast
        
        Args:
            response_times: List of response times in seconds
            
        Returns:
            Processing speed category
        """
        if not response_times:
            return "medium"
        
        avg_time = np.mean(response_times)
        
        if avg_time < 5:
            return "fast"
        elif avg_time < 15:
            return "medium"
        else:
            return "slow"
    
    def classify_working_memory(self, 
                               recall_scores: List[float],
                               task_complexity: List[int]) -> str:
        """
        Classify working memory capacity
        
        Args:
            recall_scores: Scores on recall tasks (0-1)
            task_complexity: Complexity of recall tasks (1-10)
            
        Returns:
            Working memory category (low, medium, high)
        """
        if not recall_scores:
            return "medium"
        
        # Weight scores by complexity
        weighted_score = np.average(recall_scores, weights=task_complexity) if task_complexity else np.mean(recall_scores)
        
        if weighted_score < 0.4:
            return "low"
        elif weighted_score < 0.7:
            return "medium"
        else:
            return "high"
    
    def create_cognitive_profile(self, 
                                user_id: str,
                                assessment_data: Dict) -> CognitiveProfile:
        """
        Create comprehensive cognitive profile from assessment data
        
        Args:
            user_id: User identifier
            assessment_data: Dictionary containing assessment results
            
        Returns:
            CognitiveProfile object
        """
        # Calculate VARK scores
        vark_responses = assessment_data.get("vark_responses", [])
        vark_scores = self.calculate_vark_scores(vark_responses)
        dominant, secondary, is_multimodal = self.determine_learning_style(vark_scores)
        
        # Assess cognitive capabilities
        response_times = assessment_data.get("response_times", [])
        error_rates = assessment_data.get("error_rates", [])
        task_complexity = assessment_data.get("task_complexity", [])
        
        cognitive_load = self.assess_cognitive_load_capacity(
            response_times, error_rates, task_complexity
        )
        
        session_durations = assessment_data.get("session_durations", [])
        focus_scores = assessment_data.get("focus_scores", [])
        attention_span = self.estimate_attention_span(session_durations, focus_scores)
        
        processing_speed = self.classify_processing_speed(response_times)
        
        recall_scores = assessment_data.get("recall_scores", [])
        working_memory = self.classify_working_memory(recall_scores, task_complexity)
        
        # Determine strengths and weaknesses
        strengths = []
        weaknesses = []
        
        if cognitive_load > 7:
            strengths.append("High cognitive load capacity")
        elif cognitive_load < 4:
            weaknesses.append("Limited cognitive load capacity")
        
        if processing_speed == "fast":
            strengths.append("Fast information processing")
        elif processing_speed == "slow":
            weaknesses.append("Slower information processing")
        
        if working_memory == "high":
            strengths.append("Strong working memory")
        elif working_memory == "low":
            weaknesses.append("Limited working memory")
        
        # Create profile
        profile = CognitiveProfile(
            user_id=user_id,
            learning_style=dominant,
            learning_style_scores=vark_scores,
            cognitive_load_capacity=cognitive_load,
            attention_span_minutes=attention_span,
            preferred_modality=dominant,
            processing_speed=processing_speed,
            working_memory_capacity=working_memory,
            strengths=strengths,
            weaknesses=weaknesses
        )
        
        return profile
