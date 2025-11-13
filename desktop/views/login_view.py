"""
Login view for the Task Manager Desktop application.

This module handles user authentication via the API client.
Uses modular components from desktop.components.login_helpers.
"""

import flet as ft
from api_client import APIClient
from components.login_helpers import (
    create_login_form_fields,
    create_login_handler,
    create_keyboard_handler,
    create_login_layout
)


def create_login_view(page: ft.Page, api: APIClient, on_login_success):
    """
    Create the login view.
    
    Args:
        page: The Flet Page instance for UI rendering.
        api: API client instance for authentication.
        on_login_success: Callback function(user) called when login succeeds.
    
    Returns:
        ft.Container: The complete login view container.
    """
    
    # Create form fields using helper
    username_field, password_field, error_text, loading = create_login_form_fields()

    # Create login handler
    login_handler = create_login_handler(
        page=page,
        api=api,
        username_field=username_field,
        password_field=password_field,
        error_text=error_text,
        loading=loading,
        on_success=on_login_success
    )

    # Create login button
    login_button = ft.ElevatedButton(
        text="Log In",
        width=300,
        height=45,
        on_click=login_handler,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )

    # Set up keyboard handler for Enter key
    page.on_keyboard_event = create_keyboard_handler(login_handler)

    # Create and return layout
    return create_login_layout(
        username_field=username_field,
        password_field=password_field,
        login_button=login_button,
        loading=loading,
        error_text=error_text
    )