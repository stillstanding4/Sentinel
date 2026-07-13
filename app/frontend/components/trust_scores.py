from __future__ import annotations


TRUST_SCORE_STATES = (
    {
        "min": 90,
        "label": "Trusted",
        "status": "trusted",
        "metric_status": "good",
        "color": "#067647",
    },
    {
        "min": 75,
        "label": "Watch",
        "status": "watch",
        "metric_status": "watch",
        "color": "#b54708",
    },
    {
        "min": 60,
        "label": "High Risk",
        "status": "high-risk",
        "metric_status": "high-risk",
        "color": "#ea580c",
    },
    {
        "min": 0,
        "label": "Critical",
        "status": "critical",
        "metric_status": "critical",
        "color": "#b42318",
    },
)


def trust_score_state(score: int | float | None) -> dict[str, str]:
    normalized_score = int(score or 0)
    for state in TRUST_SCORE_STATES:
        if normalized_score >= state["min"]:
            return state
    return TRUST_SCORE_STATES[-1]
