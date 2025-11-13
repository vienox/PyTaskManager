import flet as ft
from views.ui.components import navbar, task_card, empty_state


def create_tasks_view(page, api, user, on_logout, on_back_to_profile=None):
    task_list = ft.Column(spacing=10, scroll=ft.ScrollMode.ALWAYS, expand=True)
    all_tasks = []
    search_query = ""
    
    title_field = ft.TextField(label="Title *", width=500, autofocus=True)
    desc_field = ft.TextField(label="Description", multiline=True, width=500, min_lines=3)
    error_text = ft.Text("", color=ft.Colors.RED, size=12)
    
    edit_title = ft.TextField(label="Title *", width=500)
    edit_desc = ft.TextField(label="Description", multiline=True, width=500, min_lines=3)
    edit_error = ft.Text("", color=ft.Colors.RED, size=12)
    edit_task_id = None
    
    def load_tasks():
        nonlocal all_tasks
        try:
            all_tasks = api.get_tasks()
            filter_tasks()
        except Exception as e:
            task_list.controls.clear()
            task_list.controls.append(ft.Text(f"Error: {str(e)}", color="red"))
            page.update()
    
    def filter_tasks():
        task_list.controls.clear()
        query = search_query.lower()
        filtered = [t for t in all_tasks if query in t["title"].lower() or query in t.get("description", "").lower()] if query else all_tasks
        
        if not filtered:
            task_list.controls.append(empty_state("No tasks" if not query else "No matching tasks"))
        else:
            for task in filtered:
                task_list.controls.append(task_card(task, toggle_task, edit_task, delete_task))
        page.update()
    
    def toggle_task(task_id, completed):
        try:
            api.update_task(task_id, completed=completed)
            load_tasks()
        except Exception as e:
            print(f"Error: {e}")
    
    def edit_task(task):
        nonlocal edit_task_id
        edit_task_id = task["id"]
        edit_title.value = task["title"]
        edit_desc.value = task.get("description", "")
        edit_error.value = ""
        edit_dialog.open = True
        page.update()
    
    def delete_task(task_id):
        try:
            api.delete_task(task_id)
            load_tasks()
        except Exception as e:
            print(f"Error: {e}")
    
    def add_task(e):
        error_text.value = ""
        if not title_field.value or len(title_field.value.strip()) < 3:
            error_text.value = "Title must be at least 3 characters"
            page.update()
            return
        try:
            api.create_task(title_field.value.strip(), desc_field.value.strip() if desc_field.value else "")
            title_field.value = ""
            desc_field.value = ""
            add_dialog.open = False
            load_tasks()
            page.update()
        except Exception as err:
            error_text.value = f"Error: {str(err)}"
            page.update()
    
    def save_edit(e):
        edit_error.value = ""
        if not edit_title.value or len(edit_title.value.strip()) < 3:
            edit_error.value = "Title must be at least 3 characters"
            page.update()
            return
        try:
            api.update_task(edit_task_id, title=edit_title.value.strip(), description=edit_desc.value.strip() if edit_desc.value else "")
            edit_dialog.open = False
            load_tasks()
            page.update()
        except Exception as err:
            edit_error.value = f"Error: {str(err)}"
            page.update()
    
    add_dialog = ft.AlertDialog(
        title=ft.Text("New Task"),
        content=ft.Container(content=ft.Column([title_field, desc_field, error_text], tight=True, spacing=10), width=500),
        actions=[ft.TextButton("Cancel", on_click=lambda e: setattr(add_dialog, 'open', False) or page.update()), ft.ElevatedButton("Add", on_click=add_task)]
    )
    
    edit_dialog = ft.AlertDialog(
        title=ft.Text("Edit Task"),
        content=ft.Container(content=ft.Column([edit_title, edit_desc, edit_error], tight=True, spacing=10), width=500),
        actions=[ft.TextButton("Cancel", on_click=lambda e: setattr(edit_dialog, 'open', False) or page.update()), ft.ElevatedButton("Save", on_click=save_edit)]
    )
    
    page.overlay.extend([add_dialog, edit_dialog])
    
    search_field = ft.TextField(hint_text="Search tasks...", prefix_icon=ft.Icons.SEARCH, width=300, height=40, on_change=lambda e: (globals().__setitem__('search_query', e.control.value), filter_tasks()))
    
    def search_changed(e):
        nonlocal search_query
        search_query = e.control.value
        filter_tasks()
    
    search_field.on_change = search_changed
    
    load_tasks()
    
    return ft.Column([
        navbar(page, user, on_logout, "My Tasks", show_home=bool(on_back_to_profile), on_home=on_back_to_profile),
        ft.Container(
            content=ft.Column([
                ft.Row([
                    search_field,
                    ft.IconButton(icon=ft.Icons.CLEAR, on_click=lambda e: (setattr(search_field, 'value', ""), search_changed(e))),
                    ft.Container(expand=True),
                    ft.ElevatedButton("Add Task", icon=ft.Icons.ADD_TASK, on_click=lambda e: (setattr(add_dialog, 'open', True), page.update()))
                ]),
                ft.Container(content=task_list, height=500, padding=10, bgcolor="#E3F2FD", border_radius=10)
            ], spacing=10),
            padding=20
        )
    ], expand=True, spacing=0)
