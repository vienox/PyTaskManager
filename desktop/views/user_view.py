import flet as ft

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
    
    # Stats
    total_tasks = ft.Text("0", size=32, weight=ft.FontWeight.BOLD)
    completed_tasks = ft.Text("0", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN)
    pending_tasks = ft.Text("0", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE)
    
    def load_stats():
        """Oblicz statystyki tasków"""
        try:
            tasks = api.get_tasks()
            total = len(tasks)
            completed = len([t for t in tasks if t["completed"]])
            pending = total - completed
            
            total_tasks.value = str(total)
            completed_tasks.value = str(completed)
            pending_tasks.value = str(pending)
            
            page.update()
        except Exception as e:
            print(f"Błąd stats: {e}")
    
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
    # Navbar - zamiast AppBar
    navbar = ft.Container(
        content=ft.Row([
            # Tytuł
            ft.Row([
                ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE, size=28),
                ft.Text("Profil Użytkownika", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
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
                ft.Row([
                    # Total tasks
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.TASK, size=40, color=ft.Colors.BLUE),
                            total_tasks,
                            ft.Text("Wszystkie", size=12, color=ft.Colors.GREY)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=20,
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=10,
                        expand=True
                    ),
                    
                    # Completed
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.CHECK_CIRCLE, size=40, color=ft.Colors.GREEN),
                            completed_tasks,
                            ft.Text("Ukończone", size=12, color=ft.Colors.GREY)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=20,
                        bgcolor=ft.Colors.GREEN_50,
                        border_radius=10,
                        expand=True
                    ),
                    
                    # Pending
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.PENDING, size=40, color=ft.Colors.ORANGE),
                            pending_tasks,
                            ft.Text("Do zrobienia", size=12, color=ft.Colors.GREY)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=20,
                        bgcolor=ft.Colors.ORANGE_50,
                        border_radius=10,
                        expand=True
                    ),
                ], spacing=10),
                
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
    load_stats()
    
    return view