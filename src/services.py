from sqlalchemy.orm import Session
from src.models import Sprint, Story


def calculate_velocity(db: Session) -> dict:
    completed_sprints = db.query(Sprint).filter(Sprint.status == "completed").all()
    
    sprint_velocities = []
    total_velocity = 0
    
    for sprint in completed_sprints:
        completed_stories = [
            story for story in sprint.stories 
            if story.status == "done" and story.story_points
        ]
        sprint_points = sum(story.story_points for story in completed_stories)
        
        sprint_velocities.append({
            "sprint_id": sprint.id,
            "sprint_name": sprint.name,
            "points_completed": sprint_points
        })
        total_velocity += sprint_points
    
    avg_velocity = total_velocity / len(completed_sprints) if completed_sprints else 0
    
    return {
        "average_velocity": round(avg_velocity, 1),
        "completed_sprints": len(completed_sprints),
        "recent_sprints": sprint_velocities[-5:]
    }
