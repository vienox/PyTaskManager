import flet as ft
from components.task_card import create_admin_task_card


def create_admin_task_manager(page: ft.Page, api):
    """
    Komponent zarządzania taskami dla administratora
    Pozwala na dodawanie, edycję i usuwanie tasków użytkowników
    
    Args:
        page: Flet Page
        api: APIClient instance
        
    Returns:
        tuple: (widget, load_tasks_callback)
    """
    
    tasks_list = ft.Column(spacing=10, scroll=ft.ScrollMode.ALWAYS, expand=True)
    tasks_stats_text = ft.Text("", size=14, color=ft.Colors.GREY)
    
    # Wyszukiwanie
    search_query = ft.Ref[str]()
    search_query.current = ""
    
    # Filtrowanie
    all_tasks_cache = []
    filter_dropdown = None  # Inicjalizowane później
    
    # Formularze
    new_task_title = ft.TextField(
        label="Tytuł *",
        autofocus=True,
        hint_text="Min. 3 znaki",
        on_change=lambda e: validate_new_title()
    )
    new_task_desc = ft.TextField(
        label="Opis",
        multiline=True,
        min_lines=2,
        hint_text="Opcjonalny opis zadania"
    )
    new_task_user_id = ft.TextField(label="ID użytkownika *", keyboard_type=ft.KeyboardType.NUMBER)
    
    edit_task_id = None
    edit_task_title = ft.TextField(
        label="Tytuł *",
        hint_text="Min. 3 znaki",
        on_change=lambda e: validate_edit_title()
    )
    edit_task_desc = ft.TextField(label="Opis", multiline=True, min_lines=2)
    edit_task_completed = ft.Checkbox(label="Ukończone")
    
    error_text = ft.Text("", color=ft.Colors.RED, size=12)
    edit_error_text = ft.Text("", color=ft.Colors.RED, size=12)
    
    # Wyszukiwanie użytkowników w dialogu
    user_search_query = ft.Ref[str]()
    user_search_query.current = ""
    all_users_for_dropdown = []
    
    # Lista użytkowników dla dropdowna
    users_dropdown = ft.Dropdown(
        label="Wybierz użytkownika *",
        width=400,
        hint_text="Wybierz z listy"
    )
    
    user_search_field = ft.TextField(
        hint_text="Szukaj użytkownika...",
        prefix_icon=ft.Icons.SEARCH,
        width=400,
        on_change=lambda e: filter_users_dropdown(e.control.value)
    )
    
    # Walidacje
    def validate_new_title():
        """Walidacja tytułu nowego taska"""
        if new_task_title.value and len(new_task_title.value.strip()) < 3:
            new_task_title.error_text = "Min. 3 znaki"
        else:
            new_task_title.error_text = None
        page.update()
    
    def validate_edit_title():
        """Walidacja tytułu edytowanego taska"""
        if edit_task_title.value and len(edit_task_title.value.strip()) < 3:
            edit_task_title.error_text = "Min. 3 znaki"
        else:
            edit_task_title.error_text = None
        page.update()
    
    def load_tasks():
        """Ładuje wszystkie taski z systemu"""
        nonlocal all_tasks_cache
        try:
            all_tasks = api.get_all_tasks()
            all_tasks_cache = all_tasks
            
            # Załaduj użytkowników do filtra
            load_users_filter()
            
            # Zastosuj filtr
            filter_tasks()
            
        except Exception as e:
            print(f"❌ Błąd ładowania tasków: {e}")
            tasks_list.controls.clear()
            tasks_list.controls.append(
                ft.Text(f"❌ Błąd: {str(e)}", color=ft.Colors.RED)
            )
            page.update()
    
    def filter_tasks():
        """Filtruje taski według wybranego użytkownika i wyszukiwania"""
        tasks_list.controls.clear()
        
        # Pobierz wybrany user_id z dropdowna
        selected_user_id = filter_dropdown.value
        
        # Filtruj po użytkowniku
        if selected_user_id and selected_user_id != "all":
            filtered = [t for t in all_tasks_cache if str(t["owner_id"]) == selected_user_id]
        else:
            filtered = all_tasks_cache
        
        # Filtruj po wyszukiwaniu
        query = search_query.current.lower()
        if query:
            filtered = [t for t in filtered 
                       if query in t["title"].lower() or 
                          query in t.get("description", "").lower()]
        
        if not filtered:
            if query:
                tasks_list.controls.append(
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
                tasks_list.controls.append(create_empty_state())
        else:
            for task in filtered:
                tasks_list.controls.append(create_editable_admin_task_card(task))
        
        # Aktualizuj statystyki
        total = len(all_tasks_cache)
        shown = len(filtered)
        if selected_user_id and selected_user_id != "all":
            tasks_stats_text.value = f"Wyświetlono: {shown} / {total} tasków"
        else:
            tasks_stats_text.value = f"Łącznie tasków: {total}"
        
        page.update()
    
    def search_changed(e):
        """Obsługa zmiany w polu wyszukiwania"""
        search_query.current = e.control.value
        filter_tasks()
    
    def load_users_filter():
        """Ładuje użytkowników do dropdowna filtrowania"""
        try:
            users = api.get_all_users()
            
            # Unikalne ID użytkowników z tasków
            user_ids_with_tasks = set(t["owner_id"] for t in all_tasks_cache)
            
            # Mapowanie user_id -> username
            user_map = {u["id"]: u["username"] for u in users}
            
            # Opcje dropdowna
            options = [ft.dropdown.Option(key="all", text="🌐 Wszyscy użytkownicy")]
            for user_id in sorted(user_ids_with_tasks):
                username = user_map.get(user_id, f"User {user_id}")
                task_count = sum(1 for t in all_tasks_cache if t["owner_id"] == user_id)
                options.append(
                    ft.dropdown.Option(
                        key=str(user_id),
                        text=f"👤 {username} ({task_count})"
                    )
                )
            
            filter_dropdown.options = options
            page.update()
        except Exception as e:
            print(f"❌ Błąd ładowania użytkowników do filtra: {e}")
    
    def filter_users_dropdown(search_text):
        """Filtruje użytkowników w dropdownie według wyszukiwania"""
        query = search_text.lower() if search_text else ""
        
        if query:
            filtered = [u for u in all_users_for_dropdown 
                       if query in u["username"].lower() or query in u["email"].lower()]
        else:
            filtered = all_users_for_dropdown
        
        users_dropdown.options = [
            ft.dropdown.Option(
                key=str(u["id"]), 
                text=f"{u['username']} ({u['email']})"
            )
            for u in filtered
        ]
        page.update()
    
    def load_users_for_dropdown():
        """Ładuje użytkowników do dropdowna z wyszukiwarką"""
        nonlocal all_users_for_dropdown
        try:
            users = api.get_all_users()
            all_users_for_dropdown = users
            users_dropdown.options = [
                ft.dropdown.Option(
                    key=str(u["id"]), 
                    text=f"{u['username']} ({u['email']})"
                )
                for u in users
            ]
            user_search_field.value = ""
            page.update()
        except Exception as e:
            print(f"❌ Błąd ładowania użytkowników: {e}")
    
    def create_empty_state():
        """Stan pusty"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.INBOX, size=100, color=ft.Colors.GREY_400),
                ft.Text("Brak tasków w systemie", size=20, color=ft.Colors.GREY_600)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            expand=True
        )
    
    def create_editable_admin_task_card(task):
        """Karta taska z przyciskami edycji i usuwania"""
        return ft.Card(
            content=ft.Container(
                content=ft.Row([
                    # Checkbox statusu
                    ft.Checkbox(
                        value=task["completed"],
                        on_change=lambda e: toggle_task(task["id"], e.control.value),
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
                        ) if task.get("description") else ft.Container(),
                        ft.Row([
                            ft.Icon(ft.Icons.PERSON, size=14, color=ft.Colors.BLUE_600),
                            ft.Text(
                                f"User ID: {task['owner_id']}",
                                size=11,
                                color=ft.Colors.BLUE_600
                            )
                        ], spacing=3)
                    ], expand=True, spacing=3),
                    
                    # Przyciski akcji
                    ft.Row([
                        ft.IconButton(
                            ft.Icons.EDIT,
                            on_click=lambda e: show_edit_dialog(task),
                            icon_color=ft.Colors.BLUE_600,
                            tooltip="Edytuj task"
                        ),
                        ft.IconButton(
                            ft.Icons.DELETE,
                            on_click=lambda e: delete_task_confirm(task),
                            icon_color=ft.Colors.RED_600,
                            tooltip="Usuń task"
                        )
                    ], spacing=5)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=15
            ),
            elevation=2
        )
    
    def toggle_task(task_id, completed):
        """Zmiana statusu zadania"""
        try:
            api.update_task_admin(task_id, completed=completed)
            load_tasks()
        except Exception as e:
            print(f"❌ Błąd toggle: {e}")
    
    def show_add_dialog(e):
        """Pokazuje dialog dodawania taska"""
        load_users_for_dropdown()
        error_text.value = ""
        new_task_title.value = ""
        new_task_desc.value = ""
        users_dropdown.value = None
        new_task_title.error_text = None
        add_dialog.open = True
        page.update()
    
    def create_task_submit(e):
        """Tworzy nowy task dla użytkownika z walidacją"""
        error_text.value = ""
        
        # Walidacja tytułu
        if not new_task_title.value or len(new_task_title.value.strip()) < 3:
            error_text.value = "❌ Tytuł musi mieć min. 3 znaki"
            new_task_title.error_text = "Min. 3 znaki"
            page.update()
            return
        
        # Walidacja użytkownika
        if not users_dropdown.value:
            error_text.value = "❌ Wybierz użytkownika z listy"
            page.update()
            return
        
        try:
            api.create_task_for_user(
                owner_id=int(users_dropdown.value),
                title=new_task_title.value.strip(),
                description=new_task_desc.value.strip() if new_task_desc.value else ""
            )
            add_dialog.open = False
            new_task_title.error_text = None
            load_tasks()
            page.update()
        except Exception as ex:
            error_msg = str(ex)
            
            if "401" in error_msg or "403" in error_msg:
                error_text.value = "❌ Brak uprawnień. Zaloguj się ponownie jako admin."
            elif "404" in error_msg:
                error_text.value = "❌ Użytkownik nie istnieje"
            elif "500" in error_msg:
                error_text.value = "❌ Błąd serwera. Spróbuj ponownie."
            else:
                error_text.value = f"❌ Błąd: {error_msg}"
            
            page.update()
    
    def show_edit_dialog(task):
        """Pokazuje dialog edycji taska"""
        nonlocal edit_task_id
        edit_task_id = task["id"]
        edit_task_title.value = task["title"]
        edit_task_desc.value = task.get("description", "")
        edit_task_completed.value = task["completed"]
        edit_error_text.value = ""
        edit_task_title.error_text = None
        edit_dialog.open = True
        page.update()
    
    def edit_task_submit(e):
        """Zapisuje edycję taska z walidacją"""
        edit_error_text.value = ""
        
        # Walidacja tytułu
        if not edit_task_title.value or len(edit_task_title.value.strip()) < 3:
            edit_error_text.value = "❌ Tytuł musi mieć min. 3 znaki"
            edit_task_title.error_text = "Min. 3 znaki"
            page.update()
            return
        
        try:
            api.update_task_admin(
                edit_task_id,
                title=edit_task_title.value.strip(),
                description=edit_task_desc.value.strip() if edit_task_desc.value else "",
                completed=edit_task_completed.value
            )
            edit_dialog.open = False
            edit_task_title.error_text = None
            load_tasks()
            page.update()
        except Exception as ex:
            error_msg = str(ex)
            
            if "401" in error_msg or "403" in error_msg:
                edit_error_text.value = "❌ Brak uprawnień"
            elif "404" in error_msg:
                edit_error_text.value = "❌ Task nie istnieje"
            elif "500" in error_msg:
                edit_error_text.value = "❌ Błąd serwera"
            else:
                edit_error_text.value = f"❌ Błąd: {error_msg}"
            
            page.update()
    
    def delete_task_confirm(task):
        """Potwierdza usunięcie taska"""
        def delete_confirmed(e):
            try:
                api.delete_task_admin(task["id"])
                confirm_dialog.open = False
                load_tasks()
                page.update()
            except Exception as ex:
                print(f"❌ Błąd usuwania: {ex}")
                confirm_dialog.open = False
                page.update()
        
        confirm_dialog.content = ft.Text(
            f'Czy na pewno usunąć task:\n"{task["title"]}"?',
            text_align=ft.TextAlign.CENTER
        )
        confirm_dialog.actions = [
            ft.TextButton("Anuluj", on_click=lambda e: setattr(confirm_dialog, 'open', False) or page.update()),
            ft.ElevatedButton("Usuń", on_click=delete_confirmed, bgcolor=ft.Colors.RED_600, color=ft.Colors.WHITE)
        ]
        confirm_dialog.open = True
        page.update()
    
    # ========== DIALOGI ==========
    add_dialog = ft.AlertDialog(
        title=ft.Text("Dodaj Task dla Użytkownika"),
        content=ft.Container(
            content=ft.Column([
                user_search_field,
                users_dropdown,
                new_task_title,
                new_task_desc,
                error_text
            ], tight=True, spacing=10),
            width=450
        ),
        actions=[
            ft.TextButton("Anuluj", on_click=lambda e: setattr(add_dialog, 'open', False) or page.update()),
            ft.ElevatedButton("Dodaj", on_click=create_task_submit)
        ]
    )
    
    edit_dialog = ft.AlertDialog(
        title=ft.Text("✏️ Edytuj Task"),
        content=ft.Container(
            content=ft.Column([
                edit_task_title,
                edit_task_desc,
                edit_task_completed,
                edit_error_text
            ], tight=True, spacing=10),
            width=400
        ),
        actions=[
            ft.TextButton("Anuluj", on_click=lambda e: setattr(edit_dialog, 'open', False) or page.update()),
            ft.ElevatedButton("Zapisz", on_click=edit_task_submit)
        ]
    )
    
    confirm_dialog = ft.AlertDialog(
        title=ft.Text("⚠️ Potwierdzenie"),
        modal=True
    )
    
    page.overlay.extend([add_dialog, edit_dialog, confirm_dialog])
    
    # ========== INICJALIZACJA FILTRA (po definicji funkcji) ==========
    filter_dropdown = ft.Dropdown(
        label="Filtruj po użytkowniku",
        hint_text="Wszyscy użytkownicy",
        width=250,
        on_change=lambda e: filter_tasks()
    )
    
    # ========== GŁÓWNY WIDGET ==========
    search_field = ft.TextField(
        hint_text="Szukaj taska...",
        prefix_icon=ft.Icons.SEARCH,
        on_change=search_changed,
        width=250,
        height=40,
        text_size=14
    )
    
    widget = ft.Column([
        ft.Row([
            ft.Text("Wszystkie Taski", size=20, weight=ft.FontWeight.BOLD),
            ft.Container(expand=True),
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
            filter_dropdown,
            ft.IconButton(
                icon=ft.Icons.FILTER_ALT_OFF,
                tooltip="Wyczyść filtr użytkownika",
                on_click=lambda e: (
                    setattr(filter_dropdown, 'value', "all"),
                    filter_tasks()
                )
            ),
            tasks_stats_text,
            ft.ElevatedButton(
                "Dodaj Task",
                icon=ft.Icons.ADD_TASK,
                on_click=show_add_dialog
            )
        ], spacing=10),
        ft.Divider(),
        ft.Container(
            content=tasks_list,
            height=750,  # Stała wysokość dla scrollowania
            padding=10,
            bgcolor="#E3F2FD",
            border_radius=10
        )
    ], spacing=15)
    
    return widget, load_tasks
