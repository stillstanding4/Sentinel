from __future__ import annotations

from app.agents.state import AuditWorkflowState
from app.utils.ids import new_id
from app.utils.time import utc_now_iso
from app.utils.trust_score_model import calculate_trust_score_from_state


def calculate_trust_score(state: AuditWorkflowState) -> AuditWorkflowState:
    components = calculate_trust_score_from_state(state)
    state["review_status"] = components.review_status_label
    state["trust_score_breakdown"] = {
        "policies_passed": components.policies_passed,
        "total_policies": components.total_policies,
        "hallucination_check_passed": components.hallucination_check_passed,
        "pii_check_passed": components.pii_check_passed,
        "review_status": components.review_status_label,
    }

    state["trust_score"] = {
        "id": new_id("trust"),
        "agent_id": state["agent_id"],
        "audit_run_id": state["audit_run_id"],
        "overall_score": components.overall_score,
        "hallucination_score": components.safety,
        "policy_score": components.policy_compliance,
        "cost_score": components.cost_efficiency,
        "feedback_score": components.review_status,
        "calculation_notes": (
            "Trust Score = 40% Policy Compliance + 30% Safety + "
            "20% Cost Efficiency + 10% Review Status."
        ),
        "created_at": utc_now_iso(),
    }
    return state
