"""
Synthetic Data Generator
Generates realistic synthetic data for training and testing
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import os


class SyntheticDataGenerator:
    """Generate synthetic user interaction and assessment data"""
    
    def __init__(self, random_seed=42):
        np.random.seed(random_seed)
        self.learning_styles = ['visual', 'auditory', 'reading_writing', 'kinesthetic']
        self.difficulty_levels = ['beginner', 'intermediate', 'advanced', 'expert']
    
    def generate_user_profiles(self, n_users=100):
        """Generate synthetic user profiles"""
        profiles = []
        
        for i in range(n_users):
            profile = {
                'user_id': f'user_{i:04d}',
                'age': np.random.randint(15, 60),
                'education_level': np.random.choice([
                    'High School', 'Bachelor\'s', 'Master\'s', 'PhD'
                ]),
                'learning_style': np.random.choice(self.learning_styles),
                'cognitive_load_capacity': np.random.uniform(3, 10),
                'processing_speed': np.random.choice(['slow', 'medium', 'fast']),
                'attention_span_minutes': np.random.randint(15, 90),
                'current_difficulty': np.random.choice(self.difficulty_levels),
                'created_at': (datetime.now() - timedelta(days=np.random.randint(0, 365))).isoformat()
            }
            profiles.append(profile)
        
        return pd.DataFrame(profiles)
    
    def generate_assessment_responses(self, user_profile, n_questions=20):
        """Generate assessment responses for a user"""
        responses = []
        
        base_accuracy = min(user_profile['cognitive_load_capacity'] / 10, 1.0)
        
        for i in range(n_questions):
            # Performance varies based on cognitive capacity
            is_correct = np.random.random() < base_accuracy
            
            # Response time based on processing speed
            if user_profile['processing_speed'] == 'fast':
                base_time = np.random.uniform(3, 8)
            elif user_profile['processing_speed'] == 'medium':
                base_time = np.random.uniform(8, 15)
            else:
                base_time = np.random.uniform(15, 30)
            
            response = {
                'question_id': f'q_{i:03d}',
                'user_id': user_profile['user_id'],
                'is_correct': is_correct,
                'response_time_seconds': base_time * np.random.uniform(0.8, 1.2),
                'confidence_level': np.random.randint(1, 6),
                'difficulty': np.random.choice(self.difficulty_levels)
            }
            responses.append(response)
        
        return responses
    
    def generate_engagement_data(self, user_profile, n_sessions=10):
        """Generate engagement data for learning sessions"""
        sessions = []
        
        base_engagement = user_profile['cognitive_load_capacity'] / 10
        
        for i in range(n_sessions):
            session_duration = min(
                np.random.exponential(user_profile['attention_span_minutes']),
                120  # Max 2 hours
            )
            
            session = {
                'session_id': f'session_{i:04d}',
                'user_id': user_profile['user_id'],
                'duration_minutes': session_duration,
                'engagement_score': np.clip(
                    base_engagement + np.random.normal(0, 0.1),
                    0, 1
                ),
                'focus_level': np.random.beta(8, 2),  # Skewed towards high focus
                'interaction_count': int(session_duration * np.random.uniform(0.5, 2)),
                'completion_rate': np.random.beta(6, 2),
                'error_rate': np.random.beta(2, 8),
                'timestamp': (datetime.now() - timedelta(days=i)).isoformat()
            }
            sessions.append(session)
        
        return sessions
    
    def generate_content_library(self, n_items=50):
        """Generate learning content metadata"""
        content = []
        topics = [
            'Python Programming', 'Data Structures', 'Algorithms',
            'Machine Learning', 'Web Development', 'Databases',
            'Cloud Computing', 'DevOps', 'Security', 'Mobile Development'
        ]
        
        content_types = ['video', 'text', 'interactive', 'quiz']
        
        for i in range(n_items):
            item = {
                'content_id': f'content_{i:04d}',
                'title': f'{np.random.choice(topics)} - Module {i+1}',
                'difficulty_level': np.random.choice(self.difficulty_levels),
                'content_type': np.random.choice(content_types),
                'duration_minutes': np.random.randint(15, 120),
                'complexity_rating': np.random.randint(1, 11),
                'primary_modality': np.random.choice(self.learning_styles),
                'prerequisites': [],  # Would be filled based on difficulty progression
                'learning_objectives': [
                    f'Objective {j+1}' for j in range(np.random.randint(2, 6))
                ]
            }
            content.append(item)
        
        return pd.DataFrame(content)
    
    def save_datasets(self, output_dir='data/processed'):
        """Generate and save all synthetic datasets"""
        os.makedirs(output_dir, exist_ok=True)
        
        print("Generating synthetic datasets...")
        
        # User profiles
        print("  - User profiles...")
        users = self.generate_user_profiles(n_users=100)
        users.to_csv(f'{output_dir}/users.csv', index=False)
        
        # Content library
        print("  - Content library...")
        content = self.generate_content_library(n_items=50)
        content.to_csv(f'{output_dir}/content_library.csv', index=False)
        
        # Assessment responses and engagement data
        print("  - Assessment responses and engagement data...")
        all_responses = []
        all_sessions = []
        
        for _, user in users.iterrows():
            responses = self.generate_assessment_responses(user, n_questions=20)
            all_responses.extend(responses)
            
            sessions = self.generate_engagement_data(user, n_sessions=10)
            all_sessions.extend(sessions)
        
        # Save responses
        responses_df = pd.DataFrame(all_responses)
        responses_df.to_csv(f'{output_dir}/assessment_responses.csv', index=False)
        
        # Save sessions
        sessions_df = pd.DataFrame(all_sessions)
        sessions_df.to_csv(f'{output_dir}/engagement_sessions.csv', index=False)
        
        print(f"\n✅ Datasets saved to {output_dir}/")
        print(f"   - Users: {len(users)} profiles")
        print(f"   - Content: {len(content)} items")
        print(f"   - Responses: {len(all_responses)} records")
        print(f"   - Sessions: {len(all_sessions)} records")


if __name__ == '__main__':
    generator = SyntheticDataGenerator()
    generator.save_datasets()
