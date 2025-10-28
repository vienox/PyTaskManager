import flet as ft


def create_user_stats(page: ft.Page, api):
    """
    Komponent wyświetlający statystyki użytkownika
    
    Args:
        page: Flet Page
        api: APIClient instance
        
    Returns:
        tuple: (widget, load_stats_callback)
    """
    
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
    
    # Widget statystyk
    widget = ft.Row([
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
    ], spacing=10)
    
    return widget, load_stats
