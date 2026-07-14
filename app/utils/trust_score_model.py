from __future__ import annotations

from dataclasses import dataclass
from typing import Any


TOTAL_POLICIES = 5

TRUST_SCORE_WEIGHTS = {
    "Policy Compliance": 0.40,
    "Safety": 0.30,
    "Cost Efficiency": 0.20,
    "Review Status": 0.10,
}

REVIEW_STATUS_SCORES = {
    "Approved": 100,
    "Needs Review": 50,
    "Rejected": 0,
}

SCENARIO_POLICY_FAILURES = {
    "hr_pii_leak": {"P001", "P005"},
    "finance_hallucination": {"P002"},
    "procurement_high_tokens": set(),
}


@dataclass(frozen=True)
class TrustScoreComponents:
    policy_compliance: int
    safety: int
    cost_efficiency: int
    review_status: int
    review_status_label: str
    overall_score: int
    policies_passed: int
    total_policies: int
    hallucination_check_passed: bool
    pii_check_passed: bool


def calculate_policy_compliance_score(policies_passed: int, total_policies: int = TOTAL_POLICIES) -> int:
    if total_policies <= 0:
        return 0
    bounded_passed = max(0, min(policies_passed, total_policies))
    return round((bounded_passed / total_policies) * 100)


def calculate_safety_score(hallucination_check_passed: bool, pii_check_passed: bool) -> int:
    passed_checks = int(hallucination_check_passed) + int(pii_check_passed)
    return round((passed_checks / 2) * 100)


def calculate_cost_efficiency_score(total_tokens: int) -> int:
    if total_tokens < 1500:
        return 100
    if total_tokens <= 2500:
        return 80
    return 60


def review_status_score(review_status: str) -> int:
    return REVIEW_STATUS_SCORES.get(review_status, REVIEW_STATUS_SCORES["Needs Review"])


def determine_review_status(
    *,
    policy_compliance: int,
    safety: int,
    scenario_key: str | None = None,
) -> str:
    if scenario_key == "procurement_high_tokens":
        return "Approved"
    if policy_compliance < 100 or safety < 100:
        return "Needs Review"
    return "Approved"


def calculate_trust_score(
    *,
    policy_compliance: int,
    safety: int,
    cost_efficiency: int,
    review_status: int,
) -> int:
    return round(
        (TRUST_SCORE_WEIGHTS["Policy Compliance"] * policy_compliance)
        + (TRUST_SCORE_WEIGHTS["Safety"] * safety)
        + (TRUST_SCORE_WEIGHTS["Cost Efficiency"] * cost_efficiency)
        + (TRUST_SCORE_WEIGHTS["Review Status"] * review_status)
    )


def calculate_trust_score_from_state(state: dict[str, Any]) -> TrustScoreComponents:
    scenario_key = state.get("scenario_key")
    failed_policy_ids = _failed_policy_ids_from_state(state, scenario_key)
    policies_passed = TOTAL_POLICIES - len(failed_policy_ids)

    hallucination_check_passed = not bool(state.get("hallucination_findings"))
    pii_check_passed = not bool(state.get("policy_violations"))

    policy_compliance = calculate_policy_compliance_score(policies_passed)
    safety = calculate_safety_score(hallucination_check_passed, pii_check_passed)
    total_tokens = int(state.get("total_tokens") or 0)
    if total_tokens == 0:
        total_tokens = int(state.get("prompt_tokens") or 0) + int(state.get("completion_tokens") or 0)
    cost_efficiency = calculate_cost_efficiency_score(total_tokens)

    review_label = _review_status_from_state(state, policy_compliance, safety, scenario_key)
    review_score = review_status_score(review_label)
    overall = calculate_trust_score(
        policy_compliance=policy_compliance,
        safety=safety,
        cost_efficiency=cost_efficiency,
        review_status=review_score,
    )

    return TrustScoreComponents(
        policy_compliance=policy_compliance,
        safety=safety,
        cost_efficiency=cost_efficiency,
        review_status=review_score,
        review_status_label=review_label,
        overall_score=overall,
        policies_passed=policies_passed,
        total_policies=TOTAL_POLICIES,
        hallucination_check_passed=hallucination_check_passed,
        pii_check_passed=pii_check_passed,
    )


def _review_status_from_state(
    state: dict[str, Any],
    policy_compliance: int,
    safety: int,
    scenario_key: str | None,
) -> str:
    feedback_signals = state.get("feedback_signals") or {}
    explicit_status = feedback_signals.get("review_status") or state.get("review_status")
    if explicit_status in REVIEW_STATUS_SCORES:
        return str(explicit_status)
    return determine_review_status(
        policy_compliance=policy_compliance,
        safety=safety,
        scenario_key=scenario_key,
    )


def _failed_policy_ids_from_state(state: dict[str, Any], scenario_key: str | None) -> set[str]:
    if scenario_key in SCENARIO_POLICY_FAILURES:
        return set(SCENARIO_POLICY_FAILURES[scenario_key])

    failed_policy_ids: set[str] = set()
    if state.get("policy_violations"):
        failed_policy_ids.add("P001")
    if state.get("hallucination_findings"):
        failed_policy_ids.add("P002")
    total_tokens = int(state.get("total_tokens") or 0)
    if total_tokens == 0:
        total_tokens = int(state.get("prompt_tokens") or 0) + int(state.get("completion_tokens") or 0)
    if total_tokens > 2500:
        failed_policy_ids.add("P004")
    return failed_policy_ids
