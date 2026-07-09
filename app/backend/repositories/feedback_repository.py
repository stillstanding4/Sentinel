from __future__ import annotations

from typing import Any

from sqlalchemy import select

from app.backend.repositories.base import BaseRepository
from app.models import Agent, Feedback, User
from app.utils.time import utc_now_iso


class FeedbackRepository(BaseRepository):
    def create_feedback(self, feedback: dict[str, Any]) -> None:
        with self.session() as session:
            existing = session.get(Feedback, feedback["id"])
            if existing is None:
                session.add(
                    Feedback(
                        id=feedback["id"],
                        audit_run_id=feedback["audit_run_id"],
                        agent_id=feedback["agent_id"],
                        user_id=feedback["user_id"],
                        rating=feedback["rating"],
                        comment=feedback.get("comment", ""),
                        decision=feedback["decision"],
                        created_at=feedback.get("created_at", utc_now_iso()),
                    )
                )
                return
            existing.rating = feedback["rating"]
            existing.comment = feedback.get("comment", "")
            existing.decision = feedback["decision"]

    def list_feedback(self, agent_id: str | None = None) -> list[dict[str, Any]]:
        statement = (
            select(
                Feedback.id,
                Feedback.audit_run_id,
                Feedback.agent_id,
                Feedback.user_id,
                Feedback.rating,
                Feedback.comment,
                Feedback.decision,
                Feedback.created_at,
                Agent.name.label("agent_name"),
                User.name.label("user_name"),
                User.role.label("user_role"),
            )
            .join(Agent, Agent.id == Feedback.agent_id)
            .join(User, User.id == Feedback.user_id)
            .order_by(Feedback.created_at.desc())
        )
        if agent_id:
            statement = statement.where(Feedback.agent_id == agent_id)
        with self.session() as session:
            return [dict(row) for row in session.execute(statement).mappings().all()]
