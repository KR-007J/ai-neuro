"""
Learning Style Classifier Training
Trains a model to predict VARK learning styles
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os

# Configuration
MODEL_PATH = "app/models/"
MODEL_NAME = "learning_style.pkl"


def generate_synthetic_data(n_samples=1000):
    """
    Generate synthetic training data for learning style classification
    
    Features:
    - Response patterns to visual content
    - Response patterns to auditory content
    - Response patterns to reading material
    - Response patterns to hands-on activities
    - Time spent on different modalities
    - Engagement with different content types
    """
    np.random.seed(42)
    
    data = []
    
    for _ in range(n_samples):
        # Generate base preference (dominant style)
        dominant_style = np.random.choice(['visual', 'auditory', 'reading_writing', 'kinesthetic'])
        
        # Create features based on dominant style
        if dominant_style == 'visual':
            visual_score = np.random.uniform(0.7, 1.0)
            auditory_score = np.random.uniform(0.1, 0.4)
            reading_score = np.random.uniform(0.1, 0.4)
            kinesthetic_score = np.random.uniform(0.1, 0.4)
        elif dominant_style == 'auditory':
            visual_score = np.random.uniform(0.1, 0.4)
            auditory_score = np.random.uniform(0.7, 1.0)
            reading_score = np.random.uniform(0.1, 0.4)
            kinesthetic_score = np.random.uniform(0.1, 0.4)
        elif dominant_style == 'reading_writing':
            visual_score = np.random.uniform(0.1, 0.4)
            auditory_score = np.random.uniform(0.1, 0.4)
            reading_score = np.random.uniform(0.7, 1.0)
            kinesthetic_score = np.random.uniform(0.1, 0.4)
        else:  # kinesthetic
            visual_score = np.random.uniform(0.1, 0.4)
            auditory_score = np.random.uniform(0.1, 0.4)
            reading_score = np.random.uniform(0.1, 0.4)
            kinesthetic_score = np.random.uniform(0.7, 1.0)
        
        # Additional features
        time_visual = visual_score * np.random.uniform(0.8, 1.2)
        time_auditory = auditory_score * np.random.uniform(0.8, 1.2)
        time_reading = reading_score * np.random.uniform(0.8, 1.2)
        time_kinesthetic = kinesthetic_score * np.random.uniform(0.8, 1.2)
        
        engagement_visual = visual_score * np.random.uniform(0.7, 1.0)
        engagement_auditory = auditory_score * np.random.uniform(0.7, 1.0)
        engagement_reading = reading_score * np.random.uniform(0.7, 1.0)
        engagement_kinesthetic = kinesthetic_score * np.random.uniform(0.7, 1.0)
        
        data.append([
            visual_score, auditory_score, reading_score, kinesthetic_score,
            time_visual, time_auditory, time_reading, time_kinesthetic,
            engagement_visual, engagement_auditory, engagement_reading, engagement_kinesthetic,
            dominant_style
        ])
    
    columns = [
        'visual_score', 'auditory_score', 'reading_score', 'kinesthetic_score',
        'time_visual', 'time_auditory', 'time_reading', 'time_kinesthetic',
        'engagement_visual', 'engagement_auditory', 'engagement_reading', 'engagement_kinesthetic',
        'learning_style'
    ]
    
    return pd.DataFrame(data, columns=columns)


def train_model(X_train, y_train):
    """Train Random Forest classifier"""
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    """Evaluate model performance"""
    predictions = model.predict(X_test)
    
    print("\n=== Classification Report ===")
    print(classification_report(y_test, predictions))
    
    print("\n=== Confusion Matrix ===")
    print(confusion_matrix(y_test, predictions))
    
    # Cross-validation score
    cv_scores = cross_val_score(model, X_test, y_test, cv=5)
    print(f"\n=== Cross-Validation Scores ===")
    print(f"Mean CV Score: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
    
    return predictions


def save_model(model, path):
    """Save trained model"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)
    print(f"\nModel saved to: {path}")


def main():
    """Main training pipeline"""
    print("🧠 Training Learning Style Classifier")
    print("=" * 50)
    
    # Generate data
    print("\n1. Generating synthetic training data...")
    df = generate_synthetic_data(n_samples=1000)
    print(f"   Generated {len(df)} samples")
    print(f"   Class distribution:\n{df['learning_style'].value_counts()}")
    
    # Prepare features and labels
    print("\n2. Preparing features and labels...")
    X = df.drop('learning_style', axis=1)
    y = df['learning_style']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   Training samples: {len(X_train)}")
    print(f"   Testing samples: {len(X_test)}")
    
    # Train model
    print("\n3. Training Random Forest classifier...")
    model = train_model(X_train, y_train)
    print("   Training complete!")
    
    # Evaluate
    print("\n4. Evaluating model performance...")
    evaluate_model(model, X_test, y_test)
    
    # Feature importance
    print("\n5. Feature Importance:")
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    print(feature_importance.head(10))
    
    # Save model
    print("\n6. Saving model...")
    model_path = os.path.join(MODEL_PATH, MODEL_NAME)
    save_model(model, model_path)
    
    print("\n✅ Training pipeline complete!")


if __name__ == "__main__":
    main()
