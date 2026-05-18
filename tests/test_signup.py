from src import app as app_module


def test_signup_for_activity_succeeds(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Signed up {email} for {activity_name}"
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_for_missing_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_signup_duplicate_email_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = app_module.activities[activity_name]["participants"][0]

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Student already signed up for this activity"


def test_signup_when_activity_is_full_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    activity = app_module.activities[activity_name]
    activity["participants"] = [f"student{i}@mergington.edu" for i in range(activity["max_participants"])]

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": "late.student@mergington.edu"},
    )
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Activity is full"
