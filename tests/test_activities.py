import pytest


def test_get_activities(client):
    # Arrange
    expected_keys = {"Chess Club", "Programming Class"}

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(data, dict)
    assert expected_keys.issubset(data.keys())
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"


def test_signup_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in participants


def test_signup_duplicate(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    body = response.json()

    # Assert
    assert response.status_code == 400
    assert body["detail"] == "Student is already signed up for this activity"


def test_signup_invalid_activity(client):
    # Arrange
    invalid_activity = "Unknown Club"
    email = "test@mergington.edu"

    # Act
    response = client.post(f"/activities/{invalid_activity}/signup", params={"email": email})
    body = response.json()

    # Assert
    assert response.status_code == 404
    assert body["detail"] == "Activity not found"


def test_remove_participant_success(client):
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/remove", params={"email": email})
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in participants


def test_remove_nonexistent_participant(client):
    # Arrange
    activity_name = "Programming Class"
    email = "notregistered@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/remove", params={"email": email})
    body = response.json()

    # Assert
    assert response.status_code == 400
    assert body["detail"] == "Student is not signed up for this activity"


def test_remove_invalid_activity(client):
    # Arrange
    invalid_activity = "Nonexistent Activity"
    email = "test@mergington.edu"

    # Act
    response = client.post(f"/activities/{invalid_activity}/remove", params={"email": email})
    body = response.json()

    # Assert
    assert response.status_code == 404
    assert body["detail"] == "Activity not found"
