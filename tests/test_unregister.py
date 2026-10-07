from fastapi.testclient import TestClient

from src.app import activities


def test_unregister_removes_student_from_activity(client: TestClient) -> None:
    # Arrange
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from {activity_name}"
    }
    assert email not in activities[activity_name]["participants"]


def test_unregister_rejects_student_not_signed_up(client: TestClient) -> None:
    # Arrange
    activity_name = "Chess Club"
    email = "not.registered@mergington.edu"
    participants_before = activities[activity_name]["participants"].copy()

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Student is not signed up for this activity"
    }
    assert activities[activity_name]["participants"] == participants_before


def test_unregister_rejects_unknown_activity(client: TestClient) -> None:
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
    assert activity_name not in activities


def test_unregister_requires_email(client: TestClient) -> None:
    # Arrange
    activity_name = "Chess Club"
    participants_before = activities[activity_name]["participants"].copy()

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister")

    # Assert
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", "email"]
    assert activities[activity_name]["participants"] == participants_before