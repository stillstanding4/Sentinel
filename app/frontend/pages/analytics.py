from __future__ import annotations

import streamlit as st

from app.backend.services.analytics_service import AnalyticsService
from app.frontend.components.charts import bar_chart, score_history
from app.frontend.components.layout import page_header, section_divider
from app.frontend.components.trust_scores import trust_score_state


def render_analytics() -> None:
    service = AnalyticsService()
    overview = service.overview()
    trends = service.trends()

    page_header(
        "Analytics",
        "Governance, trust and optimization trends for enterprise AI operations.",
    )

    enterprise_trust = trust_score_state(overview["enterprise_trust_score"])
    cols = st.columns(4)
    cols[0].metric("Enterprise Trust Score", overview["enterprise_trust_score"], enterprise_trust["label"])
    cols[1].metric("Hallucination Rate", f"{overview['hallucination_rate']}%")
    cols[2].metric("PII Incidents", overview["pii_incidents"])
    cols[3].metric("Average Cost per Run", f"${overview['average_cost_per_run']:.4f}")

    section_divider("Trust Score Trend", "Track production readiness across AuditRun history.")
    st.plotly_chart(score_history(trends["scores"]), use_container_width=True)

    left, right = st.columns(2, gap="large")
    with left:
        section_divider("Governance Signals")
        st.plotly_chart(bar_chart(trends["policy_by_severity"], "Policy Violations by Severity"), use_container_width=True)
        st.plotly_chart(bar_chart(trends["recommendation_by_type"], "Recommendations by Type"), use_container_width=True)
    with right:
        section_divider("Operational Signals")
        st.plotly_chart(bar_chart(overview["reuse_counts"], "Agent Reuse"), use_container_width=True)
        st.plotly_chart(bar_chart(trends["recommendation_by_status"], "Recommendation Status"), use_container_width=True)
