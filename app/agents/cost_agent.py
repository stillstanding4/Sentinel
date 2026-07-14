from __future__ import annotations

from app.agents.state import AuditWorkflowState
from app.utils.token_costs import estimate_cost


ELEVATED_TOKEN_THRESHOLD = 1500


def evaluate_cost(state: AuditWorkflowState) -> AuditWorkflowState:
    prompt_tokens = int(state.get("prompt_tokens", 0))
    completion_tokens = int(state.get("completion_tokens", 0))
    total_tokens = prompt_tokens + completion_tokens
    estimated_cost = estimate_cost(prompt_tokens, completion_tokens)
    is_high_usage = total_tokens >= ELEVATED_TOKEN_THRESHOLD

    state["prompt_tokens"] = prompt_tokens
    state["completion_tokens"] = completion_tokens
    state["total_tokens"] = total_tokens
    state["estimated_cost"] = estimated_cost
    state["cost_analysis"] = {
        "total_tokens": total_tokens,
        "estimated_cost": estimated_cost,
        "status": "Cost Optimization" if is_high_usage else "Efficient",
        "is_high_usage": is_high_usage,
        "description": (
            "Elevated token usage detected. Reduce duplicated context and summarize supplier evidence."
            if is_high_usage
            else "Token usage is within the expected operating range."
        ),
    }
    return state
