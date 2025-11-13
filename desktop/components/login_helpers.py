"""
Helper functions and components for login view.

This module separates login logic from UI presentation for better maintainability.
"""

import flet as ft
from typing import Callable, Optional


def create_login_form_fields() -> tuple:
    """
    Create login form input fields.
    
    Returns:
        tuple: (username_field, password_field, error_text, loading_indicator)
    """
    username_field = ft.TextField(
        label="Username",
        width=300,
        autofocus=True,
        prefix_icon=ft.Icons.PERSON
    )
    
    password_field = ft.TextField(
        label="Password",
        password=True,
        width=300,
        prefix_icon=ft.Icons.LOCK,
        can_reveal_password=True
    )
    
    error_text = ft.Text(color="red", size=12)
    loading = ft.ProgressRing(visible=False, width=30, height=30)
    
    return username_field, password_field, error_text, loading


def create_login_handler(
    page: ft.Page,
    api: 'APIClient',
    username_field: ft.TextField,
    password_field: ft.TextField,
    error_text: ft.Text,
    loading: ft.ProgressRing,
    on_success: Callable
) -> Callable:
    """
    Create login button click handler.
    
    Args:
        page: Flet Page instance
        api: API client instance
        username_field: Username TextField
        password_field: Password TextField
        error_text: Error Text component
        loading: Loading ProgressRing
        on_success: Callback(user) called on successful login
        
    Returns:
        callable: Login click handler function
    """
    
    def login_click(e):
        # Validate inputs
        if not username_field.value or not password_field.value:
            error_text.value = "Please fill in all fields"
            page.update()
            return
        
        # Show loading state
        loading.visible = True
        error_text.value = ""
        page.update()
        
        try:
            # Authenticate via API
            api.login(username_field.value, password_field.value)
            
            # Fetch user data
            user = api.get_me()
            
            # Call success callback
            on_success(user)
            
        except Exception as err:
            loading.visible = False
            error_msg = str(err)
            
            # Parse error and show user-friendly message
            if "404" in error_msg or "User not found" in error_msg:
                error_text.value = f"User '{username_field.value}' not found"
            elif "401" in error_msg or "Invalid password" in error_msg:
                error_text.value = "Invalid password"
            elif "500" in error_msg:
                error_text.value = "Server error. Please check if backend is running."
            else:
                error_text.value = f"Login failed: {error_msg}"
            
            page.update()
    
    return login_click


def create_keyboard_handler(login_handler: Callable) -> Callable:
    """
    Create keyboard event handler for Enter key login.
    
    Args:
        login_handler: Login click handler function
        
    Returns:
        callable: Keyboard event handler
    """
    def on_key_press(e: ft.KeyboardEvent):
        if e.key == "Enter":
            login_handler(None)
    
    return on_key_press


def create_login_layout(
    username_field: ft.TextField,
    password_field: ft.TextField,
    login_button: ft.ElevatedButton,
    loading: ft.ProgressRing,
    error_text: ft.Text
) -> ft.Container:
    """
    Create the main login screen layout.
    
    Args:
        username_field: Username TextField
        password_field: Password TextField
        login_button: Login button
        loading: Loading indicator
        error_text: Error Text component
        
    Returns:
        ft.Container: Complete login screen layout
    """
    return ft.Container(
        content=ft.Column([
            ft.Container(height=50),  # Top spacer
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
            login_button,
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
        )
    )
