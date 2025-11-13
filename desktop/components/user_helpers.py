"""
Helper functions and components for user profile view.

This module separates user profile logic from UI presentation.
"""

import flet as ft
from typing import Callable, Dict, List
from .ui_helpers import create_stat_card, Colors


def create_profile_header(user: Dict) -> ft.Column:
    """
    Create user profile header with avatar and info.
    
    Args:
        user: User data dict with username and email
        
    Returns:
        ft.Column: Profile header component
    """
    return ft.Column([
        ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=100, color=Colors.BLUE),
        ft.Text(user["username"], size=28, weight=ft.FontWeight.BOLD),
        ft.Text(user["email"], size=14, color=Colors.GREY),
        ft.Divider(height=40)
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)


def create_stats_row(
    total_text: ft.Text,
    completed_text: ft.Text,
    pending_text: ft.Text
) -> ft.Row:
    """
    Create task statistics row with three stat cards.
    
    Args:
        total_text: Text component for total count
        completed_text: Text component for completed count
        pending_text: Text component for pending count
        
    Returns:
        ft.Row: Row containing three stat cards
    """
    return ft.Row([
        create_stat_card(
            icon=ft.Icons.TASK,
            value=total_text,
            label="All Tasks",
            color=Colors.BLUE,
            bg_color=Colors.BLUE_LIGHT
        ),
        create_stat_card(
            icon=ft.Icons.CHECK_CIRCLE,
            value=completed_text,
            label="Completed",
            color=Colors.GREEN,
            bg_color=Colors.GREEN_LIGHT
        ),
        create_stat_card(
            icon=ft.Icons.PENDING,
            value=pending_text,
            label="Pending",
            color=Colors.ORANGE,
            bg_color=Colors.ORANGE_LIGHT
        )
    ], spacing=10)


def create_stats_loader(api, total_text: ft.Text, completed_text: ft.Text, pending_text: ft.Text, page: ft.Page) -> Callable:
    """
    Create function to load and update task statistics.
    
    Args:
        api: API client instance
        total_text: Text component for total count
        completed_text: Text component for completed count
        pending_text: Text component for pending count
        page: Flet Page for updates
        
    Returns:
        callable: Function to call for loading stats
    """
    def load_stats():
        """Fetch and display task statistics from API."""
        try:
            tasks = api.get_tasks()
            total = len(tasks)
            completed = len([t for t in tasks if t["completed"]])
            pending = total - completed
            
            total_text.value = str(total)
            completed_text.value = str(completed)
            pending_text.value = str(pending)
            
            page.update()
        except Exception as e:
            print(f"Error loading stats: {e}")
    
    return load_stats


def create_manage_tasks_button(on_click: Callable) -> ft.ElevatedButton:
    """
    Create "Manage Tasks" navigation button.
    
    Args:
        on_click: Click handler callback
        
    Returns:
        ft.ElevatedButton: Styled button component
    """
    return ft.ElevatedButton(
        text="Manage Tasks",
        on_click=on_click,
        width=300,
        height=50,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )


def create_user_profile_layout(
    navbar: ft.Container,
    profile_header: ft.Column,
    stats_row: ft.Row,
    manage_button: ft.ElevatedButton
) -> ft.Column:
    """
    Create the complete user profile view layout.
    
    Args:
        navbar: Navigation bar component
        profile_header: Profile header with avatar and info
        stats_row: Task statistics row
        manage_button: Manage tasks button
        
    Returns:
        ft.Column: Complete profile view layout
    """
    return ft.Column([
        navbar,
        ft.Container(
            content=ft.Column([
                profile_header,
                stats_row,
                ft.Container(height=30),
                manage_button,
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=40,
            alignment=ft.alignment.center,
            expand=True
        )
    ], expand=True)
