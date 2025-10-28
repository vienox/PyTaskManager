import flet as ft


def create_user_stats(page: ft.Page, api):
    """
    Create user statistics display component.
    
    Args:
        page: Flet Page instance
        api: APIClient instance
        
    Returns:
        Tuple of (widget, load_stats_callback)
    """
    
    total_tasks = ft.Text("0", size=32, weight=ft.FontWeight.BOLD)
    completed_tasks = ft.Text("0", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN)
    pending_tasks = ft.Text("0", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE)
    
    def load_stats():
        """Calculate and display task statistics."""
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
            print(f"Stats error: {e}")
    
    widget = ft.Row([
        ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.TASK, size=40, color=ft.Colors.BLUE),
                total_tasks,
                ft.Text("Total", size=12, color=ft.Colors.GREY)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=10,
            expand=True
        ),
        
        ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.CHECK_CIRCLE, size=40, color=ft.Colors.GREEN),
                completed_tasks,
                ft.Text("Completed", size=12, color=ft.Colors.GREY)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            bgcolor=ft.Colors.GREEN_50,
            border_radius=10,
            expand=True
        ),
        
        ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.PENDING, size=40, color=ft.Colors.ORANGE),
                pending_tasks,
                ft.Text("Pending", size=12, color=ft.Colors.GREY)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            bgcolor=ft.Colors.ORANGE_50,
            border_radius=10,
            expand=True
        ),
    ], spacing=10)
    
    return widget, load_stats
