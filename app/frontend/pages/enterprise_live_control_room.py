from __future__ import annotations

from html import escape
import time
from typing import Any

import streamlit as st

from app.backend.services.audit_service import AuditService
from app.demo.scenarios import DEMO_SCENARIOS
from app.frontend.components.layout import page_header, section_divider
from app.frontend.components.metric_cards import metric_card, status_badge


AGENT_SEQUENCE = [
    ("hr_pii_leak", "People Operations"),
    ("finance_hallucination", "Finance"),
    ("procurement_high_tokens", "Procurement"),
]

PIPELINE_STEPS = [
    "Capture Prompt",
    "Inspect Response",
    "Run Policy Engine",
    "Run PII Detection",
    "Run Hallucination Detection",
    "Run Cost Analysis",
    "Calculate Trust Score",
    "Generate Recommendations",
]

POLICY_LIBRARY = [
    {
        "id": "P001",
        "name": "No Personally Identifiable Information",
        "rule": "Block SSN, Aadhaar, Passport, Email and Phone.",
    },
    {
        "id": "P002",
        "name": "Financial Grounding",
        "rule": "Financial claims must reference trusted enterprise sources.",
    },
    {
        "id": "P003",
        "name": "Prompt Injection Protection",
        "rule": "Ignore instructions attempting to override system prompts.",
    },
    {
        "id": "P004",
        "name": "Cost Governance",
        "rule": "Large token usage should recommend optimization.",
    },
    {
        "id": "P005",
        "name": "Hallucination Threshold",
        "rule": "Responses with insufficient confidence require Human Review.",
    },
]


def render_enterprise_live_control_room() -> None:
    page_header(
        "Enterprise Live Control Room",
        "Sentinel actively monitors multiple enterprise AI agents as an Agent-of-Agents Auditor.",
        eyebrow="AI Operations Center",
    )

    top_cols = st.columns(4)
    with top_cols[0]:
        metric_card("Monitoring Mode", "Live Demo", "Three enterprise Agents", "neutral")
    with top_cols[1]:
        metric_card("Policy Library", "5", "Enterprise controls active", "good")
    with top_cols[2]:
        metric_card("Agent Coverage", "3", "HR, Finance, Procurement", "good")
    with top_cols[3]:
        metric_card("Audit Runtime", "6-8s", "SOC-style simulation", "watch")

    with st.expander("Enterprise Policy Library", expanded=False):
        for policy in POLICY_LIBRARY:
            st.markdown(
                f"""
                <div class="policy-row">
                    <div class="policy-id">{escape(policy['id'])}</div>
                    <div>
                        <div class="policy-name">{escape(policy['name'])}</div>
                        <div class="policy-rule">{escape(policy['rule'])}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    left, right = st.columns([0.47, 0.53], gap="large")
    with left:
        section_divider("Enterprise AI Agents", "Three simultaneously running enterprise AI agents.")
        agent_containers = {scenario_key: st.empty() for scenario_key, _unit in AGENT_SEQUENCE}
    with right:
        section_divider("Sentinel Control Tower", "Policy, risk, cost and trust evaluation pipeline.")
        pipeline_container = st.empty()
        event_container = st.empty()
        report_container = st.empty()

    _render_agent_cards(agent_containers, active_status={})
    _render_pipeline(pipeline_container, active_index=-1, completed_count=0)
    _render_event_feed(event_container, ["Sentinel monitoring standby."])

    if st.button("Start Enterprise Live Control Room", type="primary"):
        results = _run_control_room_simulation(
            agent_containers,
            pipeline_container,
            event_container,
        )
        _render_executive_audit_report(report_container, results)
        st.success("Enterprise audit complete. Dashboard, Agent Catalogue, Agent Details and Analytics have been updated.")


def _run_control_room_simulation(
    agent_containers: dict[str, Any],
    pipeline_container: Any,
    event_container: Any,
) -> list[dict]:
    events: list[str] = ["Sentinel activated enterprise monitoring."]
    active_status: dict[str, str] = {}
    audit_service = AuditService()

    for scenario_key, _unit in AGENT_SEQUENCE:
        for status in ["Receiving Prompt", "Generating Response", "Response Ready"]:
            active_status[scenario_key] = status
            _render_agent_cards(agent_containers, active_status)
            events.append(f"{_agent_name(scenario_key)}: {status}.")
            if status == "Response Ready":
                events.append(f"Sentinel automatically queued {_agent_name(scenario_key)} for audit.")
            _render_event_feed(event_container, events)
            time.sleep(0.28)

    events.append("Sentinel detected three completed agent responses.")
    _render_event_feed(event_container, events)

    results: list[dict] = []
    for index, step in enumerate(PIPELINE_STEPS):
        _render_pipeline(pipeline_container, active_index=index, completed_count=index)
        events.extend(_events_for_step(step))
        _render_event_feed(event_container, events)
        time.sleep(0.55)

        if step == "Calculate Trust Score":
            results = [audit_service.run_demo_scenario(scenario_key) for scenario_key, _unit in AGENT_SEQUENCE]
            events.extend(_events_for_results(results))
            _render_event_feed(event_container, events)

    _render_pipeline(pipeline_container, active_index=-1, completed_count=len(PIPELINE_STEPS))
    events.append("Completed: Executive Audit Report generated.")
    _render_event_feed(event_container, events)
    return results


def _render_agent_cards(containers: dict[str, Any], active_status: dict[str, str]) -> None:
    for scenario_key, unit in AGENT_SEQUENCE:
        scenario = DEMO_SCENARIOS[scenario_key]
        status = active_status.get(scenario_key, "Waiting")
        prompt = scenario["input_text"] if status != "Waiting" else "Awaiting enterprise user prompt."
        response = scenario["output_text"] if status == "Response Ready" else "Response stream pending."
        status_class = status.lower().replace(" ", "-")
        containers[scenario_key].markdown(
            f"""
            <div class="agent-runtime-card status-{status_class}">
                <div class="agent-card-topline">
                    <div>
                        <div class="agent-unit">{escape(unit)}</div>
                        <div class="agent-name">{escape(scenario['agent_name'])}</div>
                    </div>
                    <div class="agent-status">{escape(status)}</div>
                </div>
                <div class="agent-field-label">Current User Prompt</div>
                <div class="agent-field">{escape(prompt)}</div>
                <div class="agent-field-label">AI Generated Response</div>
                <div class="agent-response">{escape(response)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_pipeline(container: Any, active_index: int, completed_count: int) -> None:
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
        arrow = "<div class='pipeline-arrow'>↓</div>" if index < len(PIPELINE_STEPS) - 1 else ""
        steps_html.append(
            (
                f'<div class="pipeline-step pipeline-{state}">'
                f'<span class="pipeline-marker">{marker}</span>'
                f"<span>{escape(step)}</span>"
                "</div>"
                f"{arrow}"
            )
        )

    container.markdown(
        (
            '<div class="control-tower-panel">'
            '<div class="control-room-panel-title">Sentinel Monitoring Pipeline</div>'
            '<div class="control-room-progress">'
            f'<div class="control-room-progress-fill" style="width: {progress * 100:.0f}%"></div>'
            "</div>"
            f"{''.join(steps_html)}"
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def _render_event_feed(container: Any, events: list[str]) -> None:
    visible_events = events[-11:]
    event_items = "".join(
        f"<div class='event-feed-row'>{escape(event)}</div>" for event in reversed(visible_events)
    )
    container.markdown(
        (
            '<div class="event-feed">'
            '<div class="control-room-panel-title">Live Detections</div>'
            f"{event_items}"
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def _render_executive_audit_report(container: Any, results: list[dict]) -> None:
    if not results:
        return

    worst_result = min(results, key=lambda result: result["trust_score"]["overall_score"])
    cost_result = max(results, key=lambda result: result["audit_run"]["total_tokens"])
    policies_violated = sorted(
        {
            "P001" if violation["violation_type"] == "PII" else "P002"
            for result in results
            for violation in result["policy_violations"]
        }
    )
    if any(result["hallucination_findings"] for result in results):
        policies_violated.append("P005")
    if cost_result["audit_run"]["total_tokens"] >= 8000:
        policies_violated.append("P004")

    recommendations = [result["recommendation_cards"][0] for result in results if result["recommendation_cards"]]
    recommended_action = recommendations[0]["suggested_action"] if recommendations else "Continue monitoring."
    report = worst_result["executive_summary"]
    confidence = _average_confidence(results)
    cost_savings = _estimated_cost_savings(cost_result["audit_run"]["total_tokens"])

    container.markdown(
        (
            '<div class="executive-audit-report">'
            '<div class="control-room-panel-title">Executive Audit Report</div>'
            '<div class="report-grid">'
            '<div class="report-item"><div class="report-label">Trust Score</div>'
            f'<div class="report-value">{worst_result["trust_score"]["overall_score"]}</div></div>'
            '<div class="report-item report-risk"><div class="report-label">Risk Level</div>'
            f'<div class="report-value">{status_badge(report["risk_level"], report["risk_level"].lower())}</div></div>'
            '<div class="report-item"><div class="report-label">Policies Violated</div>'
            f'<div class="report-value">{escape(", ".join(sorted(set(policies_violated))) or "None")}</div></div>'
            '<div class="report-item"><div class="report-label">Business Impact</div>'
            f'<div class="report-value">{escape(report["business_impact"])}</div></div>'
            '<div class="report-item"><div class="report-label">Recommended Action</div>'
            f'<div class="report-value">{escape(recommended_action)}</div></div>'
            '<div class="report-item"><div class="report-label">Owner</div>'
            f'<div class="report-value">{escape(report["recommended_owner"])}</div></div>'
            '<div class="report-item"><div class="report-label">Estimated Cost Savings</div>'
            f'<div class="report-value">{escape(cost_savings)}</div></div>'
            '<div class="report-item"><div class="report-label">Confidence</div>'
            f'<div class="report-value">{confidence}%</div></div>'
            "</div>"
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def _events_for_step(step: str) -> list[str]:
    if step == "Run Policy Engine":
        return ["✓ Policy Passed for Procurement Agent.", "⚠ Financial Grounding requires source verification."]
    if step == "Run PII Detection":
        return ["🚨 PII Detected in HR Assistant response.", "⚠ Human Review Required for HR Assistant."]
    if step == "Run Hallucination Detection":
        return ["🚨 Hallucination Risk detected in Finance Copilot response."]
    if step == "Run Cost Analysis":
        return ["⚠ High Cost detected for Procurement Agent.", "✓ Cost Governance policy evaluated."]
    if step == "Calculate Trust Score":
        return ["Sentinel calculating Trust Score across all three Agents."]
    if step == "Generate Recommendations":
        return ["Sentinel generating remediation recommendations."]
    return [f"✓ {step} complete."]


def _events_for_results(results: list[dict]) -> list[str]:
    events: list[str] = []
    for result in results:
        score = result["trust_score"]["overall_score"]
        risk = result["executive_summary"]["risk_level"]
        events.append(f"{result['audit_run']['agent_name']}: Trust Score {score}, Risk {risk}.")
    return events


def _agent_name(scenario_key: str) -> str:
    return DEMO_SCENARIOS[scenario_key]["agent_name"]


def _average_confidence(results: list[dict]) -> int:
    confidences = [
        int(finding["confidence"] * 100)
        for result in results
        for finding in result["hallucination_findings"]
    ]
    if not confidences:
        return 92
    return round(sum(confidences) / len(confidences))


def _estimated_cost_savings(total_tokens: int) -> str:
    if total_tokens < 8000:
        return "$0.00 per high-volume run"
    saved_tokens = round(total_tokens * 0.35)
    return f"~{saved_tokens:,} tokens per optimized run"
