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
from app.frontend.pages.dashboard import render_dashboard
from app.frontend.pages.enterprise_live_control_room import render_enterprise_live_control_room
from app.frontend.pages.governance_framework import render_governance_framework
from app.frontend.state.session_state import ensure_state
from app.frontend.styles import apply_enterprise_theme


PAGES = {
    "Enterprise Live Control Room": render_enterprise_live_control_room,
    "Dashboard": render_dashboard,
    "Agent Catalogue": render_agent_catalogue,
    "📚 Governance Framework": render_governance_framework,
}


@st.cache_resource
def initialize_app() -> bool:
    bootstrap_application()
    return True


def render_sidebar() -> str:
    st.sidebar.markdown("## Sentinel")
    st.sidebar.caption(settings.tagline)
    st.sidebar.markdown("---")
    available_pages = list(PAGES.keys())
    if st.session_state.get("active_page") not in available_pages:
        st.session_state.active_page = available_pages[0]
    page = st.sidebar.radio(
        "Control Tower",
        available_pages,
        key="active_page",
    )
    st.sidebar.markdown("---")
    st.sidebar.success("Demo Mode active")
    st.sidebar.caption("Ships with HR Assistant, Finance Copilot and Procurement Agent.")
    with st.sidebar.expander("Demo Walkthrough", expanded=False):
        st.markdown(
            """
            <div class="sidebar-walkthrough">
                <div class="sidebar-step">
                    <div class="sidebar-step-name">1. Enterprise Live Control Room</div>
                    <div class="sidebar-step-text">Open with Sentinel monitoring multiple enterprise Agents in real time.</div>
                </div>
                <div class="sidebar-step">
                    <div class="sidebar-step-name">2. Dashboard</div>
                    <div class="sidebar-step-text">Show enterprise health, risks and latest Sentinel signals.</div>
                </div>
                <div class="sidebar-step">
                    <div class="sidebar-step-name">3. Agent Catalogue</div>
                    <div class="sidebar-step-text">Show the governed inventory of enterprise AI agents.</div>
                </div>
                <div class="sidebar-step">
                    <div class="sidebar-step-name">4. Governance Framework</div>
                    <div class="sidebar-step-text">Explain Sentinel's governance methodology for judges and enterprise users.</div>
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
        renderer = PAGES.get(page, render_enterprise_live_control_room)
        renderer()
    except Exception as exc:
        st.error("Sentinel could not load this view.")
        st.caption("The demo data and navigation are still available. Refresh the page or return to Dashboard.")
        with st.expander("Technical detail"):
            st.code(str(exc))


if __name__ == "__main__":
    main()
