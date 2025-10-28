import flet as ft
from api_client import APIClient
from components.nav_bar import create_nav_bar
from components.task_card import create_task_card, create_admin_task_card
from components.admin_task_manager import create_admin_task_manager

def create_admin_view(page: ft.Page, api, user, on_logout):
    """Panel admina - zarządzanie użytkownikami i taskami"""
    
    users_list = ft.Column(spacing=10, scroll=ft.ScrollMode.ALWAYS, expand=True)
    stats_text = ft.Text("", size=14, color=ft.Colors.GREY)
    search_query = ft.Ref[str]()
    search_query.current = ""
    all_users_cache = []
    
    # Przełącznik widoku (użytkownicy / taski)
    current_view = ft.Ref[str]()
    current_view.current = "users"
    
    # Deklaracja przycisków zakładek (wypełnione później)
    users_tab_btn = None
    tasks_tab_btn = None
    content_area = None
    
    # Pola formularza dodawania użytkownika
    new_username = ft.TextField(
        label="Nazwa użytkownika *",
        autofocus=True,
        hint_text="Min. 3 znaki",
        counter_text="",
        on_change=lambda e: validate_username_field()
    )
    new_email = ft.TextField(
        label="Email *",
        hint_text="przykład@email.com",
        keyboard_type=ft.KeyboardType.EMAIL,
        on_change=lambda e: validate_email_field()
    )
    new_password = ft.TextField(
        label="Hasło *",
        password=True,
        can_reveal_password=True,
        hint_text="Min. 6 znaków",
        on_change=lambda e: validate_password_field()
    )
    error_text = ft.Text("", color=ft.Colors.RED, size=12)
    
    def validate_email(email):
        """Walidacja formatu email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_username_field():
        """Walidacja pola username w czasie rzeczywistym"""
        if new_username.value and len(new_username.value) < 3:
            new_username.error_text = "Min. 3 znaki"
        else:
            new_username.error_text = None
        page.update()
    
    def validate_email_field():
        """Walidacja pola email w czasie rzeczywistym"""
        if new_email.value and not validate_email(new_email.value):
            new_email.error_text = "Nieprawidłowy format email"
        else:
            new_email.error_text = None
        page.update()
    
    def validate_password_field():
        """Walidacja pola hasła w czasie rzeczywistym"""
        if new_password.value and len(new_password.value) < 6:
            new_password.error_text = "Min. 6 znaków"
        else:
            new_password.error_text = None
        page.update()
    
    def load_users():
        try:
            nonlocal all_users_cache
            all_users = api.get_all_users()  # Endpoint admina
            all_users_cache = all_users
            filter_users()
        except Exception as e:
            print(f"❌ Błąd ładowania userów: {e}")
            users_list.controls.clear()
            users_list.controls.append(
                ft.Text(f"❌ Błąd: {str(e)}", color=ft.Colors.RED)
            )
            page.update()
    
    def filter_users():
        """Filtruje użytkowników według wyszukiwania"""
        users_list.controls.clear()
        
        query = search_query.current.lower()
        
        if query:
            filtered = [u for u in all_users_cache 
                       if query in u["username"].lower() or query in u["email"].lower()]
        else:
            filtered = all_users_cache
        
        for u in filtered:
            users_list.controls.append(create_user_card(u))
        
        if filtered:
            stats_text.value = f"Wyświetlono: {len(filtered)} / {len(all_users_cache)} użytkowników"
        else:
            stats_text.value = f"Łącznie użytkowników: {len(all_users_cache)}"
            if query:
                users_list.controls.clear()
                users_list.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.SEARCH_OFF, size=60, color=ft.Colors.GREY_400),
                            ft.Text("Nie znaleziono użytkowników", color=ft.Colors.GREY_600)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        alignment=ft.alignment.center,
                        padding=40
                    )
                )
        
        page.update()
    
    def search_changed(e):
        """Obsługa zmiany w polu wyszukiwania"""
        search_query.current = e.control.value
        filter_users()
    
    def create_user_card(u):
        return ft.Card(
            content=ft.Container(
                content=ft.Row([
                    ft.Icon(
                        ft.Icons.ADMIN_PANEL_SETTINGS if u["is_admin"] else ft.Icons.PERSON,
                        color=ft.Colors.AMBER if u["is_admin"] else ft.Colors.BLUE
                    ),
                    ft.Column([
                        ft.Text(u["username"], weight=ft.FontWeight.BOLD),
                        ft.Text(u["email"], size=12, color=ft.Colors.GREY)
                    ], spacing=2),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color=ft.Colors.RED,
                        tooltip="Usuń",
                        on_click=lambda e: delete_user(u["id"])
                    )
                ]),
                padding=15
            )
        )
    
    def delete_user(user_id):
        try:
            api.delete_user(user_id)
            load_users()
        except Exception as e:
            print(f"❌ Błąd usuwania: {e}")
    
    # ========== KOMPONENT ZARZĄDZANIA TASKAMI ==========
    tasks_widget, load_tasks_callback = create_admin_task_manager(page, api)
    
    def add_user_clicked(e):
        """Otwiera dialog dodawania użytkownika"""
        error_text.value = ""
        new_username.value = ""
        new_email.value = ""
        new_password.value = ""
        new_username.error_text = None
        new_email.error_text = None
        new_password.error_text = None
        dialog.open = True
        page.update()
    
    def create_user_submit(e):
        """Tworzy nowego użytkownika z pełną walidacją"""
        # Wyczyść poprzednie błędy
        error_text.value = ""
        
        # Walidacja pól
        if not new_username.value or not new_email.value or not new_password.value:
            error_text.value = "❌ Wszystkie pola są wymagane"
            page.update()
            return
        
        # Walidacja długości username
        if len(new_username.value) < 3:
            error_text.value = "❌ Nazwa użytkownika musi mieć min. 3 znaki"
            new_username.error_text = "Min. 3 znaki"
            page.update()
            return
        
        # Walidacja formatu email
        if not validate_email(new_email.value):
            error_text.value = "❌ Nieprawidłowy format adresu email"
            new_email.error_text = "Nieprawidłowy format"
            page.update()
            return
        
        # Walidacja długości hasła
        if len(new_password.value) < 6:
            error_text.value = "❌ Hasło musi mieć min. 6 znaków"
            new_password.error_text = "Min. 6 znaków"
            page.update()
            return
        
        try:
            api.create_user(
                username=new_username.value,
                email=new_email.value,
                password=new_password.value
            )
            dialog.open = False
            
            # Wyczyść pola i błędy
            new_username.value = ""
            new_email.value = ""
            new_password.value = ""
            new_username.error_text = None
            new_email.error_text = None
            new_password.error_text = None
            
            load_users()
            page.update()
        except Exception as ex:
            # Parsowanie szczegółowych błędów z API
            error_msg = str(ex)
            
            if "Username already exists" in error_msg or "username" in error_msg.lower():
                error_text.value = f"❌ Użytkownik '{new_username.value}' już istnieje"
                new_username.error_text = "Ta nazwa jest zajęta"
            elif "Email already exists" in error_msg or "email" in error_msg.lower():
                error_text.value = f"❌ Email '{new_email.value}' jest już zarejestrowany"
                new_email.error_text = "Ten email jest zajęty"
            elif "400" in error_msg:
                error_text.value = "❌ Nieprawidłowe dane. Sprawdź wszystkie pola."
            elif "401" in error_msg or "403" in error_msg:
                error_text.value = "❌ Brak uprawnień. Zaloguj się ponownie."
            elif "500" in error_msg:
                error_text.value = "❌ Błąd serwera. Spróbuj ponownie później."
            else:
                error_text.value = f"❌ Błąd: {error_msg}"
            
            page.update()
    
    # Dialog dodawania użytkownika
    dialog = ft.AlertDialog(
        title=ft.Text("Dodaj nowego użytkownika"),
        content=ft.Container(
            content=ft.Column([
                new_username,
                new_email,
                new_password,
                error_text
            ], tight=True, spacing=10),
            width=400
        ),
        actions=[
            ft.TextButton("Anuluj", on_click=lambda e: setattr(dialog, 'open', False) or page.update()),
            ft.ElevatedButton("Dodaj", on_click=create_user_submit)
        ]
    )
    
    page.overlay.append(dialog)
    
    # ========== CONTENERY WIDOKÓW ==========
    search_field = ft.TextField(
        hint_text="🔍 Szukaj użytkownika...",
        prefix_icon=ft.Icons.SEARCH,
        on_change=search_changed,
        width=300,
        height=40,
        text_size=14
    )
    
    users_content = ft.Column([
        ft.Row([
            ft.Text("Zarządzanie Użytkownikami", size=20, weight=ft.FontWeight.BOLD),
            ft.Container(expand=True),
            search_field,
            ft.IconButton(
                icon=ft.Icons.CLEAR,
                tooltip="Wyczyść wyszukiwanie",
                on_click=lambda e: (
                    setattr(search_field, 'value', ""),
                    setattr(search_query, 'current', ""),
                    filter_users()
                )
            ),
            ft.ElevatedButton(
                "Dodaj użytkownika",
                icon=ft.Icons.PERSON_ADD,
                on_click=add_user_clicked
            )
        ]),
        stats_text,
        ft.Divider(),
        ft.Container(
            content=users_list,
            height=750,  # Stała wysokość dla scrollowania
            padding=10,
            bgcolor="#E3F2FD",
            border_radius=10
        )
    ], spacing=15)
    
    # Widget tasków z admin_task_manager
    tasks_content = ft.Container(
        content=tasks_widget,
        expand=True
    )
    
    # Kontener z aktualną zawartością
    content_area_widget = ft.Container(
        content=users_content,
        padding=20,
        expand=True
    )
    content_area = content_area_widget  # Przypisz do zmiennej globalnej
    
    # ========== FUNKCJE PRZEŁĄCZANIA WIDOKÓW ==========
    def switch_to_users(e):
        """Przełącz na widok użytkowników"""
        current_view.current = "users"
        load_users()
        update_view()
    
    def switch_to_tasks(e):
        """Przełącz na widok tasków"""
        current_view.current = "tasks"
        load_tasks_callback()  # Użyj callbacka z komponentu
        update_view()
    
    def update_view():
        """Odśwież widok w zależności od current_view"""
        if current_view.current == "users":
            content_area_widget.content = users_content
            users_tab_btn_widget.bgcolor = ft.Colors.BLUE_700
            tasks_tab_btn_widget.bgcolor = None
        else:
            content_area_widget.content = tasks_content
            users_tab_btn_widget.bgcolor = None
            tasks_tab_btn_widget.bgcolor = ft.Colors.BLUE_700
        page.update()
    
    # Załaduj userów przy starcie
    load_users()
    
    # ========== PRZYCISKI ZAKŁADEK (po definicji funkcji) ==========
    users_tab_btn_widget = ft.ElevatedButton(
        "Użytkownicy",
        icon=ft.Icons.PEOPLE,
        on_click=switch_to_users,
        bgcolor=ft.Colors.BLUE_700
    )
    users_tab_btn = users_tab_btn_widget  # Przypisz do zmiennej globalnej
    
    tasks_tab_btn_widget = ft.ElevatedButton(
        "Wszystkie Taski",
        icon=ft.Icons.TASK,
        on_click=switch_to_tasks
    )
    tasks_tab_btn = tasks_tab_btn_widget  # Przypisz do zmiennej globalnej
    
    # ✅ NAVBAR
    navbar = create_nav_bar(page, user, on_logout=on_logout)
    
    return ft.Column([
        navbar,
        # Zakładki
        ft.Container(
            content=ft.Row([
                users_tab_btn_widget,
                tasks_tab_btn_widget
            ], spacing=10),
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            bgcolor=ft.Colors.BLUE_50
        ),
        # Zawartość
        content_area_widget
    ], spacing=0)