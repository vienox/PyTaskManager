"""
API Client for Task Manager Desktop Application.

This module provides a centralized HTTP client for communicating with the FastAPI backend.
Handles authentication, session management, and all API endpoints.

Architecture:
    - Stateful client (stores JWT token after login)
    - Automatic Bearer token injection for authenticated requests
    - Raises HTTPError on API failures (handle in UI layer)

Usage:
    api = APIClient()
    api.login("username", "password")
    tasks = api.get_tasks()
"""

import requests

try:
    from .config import settings
except ImportError:
    from config import settings


class APIClient:
    """
    HTTP client for Task Manager REST API.
    
    Attributes:
        base_url (str): Backend API base URL (default: http://127.0.0.1:8000)
        token (str|None): JWT access token (set after successful login)
        
    Methods:
        Authentication:
            - login(username, password): Authenticate and store token
            - get_me(): Get current user information
            
        User Tasks (Regular endpoints):
            - get_tasks(): Get current user's tasks
            - create_task(title, description, completed): Create new task
            - update_task(task_id, ...): Update task
            - delete_task(task_id): Delete task
            
        Admin Endpoints:
            - get_all_users(): List all users
            - create_user(username, email, password): Create new user
            - delete_user(user_id): Delete user
            - make_admin(user_id): Promote user to admin
            - get_all_tasks(): Get all tasks (system-wide)
            - create_task_for_user(owner_id, ...): Create task for specific user
            - update_task_admin(task_id, ...): Update any task
            - delete_task_admin(task_id): Delete any task
    """
    
    def __init__(self):
        """
        Initialize API client with default configuration.
        
        Sets base_url from config and initializes token as None.
        """
        self.base_url = settings.api_url
        self.token = None
    
    # ============ Authentication ============
    
    def login(self, username: str, password: str):
        """
        Authenticate user and store access token.
        
        Args:
            username: User's username
            password: User's password (plaintext, sent via HTTPS)
            
        Returns:
            None (stores token in self.token)
            
        Raises:
            requests.HTTPError: If login fails (404: user not found, 401: wrong password)
            
        Example:
            >>> api = APIClient()
            >>> api.login("john_doe", "secret123")
            >>> print(api.token)  # JWT token stored
        """
        response = requests.post(
            f"{self.base_url}/auth/token",
            data={"username": username, "password": password}
        )
        response.raise_for_status()
        data = response.json()
        self.token = data["access_token"]
    
    def get_me(self):
        """
        Get current authenticated user's information.
        
        Returns:
            dict: User data (id, username, email, is_admin)
            
        Raises:
            requests.HTTPError: If token is invalid or expired
            
        Example:
            >>> user = api.get_me()
            >>> print(user["username"])
            'john_doe'
        """
        response = requests.get(
            f"{self.base_url}/auth/me",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        response.raise_for_status()
        return response.json()
    
    # ============ User Task Endpoints ============
    
    def get_tasks(self):
        """
        Get all tasks for the current authenticated user.
        
        Returns:
            list: List of task dictionaries
            
        Raises:
            requests.HTTPError: If unauthorized or token expired
        """
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.get(f"{self.base_url}/tasks", headers=headers)
        r.raise_for_status()
        return r.json()
    
    def create_task(self, title: str, description: str = "", completed: bool = False):
        """
        Create a new task for the current user.
        
        Args:
            title: Task title (required)
            description: Task description (optional)
            completed: Completion status (default: False)
            
        Returns:
            dict: Created task with assigned ID
            
        Raises:
            requests.HTTPError: If validation fails or unauthorized
        """
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {"title": title, "description": description, "completed": completed}
        r = requests.post(f"{self.base_url}/tasks", json=data, headers=headers)
        r.raise_for_status()
        return r.json()
    
    def update_task(self, task_id: int, title: str = None, description: str = None, completed: bool = None):
        """
        Update an existing task (partial updates supported).
        
        Args:
            task_id: ID of task to update
            title: New title (optional)
            description: New description (optional)
            completed: New completion status (optional)
            
        Returns:
            dict: Updated task
            
        Raises:
            requests.HTTPError: If task not found or unauthorized
        """
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {}
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if completed is not None:
            data["completed"] = completed
        
        r = requests.put(f"{self.base_url}/tasks/{task_id}", json=data, headers=headers)
        r.raise_for_status()
        return r.json()
    
    def delete_task(self, task_id: int):
        """
        Delete a task owned by the current user.
        
        Args:
            task_id: ID of task to delete
            
        Returns:
            None
            
        Raises:
            requests.HTTPError: If task not found or unauthorized
        """
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.delete(f"{self.base_url}/tasks/{task_id}", headers=headers)
        r.raise_for_status()
    
    # ============ Admin User Management ============
    
    def create_user(self, username: str, email: str, password: str):
        """
        Create a new user (admin only).
        
        Args:
            username: Unique username (min 3 chars)
            email: Unique email address
            password: Password (min 6 chars)
            
        Returns:
            dict: Created user (excluding password)
            
        Raises:
            requests.HTTPError: 400 if username/email exists, 403 if not admin
        """
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {"username": username, "email": email, "password": password}
        r = requests.post(f"{self.base_url}/admin/users", json=data, headers=headers)
        r.raise_for_status()
        return r.json()
    
    def get_all_users(self):
        """
        Get all users in the system (admin only).
        
        Returns:
            list: List of all users
            
        Raises:
            requests.HTTPError: 403 if not admin
        """
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.get(f"{self.base_url}/admin/users", headers=headers)
        r.raise_for_status()
        return r.json()
    
    def delete_user(self, user_id: int):
        """
        Delete a user and all their tasks (admin only).
        
        Args:
            user_id: ID of user to delete
            
        Returns:
            None
            
        Raises:
            requests.HTTPError: 400 if deleting self, 403 if not admin, 404 if user not found
        """
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.delete(f"{self.base_url}/admin/users/{user_id}", headers=headers)
        r.raise_for_status()
    
    def make_admin(self, user_id: int):
        """
        Promote a user to administrator (admin only).
        
        Args:
            user_id: ID of user to promote
            
        Returns:
            dict: Updated user with is_admin=True
            
        Raises:
            requests.HTTPError: 403 if not admin, 404 if user not found
        """
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.put(f"{self.base_url}/admin/users/{user_id}/make-admin", headers=headers)
        r.raise_for_status()
        return r.json()
    
    # ============ Admin Task Management ============
    
    def get_all_tasks(self):
        """
        Get all tasks in the system (admin only).
        
        Returns:
            list: All tasks from all users
            
        Raises:
            requests.HTTPError: 403 if not admin
        """
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.get(f"{self.base_url}/admin/tasks", headers=headers)
        r.raise_for_status()
        return r.json()
    
    def create_task_for_user(self, owner_id: int, title: str, description: str = "", completed: bool = False):
        """
        Create a task for a specific user (admin only).
        
        Args:
            owner_id: User ID who will own the task
            title: Task title
            description: Task description (optional)
            completed: Completion status (default: False)
            
        Returns:
            dict: Created task
            
        Raises:
            requests.HTTPError: 403 if not admin, 404 if user not found
        """
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {"title": title, "description": description, "completed": completed}
        r = requests.post(f"{self.base_url}/admin/tasks?owner_id={owner_id}", json=data, headers=headers)
        r.raise_for_status()
        return r.json()
    
    def update_task_admin(self, task_id: int, title: str = None, description: str = None, completed: bool = None):
        """
        Update any task in the system (admin only).
        
        Args:
            task_id: ID of task to update
            title: New title (optional)
            description: New description (optional)
            completed: New completion status (optional)
            
        Returns:
            dict: Updated task
            
        Raises:
            requests.HTTPError: 403 if not admin, 404 if task not found
        """
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {}
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if completed is not None:
            data["completed"] = completed
        
        r = requests.put(f"{self.base_url}/admin/tasks/{task_id}", json=data, headers=headers)
        r.raise_for_status()
        return r.json()
    
    def delete_task_admin(self, task_id: int):
        """
        Delete any task in the system (admin only).
        
        Args:
            task_id: ID of task to delete
            
        Returns:
            None
            
        Raises:
            requests.HTTPError: 403 if not admin, 404 if task not found
        """
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.delete(f"{self.base_url}/admin/tasks/{task_id}", headers=headers)
        r.raise_for_status()