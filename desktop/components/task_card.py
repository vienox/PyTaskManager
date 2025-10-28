import flet as ft

def create_task_card(task: dict, on_toggle, on_edit, on_delete):
    """
    Create a single task card.
    
    Args:
        task: dict with task data {id, title, description, completed}
        on_toggle: callback(task_id, new_value) - change completed status
        on_edit: callback(task) - edit task
        on_delete: callback(task_id) - delete task
    
    Returns:
        ft.Card - task card component
    """
    
    def toggle_complete(e):
        """Change task status (completed/not completed)"""
        if on_toggle:
            on_toggle(task["id"], e.control.value)
    
    def delete_click(e):
        """Delete task"""
        if on_delete:
            on_delete(task["id"])


    
    def edit_click(e):
        """Edit task"""
        if on_edit:
            on_edit(task)
    
    # Status icon
    status_icon = ft.Icon(
        ft.Icons.CHECK_CIRCLE if task["completed"] else ft.Icons.RADIO_BUTTON_UNCHECKED,
        color=ft.Colors.GREEN if task["completed"] else ft.Colors.GREY_400,
        size=24
    )
    
    return ft.Card(
        content=ft.Container(
            content=ft.Row([
                # Checkbox to mark as completed
                ft.Checkbox(
                    value=task["completed"],
                    on_change=toggle_complete,
                    scale=1.2
                ),
                
                # Task content
                ft.Column([
                    ft.Text(
                        task["title"],
                        weight=ft.FontWeight.BOLD,
                        size=16,
                        style=ft.TextStyle(
                            decoration=ft.TextDecoration.LINE_THROUGH if task["completed"] else None,
                            color=ft.Colors.GREY_600 if task["completed"] else ft.Colors.BLACK
                        )
                    ),
                    ft.Text(
                        task.get("description", ""),
                        size=12,
                        color=ft.Colors.GREY_600,
                        italic=True
                    ) if task.get("description") else ft.Container()
                ], expand=True, spacing=5),
                
                # Action buttons
                ft.Row([
                    ft.IconButton(
                        ft.Icons.EDIT,
                        on_click=edit_click,
                        icon_color=ft.Colors.BLUE_600,
                        tooltip="Edit task"
                    ),
                    ft.IconButton(
                        ft.Icons.DELETE,
                        on_click=delete_click,
                        icon_color=ft.Colors.RED_600,
                        tooltip="Delete task"
                    )
                ], spacing=5)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=15
        ),
        elevation=2
    )


def create_empty_state():
    """
    Display empty state when no tasks available.
    
    Returns:
        ft.Container - empty state component
    """
    return ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.INBOX, size=100, color=ft.Colors.GREY_400),
            ft.Text("No tasks", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_600),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15
        ),
        alignment=ft.alignment.center,
        expand=True
    )


def create_admin_task_card(task: dict):
    """
    Create task card for administrator view (read-only).
    Displays task owner information.
    
    Args:
        task: dict with task data {id, title, description, completed, owner_id}
    
    Returns:
        ft.Card - task card component for admin
    """
    return ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    # Status icon
                    ft.Icon(
                        ft.Icons.CHECK_CIRCLE if task["completed"] else ft.Icons.CIRCLE_OUTLINED,
                        color=ft.Colors.GREEN if task["completed"] else ft.Colors.GREY_400,
                        size=24
                    ),
                    
                    # Task content
                    ft.Column([
                        ft.Text(
                            task["title"],
                            weight=ft.FontWeight.BOLD,
                            size=16,
                            style=ft.TextStyle(
                                decoration=ft.TextDecoration.LINE_THROUGH if task["completed"] else None,
                                color=ft.Colors.GREY_600 if task["completed"] else ft.Colors.BLACK
                            )
                        ),
                        ft.Text(
                            task.get("description", ""),
                            size=12,
                            color=ft.Colors.GREY_600,
                            italic=True
                        ) if task.get("description") else ft.Container()
                    ], expand=True, spacing=5),
                    
                    # Owner information
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.PERSON, size=16, color=ft.Colors.BLUE_600),
                            ft.Text(
                                f"User ID: {task['owner_id']}",
                                size=12,
                                color=ft.Colors.BLUE_600,
                                weight=ft.FontWeight.W_500
                            )
                        ], spacing=5),
                        padding=ft.padding.only(right=10)
                    )
                ])
            ], spacing=5),
            padding=15
        ),
        elevation=2
    )
