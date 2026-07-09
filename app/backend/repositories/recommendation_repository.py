from __future__ import annotations

from typing import Any

from sqlalchemy import delete, select

from app.backend.repositories.base import BaseRepository
from app.models import Agent, Recommendation
from app.utils.time import utc_now_iso


class RecommendationRepository(BaseRepository):
    def replace_for_run(self, audit_run_id: str, recommendations: list[dict[str, Any]]) -> None:
        with self.session() as session:
            session.execute(delete(Recommendation).where(Recommendation.audit_run_id == audit_run_id))
            session.add_all(
                [
                    Recommendation(
                        id=recommendation["id"],
                        audit_run_id=audit_run_id,
                        agent_id=recommendation["agent_id"],
                        recommendation_type=recommendation["recommendation_type"],
                        title=recommendation["title"],
                        description=recommendation["description"],
                        severity=recommendation["severity"],
                        status=recommendation.get("status", "open"),
                        created_at=recommendation.get("created_at", utc_now_iso()),
                        updated_at=recommendation.get(
                            "updated_at", recommendation.get("created_at", utc_now_iso())
                        ),
                    )
                    for recommendation in recommendations
                ]
            )

    def list_recommendations(self, agent_id: str | None = None) -> list[dict[str, Any]]:
        statement = (
            select(
                Recommendation.id,
                Recommendation.audit_run_id,
                Recommendation.agent_id,
                Recommendation.recommendation_type,
                Recommendation.title,
                Recommendation.description,
                Recommendation.severity,
                Recommendation.status,
                Recommendation.created_at,
                Recommendation.updated_at,
                Agent.name.label("agent_name"),
            )
            .join(Agent, Agent.id == Recommendation.agent_id)
            .order_by(Recommendation.created_at.desc())
        )
        if agent_id:
            statement = statement.where(Recommendation.agent_id == agent_id)
        with self.session() as session:
            return [dict(row) for row in session.execute(statement).mappings().all()]

    def update_status(self, recommendation_id: str, status: str) -> None:
        with self.session() as session:
            recommendation = session.get(Recommendation, recommendation_id)
            if recommendation is None:
                return
            recommendation.status = status
            recommendation.updated_at = utc_now_iso()
