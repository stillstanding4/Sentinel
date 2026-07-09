from __future__ import annotations

from typing import Any

from sqlalchemy import select

from app.backend.repositories.base import BaseRepository, model_to_dict
from app.models import Agent, PolicyViolation, TrustScore, User
from app.utils.time import utc_now_iso


class AgentRepository(BaseRepository):
    def upsert_user(self, user: dict[str, Any]) -> None:
        now = utc_now_iso()
        with self.session() as session:
            existing = session.get(User, user["id"])
            if existing is None:
                session.add(
                    User(
                        id=user["id"],
                        name=user["name"],
                        email=user["email"],
                        role=user["role"],
                        created_at=now,
                        updated_at=now,
                    )
                )
                return
            existing.name = user["name"]
            existing.email = user["email"]
            existing.role = user["role"]
            existing.updated_at = now

    def upsert_agent(self, agent: dict[str, Any]) -> None:
        now = utc_now_iso()
        with self.session() as session:
            existing = session.get(Agent, agent["id"])
            if existing is None:
                session.add(
                    Agent(
                        id=agent["id"],
                        name=agent["name"],
                        description=agent["description"],
                        owner_user_id=agent["owner_user_id"],
                        business_unit=agent["business_unit"],
                        agent_type=agent["agent_type"],
                        status=agent["status"],
                        created_at=now,
                        updated_at=now,
                    )
                )
                return
            existing.name = agent["name"]
            existing.description = agent["description"]
            existing.owner_user_id = agent["owner_user_id"]
            existing.business_unit = agent["business_unit"]
            existing.agent_type = agent["agent_type"]
            existing.status = agent["status"]
            existing.updated_at = now

    def list_agents(self) -> list[dict[str, Any]]:
        latest_trust_score = (
            select(TrustScore.overall_score)
            .where(TrustScore.agent_id == Agent.id)
            .order_by(TrustScore.created_at.desc())
            .limit(1)
            .scalar_subquery()
        )
        latest_policy_status = (
            select(PolicyViolation.policy_status)
            .where(PolicyViolation.agent_id == Agent.id)
            .order_by(PolicyViolation.created_at.desc())
            .limit(1)
            .scalar_subquery()
        )
        statement = (
            select(
                Agent.id,
                Agent.name,
                Agent.description,
                Agent.owner_user_id,
                Agent.business_unit,
                Agent.agent_type,
                Agent.status,
                Agent.created_at,
                Agent.updated_at,
                User.name.label("owner_name"),
                User.role.label("owner_role"),
                latest_trust_score.label("latest_trust_score"),
                latest_policy_status.label("latest_policy_status"),
            )
            .join(User, User.id == Agent.owner_user_id, isouter=True)
            .order_by(Agent.name)
        )
        with self.session() as session:
            return [dict(row) for row in session.execute(statement).mappings().all()]

    def get_agent(self, agent_id: str) -> dict[str, Any] | None:
        statement = (
            select(
                Agent.id,
                Agent.name,
                Agent.description,
                Agent.owner_user_id,
                Agent.business_unit,
                Agent.agent_type,
                Agent.status,
                Agent.created_at,
                Agent.updated_at,
                User.name.label("owner_name"),
                User.role.label("owner_role"),
            )
            .join(User, User.id == Agent.owner_user_id, isouter=True)
            .where(Agent.id == agent_id)
        )
        with self.session() as session:
            row = session.execute(statement).mappings().first()
            return dict(row) if row else None

    def list_users(self) -> list[dict[str, Any]]:
        with self.session() as session:
            users = session.scalars(select(User).order_by(User.name)).all()
            return [model_to_dict(user) for user in users]
