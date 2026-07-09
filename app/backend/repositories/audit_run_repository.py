from __future__ import annotations

from typing import Any

from sqlalchemy import select

from app.backend.repositories.base import BaseRepository
from app.models import Agent, AuditRun
from app.utils.time import utc_now_iso


class AuditRunRepository(BaseRepository):
    def create_audit_run(self, run: dict[str, Any]) -> None:
        now = utc_now_iso()
        with self.session() as session:
            session.add(self._build_audit_run(run, created_at=now, fallback_started_at=now))

    def upsert_audit_run(self, run: dict[str, Any]) -> None:
        now = utc_now_iso()
        with self.session() as session:
            existing = session.get(AuditRun, run["id"])
            if existing is None:
                session.add(self._build_audit_run(run, created_at=now, fallback_started_at=now))
                return
            existing.agent_id = run["agent_id"]
            existing.scenario_key = run.get("scenario_key")
            existing.input_text = run["input_text"]
            existing.output_text = run["output_text"]
            existing.context_summary = run.get("context_summary", "")
            existing.model_name = run.get("model_name", "demo-deterministic")
            existing.prompt_tokens = run.get("prompt_tokens", 0)
            existing.completion_tokens = run.get("completion_tokens", 0)
            existing.total_tokens = run.get("total_tokens", 0)
            existing.estimated_cost = run.get("estimated_cost", 0)
            existing.status = run.get("status", "completed")
            existing.started_at = run.get("started_at", existing.started_at or now)
            existing.completed_at = run.get("completed_at", now)

    def update_status(self, audit_run_id: str, status: str) -> None:
        completed_at = utc_now_iso() if status == "completed" else None
        with self.session() as session:
            audit_run = session.get(AuditRun, audit_run_id)
            if audit_run is None:
                return
            audit_run.status = status
            audit_run.completed_at = completed_at

    def get_audit_run(self, audit_run_id: str) -> dict[str, Any] | None:
        statement = self._base_select().where(AuditRun.id == audit_run_id)
        with self.session() as session:
            row = session.execute(statement).mappings().first()
            return dict(row) if row else None

    def list_recent(self, limit: int = 20) -> list[dict[str, Any]]:
        statement = self._base_select().order_by(AuditRun.created_at.desc()).limit(limit)
        with self.session() as session:
            return [dict(row) for row in session.execute(statement).mappings().all()]

    def list_by_agent(self, agent_id: str) -> list[dict[str, Any]]:
        statement = (
            self._base_select()
            .where(AuditRun.agent_id == agent_id)
            .order_by(AuditRun.created_at.desc())
        )
        with self.session() as session:
            return [dict(row) for row in session.execute(statement).mappings().all()]

    def _base_select(self):
        return select(
            AuditRun.id,
            AuditRun.agent_id,
            AuditRun.scenario_key,
            AuditRun.input_text,
            AuditRun.output_text,
            AuditRun.context_summary,
            AuditRun.model_name,
            AuditRun.prompt_tokens,
            AuditRun.completion_tokens,
            AuditRun.total_tokens,
            AuditRun.estimated_cost,
            AuditRun.status,
            AuditRun.started_at,
            AuditRun.completed_at,
            AuditRun.created_at,
            Agent.name.label("agent_name"),
            Agent.business_unit,
        ).join(Agent, Agent.id == AuditRun.agent_id)

    def _build_audit_run(
        self,
        run: dict[str, Any],
        created_at: str,
        fallback_started_at: str,
    ) -> AuditRun:
        return AuditRun(
            id=run["id"],
            agent_id=run["agent_id"],
            scenario_key=run.get("scenario_key"),
            input_text=run["input_text"],
            output_text=run["output_text"],
            context_summary=run.get("context_summary", ""),
            model_name=run.get("model_name", "demo-deterministic"),
            prompt_tokens=run.get("prompt_tokens", 0),
            completion_tokens=run.get("completion_tokens", 0),
            total_tokens=run.get("total_tokens", 0),
            estimated_cost=run.get("estimated_cost", 0),
            status=run.get("status", "pending"),
            started_at=run.get("started_at", fallback_started_at),
            completed_at=run.get("completed_at"),
            created_at=created_at,
        )
