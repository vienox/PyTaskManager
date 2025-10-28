import flet as ft


def create_user_manager(page: ft.Page, api):
    """
    Create user management component for administrator.
    Allows adding, viewing, and deleting users.
    
    Args:
        page: Flet Page instance
        api: APIClient instance
        
    Returns:
        Tuple of (widget, load_users_callback)
    """
    
    users_list = ft.Column(spacing=10, scroll=ft.ScrollMode.ALWAYS, expand=True)
    stats_text = ft.Text("", size=14, color=ft.Colors.GREY)
    search_query = ft.Ref[str]()
    search_query.current = ""
    all_users_cache = []
    
    # Form fields for adding user
    new_username = ft.TextField(
        label="Username *",
        autofocus=True,
        hint_text="Min. 3 characters",
        counter_text="",
        on_change=lambda e: validate_username_field()
    )
    new_email = ft.TextField(
        label="Email *",
        hint_text="example@email.com",
        keyboard_type=ft.KeyboardType.EMAIL,
        on_change=lambda e: validate_email_field()
    )
    new_password = ft.TextField(
        label="Password *",
        password=True,
        can_reveal_password=True,
        hint_text="Min. 6 characters",
        on_change=lambda e: validate_password_field()
    )
    error_text = ft.Text("", color=ft.Colors.RED, size=12)
    
    def validate_email(email):
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_username_field():
        """Real-time validation for username field"""
        if new_username.value and len(new_username.value) < 3:
            new_username.error_text = "Min. 3 characters"
        else:
            new_username.error_text = None
        page.update()
    
    def validate_email_field():
        """Real-time validation for email field"""
        if new_email.value and not validate_email(new_email.value):
            new_email.error_text = "Invalid email format"
        else:
            new_email.error_text = None
        page.update()
    
    def validate_password_field():
        """Real-time validation for password field"""
        if new_password.value and len(new_password.value) < 6:
            new_password.error_text = "Min. 6 characters"
        else:
            new_password.error_text = None
        page.update()
    
    def load_users():
        """Load all users"""
        try:
            nonlocal all_users_cache
            all_users = api.get_all_users()
            all_users_cache = all_users
            filter_users()
        except Exception as e:
            print(f"Error loading users: {e}")
            users_list.controls.clear()
            users_list.controls.append(
                ft.Text(f"Error: {str(e)}", color=ft.Colors.RED)
            )
            page.update()
    
    def filter_users():
        """Filter users based on search query"""
        users_list.controls.clear()
        
        query = search_query.current.lower()
        
        if query:
            filtered = [u for u in all_users_cache 
                       if query in u["username"].lower() or query in u["email"].lower()]
        else:
            filtered = all_users_cache
        
        for u in filtered:
            users_list.controls.append(create_user_card(u))
        
        if filtered:
            stats_text.value = f"Showing: {len(filtered)} / {len(all_users_cache)} users"
        else:
            stats_text.value = f"Total users: {len(all_users_cache)}"
            if query:
                users_list.controls.clear()
                users_list.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.SEARCH_OFF, size=60, color=ft.Colors.GREY_400),
                            ft.Text("No users found", color=ft.Colors.GREY_600)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        alignment=ft.alignment.center,
                        padding=40
                    )
                )
        
        page.update()
    
    def search_changed(e):
        """Handle search field changes"""
        search_query.current = e.control.value
        filter_users()
    
    def create_user_card(u):
        """Create user card"""
        return ft.Card(
            content=ft.Container(
                content=ft.Row([
                    ft.Icon(
                        ft.Icons.ADMIN_PANEL_SETTINGS if u["is_admin"] else ft.Icons.PERSON,
                        color=ft.Colors.AMBER if u["is_admin"] else ft.Colors.BLUE
                    ),
                    ft.Column([
                        ft.Text(u["username"], weight=ft.FontWeight.BOLD),
                        ft.Text(u["email"], size=12, color=ft.Colors.GREY)
                    ], spacing=2),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color=ft.Colors.RED,
                        tooltip="Delete",
                        on_click=lambda e: delete_user(u["id"])
                    )
                ]),
                padding=15
            )
        )
    
    def delete_user(user_id):
        """Delete user"""
        try:
            api.delete_user(user_id)
            load_users()
        except Exception as e:
            print(f"Error deleting user: {e}")
    
    def add_user_clicked(e):
        """Open add user dialog"""
        error_text.value = ""
        new_username.value = ""
        new_email.value = ""
        new_password.value = ""
        new_username.error_text = None
        new_email.error_text = None
        new_password.error_text = None
        dialog.open = True
        page.update()
    
    def create_user_submit(e):
        """Create new user with full validation"""
        error_text.value = ""
        
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
            
            new_username.value = ""
            new_email.value = ""
            new_password.value = ""
            new_username.error_text = None
            new_email.error_text = None
            new_password.error_text = None
            
            load_users()
            page.update()
        except Exception as ex:
            error_msg = str(ex)
            
            if "Username already exists" in error_msg or "username" in error_msg.lower():
                error_text.value = f"User '{new_username.value}' already exists"
                new_username.error_text = "Username taken"
            elif "Email already exists" in error_msg or "email" in error_msg.lower():
                error_text.value = f"Email '{new_email.value}' is already registered"
                new_email.error_text = "Email taken"
            elif "400" in error_msg:
                error_text.value = "Invalid data. Please check all fields."
            elif "401" in error_msg or "403" in error_msg:
                error_text.value = "Unauthorized. Please log in again."
            elif "500" in error_msg:
                error_text.value = "Server error. Please try again later."
            else:
                error_text.value = f"Error: {error_msg}"
            
            page.update()

    
    # Add user dialog
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
    
    page.overlay.append(dialog)
    
    # Main widget
    search_field = ft.TextField(
        hint_text="Search users...",
        prefix_icon=ft.Icons.SEARCH,
        on_change=search_changed,
        width=300,
        height=40,
        text_size=14
    )
    
    widget = ft.Column([
        ft.Row([
            ft.Text("User Management", size=20, weight=ft.FontWeight.BOLD),
            ft.Container(expand=True),
            search_field,
            ft.IconButton(
                icon=ft.Icons.CLEAR,
                tooltip="Clear search",
                on_click=lambda e: (
                    setattr(search_field, 'value', ""),
                    setattr(search_query, 'current', ""),
                    filter_users()
                )
            ),
            ft.ElevatedButton(
                "Add User",
                icon=ft.Icons.PERSON_ADD,
                on_click=add_user_clicked
            )
        ]),
        stats_text,
        ft.Divider(),
        ft.Container(
            content=users_list,
            height=650,
            padding=10,
            bgcolor="#E3F2FD",
            border_radius=10
        )
    ], spacing=15)
    
    return widget, load_users
