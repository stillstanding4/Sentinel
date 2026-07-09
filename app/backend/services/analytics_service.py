from __future__ import annotations

from collections import Counter, defaultdict
from statistics import mean

from app.backend.repositories.agent_repository import AgentRepository
from app.backend.repositories.audit_run_repository import AuditRunRepository
from app.backend.repositories.finding_repository import FindingRepository
from app.backend.repositories.recommendation_repository import RecommendationRepository
from app.backend.repositories.trust_score_repository import TrustScoreRepository


class AnalyticsService:
    def __init__(self) -> None:
        self.agents = AgentRepository()
        self.audit_runs = AuditRunRepository()
        self.findings = FindingRepository()
        self.trust_scores = TrustScoreRepository()
        self.recommendations = RecommendationRepository()

    def overview(self) -> dict:
        agents = self.agents.list_agents()
        audit_runs = self.audit_runs.list_recent(500)
        policy_violations = self.findings.list_policy_violations()
        hallucinations = self.findings.list_hallucination_findings()
        scores = self.trust_scores.list_scores()

        latest_scores_by_agent: dict[str, int] = {}
        for score in scores:
            latest_scores_by_agent[score["agent_id"]] = score["overall_score"]

        enterprise_trust_score = round(mean(latest_scores_by_agent.values())) if latest_scores_by_agent else 0
        hallucination_rate = round((len(hallucinations) / max(len(audit_runs), 1)) * 100, 1)
        pii_incidents = sum(1 for item in policy_violations if item["violation_type"] == "PII")
        average_cost = round(mean([run["estimated_cost"] for run in audit_runs]), 4) if audit_runs else 0

        reuse_counts = Counter(run["agent_name"] for run in audit_runs)
        at_risk_agents = [
            agent for agent in agents if (agent.get("latest_trust_score") or 0) < 80
        ]
        executive_insights = self._executive_insights(
            agents,
            audit_runs,
            policy_violations,
            hallucinations,
            self.recommendations.list_recommendations(),
        )

        return {
            "enterprise_trust_score": enterprise_trust_score,
            "hallucination_rate": hallucination_rate,
            "pii_incidents": pii_incidents,
            "average_cost_per_run": average_cost,
            "policy_violations": len(policy_violations),
            "agent_reuse": sum(reuse_counts.values()),
            "agents": agents,
            "audit_runs": audit_runs,
            "at_risk_agents": at_risk_agents,
            "reuse_counts": dict(reuse_counts),
            "executive_insights": executive_insights,
        }

    def trends(self) -> dict:
        scores = self.trust_scores.list_scores()
        recommendations = self.recommendations.list_recommendations()
        policy_violations = self.findings.list_policy_violations()
        hallucinations = self.findings.list_hallucination_findings()

        policy_by_severity = Counter(item["severity"] for item in policy_violations)
        recommendation_by_status = Counter(item["status"] for item in recommendations)
        recommendation_by_type = Counter(item["recommendation_type"] for item in recommendations)
        hallucination_by_agent = Counter(item["agent_name"] for item in hallucinations)

        scores_by_agent: dict[str, list[int]] = defaultdict(list)
        for score in scores:
            scores_by_agent[score["agent_name"]].append(score["overall_score"])

        return {
            "scores": scores,
            "policy_by_severity": dict(policy_by_severity),
            "recommendation_by_status": dict(recommendation_by_status),
            "recommendation_by_type": dict(recommendation_by_type),
            "hallucination_by_agent": dict(hallucination_by_agent),
            "scores_by_agent": dict(scores_by_agent),
        }

    def _executive_insights(
        self,
        agents: list[dict],
        audit_runs: list[dict],
        policy_violations: list[dict],
        hallucinations: list[dict],
        recommendations: list[dict],
    ) -> dict:
        most_recent_audit = audit_runs[0] if audit_runs else None
        highest_risk_agent = min(
            agents,
            key=lambda agent: agent.get("latest_trust_score") if agent.get("latest_trust_score") is not None else 101,
        ) if agents else None
        biggest_cost_saving = max(
            audit_runs,
            key=lambda audit_run: audit_run.get("total_tokens", 0),
        ) if audit_runs else None
        latest_recommendation = recommendations[0] if recommendations else None

        critical_policy = self._most_critical_policy_violation(policy_violations)
        most_critical_finding = critical_policy
        if most_critical_finding is None and hallucinations:
            most_critical_finding = {
                "agent_name": hallucinations[0]["agent_name"],
                "severity": "high",
                "description": hallucinations[0]["description"],
                "evidence": hallucinations[0]["evidence"],
            }

        return {
            "most_recent_audit": most_recent_audit,
            "most_critical_finding": most_critical_finding,
            "highest_risk_agent": highest_risk_agent,
            "biggest_cost_saving_opportunity": biggest_cost_saving,
            "latest_recommendation": latest_recommendation,
        }

    def _most_critical_policy_violation(self, policy_violations: list[dict]) -> dict | None:
        severity_order = {"critical": 4, "high": 3, "medium": 2, "low": 1}
        if not policy_violations:
            return None
        return max(
            policy_violations,
            key=lambda item: severity_order.get(item["severity"].lower(), 0),
        )
