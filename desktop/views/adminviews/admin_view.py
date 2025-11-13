"""
Admin view - main panel with user and task management.
Refactored into separate components for better maintainability.
"""

import flet as ft
from components.nav_bar import create_nav_bar
from components.admin_task_manager import create_admin_task_manager
from .users_panel import create_users_panel
from .user_form import create_user_form_dialog


def create_admin_view(page: ft.Page, api, user, on_logout):
    """
    Create admin panel view.
    
    Args:
        page: Flet Page instance
        api: API client
        user: Current user dict
        on_logout: Logout callback function
        
    Returns:
        ft.Column: Admin panel view
    """
    
    # State
    users_list = ft.Column(spacing=10, scroll=ft.ScrollMode.ALWAYS, expand=True)
    stats_text = ft.Text("", size=14, color=ft.Colors.GREY)
    search_query = ft.Ref[str]()
    search_query.current = ""
    all_users_cache = []
    
    current_view = ft.Ref[str]()
    current_view.current = "users"
    
    # Create users panel
    users_content, load_users, filter_users = create_users_panel(
        page, api, search_query, all_users_cache, users_list, stats_text
    )
    
    # Create user form dialog
    user_dialog, show_user_dialog = create_user_form_dialog(page, api, load_users)
    
    # Add "Add User" button to users panel
    add_user_btn = ft.ElevatedButton(
        "Add User",
        icon=ft.Icons.PERSON_ADD,
        on_click=show_user_dialog
    )
    
    # Insert button into users_content
    users_content.controls[0].controls.append(add_user_btn)
    
    # Tasks widget
    tasks_widget, load_tasks_callback = create_admin_task_manager(page, api)
    tasks_content = ft.Container(
        content=tasks_widget,
        expand=True
    )
    
    # Content area
    content_area_widget = ft.Container(
        content=users_content,
        padding=20,
        expand=True
    )
    
    # View switching functions
    def switch_to_users(e):
        """Switch to users view."""
        current_view.current = "users"
        load_users()
        update_view()
    
    def switch_to_tasks(e):
        """Switch to tasks view."""
        current_view.current = "tasks"
        load_tasks_callback()
        update_view()
    
    def update_view():
        """Update view based on current_view."""
        if current_view.current == "users":
            content_area_widget.content = users_content
            users_tab_btn.bgcolor = ft.Colors.BLUE_700
            tasks_tab_btn.bgcolor = None
        else:
            content_area_widget.content = tasks_content
            users_tab_btn.bgcolor = None
            tasks_tab_btn.bgcolor = ft.Colors.BLUE_700
        page.update()
    
    # Load users on start
    load_users()
    
    # Tab buttons
    users_tab_btn = ft.ElevatedButton(
        "Users",
        icon=ft.Icons.PEOPLE,
        on_click=switch_to_users,
        bgcolor=ft.Colors.BLUE_700
    )
    
    tasks_tab_btn = ft.ElevatedButton(
        "All Tasks",
        icon=ft.Icons.TASK,
        on_click=switch_to_tasks
    )
    
    # Navbar
    navbar = create_nav_bar(page, user, on_logout=on_logout)
    
    return ft.Column([
        navbar,
        ft.Container(
            content=ft.Row([
                users_tab_btn,
                tasks_tab_btn
            ], spacing=10),
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            bgcolor=ft.Colors.BLUE_50
        ),
        content_area_widget
    ], spacing=0)