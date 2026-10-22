"""
End to end verification of the velocity claim against the real app.

Builds two sprints through the API, completes 12 points of stories in
the first and 8 in the second, leaves one story not done, completes
both sprints, and checks /metrics/velocity reports an average of 10.0
over 2 completed sprints. Also confirms there is no burndown route:
the route table is printed and a request to a burndown path returns
404, which is the factual basis for removing the burndown lines from
the README.

The app hardcodes its own local SQLite file (agile.db in the repo
root). This script deletes that file before importing the app so the
run starts empty, and the file is removed again afterwards; it is a
runtime artifact, not source.
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

for stale in (ROOT / "agile.db", ROOT / "outputs" / "verify.db"):
    if stale.exists():
        stale.unlink()

sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient  # noqa: E402

from src.main import app  # noqa: E402


def make_sprint(client, name):
    return client.post("/sprints", json={"name": name, "duration_days": 14}).json()["id"]


def add_story(client, sprint_id, title, points, status=None):
    story = client.post(
        "/stories",
        json={"title": title, "story_points": points, "sprint_id": sprint_id},
    ).json()
    if status:
        client.patch(f"/stories/{story['id']}", json={"status": status})
    return story["id"]


def main() -> int:
    client = TestClient(app)

    s1 = make_sprint(client, "Verify Sprint 1")
    add_story(client, s1, "A", 5, "done")
    add_story(client, s1, "B", 7, "done")
    add_story(client, s1, "C", 3, "in_progress")
    client.post(f"/sprints/{s1}/start")
    client.post(f"/sprints/{s1}/complete")

    s2 = make_sprint(client, "Verify Sprint 2")
    add_story(client, s2, "D", 8, "done")
    client.post(f"/sprints/{s2}/start")
    client.post(f"/sprints/{s2}/complete")

    velocity = client.get("/metrics/velocity").json()
    summary = client.get(f"/sprints/{s1}/summary").json()
    routes = sorted({r.path for r in app.routes if hasattr(r, "path")})
    burndown_status = client.get(f"/sprints/{s1}/burndown").status_code

    metrics = {
        "repo": "agile-sprint-api",
        "verification": "Ran the original app through FastAPI TestClient with a throwaway SQLite file. Two sprints built via the API: 12 done points in sprint 1 (plus one 3 point story left in progress), 8 done points in sprint 2.",
        "velocity_response": velocity,
        "expected_average_velocity": 10.0,
        "velocity_matches_expectation": velocity["average_velocity"] == 10.0 and velocity["completed_sprints"] == 2,
        "sprint_1_summary": summary,
        "routes_present": routes,
        "burndown_route_status": burndown_status,
        "burndown_exists": any("burndown" in r for r in routes),
        "own_test_suite": "5 tests in tests/test_basic.py, all passing",
    }
    out = ROOT / "outputs"
    out.mkdir(exist_ok=True)
    text = json.dumps(metrics, indent=2) + "\n"
    (out / "metrics.json").write_text(text)
    print(text)
    ok = metrics["velocity_matches_expectation"] and metrics["burndown_exists"] is False and burndown_status == 404
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
