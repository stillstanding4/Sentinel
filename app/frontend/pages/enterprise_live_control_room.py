from __future__ import annotations

from datetime import datetime
from html import escape
import time
from typing import Any

import streamlit as st

from app.backend.services.audit_service import AuditService
from app.demo.scenarios import DEMO_SCENARIOS
from app.frontend.components.layout import page_header
from app.frontend.components.policies import (
    infer_policy_ids_for_result,
    policy_event_text,
    policy_metadata,
    policy_violation_cards_html,
)
from app.frontend.components.trust_scores import trust_score_state
from app.utils.trust_score_model import SCENARIO_POLICY_FAILURES


AGENT_SEQUENCE = [
    ("hr_pii_leak", "People Operations"),
    ("finance_hallucination", "Finance"),
    ("procurement_high_tokens", "Procurement"),
]

PIPELINE_STEPS = [
    "Capturing Prompt",
    "Inspecting Response",
    "Policy Engine",
    "PII Detection",
    "Hallucination Detection",
    "Cost Analysis",
    "Trust Score Calculation",
    "Recommendations",
]


def _scenarios_failing(policy_id: str) -> set[str]:
    return {
        scenario_key
        for scenario_key, failed_policy_ids in SCENARIO_POLICY_FAILURES.items()
        if policy_id in failed_policy_ids
    }


POLICY_CHECKS = [
    {"id": "P001", "fails_for": _scenarios_failing("P001")},
    {"id": "P002", "fails_for": _scenarios_failing("P002")},
    {"id": "P003", "fails_for": _scenarios_failing("P003")},
    {"id": "P004", "fails_for": _scenarios_failing("P004")},
    {"id": "P005", "fails_for": _scenarios_failing("P005")},
]

STATUS_SEQUENCE = ["Receiving Prompt", "Generating Response", "Auditing", "Governance Complete"]
DEFAULT_AGENT_KEY = AGENT_SEQUENCE[0][0]

STARTED_KEY = "control_room_started"
COMPLETED_KEY = "control_room_completed"
RESULTS_KEY = "control_room_results"
EVENTS_KEY = "control_room_events"
SELECTED_AGENT_KEY = "control_room_selected_agent"


def render_enterprise_live_control_room() -> None:
    _ensure_control_room_state()
    page_header(
        "Enterprise Live Control Room",
        "Sentinel watches enterprise AI agents in real time, audits their responses and turns risk signals into executive action.",
        eyebrow="AI Operations Center",
    )

    start_requested = _render_start_action()
    if start_requested:
        _reset_control_room_run()
        st.session_state[STARTED_KEY] = True

    if not st.session_state[STARTED_KEY]:
        return

    left, right = st.columns([0.58, 0.42], gap="large")
    with left:
        selected_agent_key = _render_agent_selector()
        agent_container = st.empty()

    with right:
        tower_container = st.empty()
        event_container = st.empty()

    if start_requested:
        _run_control_room_simulation(selected_agent_key, agent_container, tower_container, event_container)
        return

    _render_persisted_control_room_state(selected_agent_key, agent_container, tower_container, event_container)


def _ensure_control_room_state() -> None:
    st.session_state.setdefault(STARTED_KEY, False)
    st.session_state.setdefault(COMPLETED_KEY, False)
    st.session_state.setdefault(RESULTS_KEY, [])
    st.session_state.setdefault(EVENTS_KEY, [])
    st.session_state.setdefault(SELECTED_AGENT_KEY, DEFAULT_AGENT_KEY)


def _render_start_action() -> bool:
    if not st.session_state[STARTED_KEY]:
        left, center, right = st.columns([0.34, 0.32, 0.34])
        with center:
            return st.button("Start Enterprise Live Audit", type="primary", use_container_width=True)

    action_left, action_right = st.columns([0.74, 0.26], gap="large")
    with action_left:
        st.markdown(
            """
            <div class="control-room-live-note">
                Sentinel live audit workspace
            </div>
            """,
            unsafe_allow_html=True,
        )
    with action_right:
        return st.button("Start Enterprise Live Audit", type="primary", use_container_width=True)


def _reset_control_room_run() -> None:
    selected_agent_key = st.session_state.get(SELECTED_AGENT_KEY, DEFAULT_AGENT_KEY)
    st.session_state[COMPLETED_KEY] = False
    st.session_state[RESULTS_KEY] = []
    st.session_state[EVENTS_KEY] = []
    st.session_state[SELECTED_AGENT_KEY] = selected_agent_key


def _render_agent_selector() -> str:
    st.markdown('<div class="control-room-section-title">Enterprise AI Agents</div>', unsafe_allow_html=True)
    selected_agent_key = st.segmented_control(
        "Enterprise AI Agents",
        options=[scenario_key for scenario_key, _unit in AGENT_SEQUENCE],
        format_func=_agent_name,
        key=SELECTED_AGENT_KEY,
        label_visibility="collapsed",
    )
    return selected_agent_key or DEFAULT_AGENT_KEY


def _render_persisted_control_room_state(
    selected_agent_key: str,
    agent_container: Any,
    tower_container: Any,
    event_container: Any,
) -> None:
    results = st.session_state.get(RESULTS_KEY, [])
    events = st.session_state.get(EVENTS_KEY, [])

    if st.session_state.get(COMPLETED_KEY) and results:
        result = _result_for_agent(results, selected_agent_key)
        _render_agent_workspace(agent_container, selected_agent_key, "Governance Complete", DEMO_SCENARIOS[selected_agent_key]["output_text"])
        _render_audit_result(tower_container, result)
        _render_event_feed(event_container, events)
        return

    _render_agent_workspace(agent_container, selected_agent_key, "Receiving Prompt", "")
    _render_pipeline(tower_container, active_index=-1, completed_count=0)
    _render_event_feed(event_container, [_event("Sentinel monitoring is ready.")])


def _run_control_room_simulation(
    selected_agent_key: str,
    agent_container: Any,
    tower_container: Any,
    event_container: Any,
) -> None:
    scenario = DEMO_SCENARIOS[selected_agent_key]
    response = scenario["output_text"]
    events = [_event(f"{scenario['agent_name']} received prompt.")]

    _render_agent_workspace(agent_container, selected_agent_key, "Receiving Prompt", "")
    _render_pipeline(tower_container, active_index=-1, completed_count=0)
    _render_event_feed(event_container, events)
    time.sleep(0.35)

    _append_event(events, f"{scenario['agent_name']} started generating response.")
    for partial_response in _response_frames(response):
        _render_agent_workspace(agent_container, selected_agent_key, "Generating Response", partial_response)
        _render_event_feed(event_container, events)
        time.sleep(0.25)

    _append_event(events, f"{scenario['agent_name']} generated response.")
    _render_agent_workspace(agent_container, selected_agent_key, "Auditing", response)
    _render_event_feed(event_container, events)
    time.sleep(0.25)

    audit_service = AuditService()
    results: list[dict] = []
    for index, step in enumerate(PIPELINE_STEPS):
        if step == "Policy Engine":
            _run_policy_checks(
                selected_agent_key,
                tower_container,
                event_container,
                events,
                index,
            )
            continue

        _render_pipeline(tower_container, active_index=index, completed_count=index)
        for event_message in _events_for_step(step, selected_agent_key):
            _append_event(events, event_message)
        _render_event_feed(event_container, events)
        time.sleep(0.55)

        if step == "Trust Score Calculation":
            results = [audit_service.run_demo_scenario(scenario_key) for scenario_key, _unit in AGENT_SEQUENCE]
            selected_result = _result_for_agent(results, selected_agent_key)
            _append_event(events, f"Trust Score = {selected_result['trust_score']['overall_score']}.")
            _render_event_feed(event_container, events)

    if not results:
        results = [audit_service.run_demo_scenario(scenario_key) for scenario_key, _unit in AGENT_SEQUENCE]

    selected_result = _result_for_agent(results, selected_agent_key)
    _append_event(events, "Recommendation generated.")
    _append_event(events, "Dashboard and Agent Catalogue updated.")
    _render_agent_workspace(agent_container, selected_agent_key, "Governance Complete", response)
    _render_audit_result(tower_container, selected_result)
    _render_event_feed(event_container, events)

    st.session_state[RESULTS_KEY] = results
    st.session_state[EVENTS_KEY] = events
    st.session_state[COMPLETED_KEY] = True


def _run_policy_checks(
    scenario_key: str,
    tower_container: Any,
    event_container: Any,
    events: list[dict[str, str]],
    pipeline_index: int,
) -> dict[str, str]:
    policy_states: dict[str, str] = {}
    _append_event(events, "Policy Engine started enterprise policy checks.")
    _render_event_feed(event_container, events)

    for policy_index, policy in enumerate(POLICY_CHECKS):
        _render_pipeline(
            tower_container,
            active_index=pipeline_index,
            completed_count=pipeline_index,
            policy_states=policy_states,
            active_policy_index=policy_index,
        )
        metadata = policy_metadata(policy["id"])
        _append_event(events, f"{metadata['id']} - {metadata['name']} checking.")
        _render_event_feed(event_container, events)
        time.sleep(0.28)

        failed = scenario_key in policy["fails_for"]
        policy_states[policy["id"]] = "fail" if failed else "pass"
        if failed:
            _append_event(events, policy_event_text(policy["id"], failed=True))
            _render_pipeline(
                tower_container,
                active_index=pipeline_index,
                completed_count=pipeline_index,
                policy_states=policy_states,
                active_policy_index=policy_index,
                alert=policy,
            )
            _render_event_feed(event_container, events)
            time.sleep(0.85)
        else:
            _append_event(events, policy_event_text(policy["id"], failed=False))
            _render_pipeline(
                tower_container,
                active_index=pipeline_index,
                completed_count=pipeline_index,
                policy_states=policy_states,
                active_policy_index=policy_index,
            )
            _render_event_feed(event_container, events)
            time.sleep(0.16)

    _render_pipeline(
        tower_container,
        active_index=-1,
        completed_count=pipeline_index + 1,
        policy_states=policy_states,
    )
    return policy_states


def _render_agent_workspace(container: Any, scenario_key: str, status: str, response_text: str) -> None:
    scenario = DEMO_SCENARIOS[scenario_key]
    business_unit = _business_unit(scenario_key)
    response_html = escape(response_text) if response_text else "Waiting for AI response..."
    status_class = status.lower().replace(" ", "-")

    container.markdown(
        f"""
        <div class="agent-focus-card status-{status_class}">
            <div class="agent-focus-header">
                <div>
                    <div class="agent-focus-name">{escape(scenario['agent_name'])}</div>
                    <div class="agent-focus-meta">{escape(business_unit)}</div>
                </div>
                <div class="agent-focus-status">{escape(status)}</div>
            </div>
            <div class="conversation-panel">
                <div class="chat-row chat-row-user">
                    <div class="chat-avatar">U</div>
                    <div class="chat-bubble chat-user">{escape(scenario['input_text'])}</div>
                </div>
                <div class="chat-row chat-row-ai">
                    <div class="chat-bubble chat-ai">{response_html}</div>
                    <div class="chat-avatar chat-avatar-ai">AI</div>
                </div>
            </div>
            <div class="agent-status-rail">
                {_status_rail_html(status)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _status_rail_html(current_status: str) -> str:
    current_index = STATUS_SEQUENCE.index(current_status) if current_status in STATUS_SEQUENCE else 0
    items = []
    for index, status in enumerate(STATUS_SEQUENCE):
        if index < current_index:
            state = "complete"
            marker = "✓"
        elif index == current_index:
            state = "active"
            marker = "●"
        else:
            state = "pending"
            marker = "○"
        arrow = '<span class="status-arrow">↓</span>' if index < len(STATUS_SEQUENCE) - 1 else ""
        items.append(
            f'<span class="status-step status-{state}"><span>{marker}</span>{escape(status)}</span>{arrow}'
        )
    return "".join(items)


def _render_pipeline(
    container: Any,
    active_index: int,
    completed_count: int,
    policy_states: dict[str, str] | None = None,
    active_policy_index: int | None = None,
    alert: dict | None = None,
) -> None:
    progress = completed_count / len(PIPELINE_STEPS)
    steps_html = []
    for index, step in enumerate(PIPELINE_STEPS):
        if index < completed_count:
            state = "complete"
            marker = "✓"
        elif index == active_index:
            state = "active"
            marker = "●"
        else:
            state = "pending"
            marker = "○"
        arrow = '<div class="pipeline-flow-arrow">↓</div>' if index < len(PIPELINE_STEPS) - 1 else ""
        steps_html.append(
            (
                f'<div class="tower-step tower-{state}">'
                f'<span class="tower-step-marker">{marker}</span>'
                f'<span>{escape(step)}</span>'
                "</div>"
                f"{_policy_checks_html(index, active_policy_index, policy_states)}"
                f"{arrow}"
            )
        )

    alert_html = _policy_alert_html(alert) if alert else ""
    container.markdown(
        (
            '<div class="sentinel-tower-card">'
            '<div class="tower-eyebrow">Sentinel Control Tower</div>'
            '<div class="tower-title">Audit workflow</div>'
            f"{alert_html}"
            '<div class="tower-progress">'
            f'<div class="tower-progress-fill" style="width: {progress * 100:.0f}%"></div>'
            "</div>"
            f"{''.join(steps_html)}"
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def _policy_checks_html(
    pipeline_index: int,
    active_policy_index: int | None,
    policy_states: dict[str, str] | None,
) -> str:
    if pipeline_index != PIPELINE_STEPS.index("Policy Engine"):
        return ""
    if policy_states is None and active_policy_index is None:
        return ""

    policy_states = policy_states or {}
    rows = []
    for index, policy in enumerate(POLICY_CHECKS):
        metadata = policy_metadata(policy["id"])
        state = policy_states.get(policy["id"], "pending")
        if active_policy_index == index and state == "pending":
            state = "active"
        marker = {"pass": "✓", "fail": "!", "active": "●"}.get(state, "○")
        rows.append(
            (
                f'<div class="policy-check-row policy-check-{state}">'
                f'<span class="policy-check-marker">{marker}</span>'
                f'<span class="policy-check-id">{escape(metadata["id"])}</span>'
                f'<span>{escape(metadata["name"])}</span>'
                "</div>"
            )
        )
    return f'<div class="policy-check-list">{"".join(rows)}</div>'


def _policy_alert_html(policy: dict) -> str:
    metadata = policy_metadata(policy["id"])
    severity = str(metadata["severity"]).lower()
    return (
        f'<div class="policy-alert policy-alert-{escape(severity)}">'
        '<div class="policy-alert-title">🚨 Policy Violation Detected</div>'
        '<div class="policy-alert-grid">'
        f'<div><span>Policy ID</span><strong>{escape(metadata["id"])}</strong></div>'
        f'<div><span>Policy Name</span><strong>{escape(metadata["name"])}</strong></div>'
        f'<div><span>Severity</span><strong>{escape(metadata["severity"])}</strong></div>'
        "</div>"
        f'<div class="policy-alert-explanation">{escape(metadata["failure_explanation"])}</div>'
        "</div>"
    )


def _render_audit_result(container: Any, result: dict) -> None:
    audit_run = result["audit_run"]
    trust_score = result["trust_score"]["overall_score"]
    trust_state = trust_score_state(trust_score)
    summary = result["executive_summary"]
    policy_ids = infer_policy_ids_for_result(result)
    recommendation = _recommended_action(result)
    savings = _estimated_cost_saving_percent(audit_run.get("scenario_key"))

    container.markdown(
        (
            '<div class="audit-result-card">'
            '<div class="tower-eyebrow">Audit Result</div>'
            '<div class="audit-result-hero">'
            '<div><div class="result-label">Trust Score</div>'
            f'<div class="result-score result-score-{trust_state["status"]}">{trust_score}</div></div>'
            f'<div class="risk-chip risk-{trust_state["status"]}">{trust_state["label"]}</div>'
            "</div>"
            '<div class="result-detail-stack">'
            f'{_trust_breakdown_html(result)}'
            f'{_policy_result_line(policy_ids)}'
            f'{_result_line("Business Impact", summary["business_impact"])}'
            f'{_result_line("Recommended Action", recommendation)}'
            f'{_result_line("Owner", summary["recommended_owner"])}'
            f'{_cost_saving_result_line(savings)}'
            "</div>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def _trust_breakdown_html(result: dict) -> str:
    breakdown = result.get("score_breakdown") or []
    if not breakdown:
        return ""
    rows = []
    for factor in breakdown:
        score = int(factor["score"])
        rows.append(
            '<div class="result-breakdown-row">'
            f'<span>{escape(factor["factor"])}</span>'
            '<div class="result-breakdown-bar">'
            f'<div class="result-breakdown-fill" style="width: {score}%"></div>'
            "</div>"
            f'<strong>{score}/100</strong>'
            "</div>"
        )
    return (
        '<div class="result-breakdown">'
        '<div class="result-breakdown-title">Trust Score Breakdown</div>'
        f'{"".join(rows)}'
        f'<div class="result-breakdown-final">Final Trust Score {result["trust_score"]["overall_score"]}/100</div>'
        "</div>"
    )


def _result_line(label: str, value: str) -> str:
    return (
        '<div class="result-line">'
        f'<div class="result-line-label">{escape(label)}</div>'
        f'<div class="result-line-value">{escape(value)}</div>'
        "</div>"
    )


def _cost_saving_result_line(value: str) -> str:
    return (
        '<div class="result-line result-line-final">'
        '<div class="result-line-label">Estimated Cost Saving (%)</div>'
        f'<div class="result-line-value">{escape(value)}</div>'
        '<div class="result-line-caption">Estimated reduction in LLM inference cost after applying Sentinel recommendations.</div>'
        "</div>"
    )


def _policy_result_line(policy_ids: list[str]) -> str:
    return (
        '<div class="result-line">'
        '<div class="result-line-label">Policies Violated</div>'
        f'<div class="result-line-value">{policy_violation_cards_html(policy_ids, compact=True)}</div>'
        "</div>"
    )


def _render_event_feed(container: Any, events: list[dict[str, str]]) -> None:
    if not events:
        events = [_event("Sentinel monitoring is ready.")]
    event_items = "".join(
        (
            '<div class="event-stream-row">'
            f'<div class="event-time">{escape(item["time"])}</div>'
            f'<div class="event-message">{escape(item["message"])}</div>'
            "</div>"
        )
        for item in reversed(events)
    )
    container.markdown(
        (
            '<div class="event-stream-card">'
            '<div class="event-stream-title">Live Event Feed</div>'
            f"{event_items}"
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def _response_frames(response: str) -> list[str]:
    frame_count = 4
    return [
        response[: max(1, round(len(response) * index / frame_count))] + ("..." if index < frame_count else "")
        for index in range(1, frame_count + 1)
    ]


def _events_for_step(step: str, scenario_key: str) -> list[str]:
    agent_name = _agent_name(scenario_key)
    if step == "Capturing Prompt":
        return [f"{agent_name} prompt captured."]
    if step == "Inspecting Response":
        return [f"{agent_name} response inspected."]
    if step == "Policy Engine":
        return [_policy_engine_event(scenario_key)]
    if step == "PII Detection":
        return [policy_event_text("P001", failed=scenario_key == "hr_pii_leak")]
    if step == "Hallucination Detection":
        return (
            ["Hallucination detected. Review Status set to Needs Review."]
            if scenario_key == "finance_hallucination"
            else ["Hallucination threshold passed."]
        )
    if step == "Cost Analysis":
        return (
            ["Elevated token usage detected. Cost Efficiency scored at 80/100."]
            if scenario_key == "procurement_high_tokens"
            else ["Cost usage is within governance threshold."]
        )
    if step == "Trust Score Calculation":
        return ["Sentinel calculating Trust Score."]
    if step == "Recommendations":
        return ["Recommendation engine preparing action plan."]
    return [f"{step} complete."]


def _policy_engine_event(scenario_key: str) -> str:
    if scenario_key == "hr_pii_leak":
        return policy_event_text("P001", failed=True)
    if scenario_key == "finance_hallucination":
        return policy_event_text("P002", failed=True)
    if scenario_key == "procurement_high_tokens":
        return "Policy engine passed."
    return "Policy engine passed."


def _append_event(events: list[dict[str, str]], message: str) -> None:
    events.append(_event(message))


def _event(message: str) -> dict[str, str]:
    return {"time": datetime.now().strftime("%H:%M:%S"), "message": message}


def _result_for_agent(results: list[dict], scenario_key: str) -> dict:
    expected_agent_id = DEMO_SCENARIOS[scenario_key]["agent_id"]
    for result in results:
        if result["audit_run"]["agent_id"] == expected_agent_id:
            return result
    return min(results, key=lambda result: result["trust_score"]["overall_score"])


def _recommended_action(result: dict) -> str:
    cards = result.get("recommendation_cards", [])
    if not cards:
        return "Continue monitoring."
    return cards[0]["suggested_action"]


def _agent_name(scenario_key: str) -> str:
    return DEMO_SCENARIOS[scenario_key]["agent_name"]


def _business_unit(scenario_key: str) -> str:
    for key, business_unit in AGENT_SEQUENCE:
        if key == scenario_key:
            return business_unit
    return "Enterprise"


def _estimated_cost_saving_percent(scenario_key: str | None) -> str:
    savings_by_scenario = {
        "procurement_high_tokens": "22%",
        "finance_hallucination": "15%",
        "hr_pii_leak": "5%",
    }
    return savings_by_scenario.get(scenario_key or "", "10%")
