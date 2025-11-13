"""
API endpoint tests for PyTaskManager backend.

Tests authentication, task CRUD operations, and admin endpoints.
"""

import pytest
from fastapi.testclient import TestClient


# ============ Authentication Tests ============

def test_login_success(client: TestClient, test_user):
    """Test successful login with valid credentials."""
    response = client.post(
        "/auth/token",
        data={"username": "testuser", "password": "testpass123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_user(client: TestClient):
    """Test login with non-existent user."""
    response = client.post(
        "/auth/token",
        data={"username": "nonexistent", "password": "password"}
    )
    assert response.status_code == 404


def test_login_invalid_password(client: TestClient, test_user):
    """Test login with incorrect password."""
    response = client.post(
        "/auth/token",
        data={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 401


def test_get_current_user(client: TestClient, test_user, auth_headers):
    """Test getting current authenticated user info."""
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert data["is_admin"] is False


# ============ Task CRUD Tests ============

def test_create_task(client: TestClient, test_user, auth_headers):
    """Test creating a new task."""
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "completed": False
    }
    response = client.post("/tasks", json=task_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["completed"] is False
    assert "id" in data


def test_get_tasks(client: TestClient, test_user, auth_headers):
    """Test getting all tasks for current user."""
    # Create a task first
    client.post(
        "/tasks",
        json={"title": "Task 1", "completed": False},
        headers=auth_headers
    )
    
    response = client.get("/tasks", headers=auth_headers)
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    assert len(tasks) >= 1


def test_update_task(client: TestClient, test_user, auth_headers):
    """Test updating a task."""
    # Create task
    create_response = client.post(
        "/tasks",
        json={"title": "Original Title", "completed": False},
        headers=auth_headers
    )
    task_id = create_response.json()["id"]
    
    # Update task
    update_response = client.put(
        f"/tasks/{task_id}",
        json={"completed": True},
        headers=auth_headers
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["completed"] is True


def test_delete_task(client: TestClient, test_user, auth_headers):
    """Test deleting a task."""
    # Create task
    create_response = client.post(
        "/tasks",
        json={"title": "To Delete", "completed": False},
        headers=auth_headers
    )
    task_id = create_response.json()["id"]
    
    # Delete task
    delete_response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert delete_response.status_code == 204
    
    # Verify deletion
    get_response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert get_response.status_code == 404


# ============ Admin Tests ============

def test_create_user_as_admin(client: TestClient, test_admin, admin_headers):
    """Test admin creating a new user."""
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123"
    }
    response = client.post("/admin/users", json=user_data, headers=admin_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["is_admin"] is False


def test_create_user_as_regular_user(client: TestClient, test_user, auth_headers):
    """Test that regular users cannot create users."""
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123"
    }
    response = client.post("/admin/users", json=user_data, headers=auth_headers)
    assert response.status_code == 403


def test_get_all_users_as_admin(client: TestClient, test_admin, admin_headers):
    """Test admin getting all users."""
    response = client.get("/admin/users", headers=admin_headers)
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) >= 1


def test_get_all_tasks_as_admin(client: TestClient, test_admin, admin_headers):
    """Test admin getting all tasks system-wide."""
    response = client.get("/admin/tasks", headers=admin_headers)
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)


# ============ Authorization Tests ============

def test_access_without_token(client: TestClient):
    """Test that protected endpoints require authentication."""
    response = client.get("/tasks")
    assert response.status_code == 401


def test_access_with_invalid_token(client: TestClient):
    """Test that invalid tokens are rejected."""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/tasks", headers=headers)
    assert response.status_code == 401


# ============ Health Check ============

def test_health_check(client: TestClient):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
