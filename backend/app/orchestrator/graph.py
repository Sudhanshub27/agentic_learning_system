from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from app.orchestrator.state import AgentState
from app.orchestrator.nodes import (
    planner_node,
    tutor_node,
    generate_assessment_node,
    grade_assessment_node,
    analyzer_node,
    strategy_node,
    update_state_node,
    memory_node
)

def should_end(state: AgentState) -> str:
    """Conditional edge routing based on the strategy output."""
    action = state.get("next_action")
    
    if action == "advance":
        # Check if we reached the end of the curriculum
        if state["current_topic_index"] >= len(state["curriculum"]) - 1:
            return "end"
        return "continue"
    elif action in ["reteach", "review_prerequisite"]:
        return "continue"
        
    return "end"

def build_graph():
    """Constructs the LangGraph state machine."""
    workflow = StateGraph(AgentState)
    
    # Add Nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("tutor", tutor_node)
    workflow.add_node("generate_assessment", generate_assessment_node)
    # The frontend interaction would happen between generate and grade.
    # In LangGraph, we handle this via checkpoints and interrupts.
    workflow.add_node("grade_assessment", grade_assessment_node)
    workflow.add_node("analyzer", analyzer_node)
    workflow.add_node("strategy", strategy_node)
    workflow.add_node("update_state", update_state_node)
    workflow.add_node("memory", memory_node)
    
    # Define Edges
    workflow.set_entry_point("planner")
    
    # Planner -> Tutor -> Generate Assessment
    workflow.add_edge("planner", "tutor")
    workflow.add_edge("tutor", "generate_assessment")
    
    # Generate -> Grade (Interrupt point)
    workflow.add_edge("generate_assessment", "grade_assessment")
    
    # Grade -> Analyzer -> Strategy -> Update
    workflow.add_edge("grade_assessment", "analyzer")
    workflow.add_edge("analyzer", "strategy")
    workflow.add_edge("strategy", "update_state")
    
    # After state update, decide whether to loop or end
    workflow.add_conditional_edges(
        "update_state",
        should_end,
        {
            "continue": "tutor",     # Loop back to tutor (new topic, reteach, or prerequisite)
            "end": "memory"          # Finish session
        }
    )
    
    # Memory -> END
    workflow.add_edge("memory", END)
    
    # Set up memory saver for state persistence (allows pausing/resuming)
    memory = MemorySaver()
    
    # Compile the graph
    app = workflow.compile(
        checkpointer=memory,
        # interrupt_before=["grade_assessment"] # Uncomment when tying to frontend
    )
    
    return app

# The compiled singleton graph instance
learning_graph = build_graph()
