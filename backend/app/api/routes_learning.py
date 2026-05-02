import logging
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.orchestrator.graph import learning_graph
from app.orchestrator.state import AgentState

logger = logging.getLogger(__name__)

router = APIRouter()

# --- Schemas ---

class StartSessionRequest(BaseModel):
    user_id: str
    subject_name: str
    subject_description: str = ""
    user_goals: str = "Learn the basics"
    current_level: str = "Beginner"

class StartSessionResponse(BaseModel):
    session_id: str
    curriculum: List[Dict[str, Any]]
    current_topic: str
    teaching_materials: str
    assessment_questions: List[Dict[str, Any]]

class SubmitAnswersRequest(BaseModel):
    session_id: str
    user_id: str
    answers: Dict[str, str] # question_id -> answer text

class SubmitAnswersResponse(BaseModel):
    grading_results: List[Dict[str, Any]]
    analysis_summary: str
    next_action: str
    # If the system looped back to tutor, these will be populated with the *next* topic's data
    next_topic: str = ""
    next_teaching_materials: str = ""
    next_assessment_questions: List[Dict[str, Any]] = []

# --- Routes ---

@router.post("/start", response_model=StartSessionResponse)
async def start_learning_session(req: StartSessionRequest):
    """
    Initializes a new learning session, generates a curriculum, teaches the first topic,
    and generates the first assessment.
    """
    import uuid
    session_id = str(uuid.uuid4())
    
    # Initialize the state
    initial_state = {
        "session_id": session_id,
        "user_id": req.user_id,
        "subject_name": req.subject_name,
        "subject_description": req.subject_description,
        "user_goals": req.user_goals,
        "user_level": req.current_level,
        "curriculum": [],
        "current_topic_index": 0,
        "current_topic_name": "",
        "current_topic_content_type": "",
        "current_mastery_score": 0.0,
        "attempts_on_current_topic": 0,
        "known_weaknesses": [],
    }
    
    # Configuration for the checkpointer (memory saver)
    config = {"configurable": {"thread_id": session_id}}
    
    try:
        # Run the graph until the end of the generate_assessment node
        # In a real setup with interrupts, it pauses automatically. 
        # For now, we just invoke it and it runs all the way through because we mocked user input,
        # wait, we didn't add the interrupt. Let's just run it. 
        # Actually, without the interrupt it will crash on grading because user_answers is missing.
        # So we MUST run it node-by-node or add the interrupt.
        # Let's run it step by step for the API manually if interrupt isn't configured,
        # OR just call ainvoker. 
        
        # Let's use standard ainvoke. We will just pass empty answers so it doesn't crash if it goes too far.
        # But actually, the graph is configured to run straight through.
        # Since this is a portfolio project, we will simulate the "pause" by returning the state 
        # at a specific point.
        pass
        
    except Exception as e:
        logger.error(f"Failed to start session: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error starting session")
        
    # To keep this simple and robust without relying on LangGraph interrupts (which can be finicky in FastAPI),
    # we will just call the nodes directly for the API layer to have fine-grained control.
    from app.orchestrator.nodes import planner_node, tutor_node, generate_assessment_node
    
    state = initial_state.copy()
    
    # Run Planner
    planner_updates = await planner_node(state)
    state.update(planner_updates)
    
    # Run Tutor
    tutor_updates = await tutor_node(state)
    state.update(tutor_updates)
    
    # Run Generate Assessment
    eval_updates = await generate_assessment_node(state)
    state.update(eval_updates)
    
    # Save the state manually to an in-memory dictionary for this demo
    # (In prod, this goes to PostgreSQL/Redis)
    global_session_store[session_id] = state
    
    return StartSessionResponse(
        session_id=session_id,
        curriculum=state.get("curriculum", []),
        current_topic=state.get("current_topic_name", ""),
        teaching_materials=state.get("teaching_materials", ""),
        assessment_questions=state.get("assessment_questions", [])
    )

# A simple dictionary to hold session state in memory for the API demo
global_session_store = {}

@router.post("/submit_answers", response_model=SubmitAnswersResponse)
async def submit_answers(req: SubmitAnswersRequest):
    """
    Submits answers, grades them, analyzes performance, updates strategy,
    and returns the NEXT step.
    """
    state = global_session_store.get(req.session_id)
    if not state:
        raise HTTPException(status_code=404, detail="Session not found")
        
    state["user_answers"] = req.answers
    
    from app.orchestrator.nodes import (
        grade_assessment_node, 
        analyzer_node, 
        strategy_node, 
        update_state_node,
        tutor_node,
        generate_assessment_node
    )
    
    # 1. Grade
    grade_updates = await grade_assessment_node(state)
    state.update(grade_updates)
    
    # 2. Analyze
    analyze_updates = await analyzer_node(state)
    state.update(analyze_updates)
    
    # 3. Strategy
    strategy_updates = await strategy_node(state)
    state.update(strategy_updates)
    
    # 4. Update State
    state_updates = await update_state_node(state)
    state.update(state_updates)
    
    response = SubmitAnswersResponse(
        grading_results=state.get("grading_results", []),
        analysis_summary=state.get("analysis_summary", ""),
        next_action=state.get("next_action", "")
    )
    
    # If the action dictates continuing the loop, we run tutor and eval again for the new/reteach topic
    if state["next_action"] in ["advance", "reteach", "review_prerequisite"]:
        tutor_updates = await tutor_node(state)
        state.update(tutor_updates)
        
        eval_updates = await generate_assessment_node(state)
        state.update(eval_updates)
        
        response.next_topic = state.get("current_topic_name", "")
        response.next_teaching_materials = state.get("teaching_materials", "")
        response.next_assessment_questions = state.get("assessment_questions", [])
    else:
        # End of session, save memory
        from app.orchestrator.nodes import memory_node
        await memory_node(state)
        
    # Save state back
    global_session_store[req.session_id] = state
    
    return response
