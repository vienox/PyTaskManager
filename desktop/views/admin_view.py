import flet as ft
from api_client import APIClient
from components.admin_navbar import create_admin_navbar, create_admin_tabs
from components.user_manager import create_user_manager
from components.admin_task_manager import create_admin_task_manager

def create_admin_view(page: ft.Page, api, user, on_logout):
    """Create admin panel view for managing users and tasks."""
    
    current_view = ft.Ref[str]()
    current_view.current = "users"
    
    users_tab_btn = None
    tasks_tab_btn = None
    content_area = None
    
    users_widget, load_users_callback = create_user_manager(page, api)
    tasks_widget, load_tasks_callback = create_admin_task_manager(page, api)
    
    users_content = ft.Container(
        content=users_widget,
        padding=20,
        expand=True
    )
    
    tasks_content = ft.Container(
        content=tasks_widget,
        expand=True
    )
    
    content_area_widget = ft.Container(
        content=users_content,
        padding=20,
        expand=True
    )
    content_area = content_area_widget
    
    def switch_to_users(e):
        """Switch to users management view."""
        current_view.current = "users"
        load_users_callback()
        update_view()
    
    def switch_to_tasks(e):
        """Switch to tasks management view."""
        current_view.current = "tasks"
        load_tasks_callback()
        update_view()
    
    def update_view():
        """Update view based on current_view selection."""
        if current_view.current == "users":
            content_area_widget.content = users_content
            users_tab_btn_widget.bgcolor = ft.Colors.BLUE_700
            tasks_tab_btn_widget.bgcolor = None
        else:
            content_area_widget.content = tasks_content
            users_tab_btn_widget.bgcolor = None
            tasks_tab_btn_widget.bgcolor = ft.Colors.BLUE_700
        page.update()
    
    load_users_callback()
    
    navbar = create_admin_navbar(page, user, on_logout, switch_to_users, switch_to_tasks)
    tabs_container, users_tab_btn_widget, tasks_tab_btn_widget = create_admin_tabs(
        switch_to_users, 
        switch_to_tasks, 
        current_view.current
    )
    
    return ft.Column([
        navbar,
        tabs_container,
        content_area_widget
    ], spacing=0)