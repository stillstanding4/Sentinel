from __future__ import annotations

from html import escape

import streamlit as st


def metric_card(label: str, value: str, detail: str, status: str = "neutral") -> None:
    st.markdown(
        f"""
        <div class="metric-card metric-{status}">
            <div class="metric-label"><span class="metric-dot"></span>{escape(str(label))}</div>
            <div class="metric-value">{escape(str(value))}</div>
            <div class="metric-detail">{escape(str(detail))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_badge(label: str, status: str) -> str:
    normalized = status.lower().replace(" ", "-")
    return f'<span class="status-badge status-{normalized}">{escape(str(label))}</span>'
