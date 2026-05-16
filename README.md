# Agile Sprint API

A lightweight sprint planning and tracking system. Manages user stories, sprints, and calculates team velocity.

## What this demonstrates

- User story management with acceptance criteria and story points
- Sprint planning and execution tracking
- Velocity calculation across sprints
- Story point estimation and burn tracking
- RESTful API design for agile workflows

## Setup

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python -m uvicorn src.main:app --reload
```

API docs at http://localhost:8000/docs

## Quick start

```bash
# Create a sprint
curl -X POST http://localhost:8000/sprints \
  -H "Content-Type: application/json" \
  -d '{"name": "Sprint 1", "duration_days": 14, "goal": "MVP features"}'

# Add a story
curl -X POST http://localhost:8000/stories \
  -H "Content-Type: application/json" \
  -d '{"title": "User login", "description": "As a user I can log in", "story_points": 5, "sprint_id": 1}'

# Check velocity
curl http://localhost:8000/metrics/velocity
```

## What's intentionally simplified

- No authentication (would add JWT in production)
- SQLite instead of Postgres
- No task assignment to individuals yet
- Burndown is calculated on-demand, not cached

## Next steps

See `roadmap.md` for planned improvements.

## Tests

```bash
pytest
```
