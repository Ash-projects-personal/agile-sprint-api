from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_create_sprint():
    response = client.post(
        "/sprints",
        json={"name": "Test Sprint", "goal": "Testing", "duration_days": 7}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Sprint"
    assert data["status"] == "planned"


def test_create_story():
    sprint_response = client.post(
        "/sprints",
        json={"name": "Sprint for Story", "duration_days": 14}
    )
    sprint_id = sprint_response.json()["id"]
    
    response = client.post(
        "/stories",
        json={
            "title": "Test Story",
            "description": "As a user...",
            "story_points": 3,
            "sprint_id": sprint_id
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Story"
    assert data["story_points"] == 3
    assert data["status"] == "todo"


def test_update_story_status():
    story_response = client.post(
        "/stories",
        json={"title": "Story to Update", "story_points": 5}
    )
    story_id = story_response.json()["id"]
    
    update_response = client.patch(
        f"/stories/{story_id}",
        json={"status": "done"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "done"


def test_velocity_calculation():
    response = client.get("/metrics/velocity")
    assert response.status_code == 200
    data = response.json()
    assert "average_velocity" in data
    assert "completed_sprints" in data
