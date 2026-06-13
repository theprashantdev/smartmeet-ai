import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Integer, DateTime, JSON
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Meeting(Base):
    __tablename__ = "meetings"
    id = Column(String, primary_key=True, default=lambda: f"mtg_{uuid.uuid4().hex[:12]}")
    filename = Column(String(255))
    transcript = Column(Text)
    summary = Column(Text)
    action_items = Column(JSON)
    decisions = Column(JSON)
    open_questions = Column(JSON)
    duration_seconds = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
