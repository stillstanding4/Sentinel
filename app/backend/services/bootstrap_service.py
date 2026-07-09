from __future__ import annotations

from app.agents.graph import run_audit_workflow
from app.backend.repositories.agent_repository import AgentRepository
from app.backend.repositories.feedback_repository import FeedbackRepository
from app.backend.services.persistence_service import WorkflowPersistenceService
from app.demo.scenarios import DEMO_AGENTS, DEMO_SCENARIOS, DEMO_USERS
from app.models.database import initialize_database
from app.utils.time import utc_now_iso
from app.vectorstore.seed_data import seed_vectorstore


class BootstrapService:
    def __init__(self) -> None:
        self.agents = AgentRepository()
        self.feedback = FeedbackRepository()
        self.persistence = WorkflowPersistenceService()

    def initialize(self) -> None:
        initialize_database()
        seed_vectorstore()
        self._seed_users_and_agents()
        self._seed_demo_audit_runs()

    def _seed_users_and_agents(self) -> None:
        for user in DEMO_USERS:
            self.agents.upsert_user(user)
        for agent in DEMO_AGENTS:
            self.agents.upsert_agent(agent)

    def _seed_demo_audit_runs(self) -> None:
        for scenario_key, scenario in DEMO_SCENARIOS.items():
            audit_run_id = f"demo_run_{scenario_key}"
            workflow_state = run_audit_workflow(
                {
                    "audit_run_id": audit_run_id,
                    "agent_id": scenario["agent_id"],
                    "scenario_key": scenario_key,
                    "input_text": scenario["input_text"],
                    "output_text": scenario["output_text"],
                    "context_summary": scenario["context_summary"],
                    "prompt_tokens": scenario["prompt_tokens"],
                    "completion_tokens": scenario["completion_tokens"],
                }
            )
            self.persistence.persist(workflow_state)

        self.feedback.create_feedback(
            {
                "id": "demo_feedback_policy_review",
                "audit_run_id": "demo_run_hr_pii_leak",
                "agent_id": "agent_hr_assistant",
                "user_id": "user_compliance_officer",
                "rating": 2,
                "comment": "PII exposure requires remediation before production readiness.",
                "decision": "needs_review",
                "created_at": utc_now_iso(),
            }
        )
        self.feedback.create_feedback(
            {
                "id": "demo_feedback_finance_review",
                "audit_run_id": "demo_run_finance_hallucination",
                "agent_id": "agent_finance_copilot",
                "user_id": "user_ai_platform_owner",
                "rating": 3,
                "comment": "Revenue claims must cite approved finance evidence.",
                "decision": "needs_review",
                "created_at": utc_now_iso(),
            }
        )
        self.feedback.create_feedback(
            {
                "id": "demo_feedback_procurement_review",
                "audit_run_id": "demo_run_procurement_high_tokens",
                "agent_id": "agent_procurement_agent",
                "user_id": "user_ai_developer",
                "rating": 4,
                "comment": "Useful result, but token usage should be optimized.",
                "decision": "approve",
                "created_at": utc_now_iso(),
            }
        )


def bootstrap_application() -> None:
    BootstrapService().initialize()
