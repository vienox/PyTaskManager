import flet as ft
from components.task_card import create_task_card, create_empty_state

def create_tasks_view(page: ft.Page, api, user, on_logout):
    """
    Widok tasków dla zwykłego usera
    
    Args:
        page: Flet Page
        api: APIClient instance
        user: dict z danymi usera (username, email, is_admin)
        on_logout: callback - wywołany po kliknięciu logout
    """
    
    task_list = ft.Column(scroll=ft.ScrollMode.ADAPTIVE, expand=True, spacing=10)
    
    # Komunikat o błędach
    add_error = ft.Text("", color=ft.Colors.RED, size=12)
    edit_error = ft.Text("", color=ft.Colors.RED, size=12)
    
    def load_tasks():
        """Pobierz taski z API i wyświetl"""
        task_list.controls.clear()
        
        try:
            tasks = api.get_tasks()
            
            if not tasks:
                task_list.controls.append(create_empty_state())
            else:
                for task in tasks:
                    task_list.controls.append(
                        create_task_card(
                            task,
                            on_toggle=handle_toggle,
                            on_edit=handle_edit,
                            on_delete=handle_delete
                        )
                    )
                    
        except Exception as e:
            task_list.controls.append(
                ft.Text(f"❌ Błąd ładowania: {str(e)}", color="red")
            )
        
        page.update()
    
    def handle_toggle(task_id, new_value):
        """Obsługa zmiany statusu zadania"""
        try:
            api.update_task(task_id, completed=new_value)
            load_tasks()
        except Exception as err:
            print(f"Błąd toggle: {err}")
    
    def handle_edit(task):
        """Obsługa edycji zadania"""
        show_edit_dialog(task)
    
    def handle_delete(task_id):
        """Obsługa usunięcia zadania"""
        try:
            api.delete_task(task_id)
            load_tasks()
        except Exception as err:
            print(f"Błąd usuwania: {err}")
    
    # ========== DIALOG DODAWANIA TASKU ==========
    title_field = ft.TextField(
        label="Tytuł *",
        width=500,
        autofocus=True,
        hint_text="Min. 3 znaki",
        on_change=lambda e: validate_add_title()
    )
    desc_field = ft.TextField(
        label="Opis",
        multiline=True,
        width=500,
        min_lines=3,
        hint_text="Opcjonalny szczegółowy opis"
    )
    
    def validate_add_title():
        """Walidacja tytułu dodawania"""
        if title_field.value and len(title_field.value.strip()) < 3:
            title_field.error_text = "Min. 3 znaki"
        else:
            title_field.error_text = None
        page.update()
    
    def add_task_click(e):
        add_error.value = ""
        
        # Walidacja
        if not title_field.value or len(title_field.value.strip()) < 3:
            add_error.value = "❌ Tytuł musi mieć min. 3 znaki"
            title_field.error_text = "Min. 3 znaki"
            page.update()
            return
        
        try:
            api.create_task(title_field.value.strip(), desc_field.value.strip() if desc_field.value else "")
            title_field.value = ""
            desc_field.value = ""
            title_field.error_text = None
            load_tasks()
            page.dialog.open = False
            page.update()
        except Exception as err:
            error_msg = str(err)
            if "401" in error_msg or "403" in error_msg:
                add_error.value = "❌ Sesja wygasła. Zaloguj się ponownie."
            elif "500" in error_msg:
                add_error.value = "❌ Błąd serwera. Spróbuj ponownie."
            else:
                add_error.value = f"❌ Błąd: {error_msg}"
            page.update()
    
    add_dialog = ft.AlertDialog(
        title=ft.Text("➕ Nowy Task"),
        content=ft.Container(
            content=ft.Column([title_field, desc_field, add_error], tight=True, spacing=10),
            width=500
        ),
        actions=[
            ft.TextButton("Anuluj", on_click=lambda e: close_dialog()),
            ft.ElevatedButton("Dodaj", on_click=add_task_click)
        ]
    )
    
    # ========== DIALOG EDYCJI TASKU ==========
    edit_title_field = ft.TextField(
        label="Tytuł *",
        width=500,
        hint_text="Min. 3 znaki",
        on_change=lambda e: validate_edit_title()
    )
    edit_desc_field = ft.TextField(label="Opis", multiline=True, width=500, min_lines=3)
    edit_task_id = None
    
    def validate_edit_title():
        """Walidacja tytułu edycji"""
        if edit_title_field.value and len(edit_title_field.value.strip()) < 3:
            edit_title_field.error_text = "Min. 3 znaki"
        else:
            edit_title_field.error_text = None
        page.update()
    
    def show_edit_dialog(task):
        nonlocal edit_task_id
        edit_task_id = task["id"]
        edit_title_field.value = task["title"]
        edit_desc_field.value = task.get("description", "")
        edit_error.value = ""
        edit_title_field.error_text = None
        
        page.dialog = edit_dialog
        edit_dialog.open = True
        page.update()
    
    def save_edit_click(e):
        edit_error.value = ""
        
        # Walidacja
        if not edit_title_field.value or len(edit_title_field.value.strip()) < 3:
            edit_error.value = "❌ Tytuł musi mieć min. 3 znaki"
            edit_title_field.error_text = "Min. 3 znaki"
            page.update()
            return
        
        try:
            api.update_task(
                edit_task_id,
                title=edit_title_field.value.strip(),
                description=edit_desc_field.value.strip() if edit_desc_field.value else ""
            )
            edit_title_field.error_text = None
            load_tasks()
            page.dialog.open = False
            page.update()
        except Exception as err:
            error_msg = str(err)
            if "401" in error_msg or "403" in error_msg:
                edit_error.value = "❌ Sesja wygasła"
            elif "404" in error_msg:
                edit_error.value = "❌ Task nie istnieje"
            else:
                edit_error.value = f"❌ Błąd: {error_msg}"
            page.update()
    
    edit_dialog = ft.AlertDialog(
        title=ft.Text("✏️ Edytuj Task"),
        content=ft.Container(
            content=ft.Column([edit_title_field, edit_desc_field, edit_error], tight=True, spacing=10),
            width=500
        ),
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
        add_error.value = ""
        title_field.error_text = None
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
            content=ft.ListView(
                controls=[task_list],
                spacing=0,
                padding=10,
                auto_scroll=False,
                expand=True
            ),
            padding=10,
            expand=True
        ),
        ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            on_click=show_add_dialog,
            tooltip="Dodaj task"
        )
    ], expand=True, spacing=0)
    
    # Załaduj taski na start
    load_tasks()
    
    return view