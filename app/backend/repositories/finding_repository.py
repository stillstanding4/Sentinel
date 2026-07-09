from __future__ import annotations

from typing import Any

from sqlalchemy import delete, select

from app.backend.repositories.base import BaseRepository
from app.models import Agent, HallucinationFinding, PolicyViolation
from app.utils.time import utc_now_iso


class FindingRepository(BaseRepository):
    def replace_policy_violations(self, audit_run_id: str, violations: list[dict[str, Any]]) -> None:
        with self.session() as session:
            session.execute(delete(PolicyViolation).where(PolicyViolation.audit_run_id == audit_run_id))
            session.add_all(
                [
                    PolicyViolation(
                        id=violation["id"],
                        audit_run_id=audit_run_id,
                        agent_id=violation["agent_id"],
                        violation_type=violation["violation_type"],
                        description=violation["description"],
                        evidence=violation["evidence"],
                        severity=violation["severity"],
                        policy_status=violation["policy_status"],
                        created_at=violation.get("created_at", utc_now_iso()),
                    )
                    for violation in violations
                ]
            )

    def replace_hallucination_findings(self, audit_run_id: str, findings: list[dict[str, Any]]) -> None:
        with self.session() as session:
            session.execute(
                delete(HallucinationFinding).where(HallucinationFinding.audit_run_id == audit_run_id)
            )
            session.add_all(
                [
                    HallucinationFinding(
                        id=finding["id"],
                        audit_run_id=audit_run_id,
                        agent_id=finding["agent_id"],
                        claim=finding["claim"],
                        evidence=finding["evidence"],
                        finding_status=finding["finding_status"],
                        confidence=finding["confidence"],
                        description=finding["description"],
                        created_at=finding.get("created_at", utc_now_iso()),
                    )
                    for finding in findings
                ]
            )

    def list_policy_violations(self, audit_run_id: str | None = None) -> list[dict[str, Any]]:
        statement = (
            select(
                PolicyViolation.id,
                PolicyViolation.audit_run_id,
                PolicyViolation.agent_id,
                PolicyViolation.violation_type,
                PolicyViolation.description,
                PolicyViolation.evidence,
                PolicyViolation.severity,
                PolicyViolation.policy_status,
                PolicyViolation.created_at,
                Agent.name.label("agent_name"),
            )
            .join(Agent, Agent.id == PolicyViolation.agent_id)
            .order_by(PolicyViolation.created_at.desc())
        )
        if audit_run_id:
            statement = statement.where(PolicyViolation.audit_run_id == audit_run_id)
        with self.session() as session:
            return [dict(row) for row in session.execute(statement).mappings().all()]

    def list_hallucination_findings(self, audit_run_id: str | None = None) -> list[dict[str, Any]]:
        statement = (
            select(
                HallucinationFinding.id,
                HallucinationFinding.audit_run_id,
                HallucinationFinding.agent_id,
                HallucinationFinding.claim,
                HallucinationFinding.evidence,
                HallucinationFinding.finding_status,
                HallucinationFinding.confidence,
                HallucinationFinding.description,
                HallucinationFinding.created_at,
                Agent.name.label("agent_name"),
            )
            .join(Agent, Agent.id == HallucinationFinding.agent_id)
            .order_by(HallucinationFinding.created_at.desc())
        )
        if audit_run_id:
            statement = statement.where(HallucinationFinding.audit_run_id == audit_run_id)
        with self.session() as session:
            return [dict(row) for row in session.execute(statement).mappings().all()]
