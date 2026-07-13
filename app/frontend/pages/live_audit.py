from __future__ import annotations

from html import escape
import time
from collections.abc import Callable

import streamlit as st

from app.backend.services.agent_catalogue_service import AgentCatalogueService
from app.backend.services.audit_service import AuditService, ProgressCallback
from app.backend.services.feedback_service import FeedbackService
from app.demo.scenarios import DEMO_SCENARIOS
from app.frontend.components.layout import empty_state, page_header, section_divider
from app.frontend.components.metric_cards import metric_card, status_badge
from app.frontend.components.policies import infer_policy_ids_for_result, policy_violation_cards_html
from app.frontend.components.tables import dataframe
from app.frontend.components.trust_scores import trust_score_state


def _run_interactive_audit(audit_runner: Callable[[ProgressCallback], dict]) -> dict:
    result: dict | None = None
    progress = st.progress(0, text="Preparing Live Agent Audit...")

    with st.status("Sentinel Live Agent Audit in progress", expanded=True) as status:
        def update_progress(message: str, step_number: int, total_steps: int) -> None:
            st.write(message)
            progress.progress(
                int((step_number - 1) / total_steps * 100),
                text=message,
            )
            time.sleep(0.6)
            st.success(f"{message} complete")

        result = audit_runner(update_progress)
        progress.progress(100, text="Live Agent Audit complete.")
        status.update(label="Sentinel Live Agent Audit complete", state="complete", expanded=True)

    st.success("Audit stored. Trust Score, Dashboard KPIs, Analytics, Agent Details and Recommendations updated.")
    return result


def _render_result(result: dict) -> None:
    audit_run = result["audit_run"]
    trust_score = result.get("trust_score") or {}
    executive_summary = result.get("executive_summary") or {}
    overall_score = trust_score.get("overall_score", 0)
    trust_state = trust_score_state(overall_score)
    section_divider("Live Agent Audit Result", "Sentinel has captured, evaluated, scored and stored this Agent execution.")
    cols = st.columns(5)
    with cols[0]:
        metric_card("Agent", audit_run["agent_name"], audit_run["business_unit"], "neutral")
    with cols[1]:
        metric_card("Tokens", f"{audit_run['total_tokens']:,}", "Cost Analysis", "watch" if audit_run["total_tokens"] > 8000 else "good")
    with cols[2]:
        metric_card("Estimated Cost", f"${audit_run['estimated_cost']:.4f}", "Average Cost per Run signal", "neutral")
    with cols[3]:
        metric_card("Trust Score", str(overall_score), "Overall Trust Score", trust_state["metric_status"])
    with cols[4]:
        metric_card("Risk Level", trust_state["label"], "Enterprise Trust Score band", trust_state["metric_status"])

    _render_executive_summary(executive_summary)
    _render_score_breakdown(result)

    section_divider("Audit Workflow", "Timestamped Sentinel audit lifecycle.")
    _render_audit_timeline(result.get("audit_timeline", []))

    tabs = st.tabs(["Hallucination Check", "Policy Check", "Recommendations", "Human Feedback"])
    with tabs[0]:
        dataframe(
            [
                {
                    "Claim": item["claim"],
                    "Status": item["finding_status"],
                    "Confidence": item["confidence"],
                    "Evidence": item["evidence"],
                }
                for item in result["hallucination_findings"]
            ]
        )
    with tabs[1]:
        policy_ids = infer_policy_ids_for_result(result)
        if policy_ids:
            st.markdown(
                f'<div class="policy-violation-list">{policy_violation_cards_html(policy_ids)}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.success("Policy Evaluator returned PASS.")
    with tabs[2]:
        _render_recommendation_cards(result.get("recommendation_cards", []))
    with tabs[3]:
        users = AgentCatalogueService().list_users()
        user_by_label = {f"{user['name']} ({user['role']})": user["id"] for user in users}
        with st.form("feedback_form"):
            reviewer = st.selectbox("Reviewer", list(user_by_label.keys()))
            rating = st.slider("Rating", min_value=1, max_value=5, value=4)
            decision = st.selectbox("Decision", ["approve", "reject", "needs_review", "resolved"])
            comment = st.text_area("Comment", value="Reviewed during Live Agent Audit.")
            submitted = st.form_submit_button("Submit Human Feedback")
        if submitted:
            FeedbackService().submit_feedback(
                audit_run_id=audit_run["id"],
                agent_id=audit_run["agent_id"],
                user_id=user_by_label[reviewer],
                rating=rating,
                comment=comment,
                decision=decision,
            )
            st.success("Human Feedback captured. Dashboard Updated.")


def _render_executive_summary(summary: dict) -> None:
    if not summary:
        return
    risk_status = summary["risk_level"].lower()
    section_divider("Executive Summary")
    st.markdown(
        f"""
        <div class="executive-panel">
          <div class="executive-grid">
            <div class="executive-item">
              <div class="executive-label">Business Impact</div>
              <div class="executive-value">{escape(summary['business_impact'])}</div>
            </div>
            <div class="executive-item executive-item-risk-{risk_status}">
              <div class="executive-label">Risk Level</div>
              <div class="executive-value">{status_badge(summary['risk_level'], risk_status)}</div>
            </div>
            <div class="executive-item">
              <div class="executive-label">Estimated Business Impact</div>
              <div class="executive-value">{escape(summary['estimated_business_impact'])}</div>
            </div>
            <div class="executive-item">
              <div class="executive-label">Recommended Owner</div>
              <div class="executive-value">{escape(summary['recommended_owner'])}</div>
            </div>
            <div class="executive-item">
              <div class="executive-label">Priority</div>
              <div class="executive-value">{escape(summary['priority'])}</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_score_breakdown(result: dict) -> None:
    trust_score = result.get("trust_score") or {}
    breakdown = result.get("score_breakdown") or []
    if not trust_score or not breakdown:
        return

    section_divider("Explainable Trust Score", "Weighted contribution of each factor to the Agent trust decision.")
    state = trust_score_state(trust_score["overall_score"])
    st.metric("Overall Trust Score", trust_score["overall_score"], state["label"])
    for factor in breakdown:
        st.progress(
            factor["score"] / 100,
            text=(
                f"{factor['factor']}: {factor['score']}/100 | "
                f"Weight {factor['weight']:.0%} | Contribution {factor['weighted_points']} pts"
            ),
        )
        st.caption(factor["explanation"])


def _render_recommendation_cards(cards: list[dict]) -> None:
    if not cards:
        empty_state("No recommendations generated", "Sentinel did not find a remediation action for this AuditRun.")
        return
    for card in cards:
        severity = card["severity"].lower()
        st.markdown(
            f"""
            <div class="recommendation-card recommendation-card-{severity}">
              <div class="recommendation-title">{escape(card['title'])} {status_badge(card['severity'], severity)}</div>
              <div class="recommendation-row">
                <div class="recommendation-key">Reason</div>
                <div class="recommendation-value">{escape(card['reason'])}</div>
              </div>
              <div class="recommendation-row">
                <div class="recommendation-key">Expected Benefit</div>
                <div class="recommendation-value">{escape(card['expected_benefit'])}</div>
              </div>
              <div class="recommendation-row">
                <div class="recommendation-key">Estimated Impact</div>
                <div class="recommendation-value">{escape(card['estimated_impact'])}</div>
              </div>
              <div class="recommendation-row">
                <div class="recommendation-key">Suggested Action</div>
                <div class="recommendation-value">{escape(card['suggested_action'])}</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_audit_timeline(timeline: list[dict]) -> None:
    if not timeline:
        for step in ["Agent Executed", "Captured", "Hallucination Check", "Policy Validation", "Trust Calculation", "Recommendations", "Governance Complete"]:
            st.markdown(f'<div class="audit-step">{step}</div>', unsafe_allow_html=True)
        return
    for index, item in enumerate(timeline):
        arrow = "down" if index < len(timeline) - 1 else ""
        st.markdown(
            f"""
            <div class="timeline-row">
              <div class="timeline-event">{escape(item['event'])}</div>
              <div class="timeline-dot"></div>
              <div class="timeline-time">{escape(item['timestamp'])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if arrow:
            st.markdown("<div style='margin-left: 190px; color: #667085;'>↓</div>", unsafe_allow_html=True)


def render_live_audit() -> None:
    page_header(
        "Live Agent Audit",
        "Capture an Enterprise Agent run, evaluate it, calculate Trust Score and produce Recommendations.",
    )

    mode = st.radio("Audit Mode", ["Demo Mode", "Manual Capture"], horizontal=True)
    audit_service = AuditService()

    if mode == "Demo Mode":
        labels = {scenario["label"]: key for key, scenario in DEMO_SCENARIOS.items()}
        selected_label = st.selectbox("Predefined Enterprise Scenario", list(labels.keys()))
        scenario = DEMO_SCENARIOS[labels[selected_label]]
        st.text_area("Input", scenario["input_text"], height=90, disabled=True)
        st.text_area("Output", scenario["output_text"], height=130, disabled=True)
        st.text_area("Context Summary", scenario["context_summary"], height=90, disabled=True)
        st.write(f"Expected Demo Signal: **{scenario['expected_result']}**")
        if st.button("Run Live Agent Audit", type="primary"):
            st.session_state.last_audit_result = _run_interactive_audit(
                lambda progress_callback: audit_service.run_demo_scenario(
                    labels[selected_label],
                    progress_callback=progress_callback,
                )
            )
    else:
        agents = AgentCatalogueService().list_agents()
        if not agents:
            empty_state("No agents available", "Demo Mode will seed enterprise agents on startup.")
            return
        agent_names = {agent["name"]: agent["id"] for agent in agents}
        selected_agent = st.selectbox("Agent", list(agent_names.keys()))
        input_text = st.text_area("Input", height=100)
        output_text = st.text_area("Output", height=140)
        context_summary = st.text_area("Context Summary", height=100)
        left, right = st.columns(2)
        with left:
            prompt_tokens = st.number_input("Prompt Tokens", min_value=0, value=1000, step=100)
        with right:
            completion_tokens = st.number_input("Completion Tokens", min_value=0, value=500, step=100)
        if st.button("Run Live Agent Audit", type="primary"):
            st.session_state.last_audit_result = _run_interactive_audit(
                lambda progress_callback: audit_service.run_custom_audit(
                    agent_id=agent_names[selected_agent],
                    input_text=input_text,
                    output_text=output_text,
                    context_summary=context_summary,
                    prompt_tokens=int(prompt_tokens),
                    completion_tokens=int(completion_tokens),
                    progress_callback=progress_callback,
                )
            )

    if st.session_state.last_audit_result:
        _render_result(st.session_state.last_audit_result)
