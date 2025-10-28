import flet as ft


def create_user_navbar(page: ft.Page, user, on_logout):
    """
    Navbar dla zwykłego użytkownika
    
    Args:
        page: Flet Page
        user: dict z danymi użytkownika
        on_logout: callback wylogowania
        
    Returns:
        Container z navbarem
    """
    
    return ft.Container(
        content=ft.Row([
            # Tytuł
            ft.Row([
                ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE, size=28),
                ft.Text(
                    "Profil Użytkownika",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE
                )
            ], spacing=10),
            
            # Spacer
            ft.Container(expand=True),
            
            # Logout
            ft.IconButton(
                icon=ft.Icons.LOGOUT,
                icon_color=ft.Colors.WHITE,
                tooltip="Wyloguj",
                on_click=lambda e: on_logout()
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=15,
        bgcolor=ft.Colors.BLUE_700,
        border_radius=ft.border_radius.only(bottom_left=10, bottom_right=10)
    )
