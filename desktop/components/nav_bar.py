import flet as ft

def create_nav_bar(page: ft.Page, current_user: dict, on_logout, on_profile=None, on_tasks=None, on_admin=None):
    """
    Nawigacja górna z nazwą użytkownika i guzikami
    
    Args:
        page: Flet Page
        current_user: dict z danymi usera (username, is_admin)
        on_logout: callback - wylogowanie
        on_profile: callback - przejście do profilu (opcjonalne)
        on_tasks: callback - przejście do tasków (opcjonalne)
        on_admin: callback - przejście do panelu admina (opcjonalne, tylko dla adminów)
    """
    
    # Menu buttons
    menu_buttons = []
    
    if on_profile:
        menu_buttons.append(
            ft.TextButton(
                "📊 Profil",
                on_click=lambda e: on_profile(),
                style=ft.ButtonStyle(color=ft.Colors.WHITE)
            )
        )
    
    if on_tasks:
        menu_buttons.append(
            ft.TextButton(
                "📝 Taski",
                on_click=lambda e: on_tasks(),
                style=ft.ButtonStyle(color=ft.Colors.WHITE)
            )
        )
    
    # Admin panel - tylko dla adminów
    if current_user.get("is_admin") and on_admin:
        menu_buttons.append(
            ft.TextButton(
                "🛡️ Panel Admina",
                on_click=lambda e: on_admin(),
                style=ft.ButtonStyle(color=ft.Colors.AMBER_200)
            )
        )
    
    return ft.Container(
        content=ft.Row([
            # Logo/Tytuł
            ft.Row([
                ft.Icon(ft.Icons.TASK_ALT, color=ft.Colors.WHITE, size=28),
                ft.Text(
                    "Task Manager",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE
                )
            ], spacing=10),
            
            # Spacer
            ft.Container(expand=True),
            
            # Menu buttons
            ft.Row(menu_buttons, spacing=5),
            
            # User info + logout
            ft.Container(
                content=ft.Row([
                    ft.Icon(
                        ft.Icons.ADMIN_PANEL_SETTINGS if current_user.get("is_admin") else ft.Icons.PERSON,
                        color=ft.Colors.AMBER_200 if current_user.get("is_admin") else ft.Colors.WHITE,
                        size=20
                    ),
                    ft.Text(
                        current_user.get("username", "User"),
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