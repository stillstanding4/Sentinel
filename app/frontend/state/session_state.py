from __future__ import annotations

import streamlit as st


def ensure_state() -> None:
    st.session_state.setdefault("selected_agent_id", "agent_hr_assistant")
    st.session_state.setdefault("last_audit_result", None)
    st.session_state.setdefault("active_page", "Dashboard")
