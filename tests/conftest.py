"""
Test configuration and fixtures for PyTaskManager.

This module provides pytest fixtures for backend API testing.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from api.app import app
from api.db import get_session
from api.models import User
from api.auth import hash_password


@pytest.fixture(name="session")
def session_fixture():
    """
    Create a fresh in-memory database for each test.
    
    Yields:
        Session: SQLModel database session
    """
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """
    Create FastAPI test client with test database.
    
    Args:
        session: Test database session
        
    Yields:
        TestClient: FastAPI test client
    """
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="test_user")
def test_user_fixture(session: Session):
    """
    Create a test user in the database.
    
    Args:
        session: Test database session
        
    Returns:
        User: Created test user
    """
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hash_password("testpass123"),
        is_admin=False
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="test_admin")
def test_admin_fixture(session: Session):
    """
    Create a test admin user in the database.
    
    Args:
        session: Test database session
        
    Returns:
        User: Created test admin user
    """
    admin = User(
        username="admin",
        email="admin@example.com",
        hashed_password=hash_password("admin123"),
        is_admin=True
    )
    session.add(admin)
    session.commit()
    session.refresh(admin)
    return admin


@pytest.fixture(name="user_token")
def user_token_fixture(client: TestClient):
    """
    Get JWT token for test user.
    
    Args:
        client: FastAPI test client
        
    Returns:
        str: JWT access token
    """
    response = client.post(
        "/auth/token",
        data={"username": "testuser", "password": "testpass123"}
    )
    return response.json()["access_token"]


@pytest.fixture(name="admin_token")
def admin_token_fixture(client: TestClient):
    """
    Get JWT token for test admin.
    
    Args:
        client: FastAPI test client
        
    Returns:
        str: JWT access token for admin
    """
    response = client.post(
        "/auth/token",
        data={"username": "admin", "password": "admin123"}
    )
    return response.json()["access_token"]


@pytest.fixture(name="auth_headers")
def auth_headers_fixture(user_token: str):
    """
    Get authorization headers for authenticated requests.
    
    Args:
        user_token: JWT token for test user
        
    Returns:
        dict: Authorization headers
    """
    return {"Authorization": f"Bearer {user_token}"}


@pytest.fixture(name="admin_headers")
def admin_headers_fixture(admin_token: str):
    """
    Get authorization headers for admin requests.
    
    Args:
        admin_token: JWT token for admin user
        
    Returns:
        dict: Authorization headers with admin token
    """
    return {"Authorization": f"Bearer {admin_token}"}
