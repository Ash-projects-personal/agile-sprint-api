from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from src.database import engine, get_db, Base
from src.models import Sprint, Story
from src.schemas import SprintCreate, SprintResponse, StoryCreate, StoryResponse, StoryUpdate, VelocityResponse
from src.services import calculate_velocity

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Agile Sprint API", version="1.0.0")


@app.get("/")
def root():
    return {"message": "Agile Sprint API - see /docs for endpoints"}


@app.post("/sprints", response_model=SprintResponse)
def create_sprint(sprint: SprintCreate, db: Session = Depends(get_db)):
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=sprint.duration_days)
    
    db_sprint = Sprint(
        name=sprint.name,
        goal=sprint.goal,
        start_date=start_date,
        end_date=end_date,
        status="planned"
    )
    db.add(db_sprint)
    db.commit()
    db.refresh(db_sprint)
    return db_sprint


@app.get("/sprints", response_model=List[SprintResponse])
def list_sprints(db: Session = Depends(get_db)):
    return db.query(Sprint).all()


@app.get("/sprints/{sprint_id}", response_model=SprintResponse)
def get_sprint(sprint_id: int, db: Session = Depends(get_db)):
    sprint = db.query(Sprint).filter(Sprint.id == sprint_id).first()
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    return sprint


@app.post("/sprints/{sprint_id}/start")
def start_sprint(sprint_id: int, db: Session = Depends(get_db)):
    sprint = db.query(Sprint).filter(Sprint.id == sprint_id).first()
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    sprint.status = "active"
    db.commit()
    return {"message": f"Sprint {sprint_id} started"}


@app.post("/sprints/{sprint_id}/complete")
def complete_sprint(sprint_id: int, db: Session = Depends(get_db)):
    sprint = db.query(Sprint).filter(Sprint.id == sprint_id).first()
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    sprint.status = "completed"
    db.commit()
    return {"message": f"Sprint {sprint_id} completed"}


@app.post("/stories", response_model=StoryResponse)
def create_story(story: StoryCreate, db: Session = Depends(get_db)):
    if story.sprint_id:
        sprint = db.query(Sprint).filter(Sprint.id == story.sprint_id).first()
        if not sprint:
            raise HTTPException(status_code=404, detail="Sprint not found")
    
    db_story = Story(
        title=story.title,
        description=story.description,
        acceptance_criteria=story.acceptance_criteria,
        story_points=story.story_points,
        status="todo",
        sprint_id=story.sprint_id
    )
    db.add(db_story)
    db.commit()
    db.refresh(db_story)
    return db_story


@app.get("/stories", response_model=List[StoryResponse])
def list_stories(sprint_id: int = None, db: Session = Depends(get_db)):
    query = db.query(Story)
    if sprint_id:
        query = query.filter(Story.sprint_id == sprint_id)
    return query.all()


@app.get("/stories/{story_id}", response_model=StoryResponse)
def get_story(story_id: int, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story


@app.patch("/stories/{story_id}", response_model=StoryResponse)
def update_story(story_id: int, story_update: StoryUpdate, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    update_data = story_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(story, field, value)
    
    db.commit()
    db.refresh(story)
    return story


@app.get("/metrics/velocity", response_model=VelocityResponse)
def get_velocity(db: Session = Depends(get_db)):
    velocity_data = calculate_velocity(db)
    return velocity_data


@app.get("/sprints/{sprint_id}/summary")
def get_sprint_summary(sprint_id: int, db: Session = Depends(get_db)):
    sprint = db.query(Sprint).filter(Sprint.id == sprint_id).first()
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    
    stories = db.query(Story).filter(Story.sprint_id == sprint_id).all()
    
    total_points = sum(s.story_points for s in stories if s.story_points)
    completed_points = sum(s.story_points for s in stories if s.status == "done" and s.story_points)
    
    return {
        "sprint": sprint,
        "total_stories": len(stories),
        "total_points": total_points,
        "completed_points": completed_points,
        "completion_rate": round(completed_points / total_points * 100, 1) if total_points > 0 else 0
    }
