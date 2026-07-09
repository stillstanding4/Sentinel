from __future__ import annotations

from app.backend.repositories.feedback_repository import FeedbackRepository
from app.utils.ids import new_id


class FeedbackService:
    def __init__(self) -> None:
        self.feedback = FeedbackRepository()

    def submit_feedback(
        self,
        audit_run_id: str,
        agent_id: str,
        user_id: str,
        rating: int,
        comment: str,
        decision: str,
    ) -> None:
        self.feedback.create_feedback(
            {
                "id": new_id("feedback"),
                "audit_run_id": audit_run_id,
                "agent_id": agent_id,
                "user_id": user_id,
                "rating": rating,
                "comment": comment,
                "decision": decision,
            }
        )
