from __future__ import annotations

from app.agents.state import AuditWorkflowState
from app.backend.repositories.audit_run_repository import AuditRunRepository
from app.backend.repositories.finding_repository import FindingRepository
from app.backend.repositories.recommendation_repository import RecommendationRepository
from app.backend.repositories.trust_score_repository import TrustScoreRepository
from app.utils.time import utc_now_iso


class WorkflowPersistenceService:
    def __init__(self) -> None:
        self.audit_runs = AuditRunRepository()
        self.findings = FindingRepository()
        self.trust_scores = TrustScoreRepository()
        self.recommendations = RecommendationRepository()

    def persist(self, state: AuditWorkflowState) -> None:
        now = utc_now_iso()
        self.audit_runs.upsert_audit_run(
            {
                "id": state["audit_run_id"],
                "agent_id": state["agent_id"],
                "scenario_key": state.get("scenario_key"),
                "input_text": state["input_text"],
                "output_text": state["output_text"],
                "context_summary": state.get("context_summary", ""),
                "model_name": "demo-deterministic",
                "prompt_tokens": state.get("prompt_tokens", 0),
                "completion_tokens": state.get("completion_tokens", 0),
                "total_tokens": state.get("total_tokens", 0),
                "estimated_cost": state.get("estimated_cost", 0),
                "status": "completed",
                "started_at": now,
                "completed_at": now,
            }
        )
        self.findings.replace_policy_violations(
            state["audit_run_id"], state.get("policy_violations", [])
        )
        self.findings.replace_hallucination_findings(
            state["audit_run_id"], state.get("hallucination_findings", [])
        )
        self.trust_scores.replace_for_run(state["audit_run_id"], state["trust_score"])
        self.recommendations.replace_for_run(
            state["audit_run_id"], state.get("recommendations", [])
        )
