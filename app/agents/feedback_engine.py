from __future__ import annotations

from app.agents.state import AuditWorkflowState


def apply_feedback_signals(state: AuditWorkflowState) -> AuditWorkflowState:
    scenario_key = state.get("scenario_key")
    if scenario_key == "procurement_high_tokens":
        review_status = "Approved"
    elif scenario_key in {"hr_pii_leak", "finance_hallucination"}:
        review_status = "Needs Review"
    else:
        state.setdefault(
            "feedback_signals",
            {
                "source": "Sentinel automatic review status",
            },
        )
        return state
    state.setdefault(
        "feedback_signals",
        {
            "review_status": review_status,
            "source": "Sentinel automatic review status",
        },
    )
    return state
