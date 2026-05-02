import logging
from typing import Dict, Any

from app.orchestrator.state import AgentState
from app.agents.planner import planner_agent
from app.agents.tutor import tutor_agent
from app.agents.evaluator import evaluator_agent, QuestionSchema
from app.agents.analyzer import analyzer_agent
from app.agents.strategy import strategy_agent
from app.agents.memory import memory_agent

logger = logging.getLogger(__name__)

async def planner_node(state: AgentState) -> Dict[str, Any]:
    """Generates the curriculum if it doesn't exist."""
    logger.info("--- PLANNER NODE ---")
    
    if state.get("curriculum"):
        logger.info("Curriculum already exists. Skipping planner.")
        return {}
        
    result = await planner_agent.generate_curriculum(
        subject_name=state["subject_name"],
        subject_description=state["subject_description"],
        user_goals=state["user_goals"],
        current_level=state["user_level"]
    )
    
    topics = [t.model_dump() for t in result.topics]
    
    # Initialize the first topic
    first_topic = topics[0]
    
    return {
        "curriculum": topics,
        "current_topic_index": 0,
        "current_topic_name": first_topic["name"],
        "current_topic_content_type": first_topic["content_type"],
        "current_mastery_score": 0.0,
        "attempts_on_current_topic": 0,
        "known_weaknesses": []
    }

async def tutor_node(state: AgentState) -> Dict[str, Any]:
    """Teaches the current topic."""
    logger.info("--- TUTOR NODE ---")
    
    # If strategy dictated a specific focus, we could inject it here
    strategy_config = state.get("strategy_config", {})
    focus_areas = strategy_config.get("focus_areas", [])
    combined_weaknesses = state.get("known_weaknesses", []) + focus_areas
    
    materials = await tutor_agent.teach_topic(
        topic_name=state["current_topic_name"],
        subject_domain=state["subject_name"],
        user_level=state["user_level"],
        mastery_score=state["current_mastery_score"],
        known_weaknesses=combined_weaknesses,
        content_type=state["current_topic_content_type"]
    )
    
    return {
        "teaching_materials": materials,
        "attempts_on_current_topic": state.get("attempts_on_current_topic", 0) + 1
    }

async def generate_assessment_node(state: AgentState) -> Dict[str, Any]:
    """Generates questions for the current topic."""
    logger.info("--- EVALUATOR NODE (GENERATE) ---")
    
    difficulty = 5 # Default, could be scaled by mastery
    if state.get("strategy_config", {}).get("difficulty_adjustment") == "decrease":
        difficulty = 3
    elif state.get("strategy_config", {}).get("difficulty_adjustment") == "increase":
        difficulty = 7
        
    result = await evaluator_agent.generate_assessment(
        topic_name=state["current_topic_name"],
        difficulty_level=difficulty,
        content_type=state["current_topic_content_type"]
    )
    
    questions = [q.model_dump() for q in result.questions]
    return {"assessment_questions": questions}

# NOTE: In a real system, the graph would pause here using `interrupt_before`
# to wait for the user to answer the questions via the frontend. 
# For testing, we assume `user_answers` is populated.

async def grade_assessment_node(state: AgentState) -> Dict[str, Any]:
    """Grades the user's answers."""
    logger.info("--- EVALUATOR NODE (GRADE) ---")
    
    grading_results = []
    user_answers = state.get("user_answers", {})
    
    for q_data in state["assessment_questions"]:
        q_id = q_data["question_id"]
        answer = user_answers.get(q_id, "I don't know")
        
        # Convert dict back to Pydantic for the agent
        q_obj = QuestionSchema(**q_data)
        
        result = await evaluator_agent.grade_answer(q_obj, answer)
        res_dict = result.model_dump()
        res_dict["question_id"] = q_id
        grading_results.append(res_dict)
        
    return {"grading_results": grading_results}

async def analyzer_node(state: AgentState) -> Dict[str, Any]:
    """Analyzes the test results to calculate mastery and detect weaknesses."""
    logger.info("--- ANALYZER NODE ---")
    
    result = await analyzer_agent.analyze_results(
        topic_name=state["current_topic_name"],
        current_mastery_score=state["current_mastery_score"],
        test_results=state["grading_results"]
    )
    
    return {
        "new_mastery_score": result.new_mastery_score,
        "detected_weaknesses": [w.model_dump() for w in result.detected_weaknesses],
        "analysis_summary": result.analysis_summary
    }

async def strategy_node(state: AgentState) -> Dict[str, Any]:
    """Decides the next loop transition."""
    logger.info("--- STRATEGY NODE ---")
    
    result = await strategy_agent.determine_next_step(
        topic_name=state["current_topic_name"],
        analysis_summary=state["analysis_summary"],
        new_mastery_score=state["new_mastery_score"],
        detected_weaknesses=state["detected_weaknesses"],
        attempts=state["attempts_on_current_topic"]
    )
    
    return {
        "next_action": result.action,
        "strategy_config": result.strategy_config.model_dump()
    }

async def update_state_node(state: AgentState) -> Dict[str, Any]:
    """Utility node to apply the strategy's decision to the state."""
    logger.info("--- UPDATE STATE NODE ---")
    
    action = state["next_action"]
    updates = {
        "current_mastery_score": state["new_mastery_score"],
        # Append new weaknesses to known weaknesses
        "known_weaknesses": state.get("known_weaknesses", []) + [w["description"] for w in state.get("detected_weaknesses", [])]
    }
    
    if action == "advance":
        logger.info("Action: ADVANCE")
        next_idx = state["current_topic_index"] + 1
        if next_idx < len(state["curriculum"]):
            next_topic = state["curriculum"][next_idx]
            updates["current_topic_index"] = next_idx
            updates["current_topic_name"] = next_topic["name"]
            updates["current_topic_content_type"] = next_topic["content_type"]
            updates["attempts_on_current_topic"] = 0
            # Reset mastery for the new topic
            updates["current_mastery_score"] = 0.0 
        else:
            logger.info("Curriculum complete!")
            
    elif action == "review_prerequisite":
        logger.info("Action: REVIEW PREREQUISITE")
        prev_idx = max(0, state["current_topic_index"] - 1)
        prev_topic = state["curriculum"][prev_idx]
        updates["current_topic_index"] = prev_idx
        updates["current_topic_name"] = prev_topic["name"]
        updates["current_topic_content_type"] = prev_topic["content_type"]
        updates["attempts_on_current_topic"] = 0
        
    elif action == "reteach":
        logger.info("Action: RETEACH")
        # Keep same topic, attempts already incremented in tutor_node
        pass
        
    return updates

async def memory_node(state: AgentState) -> Dict[str, Any]:
    """Summarizes the session and saves to vector DB (Phase 5)."""
    logger.info("--- MEMORY NODE ---")
    
    weaknesses = [w["description"] for w in state.get("detected_weaknesses", [])]
    
    summary = await memory_agent.summarize_session(
        subject=state["subject_name"],
        topics_covered=[state["current_topic_name"]],
        overall_performance=f"Score: {state.get('new_mastery_score', 0.0)}",
        key_weaknesses=weaknesses
    )
    
    # In Phase 5, we will write this to ChromaDB and Postgres
    logger.info(f"Session Summary Generated: {summary[:100]}...")
    
    return {}
