from __future__ import annotations

from app.backend.services.agent_catalogue_service import AgentCatalogueService
from app.backend.services.analytics_service import AnalyticsService
from app.backend.services.audit_service import AuditService
from app.backend.services.bootstrap_service import bootstrap_application

try:
    from fastapi import FastAPI
except ImportError:  # pragma: no cover - optional local API dependency
    FastAPI = None


def create_app():
    if FastAPI is None:
        raise RuntimeError("FastAPI is not installed. The Streamlit app does not require the API server.")

    bootstrap_application()
    api = FastAPI(title="Sentinel - Agent of Agents")

    @api.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @api.get("/agents")
    def list_agents() -> list[dict]:
        return AgentCatalogueService().list_agents()

    @api.get("/audit-runs")
    def list_audit_runs() -> list[dict]:
        return AuditService().list_recent_audit_runs()

    @api.post("/audit-runs/demo/{scenario_key}")
    def run_demo_scenario(scenario_key: str) -> dict:
        return AuditService().run_demo_scenario(scenario_key)

    @api.get("/analytics/overview")
    def analytics_overview() -> dict:
        return AnalyticsService().overview()

    return api


app = create_app() if FastAPI is not None else None
