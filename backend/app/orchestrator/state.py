from typing import TypedDict, List, Dict, Any, Optional

class AgentState(TypedDict):
    """
    The shared state passed between all agents in the LangGraph workflow.
    """
    
    # Context
    session_id: str
    user_id: str
    
    # Curriculum Data
    subject_name: str
    subject_description: str
    user_goals: str
    user_level: str
    curriculum: List[Dict[str, Any]]  # List of Topic dictionaries
    
    # Current Execution State
    current_topic_index: int
    current_topic_name: str
    current_topic_content_type: str
    current_mastery_score: float
    attempts_on_current_topic: int
    known_weaknesses: List[str]
    
    # Generated Outputs
    teaching_materials: str
    assessment_questions: List[Dict[str, Any]]
    
    # User Interaction (in a real system, the graph would pause to wait for this)
    user_answers: Dict[str, str] # Map of question_id to user_answer
    
    # Evaluation & Analysis
    grading_results: List[Dict[str, Any]]
    analysis_summary: str
    detected_weaknesses: List[Dict[str, str]]
    new_mastery_score: float
    
    # Strategy
    next_action: str # advance, reteach, review_prerequisite
    strategy_config: Dict[str, Any]
