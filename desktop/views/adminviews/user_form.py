"""
User creation form dialog for admin panel.
"""

import flet as ft


def validate_email(email):
    """Validate email format."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def create_user_form_dialog(page, api, on_user_created):
    """
    Create user form dialog.
    
    Args:
        page: Flet Page instance
        api: API client
        on_user_created: Callback function called after user creation
        
    Returns:
        tuple: (dialog widget, show_dialog function)
    """
    
    # Form fields
    new_username = ft.TextField(
        label="Username *",
        autofocus=True,
        hint_text="Min. 3 characters",
        counter_text="",
    )
    
    new_email = ft.TextField(
        label="Email *",
        hint_text="example@email.com",
        keyboard_type=ft.KeyboardType.EMAIL,
    )
    
    new_password = ft.TextField(
        label="Password *",
        password=True,
        can_reveal_password=True,
        hint_text="Min. 6 characters",
    )
    
    error_text = ft.Text("", color=ft.Colors.RED, size=12)
    
    def validate_username_field(e=None):
        """Validate username field in real-time."""
        if new_username.value and len(new_username.value) < 3:
            new_username.error_text = "Min. 3 characters"
        else:
            new_username.error_text = None
        page.update()
    
    def validate_email_field(e=None):
        """Validate email field in real-time."""
        if new_email.value and not validate_email(new_email.value):
            new_email.error_text = "Invalid email format"
        else:
            new_email.error_text = None
        page.update()
    
    def validate_password_field(e=None):
        """Validate password field in real-time."""
        if new_password.value and len(new_password.value) < 6:
            new_password.error_text = "Min. 6 characters"
        else:
            new_password.error_text = None
        page.update()
    
    # Attach validators
    new_username.on_change = validate_username_field
    new_email.on_change = validate_email_field
    new_password.on_change = validate_password_field
    
    def create_user_submit(e):
        """Submit user creation form."""
        error_text.value = ""
        
        # Validate fields
        if not new_username.value or not new_email.value or not new_password.value:
            error_text.value = "All fields are required"
            page.update()
            return
        
        if len(new_username.value) < 3:
            error_text.value = "Username must be at least 3 characters"
            new_username.error_text = "Min. 3 characters"
            page.update()
            return
        
        if not validate_email(new_email.value):
            error_text.value = "Invalid email format"
            new_email.error_text = "Invalid format"
            page.update()
            return
        
        if len(new_password.value) < 6:
            error_text.value = "Password must be at least 6 characters"
            new_password.error_text = "Min. 6 characters"
            page.update()
            return
        
        try:
            api.create_user(
                username=new_username.value,
                email=new_email.value,
                password=new_password.value
            )
            dialog.open = False
            
            # Clear fields
            new_username.value = ""
            new_email.value = ""
            new_password.value = ""
            new_username.error_text = None
            new_email.error_text = None
            new_password.error_text = None
            
            page.update()
            
            # Callback to refresh users list
            if on_user_created:
                on_user_created()
                
        except Exception as ex:
            error_msg = str(ex)
            
            if "Username already exists" in error_msg or "username" in error_msg.lower():
                error_text.value = f"Username '{new_username.value}' already exists"
                new_username.error_text = "Username taken"
            elif "Email already exists" in error_msg or "email" in error_msg.lower():
                error_text.value = f"Email '{new_email.value}' is already registered"
                new_email.error_text = "Email taken"
            elif "400" in error_msg:
                error_text.value = "Invalid data. Check all fields."
            elif "401" in error_msg or "403" in error_msg:
                error_text.value = "No permission. Please login again."
            elif "500" in error_msg:
                error_text.value = "Server error. Try again later."
            else:
                error_text.value = f"Error: {error_msg}"
            
            page.update()
    
    # Dialog
    dialog = ft.AlertDialog(
        title=ft.Text("Add New User"),
        content=ft.Container(
            content=ft.Column([
                new_username,
                new_email,
                new_password,
                error_text
            ], tight=True, spacing=10),
            width=400
        ),
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: setattr(dialog, 'open', False) or page.update()),
            ft.ElevatedButton("Add", on_click=create_user_submit)
        ]
    )
    
    def show_dialog(e=None):
        """Show the user creation dialog."""
        error_text.value = ""
        new_username.value = ""
        new_email.value = ""
        new_password.value = ""
        new_username.error_text = None
        new_email.error_text = None
        new_password.error_text = None
        dialog.open = True
        page.update()
    
    page.overlay.append(dialog)
    
    return dialog, show_dialog
