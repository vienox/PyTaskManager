"""
FastAPI Task Management REST API with JWT Authentication.

This application provides a role-based task management system with:
    - JWT token-based authentication
    - Admin and regular user roles
    - CRUD operations for tasks and users
    - Role-based access control (RBAC)

Architecture:
    - Backend: FastAPI REST API (this file)
    - Desktop Client: Flet application (desktop/)
    - Database: SQLite with SQLModel ORM
    - Auth: JWT tokens with bcrypt password hashing

Access Control:
    - Regular users: Can only manage their own tasks
    - Admin users: Full CRUD access to all users and tasks
    - Public registration is DISABLED - only admins can create users
"""

from typing import List
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import select, Session
from .models import User, UserCreate, UserRead, Task, TaskCreate, TaskUpdate
from .db import init_db, get_session
from .auth import hash_password, verify_password, create_access_token, decode_token

# Initialize FastAPI application
app = FastAPI(title="Tasks API (JWT)", version="2.0.0")

# OAuth2 configuration for JWT bearer tokens
# tokenUrl points to the login endpoint that returns tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@app.on_event("startup")
def on_startup():
    """
    Application startup event handler.
    
    Initializes database tables on first run.
    Safe to call multiple times - won't recreate existing tables.
    """
    init_db()


# ============ Authentication Dependencies ============

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> User:
    """
    Dependency to extract and validate current user from JWT token.
    
    Args:
        token: JWT bearer token from Authorization header
        session: Database session
        
    Returns:
        User: Authenticated user object from database
        
    Raises:
        HTTPException 401: If token is invalid or user not found
        
    Usage:
        @app.get("/protected")
        def protected_route(current_user: User = Depends(get_current_user)):
            # Route accessible only to authenticated users
            pass
    """
    username = decode_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to ensure current user has admin privileges.
    
    Args:
        current_user: Authenticated user (from get_current_user dependency)
        
    Returns:
        User: Authenticated admin user
        
    Raises:
        HTTPException 403: If user is not an administrator
        
    Usage:
        @app.delete("/admin/users/{user_id}")
        def delete_user(user_id: int, admin: User = Depends(get_admin_user)):
            # Route accessible only to admins
            pass
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")
    return current_user


# ============ Health Check ============

@app.get("/health")
def health():
    """
    Health check endpoint for monitoring.
    
    Returns:
        dict: Simple status response
        
    Example:
        GET /health
        Response: {"status": "ok"}
    """
    return {"status": "ok"}


# ============ Authentication Endpoints ============

@app.post("/auth/token")
def login(form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """
    User login endpoint - returns JWT access token.
    
    Args:
        form: OAuth2 password form (username + password)
        session: Database session
        
    Returns:
        dict: Access token and token type
        
    Raises:
        HTTPException 404: User not found
        HTTPException 401: Invalid password
        
    Example:
        POST /auth/token
        Body: username=john_doe&password=secret123
        Response: {"access_token": "eyJ...", "token_type": "bearer"}
    """
    user = session.exec(select(User).where(User.username == form.username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    token = create_access_token(user.username)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/auth/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user's information.
    
    Args:
        current_user: Authenticated user (from JWT token)
        
    Returns:
        UserRead: Current user data (excluding password)
        
    Example:
        GET /auth/me
        Headers: Authorization: Bearer <token>
        Response: {"id": 1, "username": "john_doe", "email": "john@example.com", "is_admin": false}
    """
    return current_user


# ============ Task Endpoints (User Scope) ============

@app.get("/tasks", response_model=List[Task])
def get_tasks(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Get all tasks for the current authenticated user.
    
    Regular users can only see their own tasks (filtered by owner_id).
    
    Args:
        current_user: Authenticated user
        session: Database session
        
    Returns:
        List[Task]: User's tasks
    """
    tasks = session.exec(select(Task).where(Task.owner_id == current_user.id)).all()
    return tasks


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(data: TaskCreate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Create a new task for the current user.
    
    Args:
        data: Task creation data (title, description, completed)
        current_user: Authenticated user (becomes task owner)
        session: Database session
        
    Returns:
        Task: Newly created task with ID
        
    Example:
        POST /tasks
        Body: {"title": "Buy groceries", "description": "Milk, eggs, bread", "completed": false}
        Response: {"id": 1, "title": "Buy groceries", ..., "owner_id": 1}
    """
    task = Task(**data.dict(), owner_id=current_user.id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Get a specific task by ID.
    
    Users can only access their own tasks.
    
    Args:
        task_id: Task ID to retrieve
        current_user: Authenticated user
        session: Database session
        
    Returns:
        Task: Task details
        
    Raises:
        HTTPException 404: Task not found or not owned by user
    """
    task = session.get(Task, task_id)
    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, data: TaskUpdate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Update an existing task (partial updates supported).
    
    Users can only update their own tasks.
    
    Args:
        task_id: Task ID to update
        data: Fields to update (all optional)
        current_user: Authenticated user
        session: Database session
        
    Returns:
        Task: Updated task
        
    Raises:
        HTTPException 404: Task not found or not owned by user
        
    Example:
        PUT /tasks/1
        Body: {"completed": true}
        Response: Updated task with completed=true
    """
    task = session.get(Task, task_id)
    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for key, value in data.dict(exclude_unset=True).items():
        setattr(task, key, value)
    
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Delete a task.
    
    Users can only delete their own tasks.
    
    Args:
        task_id: Task ID to delete
        current_user: Authenticated user
        session: Database session
        
    Returns:
        None (204 No Content)
        
    Raises:
        HTTPException 404: Task not found or not owned by user
    """
    task = session.get(Task, task_id)
    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    session.delete(task)
    session.commit()
    return None


# ============ Admin Endpoints ============
# All endpoints below require admin privileges (is_admin=True)

@app.post("/admin/users", response_model=UserRead, status_code=201)
def create_user_admin(data: UserCreate, admin: User = Depends(get_admin_user), session: Session = Depends(get_session)):
    """
    Create a new user (admin only).
    
    This is the ONLY way to create users - public registration is disabled.
    
    Args:
        data: User creation data (username, email, password)
        admin: Authenticated admin user
        session: Database session
        
    Returns:
        UserRead: Created user (excluding password)
        
    Raises:
        HTTPException 400: Username or email already exists
        HTTPException 403: User is not an admin
        
    Example:
        POST /admin/users
        Body: {"username": "jane_doe", "email": "jane@example.com", "password": "secret123"}
        Response: {"id": 2, "username": "jane_doe", "email": "jane@example.com", "is_admin": false}
    """
    existing = session.exec(select(User).where(User.username == data.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    existing_email = session.exec(select(User).where(User.email == data.email)).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password),
        is_admin=False  # New users are NOT admins by default
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.get("/admin/users", response_model=List[UserRead])
def get_all_users(admin: User = Depends(get_admin_user), session: Session = Depends(get_session)):
    """
    Get all users in the system (admin only).
    
    Args:
        admin: Authenticated admin user
        session: Database session
        
    Returns:
        List[UserRead]: All users (excluding passwords)
    """
    users = session.exec(select(User)).all()
    return users


@app.get("/admin/tasks", response_model=List[Task])
def get_all_tasks(admin: User = Depends(get_admin_user), session: Session = Depends(get_session)):
    """
    Get all tasks in the system (admin only).
    
    Args:
        admin: Authenticated admin user
        session: Database session
        
    Returns:
        List[Task]: All tasks from all users
    """
    tasks = session.exec(select(Task)).all()
    return tasks


@app.post("/admin/tasks", response_model=Task, status_code=201)
def create_task_admin(data: TaskCreate, owner_id: int, admin: User = Depends(get_admin_user), session: Session = Depends(get_session)):
    """
    Create a task for a specific user (admin only).
    
    Args:
        data: Task creation data
        owner_id: ID of the user who will own the task
        admin: Authenticated admin user
        session: Database session
        
    Returns:
        Task: Newly created task
        
    Raises:
        HTTPException 404: User (owner_id) not found
        
    Example:
        POST /admin/tasks?owner_id=2
        Body: {"title": "Review documents", "completed": false}
        Response: Task assigned to user with ID 2
    """
    # Check if user exists
    owner = session.get(User, owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="User not found")
    
    task = Task(**data.dict(), owner_id=owner_id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.put("/admin/tasks/{task_id}", response_model=Task)
def update_task_admin(task_id: int, data: TaskUpdate, admin: User = Depends(get_admin_user), session: Session = Depends(get_session)):
    """
    Update any task in the system (admin only).
    
    Args:
        task_id: Task ID to update
        data: Fields to update
        admin: Authenticated admin user
        session: Database session
        
    Returns:
        Task: Updated task
        
    Raises:
        HTTPException 404: Task not found
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for key, value in data.dict(exclude_unset=True).items():
        setattr(task, key, value)
    
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.delete("/admin/tasks/{task_id}", status_code=204)
def delete_task_admin(task_id: int, admin: User = Depends(get_admin_user), session: Session = Depends(get_session)):
    """
    Delete any task in the system (admin only).
    
    Args:
        task_id: Task ID to delete
        admin: Authenticated admin user
        session: Database session
        
    Returns:
        None (204 No Content)
        
    Raises:
        HTTPException 404: Task not found
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    session.delete(task)
    session.commit()
    return None


@app.delete("/admin/users/{user_id}", status_code=204)
def delete_user(user_id: int, admin: User = Depends(get_admin_user), session: Session = Depends(get_session)):
    """
    Delete a user and all their tasks (admin only).
    
    Args:
        user_id: User ID to delete
        admin: Authenticated admin user
        session: Database session
        
    Returns:
        None (204 No Content)
        
    Raises:
        HTTPException 404: User not found
        HTTPException 400: Attempting to delete yourself
        
    Note:
        User's tasks are automatically deleted due to foreign key cascade.
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    
    session.delete(user)
    session.commit()
    return None


@app.put("/admin/users/{user_id}/make-admin", response_model=UserRead)
def make_admin(user_id: int, admin: User = Depends(get_admin_user), session: Session = Depends(get_session)):
    """
    Promote a user to administrator (admin only).
    
    Args:
        user_id: User ID to promote
        admin: Authenticated admin user
        session: Database session
        
    Returns:
        UserRead: Updated user with is_admin=True
        
    Raises:
        HTTPException 404: User not found
        
    Example:
        PUT /admin/users/2/make-admin
        Response: User with ID 2 now has admin privileges
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_admin = True
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
