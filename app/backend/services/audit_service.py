from __future__ import annotations

from collections.abc import Callable
from typing import Any

from app.agents.cost_agent import evaluate_cost
from app.agents.feedback_engine import apply_feedback_signals
from app.agents.graph import WORKFLOW_STEPS
from app.agents.hallucination_agent import evaluate_hallucinations
from app.agents.policy_agent import evaluate_policy
from app.agents.recommendation_engine import generate_recommendations
from app.agents.state import AuditWorkflowState
from app.agents.trust_score_aggregator import calculate_trust_score
from app.backend.repositories.audit_run_repository import AuditRunRepository
from app.backend.repositories.finding_repository import FindingRepository
from app.backend.repositories.recommendation_repository import RecommendationRepository
from app.backend.repositories.trust_score_repository import TrustScoreRepository
from app.backend.services.explainability_service import ExplainabilityService
from app.backend.services.persistence_service import WorkflowPersistenceService
from app.demo.scenarios import DEMO_SCENARIOS
from app.utils.ids import new_id


ProgressCallback = Callable[[str, int, int], None]

LIVE_AUDIT_PROGRESS_STEPS = (
    "Capturing Agent Execution...",
    "Running Hallucination Evaluation...",
    "Running Policy Validation...",
    "Calculating Trust & Risk Score...",
    "Generating Recommendations...",
    "Updating Enterprise Dashboard...",
)


class AuditService:
    def __init__(self) -> None:
        self.audit_runs = AuditRunRepository()
        self.findings = FindingRepository()
        self.trust_scores = TrustScoreRepository()
        self.recommendations = RecommendationRepository()
        self.persistence = WorkflowPersistenceService()
        self.explainability = ExplainabilityService()

    def list_recent_audit_runs(self, limit: int = 20) -> list[dict]:
        return self.audit_runs.list_recent(limit)

    def run_demo_scenario(
        self,
        scenario_key: str,
        progress_callback: ProgressCallback | None = None,
    ) -> dict:
        scenario = DEMO_SCENARIOS[scenario_key]
        return self._execute_live_audit(
            {
                "audit_run_id": new_id("audit"),
                "agent_id": scenario["agent_id"],
                "scenario_key": scenario_key,
                "input_text": scenario["input_text"],
                "output_text": scenario["output_text"],
                "context_summary": scenario["context_summary"],
                "prompt_tokens": scenario["prompt_tokens"],
                "completion_tokens": scenario["completion_tokens"],
            },
            progress_callback,
        )

    def run_custom_audit(
        self,
        agent_id: str,
        input_text: str,
        output_text: str,
        context_summary: str,
        prompt_tokens: int,
        completion_tokens: int,
        progress_callback: ProgressCallback | None = None,
    ) -> dict:
        return self._execute_live_audit(
            {
                "audit_run_id": new_id("audit"),
                "agent_id": agent_id,
                "scenario_key": None,
                "input_text": input_text,
                "output_text": output_text,
                "context_summary": context_summary,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
            },
            progress_callback,
        )

    def _execute_live_audit(
        self,
        initial_state: dict[str, Any],
        progress_callback: ProgressCallback | None,
    ) -> dict:
        state: AuditWorkflowState = initial_state.copy()
        state.setdefault("errors", [])

        self._notify_progress(progress_callback, 0)
        state = apply_feedback_signals(state)

        self._notify_progress(progress_callback, 1)
        state = evaluate_hallucinations(state)

        self._notify_progress(progress_callback, 2)
        state = evaluate_policy(state)

        self._notify_progress(progress_callback, 3)
        state = evaluate_cost(state)
        state = calculate_trust_score(state)

        self._notify_progress(progress_callback, 4)
        state = generate_recommendations(state)

        self._notify_progress(progress_callback, 5)
        self.persistence.persist(state)

        return self.get_audit_result(state["audit_run_id"])

    def _notify_progress(
        self,
        progress_callback: ProgressCallback | None,
        step_index: int,
    ) -> None:
        if progress_callback is None:
            return
        progress_callback(
            LIVE_AUDIT_PROGRESS_STEPS[step_index],
            step_index + 1,
            len(LIVE_AUDIT_PROGRESS_STEPS),
        )

    def get_audit_result(self, audit_run_id: str) -> dict:
        audit_run = self.audit_runs.get_audit_run(audit_run_id)
        policy_violations = self.findings.list_policy_violations(audit_run_id)
        hallucination_findings = self.findings.list_hallucination_findings(audit_run_id)
        recommendations = [
            rec
            for rec in self.recommendations.list_recommendations()
            if rec["audit_run_id"] == audit_run_id
        ]
        explainability = self.explainability.build_audit_explainability(
            audit_run,
            policy_violations,
            hallucination_findings,
            recommendations,
        )
        return {
            "audit_run": audit_run,
            "policy_violations": policy_violations,
            "hallucination_findings": hallucination_findings,
            "recommendations": recommendations,
            **explainability,
            "workflow_steps": [step_name for step_name, _step in WORKFLOW_STEPS],
        }
