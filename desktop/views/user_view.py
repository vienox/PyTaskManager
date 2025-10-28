import flet as ft
from components.user_navbar import create_user_navbar
from components.user_stats import create_user_stats

def create_user_view(page: ft.Page, api, user, on_logout):
    """
    Uproszczony widok dla zwykłego użytkownika
    Wyświetla jego dane + podstawowe statystyki tasków
    
    Args:
        page: Flet Page
        api: APIClient instance
        user: dict z danymi usera
        on_logout: callback wylogowania
    """
    
    # Komponent statystyk
    stats_widget, load_stats_callback = create_user_stats(page, api)
    
    def go_to_tasks(e):
        """Przejdź do widoku tasków"""
        from views.tasks_view import create_tasks_view
        page.controls.clear()
        
        # Funkcja powrotu do profilu
        def back_to_profile():
            page.controls.clear()
            page.add(create_user_view(page, api, user, on_logout))
            page.update()
        
        page.add(create_tasks_view(page, api, user, on_logout, on_back_to_profile=back_to_profile))
        page.update()
    
    # ========== MAIN VIEW ==========
    # Navbar
    navbar = create_user_navbar(page, user, on_logout)
    
    view = ft.Column([
        navbar,
        
        ft.Container(
            content=ft.Column([
                # Avatar
                ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=100, color=ft.Colors.BLUE),
                
                # User info
                ft.Text(user["username"], size=28, weight=ft.FontWeight.BOLD),
                ft.Text(user["email"], size=14, color=ft.Colors.GREY),
                
                ft.Divider(height=40),
                
                # Stats cards
                stats_widget,
                
                ft.Container(height=30),
                
                # Action button
                ft.ElevatedButton(
                    "Zarządzaj Taskami",
                    on_click=go_to_tasks,
                    width=300,
                    height=50,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10)
                    )
                ),
                
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=40,
            alignment=ft.alignment.center,
            expand=True
        )
    ], expand=True)
    
    # Load stats
    load_stats_callback()
    
    return view