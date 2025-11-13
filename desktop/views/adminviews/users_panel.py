"""
Users management panel for admin view.
"""

import flet as ft


def create_users_panel(page, api, search_query, all_users_cache, users_list, stats_text):
    """
    Create users management panel.
    
    Args:
        page: Flet Page instance
        api: API client
        search_query: Reference to search query string
        all_users_cache: List to store all users
        users_list: Column widget for users list
        stats_text: Text widget for statistics
        
    Returns:
        tuple: (users_content widget, load_users function, filter_users function)
    """
    
    def load_users():
        """Load all users from API."""
        try:
            all_users = api.get_all_users()
            all_users_cache.clear()
            all_users_cache.extend(all_users)
            filter_users()
        except Exception as e:
            print(f"Error loading users: {e}")
            users_list.controls.clear()
            users_list.controls.append(
                ft.Text(f"Error: {str(e)}", color=ft.Colors.RED)
            )
            page.update()
    
    def filter_users():
        """Filter users based on search query."""
        users_list.controls.clear()
        
        query = search_query.current.lower() if hasattr(search_query, 'current') else ""
        
        if query:
            filtered = [u for u in all_users_cache 
                       if query in u["username"].lower() or query in u["email"].lower()]
        else:
            filtered = all_users_cache
        
        for u in filtered:
            users_list.controls.append(create_user_card(u))
        
        if filtered:
            stats_text.value = f"Shown: {len(filtered)} / {len(all_users_cache)} users"
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
    
    def create_user_card(u):
        """Create user card widget."""
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
        """Delete user by ID."""
        try:
            api.delete_user(user_id)
            load_users()
        except Exception as e:
            print(f"Error deleting user: {e}")
    
    def search_changed(e):
        """Handle search field change."""
        search_query.current = e.control.value
        filter_users()
    
    # Search field
    search_field = ft.TextField(
        hint_text="Search user...",
        prefix_icon=ft.Icons.SEARCH,
        on_change=search_changed,
        width=300,
        height=40,
        text_size=14
    )
    
    # Users content panel
    users_content = ft.Column([
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
        ]),
        stats_text,
        ft.Divider(),
        ft.Container(
            content=users_list,
            height=750,
            padding=10,
            bgcolor="#E3F2FD",
            border_radius=10
        )
    ], spacing=15)
    
    return users_content, load_users, filter_users
