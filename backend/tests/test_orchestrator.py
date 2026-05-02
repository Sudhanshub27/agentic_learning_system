import pytest
from app.orchestrator.graph import learning_graph

def test_graph_compiles():
    """Verify that the LangGraph state machine compiles without errors."""
    assert learning_graph is not None
    
    # Check that all nodes are present
    nodes = learning_graph.get_graph().nodes
    assert "planner" in nodes
    assert "tutor" in nodes
    assert "generate_assessment" in nodes
    assert "grade_assessment" in nodes
    assert "analyzer" in nodes
    assert "strategy" in nodes
    assert "update_state" in nodes
    assert "memory" in nodes
