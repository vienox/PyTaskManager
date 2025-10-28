import flet as ft

def create_task_card(task: dict, on_toggle, on_edit, on_delete):
    """
    Tworzy kartę pojedynczego zadania (task)
    
    Args:
        task: dict z danymi zadania {id, title, description, completed}
        on_toggle: callback(task_id, new_value) - zmiana statusu completed
        on_edit: callback(task) - edycja zadania
        on_delete: callback(task_id) - usunięcie zadania
    
    Returns:
        ft.Card - komponent karty zadania
    """
    
    def toggle_complete(e):
        """Zmiana statusu zadania (zrobione/niezrobione)"""
        if on_toggle:
            on_toggle(task["id"], e.control.value)
    
    def delete_click(e):
        """Usunięcie zadania"""
        if on_delete:
            on_delete(task["id"])
    
    def edit_click(e):
        """Edycja zadania"""
        if on_edit:
            on_edit(task)
    
    # Ikona statusu
    status_icon = ft.Icon(
        ft.Icons.CHECK_CIRCLE if task["completed"] else ft.Icons.RADIO_BUTTON_UNCHECKED,
        color=ft.Colors.GREEN if task["completed"] else ft.Colors.GREY_400,
        size=24
    )
    
    return ft.Card(
        content=ft.Container(
            content=ft.Row([
                # Checkbox do zaznaczenia jako zrobione
                ft.Checkbox(
                    value=task["completed"],
                    on_change=toggle_complete,
                    scale=1.2
                ),
                
                # Treść zadania
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
                
                # Przyciski akcji
                ft.Row([
                    ft.IconButton(
                        ft.Icons.EDIT,
                        on_click=edit_click,
                        icon_color=ft.Colors.BLUE_600,
                        tooltip="Edytuj zadanie"
                    ),
                    ft.IconButton(
                        ft.Icons.DELETE,
                        on_click=delete_click,
                        icon_color=ft.Colors.RED_600,
                        tooltip="Usuń zadanie"
                    )
                ], spacing=5)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=15
        ),
        elevation=2
    )


def create_empty_state():
    """
    Wyświetla stan pusty gdy brak zadań
    
    Returns:
        ft.Container - komponent stanu pustego
    """
    return ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.INBOX, size=100, color=ft.Colors.GREY_400),
            ft.Text("Brak zadań", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_600),
            ft.Text("Kliknij przycisk '+' aby dodać pierwsze zadanie", size=14, color=ft.Colors.GREY_500)
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15
        ),
        alignment=ft.alignment.center,
        expand=True
    )


def create_admin_task_card(task: dict):
    """
    Tworzy kartę zadania dla widoku administratora (read-only)
    Wyświetla informację o właścicielu zadania
    
    Args:
        task: dict z danymi zadania {id, title, description, completed, owner_id}
    
    Returns:
        ft.Card - komponent karty zadania dla admina
    """
    return ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    # Ikona statusu
                    ft.Icon(
                        ft.Icons.CHECK_CIRCLE if task["completed"] else ft.Icons.CIRCLE_OUTLINED,
                        color=ft.Colors.GREEN if task["completed"] else ft.Colors.GREY_400,
                        size=24
                    ),
                    
                    # Treść zadania
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
                    
                    # Informacja o właścicielu
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
