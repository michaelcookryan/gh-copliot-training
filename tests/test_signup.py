from fastapi.testclient import TestClient

from src.app import activities


def test_signup_adds_student_to_activity(client: TestClient) -> None:
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert activities[activity_name]["participants"].count(email) == 1


def test_signup_rejects_duplicate_student(client: TestClient) -> None:
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    participants_before = activities[activity_name]["participants"].copy()

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student already signed up for this activity"
    }
    assert activities[activity_name]["participants"] == participants_before


def test_signup_rejects_unknown_activity(client: TestClient) -> None:
    # Arrange
    activity_name = "Unknown Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
    assert activity_name not in activities


def test_signup_requires_email(client: TestClient) -> None:
    # Arrange
    activity_name = "Chess Club"
    participants_before = activities[activity_name]["participants"].copy()

    # Act
    response = client.post(f"/activities/{activity_name}/signup")

    # Assert
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", "email"]
    assert activities[activity_name]["participants"] == participants_before