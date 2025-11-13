"""
User profile view for regular (non-admin) users.

Displays user information and task statistics with navigation to tasks view.
Main orchestrator that assembles components from profile_components and stats_manager.
"""

import flet as ft
from components.nav_bar import create_nav_bar
from .profile_components import (
    create_profile_header,
    create_stats_row,
    create_manage_tasks_button,
    create_user_profile_layout
)
from .stats_manager import create_stats_loader


def create_user_view(page: ft.Page, api, user, on_logout):
    """
    Create user profile view.
    
    Displays:
    - User avatar, username, and email
    - Task statistics (total, completed, pending)
    - Button to navigate to tasks management
    
    Args:
        page: Flet Page instance for UI rendering.
        api: API client instance for fetching data.
        user: Dict with user data (username, email, is_admin).
        on_logout: Callback function called when user logs out.
    
    Returns:
        ft.Column: The complete user profile view.
    """
    
    # Create stat text components (will be updated by loader)
    total_tasks = ft.Text("0", size=32, weight=ft.FontWeight.BOLD)
    completed_tasks = ft.Text("0", size=32, weight=ft.FontWeight.BOLD)
    pending_tasks = ft.Text("0", size=32, weight=ft.FontWeight.BOLD)
    
    # Create stats loader function
    load_stats = create_stats_loader(api, total_tasks, completed_tasks, pending_tasks, page)
    
    def go_to_tasks(e):
        """Navigate to tasks management view."""
        from views.tasks_view import create_tasks_view
        page.controls.clear()
        
        def back_to_profile():
            """Return to profile view."""
            page.controls.clear()
            page.add(create_user_view(page, api, user, on_logout))
            page.update()
        
        page.add(create_tasks_view(page, api, user, on_logout, on_back_to_profile=back_to_profile))
        page.update()
    
    # Create components
    navbar = create_nav_bar(
        page=page,
        title="User Profile",
        current_user=user,
        on_logout=on_logout
    )
    
    profile_header = create_profile_header(user)
    stats_row = create_stats_row(total_tasks, completed_tasks, pending_tasks)
    manage_button = create_manage_tasks_button(go_to_tasks)
    
    # Assemble layout
    view = create_user_profile_layout(navbar, profile_header, stats_row, manage_button)
    
    # Load statistics on view creation
    load_stats()
    
    return view