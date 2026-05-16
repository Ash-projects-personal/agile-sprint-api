from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class SprintCreate(BaseModel):
    name: str
    goal: Optional[str] = None
    duration_days: int = 14


class SprintResponse(BaseModel):
    id: int
    name: str
    goal: Optional[str]
    start_date: datetime
    end_date: datetime
    status: str
    
    class Config:
        from_attributes = True


class StoryCreate(BaseModel):
    title: str
    description: Optional[str] = None
    acceptance_criteria: Optional[str] = None
    story_points: Optional[int] = None
    sprint_id: Optional[int] = None


class StoryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    acceptance_criteria: Optional[str] = None
    story_points: Optional[int] = None
    status: Optional[str] = None
    sprint_id: Optional[int] = None


class StoryResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    acceptance_criteria: Optional[str]
    story_points: Optional[int]
    status: str
    created_at: datetime
    sprint_id: Optional[int]
    
    class Config:
        from_attributes = True


class VelocityResponse(BaseModel):
    average_velocity: float
    completed_sprints: int
    recent_sprints: List[dict]
