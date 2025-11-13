"""
Task card components for displaying and managing tasks.

This module provides reusable task card components for different contexts:
- User task cards (with edit/delete actions)
- Admin task cards (read-only with owner info)
- Empty state displays
"""

import flet as ft
from .ui_helpers import create_empty_state


def create_task_card(task: dict, on_toggle: callable, on_edit: callable, on_delete: callable) -> ft.Card:
    """
    Create a task card for regular users with full CRUD controls.
    
    Features:
        - Checkbox for completion toggle
        - Strike-through styling for completed tasks
        - Edit and delete action buttons
        - Description display (if present)
    
    Args:
        task: Task dictionary with keys: id, title, description, completed
        on_toggle: Callback(task_id, new_value) when completion checkbox changed
        on_edit: Callback(task) when edit button clicked
        on_delete: Callback(task_id) when delete button clicked
    
    Returns:
        ft.Card: Task card component
        
    Example:
        >>> card = create_task_card(
        ...     task={"id": 1, "title": "Buy groceries", "description": "Milk, eggs", "completed": False},
        ...     on_toggle=handle_toggle,
        ...     on_edit=handle_edit,
        ...     on_delete=handle_delete
        ... )
    """
    
    def toggle_complete(e):
        """Handle completion checkbox change."""
        if on_toggle:
            on_toggle(task["id"], e.control.value)
    
    def delete_click(e):
        """Handle delete button click."""
        if on_delete:
            on_delete(task["id"])
    
    def edit_click(e):
        """Handle edit button click."""
        if on_edit:
            on_edit(task)
    
    return ft.Card(
        content=ft.Container(
            content=ft.Row([
                # Completion checkbox
                ft.Checkbox(
                    value=task["completed"],
                    on_change=toggle_complete,
                    scale=1.2
                ),
                
                # Task content (title + description)
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
                
                # Action buttons (edit, delete)
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


def create_admin_task_card(task: dict, on_toggle: callable = None, on_edit: callable = None, on_delete: callable = None) -> ft.Card:
    """
    Create a task card for admin view with owner information and optional controls.
    
    Features:
        - Owner ID display
        - Optional completion toggle
        - Optional edit/delete buttons (for admin task management)
        - Status icon (completed/pending)
    
    Args:
        task: Task dictionary with keys: id, title, description, completed, owner_id
        on_toggle: Optional callback(task_id, new_value) for completion toggle
        on_edit: Optional callback(task) for edit action
        on_delete: Optional callback(task_id) for delete action
    
    Returns:
        ft.Card: Admin task card component
    """
    
    # Determine if we should show action buttons
    show_actions = on_edit is not None or on_delete is not None
    show_toggle = on_toggle is not None
    
    def toggle_complete(e):
        """Handle completion checkbox change."""
        if on_toggle:
            on_toggle(task["id"], e.control.value)
    
    def delete_click(e):
        """Handle delete button click."""
        if on_delete:
            on_delete(task["id"])
    
    def edit_click(e):
        """Handle edit button click."""
        if on_edit:
            on_edit(task)
    
    # Build content based on available actions
    content_row = []
    
    # Status indicator (checkbox or icon)
    if show_toggle:
        content_row.append(
            ft.Checkbox(
                value=task["completed"],
                on_change=toggle_complete,
                scale=1.2
            )
        )
    else:
        content_row.append(
            ft.Icon(
                ft.Icons.CHECK_CIRCLE if task["completed"] else ft.Icons.CIRCLE_OUTLINED,
                color=ft.Colors.GREEN if task["completed"] else ft.Colors.GREY_400,
                size=24
            )
        )
    
    # Task content
    content_row.append(
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
            ) if task.get("description") else ft.Container(),
            ft.Row([
                ft.Icon(ft.Icons.PERSON, size=14, color=ft.Colors.BLUE_600),
                ft.Text(
                    f"User ID: {task['owner_id']}",
                    size=11,
                    color=ft.Colors.BLUE_600
                )
            ], spacing=3)
        ], expand=True, spacing=3)
    )
    
    # Action buttons (if provided)
    if show_actions:
        action_buttons = []
        if on_edit:
            action_buttons.append(
                ft.IconButton(
                    ft.Icons.EDIT,
                    on_click=edit_click,
                    icon_color=ft.Colors.BLUE_600,
                    tooltip="Edit task"
                )
            )
        if on_delete:
            action_buttons.append(
                ft.IconButton(
                    ft.Icons.DELETE,
                    on_click=delete_click,
                    icon_color=ft.Colors.RED_600,
                    tooltip="Delete task"
                )
            )
        content_row.append(ft.Row(action_buttons, spacing=5))
    
    return ft.Card(
        content=ft.Container(
            content=ft.Row(
                content_row,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding=15
        ),
        elevation=2
    )


def create_task_empty_state() -> ft.Container:
    """
    Create an empty state display for when no tasks exist.
    
    Returns:
        ft.Container: Empty state component
    """
    return create_empty_state(
        icon=ft.Icons.INBOX,
        message="No tasks yet",
        icon_size=100
    )


def create_search_empty_state() -> ft.Container:
    """
    Create an empty state display for when search returns no results.
    
    Returns:
        ft.Container: Search empty state component
    """
    return create_empty_state(
        icon=ft.Icons.SEARCH_OFF,
        message="No matching tasks found",
        icon_size=60
    )
