from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from app.backend.repositories.audit_run_repository import AuditRunRepository
from app.backend.repositories.trust_score_repository import TrustScoreRepository
from app.utils.trust_score_model import TRUST_SCORE_WEIGHTS


SEVERITY_RANK = {
    "critical": 4,
    "high": 3,
    "medium": 2,
    "low": 1,
}


class ExplainabilityService:
    def __init__(self) -> None:
        self.trust_scores = TrustScoreRepository()
        self.audit_runs = AuditRunRepository()

    def build_audit_explainability(
        self,
        audit_run: dict[str, Any],
        policy_violations: list[dict[str, Any]],
        hallucination_findings: list[dict[str, Any]],
        recommendations: list[dict[str, Any]],
    ) -> dict[str, Any]:
        trust_score = self.trust_scores.get_by_run(audit_run["id"])
        breakdown = self._score_breakdown(trust_score)
        executive_summary = self._executive_summary(
            audit_run,
            policy_violations,
            hallucination_findings,
            recommendations,
        )
        return {
            "trust_score": trust_score,
            "score_breakdown": breakdown,
            "executive_summary": executive_summary,
            "recommendation_cards": [
                self._recommendation_card(recommendation, policy_violations, hallucination_findings)
                for recommendation in recommendations
            ],
            "audit_timeline": self._audit_timeline(audit_run),
            "risk_badge": {
                "label": executive_summary["risk_level"],
                "status": executive_summary["risk_level"].lower(),
            },
        }

    def _score_breakdown(
        self,
        trust_score: dict[str, Any] | None,
    ) -> list[dict[str, Any]]:
        if not trust_score:
            return []

        factors = [
            ("Policy Compliance", trust_score["policy_score"], "Policies Passed / Total Policies."),
            ("Safety", trust_score["hallucination_score"], "Average of Hallucination Check and PII Check."),
            ("Cost Efficiency", trust_score["cost_score"], "Token usage and run-level operating cost."),
            ("Review Status", trust_score["feedback_score"], "Automatic enterprise governance review status."),
        ]
        return [
            {
                "factor": factor,
                "score": score,
                "weight": TRUST_SCORE_WEIGHTS[factor],
                "weighted_points": round(score * TRUST_SCORE_WEIGHTS[factor], 1),
                "explanation": explanation,
            }
            for factor, score, explanation in factors
        ]

    def _executive_summary(
        self,
        audit_run: dict[str, Any],
        policy_violations: list[dict[str, Any]],
        hallucination_findings: list[dict[str, Any]],
        recommendations: list[dict[str, Any]],
    ) -> dict[str, str]:
        highest_severity = self._highest_severity(policy_violations, recommendations)

        if any(item["violation_type"] == "PII" for item in policy_violations):
            return {
                "business_impact": "Potential exposure of employee PII.",
                "risk_level": "Critical",
                "estimated_business_impact": "Compliance breach risk and required remediation before production readiness.",
                "recommended_owner": "Compliance Officer",
                "priority": "Immediate",
            }
        if hallucination_findings:
            return {
                "business_impact": "Unsupported claim could enter executive decision-making.",
                "risk_level": "High",
                "estimated_business_impact": "Reduces trust in financial reporting and requires source-grounding controls.",
                "recommended_owner": "AI Platform Owner",
                "priority": "High",
            }
        if audit_run["total_tokens"] >= 1500:
            return {
                "business_impact": "Elevated token usage increases operating cost.",
                "risk_level": "Medium",
                "estimated_business_impact": "Cost reduction opportunity through context compression and reuse.",
                "recommended_owner": "AI Developer",
                "priority": "Planned",
            }

        return {
            "business_impact": "No critical governance issue detected.",
            "risk_level": highest_severity.title(),
            "estimated_business_impact": "Continue monitoring through Live Agent Audit.",
            "recommended_owner": "AI Platform Owner",
            "priority": "Routine",
        }

    def _highest_severity(
        self,
        policy_violations: list[dict[str, Any]],
        recommendations: list[dict[str, Any]],
    ) -> str:
        severities = [item["severity"] for item in policy_violations + recommendations]
        if not severities:
            return "low"
        return max(severities, key=lambda value: SEVERITY_RANK.get(value.lower(), 0))

    def _recommendation_card(
        self,
        recommendation: dict[str, Any],
        policy_violations: list[dict[str, Any]],
        hallucination_findings: list[dict[str, Any]],
    ) -> dict[str, str]:
        recommendation_type = recommendation["recommendation_type"]
        if recommendation_type == "policy":
            reason = "PII detected" if policy_violations else "Policy risk detected"
            expected_benefit = "Reduces compliance risk and protects sensitive employee data."
            estimated_impact = "Critical risk reduction"
            suggested_action = "Mask sensitive values before response generation and enforce policy guardrails."
        elif recommendation_type == "hallucination":
            reason = "Unsupported claim detected" if hallucination_findings else "Grounding gap detected"
            expected_benefit = "Improves executive trust in agent-generated analysis."
            estimated_impact = "High trust improvement"
            suggested_action = "Require approved evidence before financial or operational claims are shown."
        elif recommendation_type == "cost":
            reason = "Elevated token usage"
            expected_benefit = "Lowers Average Cost per Run and improves Agent reuse efficiency."
            estimated_impact = "Medium cost saving opportunity"
            suggested_action = "Cache repeated context, summarize vendor evidence and remove duplicated prompt sections."
        else:
            reason = "Trust monitoring signal"
            expected_benefit = "Maintains production readiness through continuous governance."
            estimated_impact = "Low operational improvement"
            suggested_action = "Keep the Agent in routine Live Agent Audit monitoring."

        return {
            "title": recommendation["title"],
            "reason": reason,
            "expected_benefit": expected_benefit,
            "estimated_impact": estimated_impact,
            "suggested_action": suggested_action,
            "severity": recommendation["severity"].title(),
            "status": recommendation["status"].title(),
        }

    def _audit_timeline(self, audit_run: dict[str, Any]) -> list[dict[str, str]]:
        started_at = self._parse_timestamp(audit_run["started_at"])
        events = [
            ("Agent Executed", started_at),
            ("Captured", started_at + timedelta(seconds=1)),
            ("Hallucination Check", started_at + timedelta(seconds=2)),
            ("Policy Validation", started_at + timedelta(seconds=3)),
            ("Trust Calculation", started_at + timedelta(seconds=4)),
            ("Recommendations", started_at + timedelta(seconds=5)),
            ("Completed", self._parse_timestamp(audit_run.get("completed_at")) or started_at + timedelta(seconds=6)),
        ]
        return [
            {"event": event, "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")}
            for event, timestamp in events
        ]

    def _parse_timestamp(self, value: str | None) -> datetime:
        if not value:
            return datetime.utcnow()
        return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None)
