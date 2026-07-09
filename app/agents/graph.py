from __future__ import annotations

from app.agents.cost_agent import evaluate_cost
from app.agents.feedback_engine import apply_feedback_signals
from app.agents.hallucination_agent import evaluate_hallucinations
from app.agents.policy_agent import evaluate_policy
from app.agents.recommendation_engine import generate_recommendations
from app.agents.state import AuditWorkflowState
from app.agents.trust_score_aggregator import calculate_trust_score


WORKFLOW_STEPS = [
    ("Sentinel Gateway", lambda state: state),
    ("Hallucination Check", evaluate_hallucinations),
    ("Policy Check", evaluate_policy),
    ("Cost Analysis", evaluate_cost),
    ("Trust Score", calculate_trust_score),
    ("Recommendations", generate_recommendations),
    ("Human Feedback", apply_feedback_signals),
    ("Dashboard Updated", lambda state: state),
]


def run_audit_workflow(initial_state: AuditWorkflowState) -> AuditWorkflowState:
    state = initial_state.copy()
    state.setdefault("errors", [])
    state = apply_feedback_signals(state)
    for _step_name, step in WORKFLOW_STEPS:
        state = step(state)
    return state


def build_langgraph_workflow():
    try:
        from langgraph.graph import END, StateGraph
    except ImportError:
        return None

    graph = StateGraph(AuditWorkflowState)
    graph.add_node("sentinel_gateway", lambda state: state)
    graph.add_node("hallucination_agent", evaluate_hallucinations)
    graph.add_node("policy_agent", evaluate_policy)
    graph.add_node("cost_agent", evaluate_cost)
    graph.add_node("trust_score_aggregator", calculate_trust_score)
    graph.add_node("recommendation_engine", generate_recommendations)
    graph.add_node("feedback_engine", apply_feedback_signals)
    graph.add_node("dashboard_update", lambda state: state)

    graph.set_entry_point("sentinel_gateway")
    graph.add_edge("sentinel_gateway", "hallucination_agent")
    graph.add_edge("hallucination_agent", "policy_agent")
    graph.add_edge("policy_agent", "cost_agent")
    graph.add_edge("cost_agent", "trust_score_aggregator")
    graph.add_edge("trust_score_aggregator", "recommendation_engine")
    graph.add_edge("recommendation_engine", "feedback_engine")
    graph.add_edge("feedback_engine", "dashboard_update")
    graph.add_edge("dashboard_update", END)
    return graph.compile()
