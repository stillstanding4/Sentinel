from __future__ import annotations

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.models.database import Base


class Agent(Base):
    __tablename__ = "Agent"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(String, nullable=False)
    owner_user_id = Column(String, ForeignKey("Users.id"), nullable=False, index=True)
    business_unit = Column(String, nullable=False)
    agent_type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)

    owner = relationship("User", back_populates="agents")
    audit_runs = relationship("AuditRun", back_populates="agent")
    recommendations = relationship("Recommendation", back_populates="agent")
    feedback = relationship("Feedback", back_populates="agent")
    trust_scores = relationship("TrustScore", back_populates="agent")
    policy_violations = relationship("PolicyViolation", back_populates="agent")
    hallucination_findings = relationship("HallucinationFinding", back_populates="agent")
