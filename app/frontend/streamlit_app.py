from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from app.backend.core.config import settings
from app.backend.services.bootstrap_service import bootstrap_application
from app.frontend.pages.agent_catalogue import render_agent_catalogue
from app.frontend.pages.agent_details import render_agent_details
from app.frontend.pages.analytics import render_analytics
from app.frontend.pages.dashboard import render_dashboard
from app.frontend.pages.live_audit import render_live_audit
from app.frontend.state.session_state import ensure_state
from app.frontend.styles import apply_enterprise_theme


PAGES = {
    "Dashboard": render_dashboard,
    "Agent Catalogue": render_agent_catalogue,
    "Agent Details": render_agent_details,
    "Live Audit": render_live_audit,
    "Analytics": render_analytics,
}


@st.cache_resource
def initialize_app() -> bool:
    bootstrap_application()
    return True


def render_sidebar() -> str:
    st.sidebar.markdown("## Sentinel")
    st.sidebar.caption(settings.tagline)
    st.sidebar.markdown("---")
    page = st.sidebar.radio(
        "Control Tower",
        list(PAGES.keys()),
        key="active_page",
    )
    st.sidebar.markdown("---")
    st.sidebar.success("Demo Mode active")
    st.sidebar.caption("Ships with HR Assistant, Finance Copilot and Procurement Agent.")
    st.sidebar.markdown(
        """
        <div class="sidebar-panel">
            <div class="sidebar-panel-title">Demo Walkthrough</div>
            <div class="sidebar-step">
                <div class="sidebar-step-name">1. Dashboard</div>
                <div class="sidebar-step-text">Open with enterprise health, risks and latest Sentinel signals.</div>
            </div>
            <div class="sidebar-step">
                <div class="sidebar-step-name">2. Agent Catalogue</div>
                <div class="sidebar-step-text">Show the governed inventory of enterprise AI agents.</div>
            </div>
            <div class="sidebar-step">
                <div class="sidebar-step-name">3. Agent Details</div>
                <div class="sidebar-step-text">Drill into ownership, Trust Score and audit history.</div>
            </div>
            <div class="sidebar-step">
                <div class="sidebar-step-name">4. Live Agent Audit</div>
                <div class="sidebar-step-text">Run Sentinel as an Agent-of-Agents Auditor.</div>
            </div>
            <div class="sidebar-step">
                <div class="sidebar-step-name">5. Analytics</div>
                <div class="sidebar-step-text">Close with trust, policy, cost and recommendation trends.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return page


def main() -> None:
    st.set_page_config(
        page_title=settings.app_name,
        page_icon="S",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    apply_enterprise_theme()
    ensure_state()
    try:
        initialize_app()
        page = render_sidebar()
        renderer = PAGES.get(page, render_dashboard)
        renderer()
    except Exception as exc:
        st.error("Sentinel could not load this view.")
        st.caption("The demo data and navigation are still available. Refresh the page or return to Dashboard.")
        with st.expander("Technical detail"):
            st.code(str(exc))


if __name__ == "__main__":
    main()
