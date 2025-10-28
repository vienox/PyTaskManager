import flet as ft
from components.task_card import create_task_card, create_empty_state


def create_user_task_manager(page: ft.Page, api):
    """
    Komponent zarządzania taskami dla zwykłego użytkownika
    Pozwala na przeglądanie, dodawanie, edycję i usuwanie własnych tasków
    
    Args:
        page: Flet Page
        api: APIClient instance
        
    Returns:
        tuple: (widget, load_tasks_callback)
    """
    
    task_list = ft.Column(spacing=10, scroll=ft.ScrollMode.ALWAYS, expand=True)
    
    # Komunikaty o błędach
    add_error = ft.Text("", color=ft.Colors.RED, size=12)
    edit_error = ft.Text("", color=ft.Colors.RED, size=12)
    
    # Wyszukiwanie
    search_query = ft.Ref[str]()
    search_query.current = ""
    all_tasks_cache = []
    
    # ========== ŁADOWANIE I FILTROWANIE ==========
    def load_tasks():
        """Pobierz taski z API i wyświetl"""
        nonlocal all_tasks_cache
        
        try:
            tasks = api.get_tasks()
            all_tasks_cache = tasks
            filter_tasks()
                    
        except Exception as e:
            task_list.controls.clear()
            task_list.controls.append(
                ft.Text(f"❌ Błąd ładowania: {str(e)}", color="red")
            )
            page.update()
    
    def filter_tasks():
        """Filtruje taski według wyszukiwania"""
        task_list.controls.clear()
        
        query = search_query.current.lower()
        
        if query:
            filtered = [t for t in all_tasks_cache 
                       if query in t["title"].lower() or 
                          query in t.get("description", "").lower()]
        else:
            filtered = all_tasks_cache
        
        if not filtered:
            if query:
                task_list.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.SEARCH_OFF, size=60, color=ft.Colors.GREY_400),
                            ft.Text("Nie znaleziono pasujących tasków", color=ft.Colors.GREY_600)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        alignment=ft.alignment.center,
                        padding=40
                    )
                )
            else:
                task_list.controls.append(create_empty_state())
        else:
            for task in filtered:
                task_list.controls.append(
                    create_task_card(
                        task,
                        on_toggle=handle_toggle,
                        on_edit=handle_edit,
                        on_delete=handle_delete
                    )
                )
        
        page.update()
    
    def search_changed(e):
        """Obsługa zmiany w polu wyszukiwania"""
        search_query.current = e.control.value
        filter_tasks()
    
    # ========== OBSŁUGA AKCJI NA TASKACH ==========
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
            add_dialog.open = False
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
    
    def show_add_dialog(e):
        title_field.value = ""
        desc_field.value = ""
        add_error.value = ""
        title_field.error_text = None
        add_dialog.open = True
        page.update()
    
    add_dialog = ft.AlertDialog(
        title=ft.Text("Nowy Task"),
        content=ft.Container(
            content=ft.Column([title_field, desc_field, add_error], tight=True, spacing=10),
            width=500
        ),
        actions=[
            ft.TextButton("Anuluj", on_click=lambda e: setattr(add_dialog, 'open', False) or page.update()),
            ft.ElevatedButton("Dodaj", on_click=add_task_click)
        ]
    )
    
    page.overlay.append(add_dialog)
    
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
            edit_dialog.open = False
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
            ft.TextButton("Anuluj", on_click=lambda e: setattr(edit_dialog, 'open', False) or page.update()),
            ft.ElevatedButton("Zapisz", on_click=save_edit_click)
        ]
    )
    
    page.overlay.append(edit_dialog)
    
    # ========== GŁÓWNY WIDGET ==========
    search_field = ft.TextField(
        hint_text="Szukaj taska...",
        prefix_icon=ft.Icons.SEARCH,
        on_change=search_changed,
        width=300,
        height=40,
        text_size=14,
        bgcolor=ft.Colors.WHITE
    )
    
    widget = ft.Column([
        ft.Row([
            search_field,
            ft.IconButton(
                icon=ft.Icons.CLEAR,
                tooltip="Wyczyść wyszukiwanie",
                on_click=lambda e: (
                    setattr(search_field, 'value', ""),
                    setattr(search_query, 'current', ""),
                    filter_tasks()
                )
            ),
            ft.Container(expand=True),
            ft.ElevatedButton(
                "Dodaj Task",
                icon=ft.Icons.ADD_TASK,
                on_click=show_add_dialog
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Divider(),
        ft.Container(
            content=task_list,
            height=500,
            padding=10,
            bgcolor="#E3F2FD",
            border_radius=10
        )
    ], spacing=10)
    
    return widget, load_tasks
