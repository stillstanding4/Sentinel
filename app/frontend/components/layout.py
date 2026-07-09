from __future__ import annotations

from html import escape

import streamlit as st


def page_header(title: str, subtitle: str, eyebrow: str = "Sentinel") -> None:
    st.markdown(
        f"""
        <div class="page-header">
            <div class="page-eyebrow">{escape(eyebrow)}</div>
            <div class="page-title">{escape(title)}</div>
            <div class="page-subtitle">{escape(subtitle)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def empty_state(title: str, message: str) -> None:
    st.markdown(
        f"""
        <div class="empty-state">
            <div class="empty-state-title">{escape(title)}</div>
            <div class="empty-state-message">{escape(message)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_divider(title: str, subtitle: str | None = None) -> None:
    subtitle_html = f'<div class="section-subtitle">{escape(subtitle)}</div>' if subtitle else ""
    st.markdown(
        f"""
        <div class="section-divider">
            <div class="section-title">{escape(title)}</div>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
