from __future__ import annotations

from html import escape
from typing import Any

from app.utils.trust_score_model import SCENARIO_POLICY_FAILURES


POLICY_ORDER = ("P001", "P002", "P003", "P004", "P005")

POLICY_LIBRARY = {
    "P001": {
        "id": "P001",
        "name": "Personally Identifiable Information (PII) Protection",
        "description": "Detect exposure of employee/customer personal data.",
        "severity": "Critical",
        "failure_explanation": "Employee or customer personal data exposure detected.",
    },
    "P002": {
        "id": "P002",
        "name": "Financial Grounding",
        "description": "Financial or operational claims must be supported by enterprise evidence.",
        "severity": "High",
        "failure_explanation": "Unsupported financial claim detected.",
    },
    "P003": {
        "id": "P003",
        "name": "Prompt Injection Protection",
        "description": "Detect prompt injection, jailbreaks and malicious instructions.",
        "severity": "High",
        "failure_explanation": "Prompt injection or malicious instruction detected.",
    },
    "P004": {
        "id": "P004",
        "name": "Cost & Efficiency",
        "description": "Detect unnecessarily expensive, repetitive or inefficient AI responses.",
        "severity": "Medium",
        "failure_explanation": "Unnecessarily expensive or repetitive AI response detected.",
    },
    "P005": {
        "id": "P005",
        "name": "Human Approval Required",
        "description": (
            "Responses affecting Finance, HR, Legal or Procurement decisions require human "
            "approval before execution."
        ),
        "severity": "High",
        "failure_explanation": "Decision-impacting response requires human approval before execution.",
    },
}

def policy_metadata(policy_id: str) -> dict[str, str]:
    return POLICY_LIBRARY.get(policy_id, {
        "id": policy_id,
        "name": "Enterprise Policy",
        "description": "Enterprise policy control.",
        "severity": "High",
        "failure_explanation": "Enterprise policy control failed.",
    })


def infer_policy_ids_for_result(result: dict[str, Any]) -> list[str]:
    policy_ids: list[str] = []
    audit_run = result.get("audit_run") or {}
    scenario_key = audit_run.get("scenario_key")

    if scenario_key in SCENARIO_POLICY_FAILURES:
        return _ordered_unique(list(SCENARIO_POLICY_FAILURES[scenario_key]))

    if result.get("policy_violations"):
        policy_ids.append("P001")
    if result.get("hallucination_findings"):
        policy_ids.append("P002")
    if int(audit_run.get("total_tokens") or 0) > 2500:
        policy_ids.append("P004")

    return _ordered_unique(policy_ids)


def policy_id_for_finding(finding: dict[str, Any]) -> str:
    if finding.get("violation_type") == "PII":
        return "P001"
    description = f"{finding.get('description', '')} {finding.get('evidence', '')}".lower()
    if "token" in description or "cost" in description:
        return "P004"
    if "prompt" in description or "jailbreak" in description:
        return "P003"
    if "financial" in description or "finance" in description or "claim" in description:
        return "P002"
    return "P005"


def policy_display_title(policy_id: str) -> str:
    policy = policy_metadata(policy_id)
    return f"{_severity_icon(policy['severity'])} {policy['id']} - {policy['name']}"


def policy_violation_cards_html(policy_ids: list[str], compact: bool = False) -> str:
    if not policy_ids:
        return '<div class="policy-empty">No policy violations detected.</div>'

    card_class = "policy-violation-card policy-violation-compact" if compact else "policy-violation-card"
    cards = []
    for policy_id in _ordered_unique(policy_ids):
        policy = policy_metadata(policy_id)
        severity = policy["severity"].lower()
        cards.append(
            (
                f'<div class="{card_class} policy-violation-{escape(severity)}">'
                '<div class="policy-violation-heading">'
                f'<div class="policy-violation-title">{escape(policy_display_title(policy_id))}</div>'
                f'<span class="policy-severity-badge policy-severity-{escape(severity)}">{escape(policy["severity"])}</span>'
                "</div>"
                f'<div class="policy-violation-explanation">{escape(policy["failure_explanation"])}</div>'
                "</div>"
            )
        )
    return "".join(cards)


def policy_event_text(policy_id: str, failed: bool) -> str:
    policy = policy_metadata(policy_id)
    if failed:
        return f"{policy_display_title(policy_id)} failed. {policy['failure_explanation']}"
    return f"{policy['id']} - {policy['name']} passed."


def _ordered_unique(policy_ids: list[str]) -> list[str]:
    unique_ids = set(policy_ids)
    ordered = [policy_id for policy_id in POLICY_ORDER if policy_id in unique_ids]
    ordered.extend(policy_id for policy_id in policy_ids if policy_id not in POLICY_ORDER)
    return ordered


def _severity_icon(severity: str) -> str:
    if severity.lower() in {"critical", "high"}:
        return "🔴"
    if severity.lower() == "medium":
        return "🟠"
    return "🟡"
