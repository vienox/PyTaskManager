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
<<<<<<< HEAD
    Create the login view.
    
    Args:
        page: The Flet Page instance for UI rendering.
        api: API client instance for authentication.
        on_login_success: Callback function(user) called when login succeeds.
    
    Returns:
        ft.Container: The complete login view container.
=======
    Create login view with authentication form.
    
    Args:
        page: Flet Page instance
        api: APIClient instance
        on_login_success: Callback function called with user data on successful login
>>>>>>> 6124b066d07b1027ac1e7848f2c94c660b46e332
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
<<<<<<< HEAD
        height=45,
        on_click=login_handler,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10)
=======
        prefix_icon=ft.Icons.LOCK,
        can_reveal_password=True
    )
    
    error_text = ft.Text(color="red", size=12)
    loading = ft.ProgressRing(visible=False, width=30, height=30)
    
    def login_click(e):
        if not username_field.value or not password_field.value:
            error_text.value = "Please fill in all fields"
            page.update()
            return
        
        loading.visible = True
        error_text.value = ""
        page.update()
        
        try:
            api.login(username_field.value, password_field.value)
            user = api.get_me()
            on_login_success(user)
            
        except Exception as err:
            loading.visible = False
            error_msg = str(err)
            
            if "404" in error_msg or "User not found" in error_msg:
                error_text.value = f"User '{username_field.value}' not found"
            elif "401" in error_msg or "Invalid password" in error_msg:
                error_text.value = "Invalid password"
            elif "500" in error_msg:
                error_text.value = "Server error. Please check if backend is running."
            else:
                error_text.value = f"Login error: {error_msg}"
            
            page.update()
    
    def on_key_press(e: ft.KeyboardEvent):
        if e.key == "Enter":
            login_click(None)
    
    page.on_keyboard_event = on_key_press
    
    return ft.Container(
        content=ft.Column([
            ft.Container(height=50),
            ft.Icon(ft.Icons.TASK_ALT, size=80, color=ft.Colors.BLUE),
            ft.Text(
                "Task Manager",
                size=32,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Text(
                "Log in to continue",
                size=14,
                color=ft.Colors.GREY,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Container(height=30),
            username_field,
            password_field,
            ft.Container(height=10),
            ft.ElevatedButton(
                "Log In",
                on_click=login_click,
                width=300,
                height=45,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10)
                )
            ),
            loading,
            error_text,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center,
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#e3f2fd", "#ffffff"]
>>>>>>> 6124b066d07b1027ac1e7848f2c94c660b46e332
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