import flet as ft
import re


def user_manager(page, api):
    users_list = ft.Column(spacing=10, scroll=ft.ScrollMode.ALWAYS, expand=True)
    all_users = []
    search_query = ""
    
    username_field = ft.TextField(label="Username *", autofocus=True, hint_text="Min. 3 characters")
    email_field = ft.TextField(label="Email *", hint_text="example@email.com")
    password_field = ft.TextField(label="Password *", password=True, can_reveal_password=True, hint_text="Min. 6 characters")
    error_text = ft.Text("", color=ft.Colors.RED, size=12)
    
    def load_users():
        nonlocal all_users
        try:
            all_users = api.get_all_users()
            filter_users()
        except Exception as e:
            users_list.controls.clear()
            users_list.controls.append(ft.Text(f"Error: {str(e)}", color="red"))
            page.update()
    
    def filter_users():
        users_list.controls.clear()
        query = search_query.lower()
        filtered = [u for u in all_users if query in u["username"].lower() or query in u["email"].lower()] if query else all_users
        
        for u in filtered:
            users_list.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS if u["is_admin"] else ft.Icons.PERSON, color=ft.Colors.AMBER if u["is_admin"] else ft.Colors.BLUE),
                            ft.Column([ft.Text(u["username"], weight=ft.FontWeight.BOLD), ft.Text(u["email"], size=12, color=ft.Colors.GREY)], spacing=2),
                            ft.Container(expand=True),
                            ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED, on_click=lambda e, uid=u["id"]: delete_user(uid))
                        ]),
                        padding=15
                    )
                )
            )
        page.update()
    
    def delete_user(user_id):
        try:
            api.delete_user(user_id)
            load_users()
        except Exception as e:
            print(f"Error: {e}")
    
    def add_user(e):
        error_text.value = ""
        if not username_field.value or not email_field.value or not password_field.value:
            error_text.value = "All fields required"
            page.update()
            return
        if len(username_field.value) < 3:
            error_text.value = "Username min. 3 characters"
            page.update()
            return
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email_field.value):
            error_text.value = "Invalid email"
            page.update()
            return
        if len(password_field.value) < 6:
            error_text.value = "Password min. 6 characters"
            page.update()
            return
        try:
            api.create_user(username=username_field.value, email=email_field.value, password=password_field.value)
            username_field.value = ""
            email_field.value = ""
            password_field.value = ""
            add_dialog.open = False
            load_users()
            page.update()
        except Exception as ex:
            error_text.value = f"Error: {str(ex)}"
            page.update()
    
    add_dialog = ft.AlertDialog(
        title=ft.Text("Add User"),
        content=ft.Container(content=ft.Column([username_field, email_field, password_field, error_text], tight=True, spacing=10), width=400),
        actions=[ft.TextButton("Cancel", on_click=lambda e: setattr(add_dialog, 'open', False) or page.update()), ft.ElevatedButton("Add", on_click=add_user)]
    )
    
    page.overlay.append(add_dialog)
    
    search_field = ft.TextField(hint_text="Search users...", prefix_icon=ft.Icons.SEARCH, width=300, height=40)
    
    def search_changed(e):
        nonlocal search_query
        search_query = e.control.value
        filter_users()
    
    search_field.on_change = search_changed
    
    widget = ft.Column([
        ft.Row([
            ft.Text("User Management", size=20, weight=ft.FontWeight.BOLD),
            ft.Container(expand=True),
            search_field,
            ft.IconButton(icon=ft.Icons.CLEAR, on_click=lambda e: (setattr(search_field, 'value', ""), search_changed(e))),
            ft.ElevatedButton("Add User", icon=ft.Icons.PERSON_ADD, on_click=lambda e: (setattr(add_dialog, 'open', True), page.update()))
        ]),
        ft.Divider(),
        ft.Container(content=users_list, height=650, padding=10, bgcolor="#E3F2FD", border_radius=10)
    ], spacing=15)
    
    return widget, load_users
