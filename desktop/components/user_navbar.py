import flet as ft


def create_user_navbar(page: ft.Page, user, on_logout):
    """
    Create navigation bar for regular user view.
    
    Args:
        page: Flet Page instance
        user: Dictionary containing user data
        on_logout: Callback function for logout action
        
    Returns:
        Container widget with navigation bar
    """
    
    return ft.Container(
        content=ft.Row([
            ft.Row([
                ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE, size=28),
                ft.Text(
                    "User Profile",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE
                )
            ], spacing=10),
            
            ft.Container(expand=True),
            
            ft.IconButton(
                icon=ft.Icons.LOGOUT,
                icon_color=ft.Colors.WHITE,
                tooltip="Logout",
                on_click=lambda e: on_logout()
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=15,
        bgcolor=ft.Colors.BLUE_700,
        border_radius=ft.border_radius.only(bottom_left=10, bottom_right=10)
    )
