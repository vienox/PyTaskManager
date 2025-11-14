import flet as ft
from views.ui.components import navbar


def create_user_view(page, api, user, on_logout):
    total = ft.Text("0", size=32, weight=ft.FontWeight.BOLD)
    completed = ft.Text("0", size=32, weight=ft.FontWeight.BOLD)
    pending = ft.Text("0", size=32, weight=ft.FontWeight.BOLD)
    
    def load_stats():
        try:
            tasks = api.get_tasks()
            total.value = str(len(tasks))
            completed.value = str(sum(1 for t in tasks if t["completed"]))
            pending.value = str(sum(1 for t in tasks if not t["completed"]))
            page.update()
        except:
            pass
    
    def go_to_tasks(e):
        from views.user.tasks import create_tasks_view
        page.controls.clear()
        page.add(create_tasks_view(page, api, user, on_logout, lambda: (page.controls.clear(), page.add(create_user_view(page, api, user, on_logout)), page.update())))
        page.update()
    
    load_stats()
    
    return ft.Column([
        navbar(page, user, on_logout, "Profile"),
        ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=100, color=ft.Colors.BLUE),
                ft.Text(user["username"], size=28, weight=ft.FontWeight.BOLD),
                ft.Text(user["email"], size=14, color=ft.Colors.GREY),
                ft.Divider(height=40),
                ft.Row([
                    ft.Container(ft.Column([ft.Icon(ft.Icons.TASK, size=40, color=ft.Colors.BLUE), total, ft.Text("Total", size=12, color=ft.Colors.GREY)], horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=20, bgcolor=ft.Colors.BLUE_50, border_radius=10, expand=True),
                    ft.Container(ft.Column([ft.Icon(ft.Icons.CHECK_CIRCLE, size=40, color=ft.Colors.GREEN), completed, ft.Text("Completed", size=12, color=ft.Colors.GREY)], horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=20, bgcolor=ft.Colors.GREEN_50, border_radius=10, expand=True),
                    ft.Container(ft.Column([ft.Icon(ft.Icons.PENDING, size=40, color=ft.Colors.ORANGE), pending, ft.Text("Pending", size=12, color=ft.Colors.GREY)], horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=20, bgcolor=ft.Colors.ORANGE_50, border_radius=10, expand=True)
                ], spacing=20),
                ft.Container(height=30),
                ft.ElevatedButton("Manage Tasks", on_click=go_to_tasks, width=300, height=50)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=40,
            alignment=ft.alignment.center,
            expand=True
        )
    ], expand=True)
