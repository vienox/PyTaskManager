import flet as ft


def navbar(page, user, on_logout, title="Task Manager", show_home=False, on_home=None):
    left = []
    if show_home and on_home:
        left.append(ft.IconButton(icon=ft.Icons.HOME, icon_color=ft.Colors.WHITE, on_click=lambda e: on_home()))
    left.extend([ft.Icon(ft.Icons.TASK_ALT, color=ft.Colors.WHITE, size=28), ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)])
    
    user_icon = ft.Icons.ADMIN_PANEL_SETTINGS if user.get("is_admin") else ft.Icons.PERSON
    user_color = ft.Colors.AMBER_200 if user.get("is_admin") else ft.Colors.WHITE
    
    right = ft.Row([
        ft.Icon(user_icon, color=user_color, size=20),
        ft.Text(user.get("username", "User"), color=ft.Colors.WHITE),
        ft.IconButton(icon=ft.Icons.LOGOUT, icon_color=ft.Colors.WHITE, on_click=lambda e: on_logout())
    ], spacing=10)
    
    return ft.Container(
        content=ft.Row([ft.Row(left, spacing=10), ft.Container(expand=True), right]),
        padding=15,
        bgcolor=ft.Colors.BLUE_700
    )


def task_card(task, on_toggle, on_edit, on_delete):
    return ft.Card(
        content=ft.Container(
            content=ft.Row([
                ft.Checkbox(value=task["completed"], on_change=lambda e: on_toggle(task["id"], e.control.value)),
                ft.Column([
                    ft.Text(
                        task["title"],
                        weight=ft.FontWeight.BOLD,
                        style=ft.TextStyle(
                            decoration=ft.TextDecoration.LINE_THROUGH if task["completed"] else None,
                            color=ft.Colors.GREY_600 if task["completed"] else ft.Colors.BLACK
                        )
                    ),
                    ft.Text(task.get("description", ""), size=12, color=ft.Colors.GREY_600) if task.get("description") else ft.Container()
                ], expand=True, spacing=5),
                ft.Row([
                    ft.IconButton(ft.Icons.EDIT, on_click=lambda e: on_edit(task), icon_color=ft.Colors.BLUE_600),
                    ft.IconButton(ft.Icons.DELETE, on_click=lambda e: on_delete(task["id"]), icon_color=ft.Colors.RED_600)
                ], spacing=5)
            ]),
            padding=15
        ),
        elevation=2
    )


def empty_state(message="No items"):
    return ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.INBOX, size=80, color=ft.Colors.GREY_400),
            ft.Text(message, size=18, color=ft.Colors.GREY_600)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        alignment=ft.alignment.center,
        expand=True
    )


def confirm_dialog(page, message, on_confirm):
    def close(e):
        dialog.open = False
        page.update()
    
    dialog = ft.AlertDialog(
        title=ft.Text("Confirm"),
        content=ft.Text(message),
        actions=[
            ft.TextButton("Cancel", on_click=close),
            ft.ElevatedButton("Delete", on_click=on_confirm, bgcolor=ft.Colors.RED_600, color=ft.Colors.WHITE)
        ]
    )
    return dialog
