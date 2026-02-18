"""
Recommendation Engine
Content recommendation system using collaborative filtering and profile matching
"""

import numpy as np
from typing import List, Dict, Tuple
from app.schemas.response_schema import ContentRecommendation
from app.config import settings


class RecommendationEngine:
    """
    Recommendation system for personalized learning content
    Uses hybrid approach combining:
    - Content-based filtering (user profile matching)
    - Collaborative filtering (similar user patterns)
    - Performance-based ranking
    """
    
    def __init__(self):
        self.min_recommendations = settings.MIN_RECOMMENDATIONS
        self.max_recommendations = settings.MAX_RECOMMENDATIONS
        
    def calculate_content_similarity(self,
                                    user_profile: Dict,
                                    content_profile: Dict) -> float:
        """
        Calculate similarity between user profile and content requirements
        
        Args:
            user_profile: User's learning profile
            content_profile: Content metadata and requirements
            
        Returns:
            Similarity score (0-1)
        """
        similarity_scores = []
        
        # Learning style match
        user_style = user_profile.get("learning_style", "multimodal")
        content_style = content_profile.get("primary_modality", "multimodal")
        
        if user_style == content_style:
            similarity_scores.append(1.0)
        elif content_style == "multimodal":
            similarity_scores.append(0.8)
        else:
            similarity_scores.append(0.5)
        
        # Difficulty match
        user_level = user_profile.get("current_difficulty", "intermediate")
        content_level = content_profile.get("difficulty_level", "intermediate")
        
        level_diff = abs(
            settings.DIFFICULTY_LEVELS.index(user_level) - 
            settings.DIFFICULTY_LEVELS.index(content_level)
        )
        difficulty_score = max(0, 1 - (level_diff * 0.3))
        similarity_scores.append(difficulty_score)
        
        # Duration match (attention span)
        user_attention = user_profile.get("attention_span_minutes", 30)
        content_duration = content_profile.get("duration_minutes", 30)
        
        duration_ratio = min(user_attention, content_duration) / max(user_attention, content_duration)
        similarity_scores.append(duration_ratio)
        
        # Calculate weighted average
        return np.mean(similarity_scores)
    
    def calculate_collaborative_score(self,
                                     user_id: str,
                                     content_id: str,
                                     user_interactions: Dict[str, List[str]]) -> float:
        """
        Calculate collaborative filtering score based on similar users
        
        Args:
            user_id: Current user ID
            content_id: Content ID to score
            user_interactions: Dictionary mapping user_ids to content_ids they liked
            
        Returns:
            Collaborative score (0-1)
        """
        # In production, this would use actual user interaction data
        # For now, return a baseline score
        
        if user_id not in user_interactions:
            return 0.5
        
        user_content = set(user_interactions.get(user_id, []))
        
        # Find similar users (who interacted with same content)
        similar_users = []
        for other_user, other_content in user_interactions.items():
            if other_user != user_id:
                overlap = len(user_content.intersection(set(other_content)))
                if overlap > 0:
                    similarity = overlap / max(len(user_content), len(other_content))
                    similar_users.append((other_user, similarity))
        
        # Check if similar users liked this content
        if similar_users:
            weighted_score = 0
            total_weight = 0
            
            for similar_user, similarity in similar_users:
                if content_id in user_interactions.get(similar_user, []):
                    weighted_score += similarity
                total_weight += similarity
            
            if total_weight > 0:
                return weighted_score / total_weight
        
        return 0.5
    
    def rank_by_performance_fit(self,
                               content_items: List[Dict],
                               performance_history: List[float],
                               cognitive_capacity: float) -> List[Dict]:
        """
        Rank content by fit with user's current performance level
        
        Args:
            content_items: List of content metadata dictionaries
            performance_history: Recent performance scores
            cognitive_capacity: User's cognitive load capacity (0-10)
            
        Returns:
            Sorted list of content items
        """
        if not performance_history:
            return content_items
        
        avg_performance = np.mean(performance_history[-5:])
        
        # Score each content item
        scored_items = []
        for item in content_items:
            difficulty = item.get("difficulty_level", "intermediate")
            complexity = item.get("complexity_rating", 5)
            
            # Calculate performance fit
            if avg_performance > 0.8:
                # High performers: prefer higher difficulty
                target_difficulty = settings.DIFFICULTY_LEVELS[-2:]
            elif avg_performance > 0.6:
                # Medium performers: prefer middle difficulty
                target_difficulty = settings.DIFFICULTY_LEVELS[1:3]
            else:
                # Struggling: prefer lower difficulty
                target_difficulty = settings.DIFFICULTY_LEVELS[:2]
            
            fit_score = 1.0 if difficulty in target_difficulty else 0.5
            
            # Consider cognitive load
            load_fit = 1 - abs(complexity - cognitive_capacity) / 10
            
            total_score = (fit_score * 0.6) + (load_fit * 0.4)
            scored_items.append((item, total_score))
        
        # Sort by score
        scored_items.sort(key=lambda x: x[1], reverse=True)
        return [item for item, score in scored_items]
    
    def filter_prerequisites(self,
                           content_items: List[Dict],
                           completed_content: List[str]) -> List[Dict]:
        """
        Filter content based on prerequisite completion
        
        Args:
            content_items: List of content metadata
            completed_content: List of completed content IDs
            
        Returns:
            Filtered list of accessible content
        """
        accessible = []
        
        for item in content_items:
            prerequisites = item.get("prerequisites", [])
            
            # Check if all prerequisites are met
            if all(prereq in completed_content for prereq in prerequisites):
                accessible.append(item)
        
        return accessible
    
    def generate_recommendations(self,
                                user_profile: Dict,
                                available_content: List[Dict],
                                performance_history: List[float],
                                completed_content: List[str],
                                user_interactions: Dict = None) -> List[ContentRecommendation]:
        """
        Generate personalized content recommendations
        
        Args:
            user_profile: User's cognitive and learning profile
            available_content: List of available content items
            performance_history: Recent performance scores
            completed_content: List of completed content IDs
            user_interactions: Optional collaborative filtering data
            
        Returns:
            List of ContentRecommendation objects
        """
        user_id = user_profile.get("user_id")
        cognitive_capacity = user_profile.get("cognitive_load_capacity", 5.0)
        
        # Filter by prerequisites
        accessible_content = self.filter_prerequisites(available_content, completed_content)
        
        if not accessible_content:
            return []
        
        # Rank by performance fit
        ranked_content = self.rank_by_performance_fit(
            accessible_content,
            performance_history,
            cognitive_capacity
        )
        
        # Calculate hybrid scores
        recommendations = []
        
        for content in ranked_content[:self.max_recommendations * 2]:
            # Content-based score
            content_score = self.calculate_content_similarity(user_profile, content)
            
            # Collaborative score (if available)
            collab_score = 0.5
            if user_interactions:
                collab_score = self.calculate_collaborative_score(
                    user_id,
                    content.get("content_id"),
                    user_interactions
                )
            
            # Hybrid score (70% content-based, 30% collaborative)
            relevance_score = (content_score * 0.7) + (collab_score * 0.3)
            
            # Create recommendation object
            rec = ContentRecommendation(
                content_id=content.get("content_id", ""),
                title=content.get("title", ""),
                description=content.get("description", ""),
                content_type=content.get("content_type", "text"),
                difficulty_level=content.get("difficulty_level", "intermediate"),
                estimated_duration_minutes=content.get("duration_minutes", 30),
                relevance_score=round(relevance_score, 3),
                learning_objectives=content.get("learning_objectives", []),
                prerequisites=content.get("prerequisites", [])
            )
            
            recommendations.append(rec)
        
        # Sort by relevance and return top N
        recommendations.sort(key=lambda x: x.relevance_score, reverse=True)
        return recommendations[:self.max_recommendations]
    
    def generate_learning_path(self,
                              user_profile: Dict,
                              learning_goal: str,
                              available_modules: List[Dict]) -> List[Dict]:
        """
        Generate an optimal learning path toward a goal
        
        Args:
            user_profile: User's profile
            learning_goal: Target learning objective
            available_modules: Available learning modules
            
        Returns:
            Ordered list of modules forming a learning path
        """
        # Filter relevant modules
        relevant_modules = [
            m for m in available_modules
            if learning_goal.lower() in m.get("objectives", []).lower() or
               learning_goal.lower() in m.get("title", "").lower()
        ]
        
        if not relevant_modules:
            return []
        
        # Sort by difficulty (progressive learning)
        difficulty_order = {level: i for i, level in enumerate(settings.DIFFICULTY_LEVELS)}
        
        path = sorted(
            relevant_modules,
            key=lambda x: difficulty_order.get(x.get("difficulty_level", "intermediate"), 1)
        )
        
        # Ensure prerequisite chain
        ordered_path = []
        completed = set()
        
        while path:
            for module in path:
                prereqs = set(module.get("prerequisites", []))
                if prereqs.issubset(completed):
                    ordered_path.append(module)
                    completed.add(module.get("module_id"))
                    path.remove(module)
                    break
            else:
                # No module can be added (circular prerequisites or missing modules)
                break
        
        return ordered_path
