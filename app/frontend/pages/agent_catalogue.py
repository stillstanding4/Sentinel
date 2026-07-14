from __future__ import annotations

from datetime import datetime, timezone
from html import escape
from typing import Any

import streamlit as st

from app.backend.services.agent_catalogue_service import AgentCatalogueService
from app.frontend.components.policies import POLICY_ORDER, policy_metadata
from app.utils.trust_score_model import SCENARIO_POLICY_FAILURES, TOTAL_POLICIES


AGENT_SCENARIOS = {
    "agent_hr_assistant": "hr_pii_leak",
    "agent_finance_copilot": "finance_hallucination",
    "agent_procurement_agent": "procurement_high_tokens",
}

SUMMARY_CARDS = [
    {"label": "Registered Agents", "value": "48", "state": "neutral"},
    {"label": "Healthy Agents", "value": "34", "state": "success"},
    {"label": "Needs Review", "value": "10", "state": "warning"},
    {"label": "Critical Risk", "value": "4", "state": "critical"},
]


def render_agent_catalogue() -> None:
    _inject_catalogue_styles()
    service = AgentCatalogueService()
    agents = [_agent_view_model(service, agent) for agent in service.list_agents()]

    search_query, status_filter, view_mode = _render_header()
    _render_summary_cards()

    visible_agents = _filter_agents(agents, search_query, status_filter)
    if view_mode == "Table":
        _render_table_view(visible_agents)
    else:
        _render_agent_grid(visible_agents)

    selected_agent_id = st.session_state.get("catalogue_selected_agent_id")
    if selected_agent_id:
        selected_agent = next((agent for agent in agents if agent["id"] == selected_agent_id), None)
        if selected_agent:
            _render_detail_panel(service, selected_agent)


def _render_header() -> tuple[str, str, str]:
    left, right = st.columns([0.56, 0.44], gap="large")
    with left:
        st.markdown(
            """
            <div class="catalogue-header">
                <div class="catalogue-title">Agent Catalogue</div>
                <div class="catalogue-subtitle">
                    Central inventory of enterprise AI agents with governance status, ownership and trust score.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        search_col, filter_col, view_col = st.columns([1.45, 0.58, 0.95], gap="small")
        with search_col:
            search_query = st.text_input(
                "Search agents",
                placeholder="Search agents",
                label_visibility="collapsed",
            )
        with filter_col:
            if st.button("Filter", use_container_width=True):
                st.session_state.catalogue_filters_open = not st.session_state.get("catalogue_filters_open", False)
        with view_col:
            view_mode = st.radio(
                "View",
                ["Grid", "Table"],
                horizontal=True,
                label_visibility="collapsed",
            )

    status_filter = "All"
    if st.session_state.get("catalogue_filters_open", False):
        status_filter = st.radio(
            "Governance Status",
            ["All", "Trusted", "Needs Review", "Critical", "Under Review"],
            horizontal=True,
            label_visibility="collapsed",
        )
    return search_query, status_filter, view_mode or "Grid"


def _render_summary_cards() -> None:
    cards = "".join(
        (
            f'<div class="catalogue-kpi-card catalogue-kpi-{card["state"]}">'
            f'<div class="catalogue-kpi-label">{escape(card["label"])}</div>'
            f'<div class="catalogue-kpi-value">{escape(card["value"])}</div>'
            "</div>"
        )
        for card in SUMMARY_CARDS
    )
    st.markdown(f'<div class="catalogue-kpi-grid">{cards}</div>', unsafe_allow_html=True)


def _render_agent_grid(agents: list[dict[str, Any]]) -> None:
    if not agents:
        st.markdown(
            '<div class="catalogue-empty">No agents match the current catalogue view.</div>',
            unsafe_allow_html=True,
        )
        return

    columns = st.columns(3, gap="large")
    for index, agent in enumerate(agents):
        with columns[index % 3]:
            st.markdown(_agent_card_html(agent), unsafe_allow_html=True)
            if st.button("View Details", key=f"view_agent_{agent['id']}", use_container_width=True):
                st.session_state.catalogue_selected_agent_id = agent["id"]
                st.rerun()


def _render_table_view(agents: list[dict[str, Any]]) -> None:
    rows = "".join(
        (
            "<tr>"
            f"<td>{escape(agent['name'])}</td>"
            f"<td>{escape(agent['business_unit'])}</td>"
            f"<td><strong>{agent['trust_score']}</strong></td>"
            f"<td>{_status_badge(agent['governance_label'], agent['governance_state'])}</td>"
            f"<td>{_policy_badge(agent['primary_policy'])}</td>"
            f"<td>{escape(agent['last_audit'])}</td>"
            "</tr>"
        )
        for agent in agents
    )
    st.markdown(
        f"""
        <div class="catalogue-table-card">
            <table class="catalogue-table">
                <thead>
                    <tr>
                        <th>Agent</th>
                        <th>Business Unit</th>
                        <th>Trust Score</th>
                        <th>Status</th>
                        <th>Policy Status</th>
                        <th>Last Audit</th>
                    </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _agent_card_html(agent: dict[str, Any]) -> str:
    return (
        '<div class="agent-catalogue-card">'
        '<div class="agent-card-header">'
        '<div>'
        f'<div class="agent-card-name"><span class="agent-card-icon">AI</span>{escape(agent["name"])}</div>'
        f'<div class="agent-card-unit">{escape(agent["business_unit"])}</div>'
        "</div>"
        f'{_status_badge(agent["governance_label"], agent["governance_state"])}'
        "</div>"
        '<div class="agent-score-block">'
        '<div class="agent-score-row">'
        '<span>Trust Score</span>'
        f'<strong>{agent["trust_score"]}</strong>'
        "</div>"
        '<div class="agent-score-bar">'
        f'<div class="agent-score-fill agent-score-{agent["score_state"]}" style="width: {agent["trust_score"]}%"></div>'
        "</div>"
        f'<div class="agent-score-caption">{escape(agent["score_caption"])}</div>'
        "</div>"
        '<div class="agent-stat-grid">'
        f'{_stat_item("Owner", agent["owner_name"])}'
        f'{_stat_item("Agent Type", agent["agent_type"])}'
        f'{_stat_item("Policies Passed", str(agent["policies_passed"]))}'
        f'{_stat_item("Policies Failed", str(agent["policies_failed"]))}'
        f'{_stat_item("Last Audit", agent["last_audit"])}'
        f'{_stat_item("Lifecycle", agent["lifecycle_label"])}'
        "</div>"
        '<div class="agent-policy-row">'
        '<span>Policy Status</span>'
        f'{_policy_badge(agent["primary_policy"])}'
        "</div>"
        "</div>"
    )


def _render_detail_panel(service: AgentCatalogueService, agent: dict[str, Any]) -> None:
    details = service.get_agent_details(agent["id"])
    latest_audit = (details.get("audit_runs") or [{}])[0]
    policies = "".join(_policy_detail_row(policy_id, agent["failed_policies"]) for policy_id in POLICY_ORDER)
    recent_activity = _recent_activity(latest_audit, details)

    st.markdown(
        f"""
        <div class="agent-detail-panel">
            <div class="agent-detail-header">
                <div>
                    <div class="agent-detail-eyebrow">Agent Information</div>
                    <div class="agent-detail-title">{escape(agent["name"])}</div>
                </div>
                {_status_badge(agent["governance_label"], agent["governance_state"])}
            </div>
            <div class="agent-detail-grid">
                {_detail_item("Business Unit", agent["business_unit"])}
                {_detail_item("Owner", agent["owner_name"])}
                {_detail_item("Model", latest_audit.get("model_name") or "demo-deterministic")}
                {_detail_item("Trust Score", f'{agent["trust_score"]}/100')}
                {_detail_item("Latest Audit", agent["last_audit"])}
                {_detail_item("Agent Type", agent["agent_type"])}
            </div>
            <div class="agent-detail-section-title">Policies</div>
            <div class="agent-policy-matrix">{policies}</div>
            <div class="agent-detail-section-title">Recent Activity</div>
            <div class="agent-activity-list">{recent_activity}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Close Details", key="close_agent_details"):
        st.session_state.catalogue_selected_agent_id = None
        st.rerun()


def _agent_view_model(service: AgentCatalogueService, agent: dict[str, Any]) -> dict[str, Any]:
    details = service.get_agent_details(agent["id"])
    latest_audit = (details.get("audit_runs") or [{}])[0]
    trust_score = int(agent.get("latest_trust_score") or 0)
    score_state, score_caption = _score_visual_state(trust_score)
    governance_label, governance_state = _governance_status(trust_score)
    lifecycle_label = _lifecycle_label(agent.get("status") or "")
    failed_policies = _failed_policy_ids(agent["id"])
    primary_policy = failed_policies[0] if failed_policies else "PASS"

    return {
        "id": agent["id"],
        "name": agent["name"],
        "owner_name": agent.get("owner_name") or "Unassigned",
        "business_unit": agent.get("business_unit") or "Enterprise",
        "agent_type": _title_case(agent.get("agent_type") or "Agent"),
        "trust_score": trust_score,
        "score_state": score_state,
        "score_caption": score_caption,
        "governance_label": governance_label,
        "governance_state": governance_state,
        "lifecycle_label": lifecycle_label,
        "failed_policies": failed_policies,
        "primary_policy": primary_policy,
        "policies_passed": TOTAL_POLICIES - len(failed_policies),
        "policies_failed": len(failed_policies),
        "last_audit": _relative_time(latest_audit.get("completed_at") or latest_audit.get("created_at")),
    }


def _filter_agents(agents: list[dict[str, Any]], search_query: str, status_filter: str) -> list[dict[str, Any]]:
    normalized_query = (search_query or "").strip().lower()
    filtered = agents
    if normalized_query:
        filtered = [
            agent
            for agent in filtered
            if normalized_query in " ".join(
                [agent["name"], agent["business_unit"], agent["owner_name"], agent["agent_type"]]
            ).lower()
        ]
    if status_filter and status_filter != "All":
        filtered = [
            agent
            for agent in filtered
            if agent["governance_label"] == status_filter or agent["lifecycle_label"] == status_filter
        ]
    return filtered


def _score_visual_state(score: int) -> tuple[str, str]:
    if score >= 90:
        return "success", "Healthy"
    if score >= 75:
        return "warning", "Needs Review"
    return "critical", "Critical"


def _governance_status(score: int) -> tuple[str, str]:
    if score >= 90:
        return "Trusted", "success"
    if score >= 75:
        return "Needs Review", "warning"
    return "Critical", "critical"


def _failed_policy_ids(agent_id: str) -> list[str]:
    scenario_key = AGENT_SCENARIOS.get(agent_id)
    failed = SCENARIO_POLICY_FAILURES.get(scenario_key, set())
    return [policy_id for policy_id in POLICY_ORDER if policy_id in failed]


def _policy_badge(policy_id: str) -> str:
    if policy_id == "PASS":
        return '<span class="policy-pill policy-pass">✓ PASS</span>'
    policy = policy_metadata(policy_id)
    state = _policy_state(policy_id)
    icon = _policy_icon(state)
    return (
        f'<span class="policy-pill policy-{state}">'
        f'{icon} {escape(policy_id)} &ndash; {escape(_compact_policy_name(policy_id, policy["name"]))}'
        "</span>"
    )


def _policy_detail_row(policy_id: str, failed_policies: list[str]) -> str:
    failed = policy_id in failed_policies
    policy = policy_metadata(policy_id)
    status = "FAIL" if failed else "PASS"
    state = "fail" if failed else "pass"
    return (
        f'<div class="agent-policy-detail agent-policy-{state}">'
        f'<span>{escape(policy_id)} &mdash; {escape(_compact_policy_name(policy_id, policy["name"]))}</span>'
        f'<strong>{status}</strong>'
        "</div>"
    )


def _policy_state(policy_id: str) -> str:
    if policy_id == "P001":
        return "critical"
    if policy_id in {"P002", "P004"}:
        return "warning"
    return "attention"


def _policy_icon(state: str) -> str:
    if state == "critical":
        return "●"
    if state == "warning":
        return "●"
    return "●"


def _compact_policy_name(policy_id: str, name: str) -> str:
    compact_names = {
        "P001": "PII Protection",
        "P002": "Financial Grounding",
        "P003": "Prompt Injection",
        "P004": "Cost Optimization",
        "P005": "Human Approval",
    }
    return compact_names.get(policy_id, name)


def _status_badge(label: str, state: str) -> str:
    return f'<span class="catalogue-status catalogue-status-{escape(state)}">{escape(label)}</span>'


def _stat_item(label: str, value: str) -> str:
    return (
        '<div class="agent-stat-item">'
        f'<span>{escape(label)}</span>'
        f'<strong>{escape(value)}</strong>'
        "</div>"
    )


def _detail_item(label: str, value: str) -> str:
    return (
        '<div class="agent-detail-item">'
        f'<span>{escape(label)}</span>'
        f'<strong>{escape(str(value))}</strong>'
        "</div>"
    )


def _recent_activity(latest_audit: dict[str, Any], details: dict[str, Any]) -> str:
    audit_time = _relative_time(latest_audit.get("completed_at") or latest_audit.get("created_at"))
    feedback = details.get("feedback") or []
    last_feedback = _relative_time(feedback[0].get("created_at")) if feedback else "Pending"
    activities = [
        ("Audit Completed", audit_time),
        ("Prompt Reviewed", audit_time),
        ("Recommendation Generated", audit_time),
        ("Last Human Approval", last_feedback),
    ]
    return "".join(
        (
            '<div class="agent-activity-row">'
            f'<span>{escape(label)}</span>'
            f'<strong>{escape(value)}</strong>'
            "</div>"
        )
        for label, value in activities
    )


def _relative_time(value: str | None) -> str:
    if not value:
        return "No audit yet"
    try:
        timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
    except ValueError:
        return "Recently"
    delta = datetime.now(timezone.utc) - timestamp.astimezone(timezone.utc)
    minutes = max(0, round(delta.total_seconds() / 60))
    if minutes < 1:
        return "Just now"
    if minutes < 60:
        return f"{minutes} mins ago"
    hours = round(minutes / 60)
    if hours < 24:
        return f"{hours} hrs ago"
    days = round(hours / 24)
    return f"{days} days ago"


def _lifecycle_label(status: str) -> str:
    if status == "under_review":
        return "Under Review"
    return _title_case(status or "Active")


def _title_case(value: str) -> str:
    return value.replace("_", " ").title()


def _inject_catalogue_styles() -> None:
    st.markdown(
        """
        <style>
        .catalogue-header {
            padding: 8px 0 24px;
        }
        .catalogue-title {
            color: #0F172A;
            font-size: 34px;
            line-height: 1.12;
            font-weight: 800;
        }
        .catalogue-subtitle {
            color: #475569;
            font-size: 16px;
            line-height: 1.45;
            margin-top: 10px;
            max-width: 760px;
            font-weight: 500;
        }
        div[data-testid="stTextInput"] input,
        div[data-testid="stButton"] button {
            border-radius: 12px;
        }
        div[data-testid="stTextInput"] input {
            min-height: 44px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 8px 22px rgba(15, 23, 42, 0.04);
        }
        div[data-testid="stButton"] button {
            min-height: 44px;
            border: 1px solid #D7DEE8;
            background: #FFFFFF;
            color: #0F172A;
            font-weight: 800;
            box-shadow: 0 8px 22px rgba(15, 23, 42, 0.04);
        }
        .catalogue-kpi-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 18px;
            margin: 4px 0 24px;
        }
        .catalogue-kpi-card,
        .agent-catalogue-card,
        .agent-detail-panel,
        .catalogue-table-card {
            background: #FFFFFF;
            border: 1px solid #E5EAF1;
            border-radius: 16px;
            box-shadow: 0 14px 34px rgba(15, 23, 42, 0.065);
        }
        .catalogue-kpi-card {
            padding: 21px 22px;
            border-left: 5px solid #2563EB;
        }
        .catalogue-kpi-success { border-left-color: #22C55E; }
        .catalogue-kpi-warning { border-left-color: #F59E0B; }
        .catalogue-kpi-critical { border-left-color: #EF4444; }
        .catalogue-kpi-label {
            color: #64748B;
            font-size: 12px;
            font-weight: 800;
            text-transform: uppercase;
        }
        .catalogue-kpi-value {
            color: #0F172A;
            font-size: 34px;
            line-height: 1;
            font-weight: 820;
            margin-top: 13px;
        }
        .agent-catalogue-card {
            padding: 22px;
            min-height: 395px;
            margin-top: 2px;
            margin-bottom: 8px;
        }
        .agent-card-header,
        .agent-score-row,
        .agent-policy-row,
        .agent-detail-header,
        .agent-policy-detail,
        .agent-activity-row {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 14px;
        }
        .agent-card-name {
            color: #0F172A;
            font-size: 19px;
            line-height: 1.25;
            font-weight: 820;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .agent-card-icon {
            width: 34px;
            height: 34px;
            border-radius: 12px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: #EFF6FF;
            color: #2563EB;
            font-size: 12px;
            font-weight: 900;
        }
        .agent-card-unit {
            color: #64748B;
            font-size: 13px;
            font-weight: 700;
            margin-top: 7px;
        }
        .catalogue-status,
        .policy-pill {
            display: inline-flex;
            align-items: center;
            border-radius: 999px;
            padding: 6px 10px;
            font-size: 11px;
            line-height: 1;
            font-weight: 850;
            white-space: nowrap;
        }
        .catalogue-status-success,
        .policy-pass {
            background: #DCFCE7;
            color: #166534;
        }
        .catalogue-status-warning {
            background: #FEF3C7;
            color: #92400E;
        }
        .catalogue-status-critical,
        .policy-critical {
            background: #FEE2E2;
            color: #991B1B;
        }
        .catalogue-status-neutral {
            background: #EFF6FF;
            color: #1D4ED8;
        }
        .policy-warning {
            background: #FFEDD5;
            color: #9A3412;
        }
        .policy-attention {
            background: #FEF3C7;
            color: #92400E;
        }
        .agent-score-block {
            margin-top: 24px;
            padding: 16px;
            border-radius: 14px;
            background: #F8FAFC;
        }
        .agent-score-row span,
        .agent-policy-row span {
            color: #64748B;
            font-size: 12px;
            font-weight: 800;
            text-transform: uppercase;
        }
        .agent-score-row strong {
            color: #0F172A;
            font-size: 28px;
            line-height: 1;
            font-weight: 850;
        }
        .agent-score-bar {
            height: 9px;
            border-radius: 999px;
            background: #E2E8F0;
            overflow: hidden;
            margin-top: 12px;
        }
        .agent-score-fill {
            height: 100%;
            border-radius: 999px;
        }
        .agent-score-success { background: #22C55E; }
        .agent-score-warning { background: #F59E0B; }
        .agent-score-critical { background: #EF4444; }
        .agent-score-caption {
            color: #475569;
            font-size: 12px;
            font-weight: 750;
            margin-top: 9px;
        }
        .agent-stat-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 12px;
            margin-top: 18px;
        }
        .agent-stat-item,
        .agent-detail-item {
            border: 1px solid #E8EEF6;
            border-radius: 12px;
            padding: 12px;
            background: #FFFFFF;
        }
        .agent-stat-item span,
        .agent-detail-item span {
            display: block;
            color: #64748B;
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
        }
        .agent-stat-item strong,
        .agent-detail-item strong {
            display: block;
            color: #0F172A;
            font-size: 13px;
            line-height: 1.35;
            font-weight: 790;
            margin-top: 6px;
            overflow-wrap: anywhere;
        }
        .agent-policy-row {
            align-items: center;
            margin-top: 18px;
            padding-top: 16px;
            border-top: 1px solid #E8EEF6;
        }
        .agent-detail-panel {
            padding: 26px;
            margin-top: 28px;
        }
        .agent-detail-eyebrow {
            color: #2563EB;
            font-size: 11px;
            font-weight: 850;
            text-transform: uppercase;
        }
        .agent-detail-title {
            color: #0F172A;
            font-size: 26px;
            line-height: 1.15;
            font-weight: 850;
            margin-top: 5px;
        }
        .agent-detail-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 14px;
            margin-top: 22px;
        }
        .agent-detail-section-title {
            color: #0F172A;
            font-size: 16px;
            font-weight: 820;
            margin-top: 24px;
            margin-bottom: 12px;
        }
        .agent-policy-matrix {
            display: grid;
            gap: 9px;
        }
        .agent-policy-detail,
        .agent-activity-row {
            align-items: center;
            background: #F8FAFC;
            border: 1px solid #E8EEF6;
            border-radius: 12px;
            padding: 12px 14px;
        }
        .agent-policy-detail span,
        .agent-activity-row span {
            color: #334155;
            font-size: 13px;
            font-weight: 760;
        }
        .agent-policy-detail strong,
        .agent-activity-row strong {
            font-size: 12px;
            font-weight: 850;
        }
        .agent-policy-pass strong { color: #166534; }
        .agent-policy-fail strong { color: #991B1B; }
        .agent-activity-list {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 10px;
        }
        .catalogue-table-card {
            padding: 22px;
            overflow-x: auto;
        }
        .catalogue-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }
        .catalogue-table th {
            color: #64748B;
            font-size: 11px;
            font-weight: 850;
            text-align: left;
            text-transform: uppercase;
            padding: 12px 10px;
            border-bottom: 1px solid #E2E8F0;
        }
        .catalogue-table td {
            color: #0F172A;
            font-weight: 650;
            padding: 14px 10px;
            border-bottom: 1px solid #EDF2F7;
            vertical-align: middle;
        }
        .catalogue-table tbody tr:last-child td {
            border-bottom: 0;
        }
        .catalogue-empty {
            background: #FFFFFF;
            border: 1px dashed #CBD5E1;
            border-radius: 16px;
            color: #64748B;
            padding: 28px;
            text-align: center;
            font-weight: 700;
        }
        @media (max-width: 1180px) {
            .catalogue-kpi-grid,
            .agent-detail-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }
        @media (max-width: 760px) {
            .catalogue-title {
                font-size: 28px;
            }
            .catalogue-kpi-grid,
            .agent-stat-grid,
            .agent-detail-grid,
            .agent-activity-list {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
