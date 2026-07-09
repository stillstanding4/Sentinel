from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.models.database import Base


class Feedback(Base):
    __tablename__ = "Feedback"

    id = Column(String, primary_key=True)
    audit_run_id = Column(String, ForeignKey("AuditRun.id"), nullable=False, index=True)
    agent_id = Column(String, ForeignKey("Agent.id"), nullable=False, index=True)
    user_id = Column(String, ForeignKey("Users.id"), nullable=False, index=True)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=False)
    decision = Column(String, nullable=False, index=True)
    created_at = Column(String, nullable=False, index=True)

    audit_run = relationship("AuditRun", back_populates="feedback")
    agent = relationship("Agent", back_populates="feedback")
    user = relationship("User", back_populates="feedback")
