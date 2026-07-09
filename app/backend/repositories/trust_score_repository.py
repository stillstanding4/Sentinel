from __future__ import annotations

from typing import Any

from sqlalchemy import delete, select

from app.backend.repositories.base import BaseRepository, model_to_dict
from app.models import Agent, TrustScore
from app.utils.time import utc_now_iso


class TrustScoreRepository(BaseRepository):
    def replace_for_run(self, audit_run_id: str, score: dict[str, Any]) -> None:
        with self.session() as session:
            session.execute(delete(TrustScore).where(TrustScore.audit_run_id == audit_run_id))
            session.add(
                TrustScore(
                    id=score["id"],
                    agent_id=score["agent_id"],
                    audit_run_id=audit_run_id,
                    overall_score=score["overall_score"],
                    hallucination_score=score["hallucination_score"],
                    policy_score=score["policy_score"],
                    cost_score=score["cost_score"],
                    feedback_score=score["feedback_score"],
                    calculation_notes=score["calculation_notes"],
                    created_at=score.get("created_at", utc_now_iso()),
                )
            )

    def latest_by_agent(self, agent_id: str) -> dict[str, Any] | None:
        statement = (
            select(TrustScore)
            .where(TrustScore.agent_id == agent_id)
            .order_by(TrustScore.created_at.desc())
            .limit(1)
        )
        with self.session() as session:
            score = session.scalars(statement).first()
            return model_to_dict(score) if score else None

    def get_by_run(self, audit_run_id: str) -> dict[str, Any] | None:
        statement = (
            select(TrustScore)
            .where(TrustScore.audit_run_id == audit_run_id)
            .order_by(TrustScore.created_at.desc())
            .limit(1)
        )
        with self.session() as session:
            score = session.scalars(statement).first()
            return model_to_dict(score) if score else None

    def list_by_agent(self, agent_id: str) -> list[dict[str, Any]]:
        statement = (
            select(TrustScore)
            .where(TrustScore.agent_id == agent_id)
            .order_by(TrustScore.created_at.asc())
        )
        with self.session() as session:
            scores = session.scalars(statement).all()
            return [model_to_dict(score) for score in scores]

    def list_scores(self) -> list[dict[str, Any]]:
        statement = (
            select(
                TrustScore.id,
                TrustScore.agent_id,
                TrustScore.audit_run_id,
                TrustScore.overall_score,
                TrustScore.hallucination_score,
                TrustScore.policy_score,
                TrustScore.cost_score,
                TrustScore.feedback_score,
                TrustScore.calculation_notes,
                TrustScore.created_at,
                Agent.name.label("agent_name"),
            )
            .join(Agent, Agent.id == TrustScore.agent_id)
            .order_by(TrustScore.created_at.asc())
        )
        with self.session() as session:
            return [dict(row) for row in session.execute(statement).mappings().all()]
