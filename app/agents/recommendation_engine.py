from __future__ import annotations

from app.agents.state import AuditWorkflowState
from app.utils.ids import new_id
from app.utils.time import utc_now_iso


def generate_recommendations(state: AuditWorkflowState) -> AuditWorkflowState:
    recommendations: list[dict[str, object]] = []
    now = utc_now_iso()

    if state.get("policy_violations"):
        recommendations.append(
            {
                "id": new_id("rec"),
                "audit_run_id": state["audit_run_id"],
                "agent_id": state["agent_id"],
                "recommendation_type": "policy",
                "title": "Block PII in HR Assistant responses",
                "description": "Add output redaction and policy guardrails before HR summaries are shown to reviewers.",
                "severity": "critical",
                "status": "open",
                "created_at": now,
                "updated_at": now,
            }
        )

    if state.get("hallucination_findings"):
        recommendations.append(
            {
                "id": new_id("rec"),
                "audit_run_id": state["audit_run_id"],
                "agent_id": state["agent_id"],
                "recommendation_type": "hallucination",
                "title": "Ground Finance Copilot claims in approved sources",
                "description": "Require cited finance evidence before revenue growth claims enter executive reporting.",
                "severity": "high",
                "status": "open",
                "created_at": now,
                "updated_at": now,
            }
        )

    if state.get("cost_analysis", {}).get("is_high_usage"):
        recommendations.append(
            {
                "id": new_id("rec"),
                "audit_run_id": state["audit_run_id"],
                "agent_id": state["agent_id"],
                "recommendation_type": "cost",
                "title": "Reduce Procurement Agent token usage",
                "description": "Cache supplier context, summarize long documents and remove duplicated vendor history.",
                "severity": "medium",
                "status": "open",
                "created_at": now,
                "updated_at": now,
            }
        )

    if not recommendations:
        recommendations.append(
            {
                "id": new_id("rec"),
                "audit_run_id": state["audit_run_id"],
                "agent_id": state["agent_id"],
                "recommendation_type": "trust",
                "title": "Continue monitoring production readiness",
                "description": "No critical findings detected. Keep the agent in routine Live Agent Audit monitoring.",
                "severity": "low",
                "status": "open",
                "created_at": now,
                "updated_at": now,
            }
        )

    state["recommendations"] = recommendations
    return state
