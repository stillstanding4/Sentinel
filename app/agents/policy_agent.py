from __future__ import annotations

from app.agents.state import AuditWorkflowState
from app.utils.ids import new_id
from app.utils.pii import detect_pii
from app.utils.time import utc_now_iso


def evaluate_policy(state: AuditWorkflowState) -> AuditWorkflowState:
    text = f"{state.get('input_text', '')}\n{state.get('output_text', '')}"
    pii_findings = detect_pii(text)
    violations: list[dict[str, object]] = []

    if pii_findings:
        evidence = ", ".join(f"{finding['type']}: {finding['evidence']}" for finding in pii_findings)
        violations.append(
            {
                "id": new_id("policy"),
                "audit_run_id": state["audit_run_id"],
                "agent_id": state["agent_id"],
                "violation_type": "PII",
                "description": "Policy Evaluator detected exposed personal information in agent output.",
                "evidence": evidence,
                "severity": "critical",
                "policy_status": "FAIL",
                "created_at": utc_now_iso(),
            }
        )

    state["policy_violations"] = violations
    return state
