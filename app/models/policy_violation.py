from __future__ import annotations

from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from app.models.database import Base


class PolicyViolation(Base):
    __tablename__ = "PolicyViolation"

    id = Column(String, primary_key=True)
    audit_run_id = Column(String, ForeignKey("AuditRun.id"), nullable=False, index=True)
    agent_id = Column(String, ForeignKey("Agent.id"), nullable=False, index=True)
    violation_type = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    evidence = Column(Text, nullable=False)
    severity = Column(String, nullable=False, index=True)
    policy_status = Column(String, nullable=False, index=True)
    created_at = Column(String, nullable=False, index=True)

    audit_run = relationship("AuditRun", back_populates="policy_violations")
    agent = relationship("Agent", back_populates="policy_violations")
