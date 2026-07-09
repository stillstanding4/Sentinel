from __future__ import annotations

from app.backend.repositories.agent_repository import AgentRepository
from app.backend.repositories.audit_run_repository import AuditRunRepository
from app.backend.repositories.feedback_repository import FeedbackRepository
from app.backend.repositories.finding_repository import FindingRepository
from app.backend.repositories.recommendation_repository import RecommendationRepository
from app.backend.repositories.trust_score_repository import TrustScoreRepository


class AgentCatalogueService:
    def __init__(self) -> None:
        self.agents = AgentRepository()
        self.audit_runs = AuditRunRepository()
        self.findings = FindingRepository()
        self.trust_scores = TrustScoreRepository()
        self.recommendations = RecommendationRepository()
        self.feedback = FeedbackRepository()

    def list_agents(self) -> list[dict]:
        return self.agents.list_agents()

    def list_users(self) -> list[dict]:
        return self.agents.list_users()

    def get_agent_details(self, agent_id: str) -> dict:
        agent = self.agents.get_agent(agent_id)
        if not agent:
            return {}
        audit_runs = self.audit_runs.list_by_agent(agent_id)
        return {
            "agent": agent,
            "audit_runs": audit_runs,
            "latest_trust_score": self.trust_scores.latest_by_agent(agent_id),
            "recommendations": self.recommendations.list_recommendations(agent_id),
            "feedback": self.feedback.list_feedback(agent_id),
        }
