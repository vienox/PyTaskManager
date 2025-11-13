import flet as ft
from views.ui.components import navbar


def create_admin_view(page, api, user, on_logout):
    from views.admin.users import user_manager
    from views.admin.tasks import task_manager
    
    current_tab = "users"
    users_widget, load_users = user_manager(page, api)
    tasks_widget, load_tasks = task_manager(page, api)
    
    content_area = ft.Container(content=users_widget, padding=20, expand=True)
    
    def switch_to_users(e):
        nonlocal current_tab
        current_tab = "users"
        content_area.content = users_widget
        users_btn.bgcolor = ft.Colors.BLUE_700
        tasks_btn.bgcolor = None
        load_users()
        page.update()
    
    def switch_to_tasks(e):
        nonlocal current_tab
        current_tab = "tasks"
        content_area.content = tasks_widget
        users_btn.bgcolor = None
        tasks_btn.bgcolor = ft.Colors.BLUE_700
        load_tasks()
        page.update()
    
    users_btn = ft.ElevatedButton("Users", icon=ft.Icons.PEOPLE, on_click=switch_to_users, bgcolor=ft.Colors.BLUE_700)
    tasks_btn = ft.ElevatedButton("Tasks", icon=ft.Icons.TASK, on_click=switch_to_tasks)
    
    load_users()
    
    return ft.Column([
        navbar(page, user, on_logout, "Admin Panel"),
        ft.Container(content=ft.Row([users_btn, tasks_btn], spacing=10), padding=10, bgcolor=ft.Colors.BLUE_50),
        content_area
    ], spacing=0)
