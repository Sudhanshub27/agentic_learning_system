from typing import List
from fastapi import APIRouter

from app.services.ml_service import ml_service

router = APIRouter()

@router.get("/mastery/{user_id}")
async def get_user_mastery(user_id: str):
    """
    Mock endpoint to retrieve overall mastery scores.
    In Phase 8/Prod, this queries the PostgreSQL database.
    """
    return {
        "user_id": user_id,
        "overall_mastery": 0.75,
        "subjects": [
            {"subject_name": "Python Programming", "mastery": 0.85},
            {"subject_name": "Constitutional Law", "mastery": 0.65}
        ]
    }

@router.get("/retention/{user_id}")
async def get_retention_warnings(user_id: str):
    """
    Queries the ML Service to find topics the user is likely forgetting.
    """
    # In a real app, query DB for user's past topics, calculate retention, and return.
    # For now, we mock the DB query and run the ML model.
    mock_past_topics = [
        {"name": "Decorators", "mastery": 0.9, "attempts": 2, "days_ago": 45, "diff": 8},
        {"name": "Generators", "mastery": 0.95, "attempts": 1, "days_ago": 2, "diff": 5}
    ]
    
    warnings = []
    for t in mock_past_topics:
        prob = ml_service.predict_retention(t["mastery"], t["attempts"], t["days_ago"], t["diff"])
        if ml_service.needs_review(prob):
            warnings.append({
                "topic": t["name"],
                "retention_probability": prob,
                "days_since_last_review": t["days_ago"]
            })
            
    return {"warnings": warnings}
