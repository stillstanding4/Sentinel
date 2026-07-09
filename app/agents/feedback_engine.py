from __future__ import annotations

from app.agents.state import AuditWorkflowState


def apply_feedback_signals(state: AuditWorkflowState) -> AuditWorkflowState:
    state.setdefault("feedback_signals", {"score": 86, "source": "Demo Mode baseline"})
    return state
