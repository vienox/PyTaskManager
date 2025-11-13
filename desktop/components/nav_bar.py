"""
Navigation bar component for desktop application.

This module provides reusable navigation bar components with user information,
menu buttons, and logout functionality.
"""

import flet as ft
from typing import Optional, Callable


def create_nav_bar(
    page: ft.Page,
    current_user: dict,
    on_logout: Callable,
    title: str = "Task Manager",
    show_home: bool = False,
    on_home: Optional[Callable] = None
) -> ft.Container:
    """
    Create a navigation bar with user info and actions.
    
    Features:
        - App title/logo
        - Optional home button
        - User avatar with role indicator
        - Logout button
    
    Args:
        page: Flet Page instance
        current_user: User dict with keys: username, is_admin
        on_logout: Callback when logout button clicked
        title: Application title to display (default: "Task Manager")
        show_home: Whether to show home/back button
        on_home: Callback when home button clicked (required if show_home=True)
        
    Returns:
        ft.Container: Navigation bar component
        
    Example:
        >>> navbar = create_nav_bar(
        ...     page=page,
        ...     current_user={"username": "john_doe", "is_admin": False},
        ...     on_logout=handle_logout,
        ...     show_home=True,
        ...     on_home=go_to_profile
        ... )
    """
    
    # Left side: Logo + Title (+ optional home button)
    left_section = []
    
    if show_home and on_home:
        left_section.append(
            ft.IconButton(
                icon=ft.Icons.HOME,
                icon_color=ft.Colors.WHITE,
                tooltip="Back to profile",
                on_click=lambda e: on_home()
            )
        )
    
    left_section.extend([
        ft.Icon(ft.Icons.TASK_ALT, color=ft.Colors.WHITE, size=28),
        ft.Text(
            title,
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE
        )
    ])
    
    # Right side: User info + Logout
    user_icon_color = ft.Colors.AMBER_200 if current_user.get("is_admin") else ft.Colors.WHITE
    user_icon = ft.Icons.ADMIN_PANEL_SETTINGS if current_user.get("is_admin") else ft.Icons.PERSON
    
    right_section = ft.Container(
        content=ft.Row([
            ft.Icon(
                user_icon,
                color=user_icon_color,
                size=20
            ),
            ft.Text(
                current_user.get("username", "User"),
                color=ft.Colors.WHITE,
                weight=ft.FontWeight.W_500
            ),
            ft.IconButton(
                icon=ft.Icons.LOGOUT,
                icon_color=ft.Colors.WHITE,
                tooltip="Logout",
                on_click=lambda e: on_logout()
            )
        ], spacing=10),
        padding=ft.padding.only(left=20)
    )
    
    return ft.Container(
        content=ft.Row([
            ft.Row(left_section, spacing=10),
            ft.Container(expand=True),  # Spacer
            right_section
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=15,
        bgcolor=ft.Colors.BLUE_700,
        border_radius=ft.border_radius.only(bottom_left=10, bottom_right=10)
    )


def create_simple_nav_bar(
    title: str = "Task Manager",
    subtitle: Optional[str] = None,
    show_back: bool = False,
    on_back: Optional[Callable] = None
) -> ft.Container:
    """
    Create a simple navigation bar with minimal elements.
    
    Used for login screen and other standalone pages.
    
    Args:
        title: Main title text
        subtitle: Optional subtitle text
        show_back: Whether to show back button
        on_back: Callback when back button clicked (required if show_back=True)
        
    Returns:
        ft.Container: Simple navigation bar component
    """
    
    left_section = []
    
    if show_back and on_back:
        left_section.append(
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color=ft.Colors.WHITE,
                tooltip="Go back",
                on_click=lambda e: on_back()
            )
        )
    
    left_section.extend([
        ft.Icon(ft.Icons.TASK_ALT, color=ft.Colors.WHITE, size=28),
        ft.Column([
            ft.Text(
                title,
                size=20,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE
            ),
            ft.Text(
                subtitle,
                size=12,
                color=ft.Colors.WHITE70
            ) if subtitle else ft.Container()
        ], spacing=0)
    ])
    
    return ft.Container(
        content=ft.Row(left_section, spacing=10),
        padding=15,
        bgcolor=ft.Colors.BLUE_700,
        border_radius=ft.border_radius.only(bottom_left=10, bottom_right=10)
    )
