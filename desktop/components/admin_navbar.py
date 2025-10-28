import flet as ft


def create_admin_navbar(page: ft.Page, user, on_logout, on_switch_users, on_switch_tasks):
    """
    Navbar dla widoku admina z zakładkami użytkowników i tasków
    
    Args:
        page: Flet Page
        user: dict z danymi użytkownika
        on_logout: callback wylogowania
        on_switch_users: callback przełączenia na użytkowników
        on_switch_tasks: callback przełączenia na taski
        
    Returns:
        Container z navbarem
    """
    
    return ft.Container(
        content=ft.Row([
            # Logo/Tytuł
            ft.Row([
                ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS, color=ft.Colors.AMBER_200, size=28),
                ft.Text(
                    "Panel Administracyjny",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE
                )
            ], spacing=10),
            
            # Spacer
            ft.Container(expand=True),
            
            # User info + logout
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS, color=ft.Colors.AMBER_200, size=20),
                    ft.Text(
                        user.get("username", "Admin"),
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.W_500
                    ),
                    ft.IconButton(
                        icon=ft.Icons.LOGOUT,
                        icon_color=ft.Colors.WHITE,
                        tooltip="Wyloguj",
                        on_click=lambda e: on_logout()
                    )
                ], spacing=10),
                padding=ft.padding.only(left=20)
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=15,
        bgcolor=ft.Colors.BLUE_700,
        border_radius=ft.border_radius.only(bottom_left=10, bottom_right=10)
    )


def create_admin_tabs(on_switch_users, on_switch_tasks, current_view="users"):
    """
    Zakładki przełączania widoków w panelu admina
    
    Args:
        on_switch_users: callback przełączenia na użytkowników
        on_switch_tasks: callback przełączenia na taski
        current_view: aktualny widok ("users" lub "tasks")
        
    Returns:
        tuple: (container_widget, users_button_ref, tasks_button_ref)
    """
    
    users_btn = ft.ElevatedButton(
        "Użytkownicy",
        icon=ft.Icons.PEOPLE,
        on_click=on_switch_users,
        bgcolor=ft.Colors.BLUE_700 if current_view == "users" else None
    )
    
    tasks_btn = ft.ElevatedButton(
        "Wszystkie Taski",
        icon=ft.Icons.TASK,
        on_click=on_switch_tasks,
        bgcolor=ft.Colors.BLUE_700 if current_view == "tasks" else None
    )
    
    widget = ft.Container(
        content=ft.Row([users_btn, tasks_btn], spacing=10),
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        bgcolor=ft.Colors.BLUE_50
    )
    
    return widget, users_btn, tasks_btn
