from __future__ import annotations

from html import escape

import streamlit as st

from app.backend.services.analytics_service import AnalyticsService
from app.backend.services.audit_service import AuditService
from app.backend.repositories.recommendation_repository import RecommendationRepository
from app.frontend.components.charts import bar_chart, trust_score_gauge
from app.frontend.components.layout import page_header, section_divider
from app.frontend.components.metric_cards import metric_card, status_badge
from app.frontend.components.policies import policy_id_for_finding, policy_violation_cards_html
from app.frontend.components.tables import dataframe
from app.frontend.components.trust_scores import trust_score_state


def render_dashboard() -> None:
    analytics = AnalyticsService().overview()
    recommendations = RecommendationRepository().list_recommendations()

    page_header(
        "Sentinel - Agent of Agents",
        "Observe. Audit. Trust. Optimize.",
        eyebrow="AgentOps Control Tower",
    )

    enterprise_trust = trust_score_state(analytics["enterprise_trust_score"])
    cols = st.columns(6)
    with cols[0]:
        metric_card(
            "Enterprise Trust Score",
            str(analytics["enterprise_trust_score"]),
            enterprise_trust["label"],
            enterprise_trust["metric_status"],
        )
    with cols[1]:
        metric_card("Hallucination Rate", f"{analytics['hallucination_rate']}%", "Unsupported claims", "watch")
    with cols[2]:
        metric_card("PII Incidents", str(analytics["pii_incidents"]), "Policy & PII violations", "risk")
    with cols[3]:
        metric_card("Average Cost per Run", f"${analytics['average_cost_per_run']:.4f}", "Operational cost", "neutral")
    with cols[4]:
        metric_card("Policy Violations", str(analytics["policy_violations"]), "Governance events", "risk")
    with cols[5]:
        metric_card("Agent Reuse", str(analytics["agent_reuse"]), "Captured runs", "good")

    _render_executive_summary(analytics)
    _render_executive_signals(analytics["executive_insights"])

    left, right = st.columns([0.42, 0.58], gap="large")
    with left:
        section_divider("Trust Score Engine", "Centralized governance score across observed Agents.")
        st.plotly_chart(trust_score_gauge(analytics["enterprise_trust_score"]), use_container_width=True)
    with right:
        section_divider("Agent Catalogue Snapshot", "Ownership, business unit and latest governance status.")
        agent_rows = []
        for agent in analytics["agents"]:
            score = agent.get("latest_trust_score") or 0
            state = trust_score_state(score)
            agent_rows.append(
                {
                    "Agent": agent["name"],
                    "Owner": agent["owner_name"],
                    "Business Unit": agent["business_unit"],
                    "Status": agent["status"],
                    "Trust Score": score,
                    "Trust State": state["label"],
                    "Policy": agent.get("latest_policy_status") or "PASS",
                }
            )
        dataframe(agent_rows)

    section_divider("Governance Watchlist", "Agents below Trusted require follow-up.")
    if analytics["at_risk_agents"]:
        cols = st.columns(len(analytics["at_risk_agents"]))
        for index, agent in enumerate(analytics["at_risk_agents"]):
            with cols[index]:
                score = agent.get("latest_trust_score") or 0
                state = trust_score_state(score)
                st.markdown(
                    f"""
                    <div class="metric-card metric-{state['metric_status']}">
                      <div class="metric-label">{agent['business_unit']}</div>
                      <div class="metric-value">{agent['name']}</div>
                      <div class="metric-detail">Trust Score {score} | {status_badge(state['label'], state['status'])}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        st.success("No agents are currently below Trusted.")

    left, right = st.columns(2, gap="large")
    with left:
        section_divider("Live Agent Audit Results")
        recent = AuditService().list_recent_audit_runs(8)
        dataframe(
            [
                {
                    "Agent": run["agent_name"],
                    "Scenario": run.get("scenario_key") or "manual",
                    "Tokens": run["total_tokens"],
                    "Cost": f"${run['estimated_cost']:.4f}",
                    "Status": run["status"],
                }
                for run in recent
            ]
        )
    with right:
        section_divider("Recommendation Engine")
        recommendation_counts: dict[str, int] = {}
        for recommendation in recommendations:
            recommendation_counts[recommendation["recommendation_type"]] = (
                recommendation_counts.get(recommendation["recommendation_type"], 0) + 1
            )
        st.plotly_chart(bar_chart(recommendation_counts, "Recommendations by Type"), use_container_width=True)


def _render_executive_summary(analytics: dict) -> None:
    insights = analytics.get("executive_insights", {})
    critical_agents = [
        agent for agent in analytics.get("agents", []) if (agent.get("latest_trust_score") or 0) < 60
    ]
    enterprise_trust = trust_score_state(analytics["enterprise_trust_score"])
    highest_business_risk = insights.get("most_critical_finding")
    cost_saving = insights.get("biggest_cost_saving_opportunity")
    latest_recommendation = insights.get("latest_recommendation")
    latest_audit = insights.get("most_recent_audit")

    section_divider("Executive Summary", "Current enterprise posture and board-level operating signals.")
    cols = st.columns(6)
    with cols[0]:
        metric_card(
            "Current Enterprise Health",
            enterprise_trust["label"],
            f"Trust Score {analytics['enterprise_trust_score']}",
            enterprise_trust["metric_status"],
        )
    with cols[1]:
        metric_card("Critical Agents", str(len(critical_agents)), "Trust Score below 60", "critical" if critical_agents else "good")
    with cols[2]:
        if highest_business_risk:
            metric_card("Highest Business Risk", highest_business_risk["agent_name"], highest_business_risk.get("description", "Governance finding"), "risk")
        else:
            metric_card("Highest Business Risk", "None", "No active critical finding", "good")
    with cols[3]:
        if cost_saving:
            metric_card("Biggest Cost Saving Opportunity", cost_saving["agent_name"], f"{cost_saving['total_tokens']:,} tokens", "watch")
        else:
            metric_card("Biggest Cost Saving Opportunity", "None", "No runs captured", "neutral")
    with cols[4]:
        if latest_recommendation:
            metric_card("Latest Recommendation", latest_recommendation["agent_name"], latest_recommendation["title"], "watch")
        else:
            metric_card("Latest Recommendation", "None", "No recommendations", "neutral")
    with cols[5]:
        if latest_audit:
            metric_card("Latest Audit Time", latest_audit.get("completed_at") or "Running", latest_audit["agent_name"], "neutral")
        else:
            metric_card("Latest Audit Time", "None", "No AuditRun captured", "neutral")


def _render_executive_signals(insights: dict) -> None:
    section_divider("Executive Signals", "Most recent operational facts from Sentinel.")
    most_recent = insights.get("most_recent_audit")
    critical = insights.get("most_critical_finding")
    highest_risk = insights.get("highest_risk_agent")
    cost_saving = insights.get("biggest_cost_saving_opportunity")
    latest_recommendation = insights.get("latest_recommendation")

    cols = st.columns(5)
    with cols[0]:
        if most_recent:
            metric_card(
                "Most Recent Audit",
                most_recent["agent_name"],
                most_recent.get("scenario_key") or "manual",
                "neutral",
            )
        else:
            metric_card("Most Recent Audit", "None", "No AuditRun captured", "neutral")
    with cols[1]:
        if critical:
            severity = critical.get("severity", "high")
            policy_html = (
                policy_violation_cards_html([policy_id_for_finding(critical)], compact=True)
                if critical.get("violation_type")
                else ""
            )
            st.markdown(
                f"""
                <div class="metric-card metric-risk">
                  <div class="metric-label">Most Critical Finding</div>
                  <div class="metric-value">{escape(critical['agent_name'])}</div>
                  <div class="metric-detail">{policy_html or f"{status_badge(severity.title(), severity.lower())} {escape(critical.get('description', 'Governance finding detected.'))}"}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            metric_card("Most Critical Finding", "None", "No active findings", "good")
    with cols[2]:
        if highest_risk:
            score = highest_risk.get("latest_trust_score") or 0
            state = trust_score_state(score)
            metric_card("Highest Risk Agent", highest_risk["name"], f"Trust Score {score} | {state['label']}", state["metric_status"])
        else:
            metric_card("Highest Risk Agent", "None", "No agents available", "neutral")
    with cols[3]:
        if cost_saving:
            metric_card(
                "Biggest Cost Saving Opportunity",
                cost_saving["agent_name"],
                f"{cost_saving['total_tokens']:,} tokens",
                "watch" if cost_saving["total_tokens"] >= 8000 else "good",
            )
        else:
            metric_card("Biggest Cost Saving Opportunity", "None", "No AuditRun captured", "neutral")
    with cols[4]:
        if latest_recommendation:
            metric_card(
                "Latest Recommendation",
                latest_recommendation["agent_name"],
                latest_recommendation["title"],
                "risk" if latest_recommendation["severity"] in {"critical", "high"} else "watch",
            )
        else:
            metric_card("Latest Recommendation", "None", "No recommendations", "neutral")
