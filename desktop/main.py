import flet as ft
from api_client import APIClient
from views.auth.login import create_login_view
from views.user.profile import create_user_view
from views.admin.panel import create_admin_view
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT


def main(page: ft.Page):
    page.title = "Task Manager"
    page.window_width = WINDOW_WIDTH
    page.window_height = WINDOW_HEIGHT
    page.window_min_width = WINDOW_MIN_WIDTH
    page.window_min_height = WINDOW_MIN_HEIGHT
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    
    api = APIClient()
    current_user = None
    
    def show_snackbar(message: str, color: str = "red"):
        """Show a snackbar notification"""
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color="white"),
            bgcolor=color
        )
        page.snack_bar.open = True
        page.update()
    
    def show_login():
        page.controls.clear()
        
        def on_login_success(user):
            nonlocal current_user
            current_user = user
            show_snackbar(f"Welcome, {user['username']}!", "green")
            if user["is_admin"]:
                show_admin()
            else:
                show_user_profile()
        
        page.add(create_login_view(page, api, on_login_success))
        page.update()
    
    def show_user_profile():
        page.controls.clear()
        page.add(create_user_view(page, api, current_user, on_logout=show_login))
        page.update()
    
    def show_admin():
        page.controls.clear()
        page.add(create_admin_view(page, api, current_user, on_logout=show_login))
        page.update()
    
    show_login()


if __name__ == "__main__":
    ft.app(target=main)