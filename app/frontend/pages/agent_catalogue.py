from __future__ import annotations

import streamlit as st

from app.backend.services.agent_catalogue_service import AgentCatalogueService
from app.frontend.components.layout import page_header, section_divider
from app.frontend.components.tables import dataframe
from app.frontend.components.trust_scores import trust_score_state


def render_agent_catalogue() -> None:
    service = AgentCatalogueService()
    agents = service.list_agents()

    page_header(
        "Agent Catalogue",
        "Central inventory of enterprise AI agents, ownership, governance status and latest Trust Score.",
    )

    rows = [
        {
            "Agent": agent["name"],
            "Description": agent["description"],
            "Owner": agent["owner_name"],
            "Owner Role": agent["owner_role"],
            "Business Unit": agent["business_unit"],
            "Agent Type": agent["agent_type"],
            "Status": agent["status"],
            "Latest Trust Score": agent.get("latest_trust_score") or 0,
            "Trust State": trust_score_state(agent.get("latest_trust_score") or 0)["label"],
            "Latest Policy Status": agent.get("latest_policy_status") or "PASS",
        }
        for agent in agents
    ]
    dataframe(rows)

    section_divider("Register Agent", "Demo Mode uses the approved enterprise scenarios for a reliable executive walkthrough.")
    st.info("Demo Mode ships with HR Assistant, Finance Copilot and Procurement Agent. Full registration persistence can be extended from the Agent Catalogue service.")
