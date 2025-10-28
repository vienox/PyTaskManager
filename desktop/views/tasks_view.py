import flet as ft
from components.user_task_manager import create_user_task_manager

def create_tasks_view(page: ft.Page, api, user, on_logout, on_back_to_profile=None):
    """
    Widok tasków dla zwykłego usera
    
    Args:
        page: Flet Page
        api: APIClient instance
        user: dict z danymi usera (username, email, is_admin)
        on_logout: callback - wywołany po kliknięciu logout
        on_back_to_profile: callback - powrót do profilu użytkownika
    """
    
    # Komponent zarządzania taskami
    tasks_widget, load_tasks_callback = create_user_task_manager(page, api)
    
    # ========== NAVBAR ==========
    navbar_actions = []
    
    # Przycisk powrotu do profilu (jeśli callback istnieje)
    if on_back_to_profile:
        navbar_actions.append(
            ft.IconButton(
                icon=ft.Icons.HOME,
                icon_color=ft.Colors.WHITE,
                tooltip="Powrót do profilu",
                on_click=lambda e: on_back_to_profile()
            )
        )
    
    # User info + logout
    navbar_actions.extend([
        ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE, size=20),
        ft.Text(user['username'], color=ft.Colors.WHITE, weight=ft.FontWeight.W_500),
        ft.IconButton(
            icon=ft.Icons.LOGOUT,
            icon_color=ft.Colors.WHITE,
            tooltip="Wyloguj",
            on_click=lambda e: on_logout()
        )
    ])
    
    navbar = ft.Container(
        content=ft.Row([
            # Tytuł
            ft.Row([
                ft.Icon(ft.Icons.TASK_ALT, color=ft.Colors.WHITE, size=28),
                ft.Text("Moje Taski", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
            ], spacing=10),
            
            # Spacer
            ft.Container(expand=True),
            
            # Actions (back + user info + logout)
            ft.Row(navbar_actions, spacing=10)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=15,
        bgcolor=ft.Colors.BLUE_700,
        border_radius=ft.border_radius.only(bottom_left=10, bottom_right=10)
    )
    
    # ========== GŁÓWNY WIDOK ==========
    view = ft.Column([
        navbar,
        ft.Container(
            content=tasks_widget,
            padding=20,
            expand=True
        )
    ], expand=True, spacing=0)
    
    # Załaduj taski na start
    load_tasks_callback()
    
    return view