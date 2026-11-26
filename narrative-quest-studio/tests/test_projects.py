import pytest


def test_tc12_save_project(client, auth_headers):
    """TC12: Save a project."""
    payload = {
        "title": "The Quest for the Crystal Orb",
        "project_type": "GAME_QUEST",
        "input_data": {"genre": "RPG", "difficulty": "Medium"},
        "generated_content": {
            "title": "The Quest for the Crystal Orb",
            "quest_description": "Retrieve the ancient crystal orb."
        },
        "image_paths": ["uploads/generated/sample.png"]
    }
    response = client.post("/api/projects", json=payload, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "The Quest for the Crystal Orb"
    assert data["project_type"] == "GAME_QUEST"
    assert len(data["images"]) == 1


def test_tc13_retrieve_project_history(client, auth_headers):
    """TC13: Retrieve project history."""
    response = client.get("/api/projects", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "projects" in data
    assert "total" in data
    assert data["total"] >= 1


def test_tc14_delete_project(client, auth_headers):
    """TC14: Delete a project."""
    create_resp = client.post("/api/projects", json={
        "title": "Project to Delete",
        "project_type": "STORY",
        "input_data": {"genre": "Horror"},
        "generated_content": {"title": "To Delete"}
    }, headers=auth_headers)
    proj_id = create_resp.json()["id"]

    del_resp = client.delete(f"/api/projects/{proj_id}", headers=auth_headers)
    assert del_resp.status_code == 200

    # Verify project no longer exists
    get_resp = client.get(f"/api/projects/{proj_id}", headers=auth_headers)
    assert get_resp.status_code == 404


def test_tc15_prevent_unauthorized_access(client, auth_headers):
    """TC15: Prevent unauthorized access to another user's project."""
    # Create project by testuser
    proj = client.post("/api/projects", json={
        "title": "Private Project",
        "project_type": "STORY",
        "input_data": {},
        "generated_content": {"title": "Secret"}
    }, headers=auth_headers).json()
    proj_id = proj["id"]

    # Register second user
    client.post("/api/auth/register", json={
        "username": "intruder",
        "email": "intruder@example.com",
        "password": "password123",
        "confirm_password": "password123"
    })
    login_resp = client.post("/api/auth/login", json={
        "email": "intruder@example.com",
        "password": "password123"
    })
    intruder_token = login_resp.json()["access_token"]
    intruder_headers = {"Authorization": f"Bearer {intruder_token}"}

    # Attempt to view project
    view_resp = client.get(f"/api/projects/{proj_id}", headers=intruder_headers)
    assert view_resp.status_code == 403

    # Attempt to delete project
    del_resp = client.delete(f"/api/projects/{proj_id}", headers=intruder_headers)
    assert del_resp.status_code == 403


def test_tc16_export_project_as_txt(client, auth_headers):
    """TC16: Export project as TXT."""
    proj = client.post("/api/projects", json={
        "title": "Exportable Story",
        "project_type": "STORY",
        "input_data": {"genre": "Fantasy"},
        "generated_content": {
            "title": "Exportable Story",
            "complete_story": "Once upon a time in a distant kingdom..."
        }
    }, headers=auth_headers).json()
    proj_id = proj["id"]

    export_resp = client.get(f"/api/projects/{proj_id}/export", headers=auth_headers)
    assert export_resp.status_code == 200
    assert "text/plain" in export_resp.headers["content-type"]
    assert "NARRATIVE STUDIO - PROJECT EXPORT" in export_resp.text
    assert "Exportable Story" in export_resp.text
