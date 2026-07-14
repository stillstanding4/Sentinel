from __future__ import annotations

from html import escape

import plotly.graph_objects as go
import streamlit as st


KPI_CARDS = [
    {
        "icon": "▣",
        "label": "Total Enterprise Agents",
        "value": "48",
        "trend": "↑ +6 this month",
        "trend_state": "up",
        "subtitle": "Registered across business units",
        "accent": "blue",
    },
    {
        "icon": "✓",
        "label": "Active Agents",
        "value": "32",
        "trend": "↑ +5%",
        "trend_state": "up",
        "subtitle": "Currently monitored by Sentinel",
        "accent": "green",
    },
    {
        "icon": "◇",
        "label": "Trust Score",
        "value": "86",
        "trend": "↑ +2",
        "trend_state": "up",
        "subtitle": "Enterprise governance score",
        "accent": "blue",
    },
    {
        "icon": "!",
        "label": "Policy Violations",
        "value": "7",
        "trend": "↓ -18%",
        "trend_state": "down-good",
        "subtitle": "Open and recent findings",
        "accent": "red",
    },
    {
        "icon": "$",
        "label": "Business Value Protected",
        "value": "$2.1M",
        "trend": "↑ Estimated annual savings",
        "trend_state": "up",
        "subtitle": "Risk and cost exposure avoided",
        "accent": "green",
    },
]

AGENT_DISTRIBUTION = {
    "Finance": 12,
    "HR": 9,
    "Procurement": 8,
    "Legal": 7,
    "Operations": 6,
    "Customer Service": 6,
}

MONTHLY_ACTIVITY = {
    "Jan": 18,
    "Feb": 27,
    "Mar": 31,
    "Apr": 44,
    "May": 41,
    "Jun": 48,
}

TOP_PERFORMING_AGENTS = [
    {"agent": "Finance Copilot", "business_unit": "Finance", "trust_score": "92", "status": "Healthy", "last_audit": "2 mins ago"},
    {"agent": "HR Assistant", "business_unit": "People Operations", "trust_score": "74", "status": "Needs Review", "last_audit": "12 mins ago"},
    {"agent": "Procurement Agent", "business_unit": "Procurement", "trust_score": "86", "status": "Healthy", "last_audit": "5 mins ago"},
]

HIGHEST_RISK_AGENTS = [
    {"agent": "HR Assistant", "risk": "Critical", "policy": "P001", "impact": "PII Exposure"},
    {"agent": "Finance Copilot", "risk": "Medium", "policy": "P002", "impact": "Financial Claim"},
    {"agent": "Procurement Agent", "risk": "Medium", "policy": "P005", "impact": "Human Approval"},
]

GOVERNANCE_WATCHLIST = [
    {"time": "11:42", "agent": "HR Assistant", "policy": "P001", "severity": "Critical", "recommendation": "Mask employee SSN", "status": "Open"},
    {"time": "11:40", "agent": "Finance Copilot", "policy": "P002", "severity": "Medium", "recommendation": "Add evidence", "status": "In Progress"},
    {"time": "11:36", "agent": "Procurement", "policy": "P005", "severity": "Low", "recommendation": "Human approval", "status": "Resolved"},
]

CHART_COLORS = ["#2563EB", "#22C55E", "#14B8A6", "#8B5CF6", "#F59E0B", "#64748B"]


def render_dashboard() -> None:
    _inject_dashboard_styles()
    _render_header()
    _render_kpis()

    chart_left, chart_right = st.columns(2, gap="large")
    with chart_left:
        st.plotly_chart(_agent_distribution_chart(), use_container_width=True)
    with chart_right:
        st.plotly_chart(_activity_trend_chart(), use_container_width=True)

    table_left, table_right = st.columns(2, gap="large")
    with table_left:
        _render_top_performing_agents()
    with table_right:
        _render_highest_risk_agents()

    _render_governance_watchlist()


def _render_header() -> None:
    st.markdown(
        """
        <div class="dash-header">
            <div class="dash-title">Sentinel - Agent of Agents</div>
            <div class="dash-subtitle">Enterprise Governance &amp; Trust Platform for AI Agents</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_kpis() -> None:
    cards = "".join(_kpi_card_html(card) for card in KPI_CARDS)
    st.markdown(f'<div class="dash-kpi-grid">{cards}</div>', unsafe_allow_html=True)


def _kpi_card_html(card: dict[str, str]) -> str:
    trend_class = f"dash-trend-{card['trend_state']}"
    return (
        f'<div class="dash-kpi-card dash-kpi-{escape(card["accent"])}">'
        '<div class="dash-kpi-top">'
        f'<div class="dash-kpi-icon">{escape(card["icon"])}</div>'
        f'<div class="dash-kpi-label">{escape(card["label"])}</div>'
        "</div>"
        f'<div class="dash-kpi-value">{escape(card["value"])}</div>'
        f'<div class="dash-kpi-trend {trend_class}">{escape(card["trend"])}</div>'
        f'<div class="dash-kpi-subtitle">{escape(card["subtitle"])}</div>'
        "</div>"
    )


def _agent_distribution_chart() -> go.Figure:
    labels = list(AGENT_DISTRIBUTION.keys())
    values = list(AGENT_DISTRIBUTION.values())
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.64,
                domain={"x": [0.02, 0.68], "y": [0.02, 0.98]},
                marker={"colors": CHART_COLORS, "line": {"color": "#FFFFFF", "width": 3}},
                textinfo="none",
                hovertemplate="%{label}: %{value} agents<extra></extra>",
            )
        ]
    )
    fig.update_layout(
        title={"text": "Enterprise AI Agent Distribution", "x": 0.02, "xanchor": "left"},
        height=360,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        margin={"l": 8, "r": 8, "t": 64, "b": 8},
        legend={
            "orientation": "v",
            "x": 0.76,
            "y": 0.5,
            "xanchor": "left",
            "yanchor": "middle",
            "font": {"size": 12, "color": "#334155"},
        },
        font={"family": "Inter, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif", "color": "#0F172A"},
        annotations=[
            {
                "text": "<b>48</b>",
                "x": 0.35,
                "y": 0.535,
                "xref": "paper",
                "yref": "paper",
                "font": {"size": 30, "color": "#0F172A"},
                "showarrow": False,
            },
            {
                "text": "Enterprise Agents",
                "x": 0.35,
                "y": 0.455,
                "xref": "paper",
                "yref": "paper",
                "font": {"size": 14, "color": "#64748B"},
                "showarrow": False,
            }
        ],
    )
    return fig


def _activity_trend_chart() -> go.Figure:
    months = list(MONTHLY_ACTIVITY.keys())
    values = list(MONTHLY_ACTIVITY.values())
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=months,
            y=values,
            mode="lines+markers",
            line={"color": "#2563EB", "width": 3},
            marker={"size": 8, "color": "#2563EB", "line": {"color": "#FFFFFF", "width": 2}},
            fill="tozeroy",
            fillcolor="rgba(37, 99, 235, 0.12)",
            hovertemplate="%{x}: %{y} active agents<extra></extra>",
        )
    )
    fig.update_layout(
        title={"text": "Enterprise Agent Activity Trend", "x": 0.02, "xanchor": "left"},
        height=340,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        margin={"l": 38, "r": 22, "t": 72, "b": 42},
        xaxis={"showgrid": False, "linecolor": "#E2E8F0", "tickfont": {"color": "#334155"}},
        yaxis={
            "title": {"text": "Active Agents", "font": {"size": 12, "color": "#475569"}},
            "gridcolor": "#E2E8F0",
            "zeroline": False,
            "tickfont": {"color": "#334155"},
        },
        font={"family": "Inter, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif", "color": "#0F172A"},
        showlegend=False,
    )
    return fig


def _render_top_performing_agents() -> None:
    rows = "".join(
        (
            "<tr>"
            f"<td>{escape(row['agent'])}</td>"
            f"<td>{escape(row['business_unit'])}</td>"
            f"<td><strong>{escape(row['trust_score'])}</strong></td>"
            f"<td>{_badge(row['status'], _status_state(row['status']))}</td>"
            f"<td>{escape(row['last_audit'])}</td>"
            "</tr>"
        )
        for row in TOP_PERFORMING_AGENTS
    )
    _render_table_card(
        "Top Performing Agents",
        "Highest trust and operational readiness",
        ["Agent", "Business Unit", "Trust Score", "Status", "Last Audit"],
        rows,
    )


def _render_highest_risk_agents() -> None:
    rows = "".join(
        (
            "<tr>"
            f"<td>{escape(row['agent'])}</td>"
            f"<td>{_badge(row['risk'], _risk_state(row['risk']))}</td>"
            f"<td><span class=\"dash-policy-pill\">{escape(row['policy'])}</span></td>"
            f"<td>{escape(row['impact'])}</td>"
            "</tr>"
        )
        for row in HIGHEST_RISK_AGENTS
    )
    _render_table_card(
        "Highest Risk Agents",
        "Priority risk signals requiring executive awareness",
        ["Agent", "Risk", "Policy Failed", "Business Impact"],
        rows,
    )


def _render_governance_watchlist() -> None:
    rows = "".join(
        (
            "<tr>"
            f"<td>{escape(row['time'])}</td>"
            f"<td>{escape(row['agent'])}</td>"
            f"<td><span class=\"dash-policy-pill\">{escape(row['policy'])}</span></td>"
            f"<td>{_badge(row['severity'], _risk_state(row['severity']))}</td>"
            f"<td>{escape(row['recommendation'])}</td>"
            f"<td>{_badge(row['status'], _status_state(row['status']))}</td>"
            "</tr>"
        )
        for row in GOVERNANCE_WATCHLIST
    )
    _render_table_card(
        "Governance Watchlist",
        "Agents and policy actions requiring follow-up",
        ["Time", "Agent", "Policy", "Severity", "Recommendation", "Status"],
        rows,
        full_width=True,
    )


def _render_table_card(
    title: str,
    subtitle: str,
    headers: list[str],
    rows: str,
    full_width: bool = False,
) -> None:
    header_html = "".join(f"<th>{escape(header)}</th>" for header in headers)
    modifier = " dash-table-card-full" if full_width else ""
    st.markdown(
        f"""
        <div class="dash-table-card{modifier}">
            <div class="dash-card-heading">
                <div>
                    <div class="dash-card-title">{escape(title)}</div>
                    <div class="dash-card-subtitle">{escape(subtitle)}</div>
                </div>
            </div>
            <table class="dash-table">
                <thead><tr>{header_html}</tr></thead>
                <tbody>{rows}</tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _badge(label: str, state: str) -> str:
    return f'<span class="dash-badge dash-badge-{escape(state)}">{escape(label)}</span>'


def _risk_state(label: str) -> str:
    normalized = label.lower()
    if normalized in {"critical", "high"}:
        return "critical"
    if normalized in {"medium", "needs review", "in progress"}:
        return "warning"
    return "success"


def _status_state(label: str) -> str:
    normalized = label.lower()
    if normalized in {"healthy", "resolved"}:
        return "success"
    if normalized in {"needs review", "in progress"}:
        return "warning"
    if normalized in {"open", "critical"}:
        return "critical"
    return "neutral"


def _inject_dashboard_styles() -> None:
    st.markdown(
        """
        <style>
        .block-container {
            max-width: 1480px;
            padding-top: 1.6rem;
        }
        .dash-header {
            padding: 8px 0 24px;
            max-width: 980px;
        }
        .dash-title {
            color: #0F172A;
            font-size: 34px;
            line-height: 1.12;
            font-weight: 800;
        }
        .dash-subtitle {
            color: #475569;
            font-size: 16px;
            line-height: 1.45;
            margin-top: 10px;
            margin-bottom: 6px;
            font-weight: 500;
        }
        .dash-kpi-grid {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 18px;
            margin: 6px 0 22px;
        }
        .dash-kpi-card {
            background: #FFFFFF;
            border: 1px solid #E5EAF1;
            border-radius: 16px;
            padding: 22px;
            min-height: 170px;
            box-shadow: 0 14px 34px rgba(15, 23, 42, 0.065);
        }
        .dash-kpi-top {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .dash-kpi-icon {
            width: 42px;
            height: 42px;
            border-radius: 14px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            font-weight: 900;
            background: #EFF6FF;
            color: #2563EB;
        }
        .dash-kpi-green .dash-kpi-icon {
            background: #ECFDF5;
            color: #22C55E;
        }
        .dash-kpi-red .dash-kpi-icon {
            background: #FEF2F2;
            color: #EF4444;
        }
        .dash-kpi-label {
            color: #334155;
            font-size: 13px;
            font-weight: 760;
            line-height: 1.25;
        }
        .dash-kpi-value {
            color: #0F172A;
            font-size: 36px;
            line-height: 1;
            font-weight: 820;
            margin-top: 20px;
        }
        .dash-kpi-trend {
            font-size: 13px;
            font-weight: 760;
            margin-top: 14px;
        }
        .dash-trend-up,
        .dash-trend-down-good {
            color: #16A34A;
        }
        .dash-trend-down {
            color: #EF4444;
        }
        .dash-kpi-subtitle {
            color: #64748B;
            font-size: 12px;
            margin-top: 6px;
        }
        div[data-testid="stPlotlyChart"] {
            background: #FFFFFF;
            border: 1px solid #E5EAF1;
            border-radius: 16px;
            padding: 10px 12px 4px;
            box-shadow: 0 14px 34px rgba(15, 23, 42, 0.065);
        }
        .dash-table-card {
            background: #FFFFFF;
            border: 1px solid #E5EAF1;
            border-radius: 16px;
            padding: 22px;
            margin-top: 18px;
            box-shadow: 0 14px 34px rgba(15, 23, 42, 0.065);
        }
        .dash-table-card-full {
            margin-top: 22px;
        }
        .dash-card-heading {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 16px;
            margin-bottom: 16px;
        }
        .dash-card-title {
            color: #0F172A;
            font-size: 17px;
            font-weight: 800;
            line-height: 1.25;
        }
        .dash-card-subtitle {
            color: #64748B;
            font-size: 12px;
            margin-top: 5px;
        }
        .dash-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }
        .dash-table th {
            color: #64748B;
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            text-align: left;
            padding: 11px 10px;
            border-bottom: 1px solid #E2E8F0;
        }
        .dash-table td {
            color: #0F172A;
            font-size: 13px;
            font-weight: 600;
            padding: 13px 10px;
            border-bottom: 1px solid #EDF2F7;
            vertical-align: middle;
        }
        .dash-table tbody tr:last-child td {
            border-bottom: 0;
        }
        .dash-badge,
        .dash-policy-pill {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 999px;
            padding: 5px 10px;
            font-size: 11px;
            font-weight: 800;
            line-height: 1;
            white-space: nowrap;
        }
        .dash-policy-pill {
            background: #EFF6FF;
            color: #1D4ED8;
            border: 1px solid #DBEAFE;
        }
        .dash-badge-success {
            background: #DCFCE7;
            color: #166534;
        }
        .dash-badge-warning {
            background: #FEF3C7;
            color: #92400E;
        }
        .dash-badge-critical {
            background: #FEE2E2;
            color: #991B1B;
        }
        .dash-badge-neutral {
            background: #F1F5F9;
            color: #334155;
        }
        @media (max-width: 1180px) {
            .dash-kpi-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }
        @media (max-width: 720px) {
            .dash-title {
                font-size: 28px;
            }
            .dash-kpi-grid {
                grid-template-columns: 1fr;
            }
            .dash-table-card {
                overflow-x: auto;
            }
            .dash-table {
                min-width: 620px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
