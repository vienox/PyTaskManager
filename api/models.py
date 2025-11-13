"""
Data models for the Task Manager application.

This module defines SQLModel schemas for:
    - User: Authentication and authorization
    - Task: User task management
    
The models use SQLModel which combines Pydantic validation with SQLAlchemy ORM.
"""

from typing import Optional
from sqlmodel import SQLModel, Field


# ============ User Models ============

class User(SQLModel, table=True):
    """
    User database model with authentication and role-based access control.
    
    Attributes:
        id: Auto-incrementing primary key
        username: Unique username for login (indexed for performance)
        email: Unique email address (indexed for performance)
        hashed_password: Bcrypt hashed password (NEVER store plain passwords)
        is_admin: Role flag - True for administrators, False for regular users
        
    Security Notes:
        - Passwords are hashed using bcrypt with SHA256 pre-hash (see auth.py)
        - Username and email must be unique (enforced at database level)
        - Admin users have full CRUD access to all users and tasks
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_admin: bool = False


class UserCreate(SQLModel):
    """
    Schema for creating a new user (admin-only endpoint).
    
    Validation Requirements:
        - username: min 3 characters, unique
        - email: valid email format, unique
        - password: min 6 characters (plaintext, will be hashed)
    """
    username: str
    email: str
    password: str


class UserRead(SQLModel):
    """
    Safe user schema for API responses (excludes password).
    
    Used in:
        - GET /auth/me (current user info)
        - GET /admin/users (list all users)
        - POST /admin/users (create user response)
    """
    id: int
    username: str
    email: str
    is_admin: bool


# ============ Task Models ============

class TaskBase(SQLModel):
    """
    Base task schema with common fields.
    
    Attributes:
        title: Task title/name (required)
        description: Optional detailed description
        completed: Completion status (default: False)
    """
    title: str
    description: Optional[str] = None
    completed: bool = False


class Task(TaskBase, table=True):
    """
    Task database model with owner relationship.
    
    Attributes:
        id: Auto-incrementing primary key
        owner_id: Foreign key to User.id (task owner)
        
    Relationships:
        - Each task belongs to one user (owner_id)
        - Regular users can only access their own tasks
        - Admins can access all tasks
        
    Cascade Behavior:
        - When a user is deleted, their tasks are automatically deleted
          (configured at database level via foreign key)
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id")


class TaskCreate(SQLModel):
    """
    Schema for creating a new task.
    
    Validation:
        - title: Required, min 3 characters (enforced in frontend)
        - description: Optional
        - completed: Optional, defaults to False
    """
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False


class TaskUpdate(SQLModel):
    """
    Schema for partial task updates.
    
    All fields are optional to support partial updates (PATCH semantics).
    Only provided fields will be updated in the database.
    
    Example:
        # Only update completion status
        {"completed": True}
        
        # Update title and description
        {"title": "New Title", "description": "New description"}
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
