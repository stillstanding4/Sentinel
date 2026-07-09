from __future__ import annotations

from sqlalchemy import Column, Float, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from app.models.database import Base


class HallucinationFinding(Base):
    __tablename__ = "HallucinationFinding"

    id = Column(String, primary_key=True)
    audit_run_id = Column(String, ForeignKey("AuditRun.id"), nullable=False, index=True)
    agent_id = Column(String, ForeignKey("Agent.id"), nullable=False, index=True)
    claim = Column(Text, nullable=False)
    evidence = Column(Text, nullable=False)
    finding_status = Column(String, nullable=False, index=True)
    confidence = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(String, nullable=False, index=True)

    audit_run = relationship("AuditRun", back_populates="hallucination_findings")
    agent = relationship("Agent", back_populates="hallucination_findings")
