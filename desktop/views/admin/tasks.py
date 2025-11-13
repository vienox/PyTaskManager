import flet as ft


def task_manager(page, api):
    tasks_list = ft.Column(spacing=10, scroll=ft.ScrollMode.ALWAYS, expand=True)
    all_tasks = []
    all_users = []
    search_query = ""
    filter_user = "all"
    
    def load_tasks():
        nonlocal all_tasks, all_users
        try:
            all_tasks = api.get_all_tasks()
            all_users = api.get_all_users()
            update_filter_dropdown()
            filter_tasks()
        except Exception as e:
            tasks_list.controls.clear()
            tasks_list.controls.append(ft.Text(f"Error: {str(e)}", color="red"))
            page.update()
    
    def update_filter_dropdown():
        user_map = {u["id"]: u["username"] for u in all_users}
        user_ids = set(t["owner_id"] for t in all_tasks)
        
        options = [ft.dropdown.Option(key="all", text="All Users")]
        for uid in sorted(user_ids):
            username = user_map.get(uid, f"User {uid}")
            count = sum(1 for t in all_tasks if t["owner_id"] == uid)
            options.append(ft.dropdown.Option(key=str(uid), text=f"{username} ({count})"))
        
        filter_dropdown.options = options
        page.update()
    
    def filter_tasks():
        tasks_list.controls.clear()
        query = search_query.lower()
        
        filtered = [t for t in all_tasks if (filter_user == "all" or str(t["owner_id"]) == filter_user)]
        if query:
            filtered = [t for t in filtered if query in t["title"].lower() or query in t.get("description", "").lower()]
        
        if not filtered:
            tasks_list.controls.append(ft.Container(
                content=ft.Column([ft.Icon(ft.Icons.INBOX, size=80, color=ft.Colors.GREY_400), ft.Text("No tasks", color=ft.Colors.GREY_600)], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center,
                expand=True
            ))
        else:
            for task in filtered:
                tasks_list.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Row([
                                ft.Checkbox(value=task["completed"], on_change=lambda e, tid=task["id"]: toggle_task(tid, e.control.value)),
                                ft.Column([
                                    ft.Text(task["title"], weight=ft.FontWeight.BOLD, style=ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH if task["completed"] else None)),
                                    ft.Text(task.get("description", ""), size=12, color=ft.Colors.GREY_600) if task.get("description") else ft.Container(),
                                    ft.Text(f"User: {task['owner_id']}", size=11, color=ft.Colors.BLUE_600)
                                ], expand=True, spacing=3),
                                ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_600, on_click=lambda e, tid=task["id"]: delete_task(tid))
                            ]),
                            padding=15
                        ),
                        elevation=2
                    )
                )
        page.update()
    
    def toggle_task(task_id, completed):
        try:
            api.update_task_admin(task_id, completed=completed)
            load_tasks()
        except Exception as e:
            print(f"Error: {e}")
    
    def delete_task(task_id):
        try:
            api.delete_task_admin(task_id)
            load_tasks()
        except Exception as e:
            print(f"Error: {e}")
    
    def add_task_dialog():
        title_field = ft.TextField(label="Title", width=400)
        desc_field = ft.TextField(label="Description", multiline=True, min_lines=3, width=400)
        user_dropdown = ft.Dropdown(label="Assign to User", width=400)
        user_dropdown.options = [ft.dropdown.Option(key=str(u["id"]), text=u["username"]) for u in all_users]
        
        def add_task(e):
            if not title_field.value or not user_dropdown.value:
                return
            try:
                api.create_task_for_user(int(user_dropdown.value), title_field.value, desc_field.value)
                dialog.open = False
                page.update()
                load_tasks()
            except Exception as ex:
                print(f"Error: {ex}")
        
        dialog = ft.AlertDialog(
            title=ft.Text("Add New Task"),
            content=ft.Column([title_field, desc_field, user_dropdown], tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: setattr(dialog, 'open', False) or page.update()),
                ft.ElevatedButton("Add Task", on_click=add_task)
            ]
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
    
    search_field = ft.TextField(hint_text="Search tasks...", prefix_icon=ft.Icons.SEARCH, width=250, height=40)
    
    def search_changed(e):
        nonlocal search_query
        search_query = e.control.value
        filter_tasks()
    
    search_field.on_change = search_changed
    
    filter_dropdown = ft.Dropdown(label="Filter by user", width=250, value="all")
    
    def filter_changed(e):
        nonlocal filter_user
        filter_user = e.control.value
        filter_tasks()
    
    filter_dropdown.on_change = filter_changed
    
    widget = ft.Column([
        ft.Row([
            ft.Text("All Tasks", size=20, weight=ft.FontWeight.BOLD),
            ft.Container(expand=True),
            ft.ElevatedButton("Add Task", icon=ft.Icons.ADD, on_click=lambda e: add_task_dialog()),
            search_field,
            ft.IconButton(icon=ft.Icons.CLEAR, on_click=lambda e: (setattr(search_field, 'value', ""), search_changed(e))),
            filter_dropdown,
            ft.IconButton(icon=ft.Icons.FILTER_ALT_OFF, on_click=lambda e: (setattr(filter_dropdown, 'value', "all"), filter_changed(e)))
        ], spacing=10),
        ft.Divider(),
        ft.Container(content=tasks_list, height=650, padding=10, bgcolor="#E3F2FD", border_radius=10)
    ], spacing=15)
    
    return widget, load_tasks
