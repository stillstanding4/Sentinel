from __future__ import annotations

from typing import Any, TypedDict


class AuditWorkflowState(TypedDict, total=False):
    audit_run_id: str
    agent_id: str
    scenario_key: str | None
    input_text: str
    output_text: str
    context_summary: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost: float
    hallucination_findings: list[dict[str, Any]]
    policy_violations: list[dict[str, Any]]
    cost_analysis: dict[str, Any]
    trust_score: dict[str, Any]
    recommendations: list[dict[str, Any]]
    feedback_signals: dict[str, Any]
    errors: list[str]
