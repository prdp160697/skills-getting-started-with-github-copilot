def test_signup_success(client, sample_activity_name, sample_email):
    # First, get initial participants
    response = client.get("/activities")
    initial_data = response.json()
    initial_count = len(initial_data[sample_activity_name]["participants"])

    # Signup
    response = client.post(f"/activities/{sample_activity_name}/signup?email={sample_email}")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]

    # Check updated
    response = client.get("/activities")
    updated_data = response.json()
    assert len(updated_data[sample_activity_name]["participants"]) == initial_count + 1
    assert sample_email in updated_data[sample_activity_name]["participants"]


def test_signup_duplicate(client, sample_activity_name, sample_email):
    # Signup first time
    client.post(f"/activities/{sample_activity_name}/signup?email={sample_email}")
    # Second time
    response = client.post(f"/activities/{sample_activity_name}/signup?email={sample_email}")
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"].lower()


def test_signup_nonexistent_activity(client, sample_email):
    response = client.post(f"/activities/Nonexistent/signup?email={sample_email}")
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_remove_participant_success(client, sample_activity_name, sample_email):
    # Add first
    client.post(f"/activities/{sample_activity_name}/signup?email={sample_email}")
    # Remove
    response = client.delete(f"/activities/{sample_activity_name}/participants?email={sample_email}")
    assert response.status_code == 200
    data = response.json()
    assert "Removed" in data["message"]

    # Check removed
    response = client.get("/activities")
    updated_data = response.json()
    assert sample_email not in updated_data[sample_activity_name]["participants"]


def test_remove_nonexistent_participant(client, sample_activity_name):
    response = client.delete(f"/activities/{sample_activity_name}/participants?email=nonexistent@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_remove_nonexistent_activity(client, sample_email):
    response = client.delete(f"/activities/Nonexistent/participants?email={sample_email}")
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()