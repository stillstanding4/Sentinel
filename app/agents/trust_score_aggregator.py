from __future__ import annotations

from app.agents.state import AuditWorkflowState
from app.utils.ids import new_id
from app.utils.time import utc_now_iso


def calculate_trust_score(state: AuditWorkflowState) -> AuditWorkflowState:
    policy_violations = state.get("policy_violations", [])
    hallucination_findings = state.get("hallucination_findings", [])
    cost_analysis = state.get("cost_analysis", {})
    feedback_signals = state.get("feedback_signals", {})

    policy_score = 30 if policy_violations else 96
    hallucination_score = 48 if hallucination_findings else 96
    cost_score = 54 if cost_analysis.get("is_high_usage") else 94
    feedback_score = int(feedback_signals.get("score", 86))

    overall = round(
        (policy_score * 0.35)
        + (hallucination_score * 0.25)
        + (cost_score * 0.20)
        + (feedback_score * 0.20)
    )

    state["trust_score"] = {
        "id": new_id("trust"),
        "agent_id": state["agent_id"],
        "audit_run_id": state["audit_run_id"],
        "overall_score": overall,
        "hallucination_score": hallucination_score,
        "policy_score": policy_score,
        "cost_score": cost_score,
        "feedback_score": feedback_score,
        "calculation_notes": (
            "Trust Score Engine combined Hallucination Evaluator, Policy Evaluator, "
            "Cost Optimizer and Feedback Loop signals."
        ),
        "created_at": utc_now_iso(),
    }
    return state
