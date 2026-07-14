from __future__ import annotations

from html import escape

import streamlit as st

from app.frontend.components.layout import page_header, section_divider
from app.utils.trust_score_model import TRUST_SCORE_WEIGHTS


POLICY_ROWS = [
    {
        "id": "P001",
        "name": "PII Protection",
        "description": "Prevent exposure of sensitive personal information such as:",
        "items": ["Email", "Phone Number", "Aadhaar", "Passport", "Employee ID"],
    },
    {
        "id": "P002",
        "name": "Evidence & Financial Grounding",
        "description": "Business or financial claims must be supported by trusted enterprise data.",
        "items": [],
    },
    {
        "id": "P003",
        "name": "Prompt Injection Protection",
        "description": "Detect jailbreaks, prompt injection and malicious instructions.",
        "items": [],
    },
    {
        "id": "P004",
        "name": "Cost Optimization",
        "description": "Identify excessive token usage, repeated context and inefficient prompts.",
        "items": [],
    },
    {
        "id": "P005",
        "name": "Human Approval Required",
        "description": (
            "Responses affecting HR, Finance, Legal or Procurement decisions require human review "
            "before execution."
        ),
        "items": [],
    },
]

SCORE_WEIGHTS = [
    ("Policy Compliance", round(TRUST_SCORE_WEIGHTS["Policy Compliance"] * 100), "Policies Passed / Total Policies"),
    ("Safety", round(TRUST_SCORE_WEIGHTS["Safety"] * 100), "Hallucination Check and PII Check"),
    ("Cost Efficiency", round(TRUST_SCORE_WEIGHTS["Cost Efficiency"] * 100), "Total token usage"),
    ("Review Status", round(TRUST_SCORE_WEIGHTS["Review Status"] * 100), "Sentinel governance review outcome"),
]


def render_governance_framework() -> None:
    page_header(
        "Governance Framework",
        "Transparent methodology for how Sentinel evaluates enterprise AI agents across policy, safety, cost and review status signals.",
        eyebrow="Sentinel Methodology",
    )

    section_divider("Enterprise Policy Library", "The controls Sentinel applies when auditing AI agent responses.")
    _render_policy_library()

    section_divider("Trust Score Calculation", "A weighted governance score designed for executive interpretation.")
    _render_score_model()

    section_divider("How Each Component Is Calculated", "Simple formulas behind each score contribution.")
    _render_component_calculations()

    section_divider("Example", "Finance Copilot Trust Score calculation.")
    _render_example()


def _render_policy_library() -> None:
    rows = "".join(_policy_row_html(policy) for policy in POLICY_ROWS)
    st.markdown(f'<div class="framework-policy-table">{rows}</div>', unsafe_allow_html=True)


def _policy_row_html(policy: dict) -> str:
    items_html = ""
    if policy["items"]:
        items = "".join(f"<li>{escape(item)}</li>" for item in policy["items"])
        items_html = f'<ul class="framework-policy-items">{items}</ul>'
    return (
        '<div class="framework-policy-row">'
        f'<div class="framework-policy-id">{escape(policy["id"])}</div>'
        '<div>'
        f'<div class="framework-policy-name">{escape(policy["id"])} – {escape(policy["name"])}</div>'
        f'<div class="framework-policy-description">{escape(policy["description"])}</div>'
        f"{items_html}"
        "</div>"
        "</div>"
    )


def _render_score_model() -> None:
    cards = "".join(
        (
            '<div class="score-weight-card">'
            f'<div class="score-weight-value">{weight}%</div>'
            f'<div class="score-weight-name">{escape(name)}</div>'
            f'<div class="score-weight-detail">{escape(detail)}</div>'
            "</div>"
        )
        for name, weight, detail in SCORE_WEIGHTS
    )
    st.markdown(
        f"""
        <div class="formula-card">
            <div class="formula-title">Trust Score =</div>
            <div class="formula-expression">
                40% Policy Compliance + 30% Safety + 20% Cost Efficiency + 10% Review Status
            </div>
        </div>
        <div class="score-weight-grid">{cards}</div>
        """,
        unsafe_allow_html=True,
    )


def _render_component_calculations() -> None:
    components = [
        {
            "icon": "✓",
            "title": "Policy Compliance",
            "body": "Policies Passed / Total Policies",
            "example": "4 of 5 Policies Passed | Score = 80%",
        },
        {
            "icon": "🛡",
            "title": "Safety",
            "body": "Average of Hallucination Check and PII Check",
            "example": "Both Pass = 100% | One Pass = 50% | Both Fail = 0%",
        },
        {
            "icon": "$",
            "title": "Cost Efficiency",
            "body": "Based on total token usage.",
            "example": "<1500 Tokens = 100% | 1500–2500 Tokens = 80% | >2500 Tokens = 60%",
        },
        {
            "icon": "👤",
            "title": "Review Status",
            "body": "Determined automatically by Sentinel after audit to simulate enterprise human governance.",
            "example": "Approved = 100% | Needs Review = 50% | Rejected = 0%",
        },
    ]
    cards = "".join(_component_card_html(component) for component in components)
    st.markdown(f'<div class="component-grid">{cards}</div>', unsafe_allow_html=True)


def _component_card_html(component: dict) -> str:
    return (
        '<div class="component-card">'
        f'<div class="component-icon">{escape(component["icon"])}</div>'
        f'<div class="component-title">{escape(component["title"])}</div>'
        f'<div class="component-body">{escape(component["body"])}</div>'
        f'<div class="component-example">{escape(component["example"])}</div>'
        "</div>"
    )


def _render_example() -> None:
    st.markdown(
        """
        <div class="example-card">
            <div class="example-header">
                <div>
                    <div class="example-eyebrow">Agent Example</div>
                    <div class="example-title">Finance Copilot</div>
                </div>
                <div class="example-score">68/100</div>
            </div>
            <div class="example-breakdown">
                <div><span>Policy Compliance</span><strong>80%</strong></div>
                <div><span>Safety</span><strong>50%</strong></div>
                <div><span>Cost Efficiency</span><strong>80%</strong></div>
                <div><span>Review Status</span><strong>50%</strong></div>
            </div>
            <div class="formula-card formula-card-compact">
                <div class="formula-expression">
                    (0.40 × 80) + (0.30 × 50) + (0.20 × 80) + (0.10 × 50) = 68/100
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
