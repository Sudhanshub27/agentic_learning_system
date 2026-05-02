import pytest
from app.services.ml_service import ml_service

def test_ml_service_initialization():
    """Verify that the ML service initializes and trains its baseline model."""
    assert ml_service.is_trained is True
    assert ml_service.model is not None

def test_ml_predict_retention():
    """Verify retention predictions make logical sense based on the baseline."""
    
    # 1. High mastery, few attempts, recent review, easy -> High retention
    high_retention = ml_service.predict_retention(
        mastery_score=1.0, 
        attempts_to_mastery=1, 
        days_since_last_review=1, 
        difficulty=2
    )
    
    # 2. Low mastery, many attempts, long time ago, hard -> Low retention
    low_retention = ml_service.predict_retention(
        mastery_score=0.5, 
        attempts_to_mastery=5, 
        days_since_last_review=45, 
        difficulty=9
    )
    
    assert high_retention > 0.8
    assert low_retention < 0.5
    assert high_retention > low_retention

def test_ml_needs_review():
    """Verify the threshold logic works."""
    assert ml_service.needs_review(0.5, threshold=0.75) is True
    assert ml_service.needs_review(0.9, threshold=0.75) is False
