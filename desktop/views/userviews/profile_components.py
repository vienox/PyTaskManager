"""
Profile UI components for user view.

Separates profile display logic from main view orchestration.
"""

import flet as ft
from typing import Dict


def create_profile_header(user: Dict) -> ft.Column:
    """
    Create user profile header with avatar and info.
    
    Args:
        user: User data dict with username and email
        
    Returns:
        ft.Column: Profile header component
    """
    return ft.Column([
        ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=100, color=ft.Colors.BLUE),
        ft.Text(user["username"], size=28, weight=ft.FontWeight.BOLD),
        ft.Text(user["email"], size=14, color=ft.Colors.GREY_600),
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
        ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.TASK, size=40, color=ft.Colors.BLUE),
                total_text,
                ft.Text("All Tasks", size=12, color=ft.Colors.GREY)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=10,
            expand=True
        ),
        ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.CHECK_CIRCLE, size=40, color=ft.Colors.GREEN),
                completed_text,
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
                pending_text,
                ft.Text("Pending", size=12, color=ft.Colors.GREY)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            bgcolor=ft.Colors.ORANGE_50,
            border_radius=10,
            expand=True
        )
    ], spacing=10)


def create_manage_tasks_button(on_click) -> ft.ElevatedButton:
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
