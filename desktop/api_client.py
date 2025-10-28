import requests

class APIClient:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.token = None
    
    def login(self, username: str, password: str):
        response = requests.post(
            f"{self.base_url}/auth/token",
            data={"username": username, "password": password}
        )
        response.raise_for_status()
        data = response.json()
        self.token = data["access_token"]
    
    def get_me(self):
        response = requests.get(
            f"{self.base_url}/auth/me",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        response.raise_for_status()
        return response.json()
    
    def get_tasks(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.get(f"{self.base_url}/tasks", headers=headers)
        r.raise_for_status()
        return r.json()
    
    def create_task(self, title: str, description: str = "", completed: bool = False):
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {"title": title, "description": description, "completed": completed}
        r = requests.post(f"{self.base_url}/tasks", json=data, headers=headers)
        r.raise_for_status()
        return r.json()
    
    def update_task(self, task_id: int, title: str = None, description: str = None, completed: bool = None):
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
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.delete(f"{self.base_url}/tasks/{task_id}", headers=headers)
        r.raise_for_status()
    
    # ============ ADMIN ENDPOINTS ============
    def create_user(self, username: str, email: str, password: str):
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {"username": username, "email": email, "password": password}
        r = requests.post(f"{self.base_url}/admin/users", json=data, headers=headers)
        r.raise_for_status()
        return r.json()
    
    def get_all_users(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.get(f"{self.base_url}/admin/users", headers=headers)
        r.raise_for_status()
        return r.json()
    
    def get_all_tasks(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.get(f"{self.base_url}/admin/tasks", headers=headers)
        r.raise_for_status()
        return r.json()
    
    def delete_user(self, user_id: int):
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.delete(f"{self.base_url}/admin/users/{user_id}", headers=headers)
        r.raise_for_status()
    
    def make_admin(self, user_id: int):
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.put(f"{self.base_url}/admin/users/{user_id}/make-admin", headers=headers)
        r.raise_for_status()
        return r.json()
    
    # ============ ADMIN TASK MANAGEMENT ============
    def create_task_for_user(self, owner_id: int, title: str, description: str = "", completed: bool = False):
        """Admin tworzy task dla określonego użytkownika"""
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {"title": title, "description": description, "completed": completed}
        r = requests.post(f"{self.base_url}/admin/tasks?owner_id={owner_id}", json=data, headers=headers)
        r.raise_for_status()
        return r.json()
    
    def update_task_admin(self, task_id: int, title: str = None, description: str = None, completed: bool = None):
        """Admin edytuje task dowolnego użytkownika"""
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
        """Admin usuwa task dowolnego użytkownika"""
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.delete(f"{self.base_url}/admin/tasks/{task_id}", headers=headers)
        r.raise_for_status()