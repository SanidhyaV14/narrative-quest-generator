import pytest


def test_tc01_register_valid_user(client):
    """TC01: Register with valid details."""
    response = client.post("/api/auth/register", json={
        "username": "new_writer",
        "email": "writer@example.com",
        "password": "secretpassword",
        "confirm_password": "secretpassword"
    })
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "writer@example.com"
    assert data["user"]["username"] == "new_writer"


def test_tc02_register_existing_email(client):
    """TC02: Register with an existing email."""
    # First registration
    client.post("/api/auth/register", json={
        "username": "writer_one",
        "email": "duplicate@example.com",
        "password": "secretpassword",
        "confirm_password": "secretpassword"
    })
    # Duplicate attempt
    response = client.post("/api/auth/register", json={
        "username": "writer_two",
        "email": "duplicate@example.com",
        "password": "secretpassword",
        "confirm_password": "secretpassword"
    })
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_tc03_login_valid_credentials(client):
    """TC03: Login with valid credentials."""
    client.post("/api/auth/register", json={
        "username": "login_user",
        "email": "login_test@example.com",
        "password": "mypassword123",
        "confirm_password": "mypassword123"
    })
    response = client.post("/api/auth/login", json={
        "email": "login_test@example.com",
        "password": "mypassword123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "login_test@example.com"


def test_tc04_login_invalid_credentials(client):
    """TC04: Login with invalid credentials."""
    response = client.post("/api/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]
