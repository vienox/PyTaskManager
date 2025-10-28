import flet as ft
from components.user_task_manager import create_user_task_manager

def create_tasks_view(page: ft.Page, api, user, on_logout, on_back_to_profile=None):
    """
    Create tasks view for regular user.
    
    Args:
        page: Flet Page instance
        api: APIClient instance
        user: Dictionary containing user data (username, email, is_admin)
        on_logout: Callback function for logout action
        on_back_to_profile: Callback function to return to user profile
    """
    
    tasks_widget, load_tasks_callback = create_user_task_manager(page, api)
    
    navbar_actions = []
    
    if on_back_to_profile:
        navbar_actions.append(
            ft.IconButton(
                icon=ft.Icons.HOME,
                icon_color=ft.Colors.WHITE,
                tooltip="Back to Profile",
                on_click=lambda e: on_back_to_profile()
            )
        )
    
    navbar_actions.extend([
        ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE, size=20),
        ft.Text(user['username'], color=ft.Colors.WHITE, weight=ft.FontWeight.W_500),
        ft.IconButton(
            icon=ft.Icons.LOGOUT,
            icon_color=ft.Colors.WHITE,
            tooltip="Logout",
            on_click=lambda e: on_logout()
        )
    ])
    
    navbar = ft.Container(
        content=ft.Row([
            ft.Row([
                ft.Icon(ft.Icons.TASK_ALT, color=ft.Colors.WHITE, size=28),
                ft.Text("My Tasks", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
            ], spacing=10),
            
            ft.Container(expand=True),
            
            ft.Row(navbar_actions, spacing=10)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=15,
        bgcolor=ft.Colors.BLUE_700,
        border_radius=ft.border_radius.only(bottom_left=10, bottom_right=10)
    )
    
    view = ft.Column([
        navbar,
        ft.Container(
            content=tasks_widget,
            padding=20,
            expand=True
        )
    ], expand=True, spacing=0)
    
    load_tasks_callback()
    
    return view