import requests
from config import API_BASE_URL

class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.token = None
    
    def login(self, username: str, password: str):
        """Logowanie - zwraca token"""
        data = {"username": username, "password": password}
        r = requests.post(f"{self.base_url}/auth/token", data=data)
        r.raise_for_status()
        self.token = r.json()["access_token"]
        return self.token
    
    def get_me(self):
        """Pobierz info o zalogowanym userze"""
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.get(f"{self.base_url}/auth/me", headers=headers)
        r.raise_for_status()
        return r.json()
    
    def get_tasks(self):
        """Lista tasków usera"""
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.get(f"{self.base_url}/tasks", headers=headers)
        r.raise_for_status()
        return r.json()
    
    def create_task(self, title: str, description: str = "", completed: bool = False):
        """Dodaj task"""
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {"title": title, "description": description, "completed": completed}
        r = requests.post(f"{self.base_url}/tasks", json=data, headers=headers)
        r.raise_for_status()
        return r.json()
    
    def update_task(self, task_id: int, title: str = None, description: str = None, completed: bool = None):
        """Edytuj task"""
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
        """Usuń task"""
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.delete(f"{self.base_url}/tasks/{task_id}", headers=headers)
        r.raise_for_status()
    
    # ============ ADMIN ENDPOINTS ============
    def create_user(self, username: str, email: str, password: str):
        """Admin tworzy nowego usera"""
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {"username": username, "email": email, "password": password}
        r = requests.post(f"{self.base_url}/admin/users", json=data, headers=headers)
        r.raise_for_status()
        return r.json()
    
    def get_all_users(self):
        """Lista wszystkich userów (admin only)"""
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.get(f"{self.base_url}/admin/users", headers=headers)
        r.raise_for_status()
        return r.json()
    
    def get_all_tasks(self):
        """Wszystkie taski (admin only)"""
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.get(f"{self.base_url}/admin/tasks", headers=headers)
        r.raise_for_status()
        return r.json()
    
    def delete_user(self, user_id: int):
        """Usuń usera (admin only)"""
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.delete(f"{self.base_url}/admin/users/{user_id}", headers=headers)
        r.raise_for_status()
    
    def make_admin(self, user_id: int):
        """Nadaj uprawnienia admina (admin only)"""
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.put(f"{self.base_url}/admin/users/{user_id}/make-admin", headers=headers)
        r.raise_for_status()
        return r.json()