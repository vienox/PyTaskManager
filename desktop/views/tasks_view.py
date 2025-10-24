import flet as ft

def create_tasks_view(page: ft.Page, api, user, on_logout):
    """
    Widok tasków dla zwykłego usera
    
    Args:
        page: Flet Page
        api: APIClient instance
        user: dict z danymi usera (username, email, is_admin)
        on_logout: callback - wywołany po kliknięciu logout
    """
    
    task_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=10)
    empty_state = ft.Container(
        content=ft.Column([
            ft.Icon(ft.icons.INBOX, size=100, color=ft.colors.GREY_400),
            ft.Text("Brak tasków", size=20, color=ft.colors.GREY),
            ft.Text("Kliknij + aby dodać pierwszy task", size=14, color=ft.colors.GREY)
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center,
        expand=True
    )
    
    def load_tasks():
        """Pobierz taski z API i wyświetl"""
        task_list.controls.clear()
        
        try:
            tasks = api.get_tasks()
            
            if not tasks:
                task_list.controls.append(empty_state)
            else:
                for task in tasks:
                    task_list.controls.append(create_task_card(task))
                    
        except Exception as e:
            task_list.controls.append(
                ft.Text(f"❌ Błąd ładowania: {str(e)}", color="red")
            )
        
        page.update()
    
    def create_task_card(task):
        """Karta pojedynczego tasku"""
        
        def toggle_complete(e):
            try:
                api.update_task(task["id"], completed=e.control.value)
                load_tasks()
            except Exception as err:
                print(f"Błąd toggle: {err}")
        
        def delete_click(e):
            try:
                api.delete_task(task["id"])
                load_tasks()
            except Exception as err:
                print(f"Błąd usuwania: {err}")
        
        def edit_click(e):
            show_edit_dialog(task)
        
        return ft.Card(
            content=ft.Container(
                content=ft.Row([
                    ft.Checkbox(
                        value=task["completed"],
                        on_change=toggle_complete,
                        scale=1.2
                    ),
                    ft.Column([
                        ft.Text(
                            task["title"],
                            weight=ft.FontWeight.BOLD,
                            size=16,
                            style=ft.TextStyle(
                                decoration=ft.TextDecoration.LINE_THROUGH if task["completed"] else None
                            )
                        ),
                        ft.Text(
                            task.get("description", ""),
                            size=12,
                            color=ft.colors.GREY,
                            italic=True
                        ) if task.get("description") else None
                    ], expand=True, spacing=5),
                    ft.IconButton(
                        ft.icons.EDIT,
                        on_click=edit_click,
                        icon_color=ft.colors.BLUE,
                        tooltip="Edytuj"
                    ),
                    ft.IconButton(
                        ft.icons.DELETE,
                        on_click=delete_click,
                        icon_color=ft.colors.RED,
                        tooltip="Usuń"
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=15
            ),
            elevation=2
        )
    
    # ========== DIALOG DODAWANIA TASKU ==========
    title_field = ft.TextField(label="Tytuł *", width=500, autofocus=True)
    desc_field = ft.TextField(label="Opis", multiline=True, width=500, min_lines=3)
    
    def add_task_click(e):
        if not title_field.value:
            return
        
        try:
            api.create_task(title_field.value, desc_field.value or "")
            title_field.value = ""
            desc_field.value = ""
            load_tasks()
            page.dialog.open = False
            page.update()
        except Exception as err:
            print(f"Błąd dodawania: {err}")
    
    add_dialog = ft.AlertDialog(
        title=ft.Text("➕ Nowy Task"),
        content=ft.Column([title_field, desc_field], tight=True, spacing=10),
        actions=[
            ft.TextButton("Anuluj", on_click=lambda e: close_dialog()),
            ft.ElevatedButton("Dodaj", on_click=add_task_click)
        ]
    )
    
    # ========== DIALOG EDYCJI TASKU ==========
    edit_title_field = ft.TextField(label="Tytuł", width=500)
    edit_desc_field = ft.TextField(label="Opis", multiline=True, width=500, min_lines=3)
    edit_task_id = None
    
    def show_edit_dialog(task):
        nonlocal edit_task_id
        edit_task_id = task["id"]
        edit_title_field.value = task["title"]
        edit_desc_field.value = task.get("description", "")
        
        page.dialog = edit_dialog
        edit_dialog.open = True
        page.update()
    
    def save_edit_click(e):
        try:
            api.update_task(
                edit_task_id,
                title=edit_title_field.value,
                description=edit_desc_field.value
            )
            load_tasks()
            page.dialog.open = False
            page.update()
        except Exception as err:
            print(f"Błąd edycji: {err}")
    
    edit_dialog = ft.AlertDialog(
        title=ft.Text("✏️ Edytuj Task"),
        content=ft.Column([edit_title_field, edit_desc_field], tight=True, spacing=10),
        actions=[
            ft.TextButton("Anuluj", on_click=lambda e: close_dialog()),
            ft.ElevatedButton("Zapisz", on_click=save_edit_click)
        ]
    )
    
    def close_dialog():
        page.dialog.open = False
        page.update()
    
    def show_add_dialog(e):
        title_field.value = ""
        desc_field.value = ""
        page.dialog = add_dialog
        add_dialog.open = True
        page.update()
    
    # ========== MAIN VIEW ==========
    view = ft.Column([
        ft.AppBar(
            title=ft.Text(f"📋 Moje Taski"),
            actions=[
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            text=f"👤 {user['username']}",
                            disabled=True
                        ),
                        ft.PopupMenuItem(),  # divider
                        ft.PopupMenuItem(
                            text="🚪 Wyloguj",
                            on_click=lambda e: on_logout()
                        )
                    ]
                )
            ],
            bgcolor=ft.colors.BLUE
        ),
        ft.Container(
            content=task_list,
            padding=20,
            expand=True
        ),
        ft.FloatingActionButton(
            icon=ft.icons.ADD,
            on_click=show_add_dialog,
            tooltip="Dodaj task"
        )
    ], expand=True)
    
    # Załaduj taski na start
    load_tasks()
    
    return view