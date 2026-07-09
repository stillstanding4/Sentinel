from __future__ import annotations

import streamlit as st

from app.backend.services.agent_catalogue_service import AgentCatalogueService
from app.frontend.components.charts import trust_score_gauge
from app.frontend.components.layout import empty_state, page_header
from app.frontend.components.metric_cards import metric_card
from app.frontend.components.tables import dataframe


def render_agent_details() -> None:
    service = AgentCatalogueService()
    agents = service.list_agents()
    page_header(
        "Agent Details",
        "Review ownership, Trust Score history, AuditRun history, Recommendations and Human Feedback for one Agent.",
    )
    if not agents:
        empty_state("No agents registered", "Demo Mode will seed HR Assistant, Finance Copilot and Procurement Agent on startup.")
        return
    agent_names = {agent["name"]: agent["id"] for agent in agents}

    selected_name = st.selectbox("Agent", list(agent_names.keys()))
    st.session_state.selected_agent_id = agent_names[selected_name]
    details = service.get_agent_details(st.session_state.selected_agent_id)
    if not details:
        empty_state("Agent not found", "Choose another Agent from the Agent Catalogue.")
        return

    agent = details["agent"]
    score = details.get("latest_trust_score") or {}
    st.markdown(f'<div class="section-divider"><div class="section-title">{agent["name"]}</div></div>', unsafe_allow_html=True)

    left, right = st.columns([0.35, 0.65], gap="large")
    with left:
        metric_card("Business Unit", agent["business_unit"], agent["owner_name"], "neutral")
        metric_card("Agent Type", agent["agent_type"], agent["status"], "good" if agent["status"] == "active" else "watch")
    with right:
        if score:
            st.plotly_chart(trust_score_gauge(score["overall_score"]), use_container_width=True)
        else:
            empty_state("No Trust Score available", "Run Live Agent Audit to generate the first Trust Score.")

    tabs = st.tabs(["AuditRun History", "Recommendations", "Human Feedback"])
    with tabs[0]:
        dataframe(
            [
                {
                    "AuditRun": run["id"],
                    "Scenario": run.get("scenario_key") or "manual",
                    "Tokens": run["total_tokens"],
                    "Cost": f"${run['estimated_cost']:.4f}",
                    "Status": run["status"],
                    "Completed": run.get("completed_at"),
                }
                for run in details["audit_runs"]
            ]
        )
    with tabs[1]:
        dataframe(
            [
                {
                    "Type": item["recommendation_type"],
                    "Title": item["title"],
                    "Severity": item["severity"],
                    "Status": item["status"],
                }
                for item in details["recommendations"]
            ]
        )
    with tabs[2]:
        dataframe(
            [
                {
                    "Reviewer": item["user_name"],
                    "Role": item["user_role"],
                    "Rating": item["rating"],
                    "Decision": item["decision"],
                    "Comment": item["comment"],
                }
                for item in details["feedback"]
            ]
        )
