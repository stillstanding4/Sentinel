from __future__ import annotations

from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.models.database import Base


class AuditRun(Base):
    __tablename__ = "AuditRun"

    id = Column(String, primary_key=True)
    agent_id = Column(String, ForeignKey("Agent.id"), nullable=False, index=True)
    scenario_key = Column(String, nullable=True, index=True)
    input_text = Column(Text, nullable=False)
    output_text = Column(Text, nullable=False)
    context_summary = Column(Text, nullable=True)
    model_name = Column(String, nullable=True)
    prompt_tokens = Column(Integer, nullable=False, default=0)
    completion_tokens = Column(Integer, nullable=False, default=0)
    total_tokens = Column(Integer, nullable=False, default=0)
    estimated_cost = Column(Float, nullable=False, default=0)
    status = Column(String, nullable=False, index=True)
    started_at = Column(String, nullable=False)
    completed_at = Column(String, nullable=True)
    created_at = Column(String, nullable=False, index=True)

    agent = relationship("Agent", back_populates="audit_runs")
    recommendations = relationship("Recommendation", back_populates="audit_run")
    feedback = relationship("Feedback", back_populates="audit_run")
    trust_scores = relationship("TrustScore", back_populates="audit_run")
    policy_violations = relationship("PolicyViolation", back_populates="audit_run")
    hallucination_findings = relationship("HallucinationFinding", back_populates="audit_run")
