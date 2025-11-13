"""
Reusable UI components and utilities.

This module provides common UI elements like empty states, loading indicators,
error displays, and statistics cards.
"""

import flet as ft


def create_empty_state(
    icon: str = ft.Icons.INBOX,
    message: str = "No items found",
    icon_size: int = 100,
    icon_color: str = None
) -> ft.Container:
    """
    Create an empty state display.
    
    Args:
        icon: Icon to display (ft.Icons constant)
        message: Message to show
        icon_size: Size of the icon (default: 100)
        icon_color: Color of the icon (default: grey)
        
    Returns:
        ft.Container: Empty state component
    """
    return ft.Container(
        content=ft.Column([
            ft.Icon(
                icon,
                size=icon_size,
                color=icon_color or ft.Colors.GREY_400
            ),
            ft.Text(
                message,
                size=20,
                color=ft.Colors.GREY_600
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        alignment=ft.alignment.center,
        expand=True,
        padding=40
    )


def create_loading_indicator(message: str = "Loading...") -> ft.Container:
    """
    Create a loading indicator with optional message.
    
    Args:
        message: Loading message to display
        
    Returns:
        ft.Container: Loading indicator component
    """
    return ft.Container(
        content=ft.Column([
            ft.ProgressRing(),
            ft.Text(message, color=ft.Colors.GREY_600)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
        alignment=ft.alignment.center,
        expand=True
    )


def create_error_display(error_message: str, retry_callback: callable = None) -> ft.Container:
    """
    Create an error display with optional retry button.
    
    Args:
        error_message: Error message to display
        retry_callback: Callback for retry button (optional)
        
    Returns:
        ft.Container: Error display component
    """
    components = [
        ft.Icon(ft.Icons.ERROR_OUTLINE, size=80, color=ft.Colors.RED_400),
        ft.Text(error_message, color=ft.Colors.RED_600, text_align=ft.TextAlign.CENTER)
    ]
    
    if retry_callback:
        components.append(
            ft.ElevatedButton(
                "Retry",
                icon=ft.Icons.REFRESH,
                on_click=retry_callback
            )
        )
    
    return ft.Container(
        content=ft.Column(
            components,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),
        alignment=ft.alignment.center,
        expand=True,
        padding=40
    )


def create_stat_card(
    title: str,
    value: str,
    icon: str,
    color: str = None,
    bgcolor: str = None
) -> ft.Container:
    """
    Create a statistics card.
    
    Args:
        title: Card title (e.g., "Total Tasks")
        value: Value to display (e.g., "24")
        icon: Icon to display (ft.Icons constant)
        color: Icon and value color
        bgcolor: Background color
        
    Returns:
        ft.Container: Statistics card component
    """
    return ft.Container(
        content=ft.Column([
            ft.Icon(icon, size=40, color=color or ft.Colors.BLUE),
            ft.Text(
                value,
                size=32,
                weight=ft.FontWeight.BOLD,
                color=color or ft.Colors.BLACK
            ),
            ft.Text(
                title,
                size=12,
                color=ft.Colors.GREY
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=20,
        bgcolor=bgcolor or ft.Colors.BLUE_50,
        border_radius=10,
        expand=True
    )


def create_search_bar(
    on_change: callable,
    on_clear: callable = None,
    hint_text: str = "Search...",
    width: int = 300
) -> ft.Row:
    """
    Create a search bar with clear button.
    
    Args:
        on_change: Callback when search text changes
        on_clear: Callback when clear button clicked (optional)
        hint_text: Placeholder text
        width: Width of the search field
        
    Returns:
        ft.Row: Search bar component with field and clear button
    """
    search_field = ft.TextField(
        hint_text=hint_text,
        prefix_icon=ft.Icons.SEARCH,
        on_change=on_change,
        width=width,
        height=40,
        text_size=14
    )
    
    def handle_clear(e):
        search_field.value = ""
        if on_clear:
            on_clear(e)
    
    return ft.Row([
        search_field,
        ft.IconButton(
            icon=ft.Icons.CLEAR,
            tooltip="Clear search",
            on_click=handle_clear
        )
    ], spacing=5)


def create_scrollable_container(
    content: ft.Control,
    height: int = 500,
    bgcolor: str = "#E3F2FD",
    padding: int = 10
) -> ft.Container:
    """
    Create a scrollable container with fixed height.
    
    IMPORTANT: Flet requires fixed height for scrolling to work properly.
    
    Args:
        content: Content to make scrollable (usually ft.Column)
        height: Fixed height in pixels (required for scrolling)
        bgcolor: Background color
        padding: Container padding
        
    Returns:
        ft.Container: Scrollable container
    """
    return ft.Container(
        content=content,
        height=height,
        padding=padding,
        bgcolor=bgcolor,
        border_radius=10
    )


def create_user_avatar(
    username: str,
    is_admin: bool = False,
    size: int = 40
) -> ft.Container:
    """
    Create a user avatar with initials.
    
    Args:
        username: Username to extract initials from
        is_admin: Whether user is admin (affects color)
        size: Avatar size
        
    Returns:
        ft.Container: User avatar component
    """
    # Get initials (first 2 letters of username)
    initials = username[:2].upper() if username else "?"
    
    return ft.Container(
        content=ft.Text(
            initials,
            size=size // 2,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE
        ),
        width=size,
        height=size,
        bgcolor=ft.Colors.AMBER if is_admin else ft.Colors.BLUE,
        border_radius=size // 2,
        alignment=ft.alignment.center
    )


class Colors:
    """Predefined color constants (HEX format for Flet reliability)."""
    
    # Primary colors
    PRIMARY = "#1976D2"
    PRIMARY_LIGHT = "#E3F2FD"
    PRIMARY_DARK = "#0D47A1"
    
    # Status colors
    SUCCESS = "#4CAF50"
    SUCCESS_LIGHT = "#E8F5E9"
    WARNING = "#FF9800"
    WARNING_LIGHT = "#FFF3E0"
    ERROR = "#F44336"
    ERROR_LIGHT = "#FFEBEE"
    
    # UI colors
    BACKGROUND = "#FFFFFF"
    SURFACE = "#F5F5F5"
    TEXT_PRIMARY = "#212121"
    TEXT_SECONDARY = "#757575"
    DIVIDER = "#BDBDBD"
    
    # Admin colors
    ADMIN = "#FFC107"
    ADMIN_LIGHT = "#FFF8E1"


class Spacing:
    """Predefined spacing constants."""
    
    XS = 4
    SM = 8
    MD = 16
    LG = 24
    XL = 32
    XXL = 48
