"""
Reusable dialog components for the desktop application.

This module provides pre-configured AlertDialog components for common operations
like adding/editing tasks, confirming deletions, and displaying errors.
"""

import flet as ft


class TaskDialog:
    """Factory for task-related dialog components."""
    
    @staticmethod
    def create_add_dialog(
        page: ft.Page,
        title_field: ft.TextField,
        desc_field: ft.TextField,
        error_text: ft.Text,
        on_submit: callable,
        on_cancel: callable = None
    ) -> ft.AlertDialog:
        """
        Create a dialog for adding new tasks.
        
        Args:
            page: Flet Page instance
            title_field: TextField for task title
            desc_field: TextField for task description
            error_text: Text component for error messages
            on_submit: Callback when submit button clicked
            on_cancel: Callback when cancel button clicked (optional)
            
        Returns:
            ft.AlertDialog: Configured add task dialog
        """
        def handle_cancel(e):
            if on_cancel:
                on_cancel(e)
            else:
                dialog.open = False
                page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Add New Task"),
            content=ft.Container(
                content=ft.Column([
                    title_field,
                    desc_field,
                    error_text
                ], tight=True, spacing=10),
                width=500
            ),
            actions=[
                ft.TextButton("Cancel", on_click=handle_cancel),
                ft.ElevatedButton("Add", on_click=on_submit)
            ]
        )
        
        return dialog
    
    @staticmethod
    def create_edit_dialog(
        page: ft.Page,
        title_field: ft.TextField,
        desc_field: ft.TextField,
        error_text: ft.Text,
        on_submit: callable,
        on_cancel: callable = None,
        include_completed: bool = False,
        completed_checkbox: ft.Checkbox = None
    ) -> ft.AlertDialog:
        """
        Create a dialog for editing existing tasks.
        
        Args:
            page: Flet Page instance
            title_field: TextField for task title
            desc_field: TextField for task description
            error_text: Text component for error messages
            on_submit: Callback when submit button clicked
            on_cancel: Callback when cancel button clicked (optional)
            include_completed: Whether to include completion checkbox
            completed_checkbox: Checkbox for completion status (required if include_completed=True)
            
        Returns:
            ft.AlertDialog: Configured edit task dialog
        """
        def handle_cancel(e):
            if on_cancel:
                on_cancel(e)
            else:
                dialog.open = False
                page.update()
        
        fields = [title_field, desc_field]
        if include_completed and completed_checkbox:
            fields.append(completed_checkbox)
        fields.append(error_text)
        
        dialog = ft.AlertDialog(
            title=ft.Text("Edit Task"),
            content=ft.Container(
                content=ft.Column(fields, tight=True, spacing=10),
                width=500
            ),
            actions=[
                ft.TextButton("Cancel", on_click=handle_cancel),
                ft.ElevatedButton("Save", on_click=on_submit)
            ]
        )
        
        return dialog
    
    @staticmethod
    def create_confirm_dialog(
        page: ft.Page,
        title: str,
        message: str,
        on_confirm: callable,
        on_cancel: callable = None,
        confirm_text: str = "Delete",
        confirm_color: str = None
    ) -> ft.AlertDialog:
        """
        Create a confirmation dialog (e.g., for deletions).
        
        Args:
            page: Flet Page instance
            title: Dialog title
            message: Confirmation message
            on_confirm: Callback when confirmed
            on_cancel: Callback when cancelled (optional)
            confirm_text: Text for confirm button (default: "Delete")
            confirm_color: Background color for confirm button (optional)
            
        Returns:
            ft.AlertDialog: Configured confirmation dialog
        """
        def handle_cancel(e):
            if on_cancel:
                on_cancel(e)
            else:
                dialog.open = False
                page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(message, text_align=ft.TextAlign.CENTER),
            modal=True,
            actions=[
                ft.TextButton("Cancel", on_click=handle_cancel),
                ft.ElevatedButton(
                    confirm_text,
                    on_click=on_confirm,
                    bgcolor=confirm_color or ft.Colors.RED_600,
                    color=ft.Colors.WHITE
                )
            ]
        )
        
        return dialog


class UserDialog:
    """Factory for user-related dialog components."""
    
    @staticmethod
    def create_add_user_dialog(
        page: ft.Page,
        username_field: ft.TextField,
        email_field: ft.TextField,
        password_field: ft.TextField,
        error_text: ft.Text,
        on_submit: callable,
        on_cancel: callable = None
    ) -> ft.AlertDialog:
        """
        Create a dialog for adding new users (admin only).
        
        Args:
            page: Flet Page instance
            username_field: TextField for username
            email_field: TextField for email
            password_field: TextField for password
            error_text: Text component for error messages
            on_submit: Callback when submit button clicked
            on_cancel: Callback when cancel button clicked (optional)
            
        Returns:
            ft.AlertDialog: Configured add user dialog
        """
        def handle_cancel(e):
            if on_cancel:
                on_cancel(e)
            else:
                dialog.open = False
                page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Add New User"),
            content=ft.Container(
                content=ft.Column([
                    username_field,
                    email_field,
                    password_field,
                    error_text
                ], tight=True, spacing=10),
                width=400
            ),
            actions=[
                ft.TextButton("Cancel", on_click=handle_cancel),
                ft.ElevatedButton("Add", on_click=on_submit)
            ]
        )
        
        return dialog
