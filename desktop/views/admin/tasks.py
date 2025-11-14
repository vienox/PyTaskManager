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
            filter_tasks()
        except Exception as e:
            tasks_list.controls.clear()
            tasks_list.controls.append(ft.Text(f"Error: {str(e)}", color="red"))
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
        
        user_suggestions = []
        selected_user_id = [None]  # Lista aby móc modyfikować w zagnieżdżonej funkcji
        
        user_field = ft.TextField(
            label="Assign to User (type username)", 
            width=400, 
            hint_text="Start typing username...",
            on_change=lambda e: update_user_suggestions(e.control.value)
        )
        
        suggestions_list = ft.Column([], height=150, scroll=ft.ScrollMode.AUTO)
        error_text = ft.Text("", color=ft.Colors.RED, size=12)
        
        def update_user_suggestions(query):
            suggestions_list.controls.clear()
            if not query:
                selected_user_id[0] = None
                page.update()
                return
            
            # Szukaj pasujących użytkowników
            query_lower = query.lower()
            matching = [u for u in all_users if query_lower in u["username"].lower()]
            
            for u in matching:
                suggestions_list.controls.append(
                    ft.TextButton(
                        text=u["username"],
                        on_click=lambda e, uid=u["id"], uname=u["username"]: select_user(uid, uname)
                    )
                )
            page.update()
        
        def select_user(user_id, username):
            selected_user_id[0] = user_id
            user_field.value = username
            suggestions_list.controls.clear()
            page.update()
        
        def add_task(e):
            error_text.value = ""
            if not title_field.value or not selected_user_id[0]:
                error_text.value = "Title and User are required"
                page.update()
                return
            
            try:
                api.create_task_for_user(selected_user_id[0], title_field.value, desc_field.value or "")
                dialog.open = False
                page.update()
                load_tasks()
            except Exception as ex:
                error_text.value = f"Error: {str(ex)}"
                page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Add New Task"),
            content=ft.Column([title_field, desc_field, user_field, suggestions_list, error_text], tight=True, height=400),
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
    
    # Filtr użytkowników z sugestiami
    selected_filter_user = [None]
    filter_search = ft.TextField(
        hint_text="Type username to filter...",
        prefix_icon=ft.Icons.PERSON_SEARCH,
        width=250,
        height=40,
        on_change=lambda e: update_filter_suggestions(e.control.value)
    )
    
    filter_suggestions = ft.Column([], spacing=5, visible=False)
    
    def update_filter_suggestions(query):
        filter_suggestions.controls.clear()
        
        if not query:
            selected_filter_user[0] = None
            filter_suggestions.visible = False
            filter_user = "all"
            filter_tasks()
            page.update()
            return
        
        query_lower = query.lower()
        matching = [u for u in all_users if query_lower in u["username"].lower()]
        
        if matching:
            filter_suggestions.visible = True
            for u in matching[:5]:  # Pokaż max 5 wyników
                filter_suggestions.controls.append(
                    ft.Container(
                        content=ft.TextButton(
                            text=u["username"],
                            on_click=lambda e, uid=u["id"], uname=u["username"]: select_filter_user(uid, uname)
                        ),
                        bgcolor=ft.Colors.WHITE,
                        padding=5,
                        border_radius=5
                    )
                )
        else:
            filter_suggestions.visible = False
        
        page.update()
    
    def select_filter_user(user_id, username):
        nonlocal filter_user
        selected_filter_user[0] = user_id
        filter_user = str(user_id)
        filter_search.value = username
        filter_suggestions.controls.clear()
        filter_suggestions.visible = False
        filter_tasks()
        page.update()
    
    def clear_filter_click(e):
        nonlocal filter_user
        filter_search.value = ""
        selected_filter_user[0] = None
        filter_suggestions.controls.clear()
        filter_suggestions.visible = False
        filter_user = "all"
        filter_search.value = ""
        filter_tasks()
        page.update()
    
    def clear_search_click(e):
        nonlocal search_query
        search_field.value = ""
        search_query = ""
        filter_tasks()
        page.update()
    
    widget = ft.Column([
        ft.Row([
            ft.Text("All Tasks", size=20, weight=ft.FontWeight.BOLD),
            ft.Container(expand=True),
            ft.ElevatedButton("Add Task", icon=ft.Icons.ADD, on_click=lambda e: add_task_dialog()),
            search_field,
            ft.IconButton(icon=ft.Icons.CLEAR, on_click=clear_search_click),
            ft.Column([filter_search, filter_suggestions], spacing=0),
            ft.IconButton(icon=ft.Icons.FILTER_ALT_OFF, on_click=clear_filter_click)
        ], spacing=10),
        ft.Divider(),
        ft.Container(content=tasks_list, height=650, padding=10, bgcolor="#E3F2FD", border_radius=10)
    ], spacing=15)
    
    return widget, load_tasks
