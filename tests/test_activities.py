import pytest


def test_get_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"


def test_signup_success(client):
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity_name]["participants"]


def test_signup_duplicate(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_invalid_activity(client):
    response = client.post("/activities/Unknown%20Club/signup", params={"email": "test@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_success(client):
    activity_name = "Programming Class"
    email = "emma@mergington.edu"

    response = client.post(f"/activities/{activity_name}/remove", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"

    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity_name]["participants"]


def test_remove_nonexistent_participant(client):
    activity_name = "Programming Class"
    email = "notregistered@mergington.edu"

    response = client.post(f"/activities/{activity_name}/remove", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_remove_invalid_activity(client):
    response = client.post("/activities/Nonexistent%20Activity/remove", params={"email": "test@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
