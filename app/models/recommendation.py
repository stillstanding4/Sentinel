from __future__ import annotations

from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from app.models.database import Base


class Recommendation(Base):
    __tablename__ = "Recommendation"

    id = Column(String, primary_key=True)
    audit_run_id = Column(String, ForeignKey("AuditRun.id"), nullable=False, index=True)
    agent_id = Column(String, ForeignKey("Agent.id"), nullable=False, index=True)
    recommendation_type = Column(String, nullable=False, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String, nullable=False, index=True)
    status = Column(String, nullable=False, index=True)
    created_at = Column(String, nullable=False, index=True)
    updated_at = Column(String, nullable=False)

    audit_run = relationship("AuditRun", back_populates="recommendations")
    agent = relationship("Agent", back_populates="recommendations")
