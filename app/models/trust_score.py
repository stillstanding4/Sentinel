from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.models.database import Base


class TrustScore(Base):
    __tablename__ = "TrustScore"

    id = Column(String, primary_key=True)
    agent_id = Column(String, ForeignKey("Agent.id"), nullable=False, index=True)
    audit_run_id = Column(String, ForeignKey("AuditRun.id"), nullable=True, index=True)
    overall_score = Column(Integer, nullable=False)
    hallucination_score = Column(Integer, nullable=False)
    policy_score = Column(Integer, nullable=False)
    cost_score = Column(Integer, nullable=False)
    feedback_score = Column(Integer, nullable=False)
    calculation_notes = Column(Text, nullable=False)
    created_at = Column(String, nullable=False, index=True)

    agent = relationship("Agent", back_populates="trust_scores")
    audit_run = relationship("AuditRun", back_populates="trust_scores")
