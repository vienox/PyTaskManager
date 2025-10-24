import flet as ft
from api_client import APIClient
from views.login_view import create_login_view
from views.user_view import create_user_view
from views.tasks_view import create_tasks_view
from views.admin_view import create_admin_view

def main(page: ft.Page):
    page.title = "Task Manager"
    page.window_width = 900
    page.window_height = 700
    page.window_min_width = 600
    page.window_min_height = 500
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    
    api = APIClient()
    current_user = None
    
    def show_login():
        """Pokaż ekran logowania"""
        page.controls.clear()
        
        def on_login_success(user):
            nonlocal current_user
            current_user = user
            
            # Routing w zależności od roli
            if user["is_admin"]:
                show_admin()
            else:
                show_user_profile()  # Najpierw profil, potem może przejść do tasków
        
        page.add(create_login_view(page, api, on_login_success))
        page.update()
    
    def show_user_profile():
        """Widok profilu użytkownika (dashboard ze statystykami)"""
        page.controls.clear()
        page.add(create_user_view(page, api, current_user, on_logout=show_login))
        page.update()
    
    def show_tasks():
        """Widok tasków dla zwykłego usera"""
        page.controls.clear()
        page.add(create_tasks_view(page, api, current_user, on_logout=show_login))
        page.update()
    
    def show_admin():
        """Panel admina"""
        page.controls.clear()
        page.add(create_admin_view(page, api, current_user, on_logout=show_login))
        page.update()
    
    # Start - pokaż login
    show_login()

if __name__ == "__main__":
    ft.app(target=main)