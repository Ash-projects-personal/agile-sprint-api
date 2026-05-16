from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from src.database import Base


class Sprint(Base):
    __tablename__ = "sprints"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    goal = Column(Text)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=False)
    status = Column(String, default="planned")
    
    stories = relationship("Story", back_populates="sprint")


class Story(Base):
    __tablename__ = "stories"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    acceptance_criteria = Column(Text)
    story_points = Column(Integer)
    status = Column(String, default="todo")
    created_at = Column(DateTime, default=datetime.utcnow)
    sprint_id = Column(Integer, ForeignKey("sprints.id"), nullable=True)
    
    sprint = relationship("Sprint", back_populates="stories")
