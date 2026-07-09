from __future__ import annotations

from app.agents.state import AuditWorkflowState
from app.utils.ids import new_id
from app.utils.time import utc_now_iso


def evaluate_hallucinations(state: AuditWorkflowState) -> AuditWorkflowState:
    output = state.get("output_text", "")
    context = state.get("context_summary", "")
    scenario_key = state.get("scenario_key")
    findings: list[dict[str, object]] = []

    unsupported_finance_claim = "42%" in output and "No approved source supports" in context
    if scenario_key == "finance_hallucination" or unsupported_finance_claim:
        findings.append(
            {
                "id": new_id("hallucination"),
                "audit_run_id": state["audit_run_id"],
                "agent_id": state["agent_id"],
                "claim": "FY2024 revenue increased by 42%.",
                "evidence": "Approved finance source does not support a 42% FY2024 revenue increase.",
                "finding_status": "unsupported",
                "confidence": 0.94,
                "description": "Finance Copilot made an unsupported revenue-growth claim.",
                "created_at": utc_now_iso(),
            }
        )

    state["hallucination_findings"] = findings
    return state
