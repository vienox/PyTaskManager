import flet as ft
from api_client import APIClient

def create_admin_view(page: ft.Page, api, user, on_logout):
    """
    Panel admina - zarządzanie użytkownikami
    
    Args:
        page: Flet Page
        api: APIClient instance
        user: dict z danymi admina
        on_logout: callback - wylogowanie
    """
    
    users_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=10)
    stats_text = ft.Text("", size=14, color=ft.colors.GREY)
    
    def load_users():
        """Pobierz wszystkich userów"""
        users_list.controls.clear()
        
        try:
            users = api.get_all_users()
            stats_text.value = f"Łącznie użytkowników: {len(users)}"
            
            if not users:
                users_list.controls.append(
                    ft.Text("Brak użytkowników", italic=True)
                )
            else:
                for u in users:
                    users_list.controls.append(create_user_card(u))
                    
        except Exception as e:
            users_list.controls.append(
                ft.Text(f"❌ Błąd: {str(e)}", color="red")
            )
        
        page.update()
    
    def create_user_card(u):
        """Karta użytkownika"""
        
        def delete_user_click(e):
            # Confirm dialog
            def confirm_delete(e):
                try:
                    api.delete_user(u["id"])
                    load_users()
                    page.dialog.open = False
                    page.update()
                except Exception as err:
                    print(f"Błąd usuwania: {err}")
            
            confirm_dialog = ft.AlertDialog(
                title=ft.Text("⚠️ Usuń użytkownika?"),
                content=ft.Text(f"Czy na pewno usunąć {u['username']}?"),
                actions=[
                    ft.TextButton("Anuluj", on_click=lambda e: close_dialog()),
                    ft.ElevatedButton(
                        "Usuń",
                        on_click=confirm_delete,
                        style=ft.ButtonStyle(bgcolor=ft.colors.RED)
                    )
                ]
            )
            
            page.dialog = confirm_dialog
            confirm_dialog.open = True
            page.update()
        
        def make_admin_click(e):
            try:
                api.make_admin(u["id"])
                load_users()
            except Exception as err:
                print(f"Błąd: {err}")
        
        # Badge roli
        role_badge = ft.Container(
            content=ft.Text(
                "ADMIN" if u["is_admin"] else "USER",
                size=10,
                color="white",
                weight=ft.FontWeight.BOLD
            ),
            bgcolor=ft.colors.RED if u["is_admin"] else ft.colors.BLUE,
            padding=ft.padding.symmetric(horizontal=10, vertical=5),
            border_radius=5
        )
        
        return ft.Card(
            content=ft.Container(
                content=ft.Row([
                    ft.Icon(
                        ft.icons.ADMIN_PANEL_SETTINGS if u["is_admin"] else ft.icons.PERSON,
                        size=40,
                        color=ft.colors.RED if u["is_admin"] else ft.colors.BLUE
                    ),
                    ft.Column([
                        ft.Text(u["username"], weight=ft.FontWeight.BOLD, size=16),
                        ft.Text(u["email"], size=12, color=ft.colors.GREY)
                    ], expand=True, spacing=5),
                    role_badge,
                    ft.IconButton(
                        ft.icons.SECURITY,
                        on_click=make_admin_click,
                        icon_color=ft.colors.ORANGE,
                        tooltip="Nadaj uprawnienia admin",
                        disabled=u["is_admin"]
                    ),
                    ft.IconButton(
                        ft.icons.DELETE,
                        on_click=delete_user_click,
                        icon_color=ft.colors.RED,
                        tooltip="Usuń użytkownika",
                        disabled=u["id"] == user["id"]  # nie może usunąć siebie
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=15
            ),
            elevation=2
        )
    
    # ========== DIALOG TWORZENIA USERA ==========
    new_username = ft.TextField(label="Username *", width=400, autofocus=True)
    new_email = ft.TextField(label="Email *", width=400)
    new_password = ft.TextField(label="Hasło *", password=True, width=400, can_reveal_password=True)
    create_error = ft.Text(color="red", size=12)
    
    def create_user_click(e):
        # Walidacja
        if not new_username.value or not new_email.value or not new_password.value:
            create_error.value = "⚠️ Wypełnij wszystkie pola"
            page.update()
            return
        
        try:
            api.create_user(new_username.value, new_email.value, new_password.value)
            new_username.value = ""
            new_email.value = ""
            new_password.value = ""
            create_error.value = ""
            load_users()
            page.dialog.open = False
            page.update()
        except Exception as err:
            create_error.value = f"❌ {str(err)}"
            page.update()
    
    create_dialog = ft.AlertDialog(
        title=ft.Text("➕ Dodaj Użytkownika"),
        content=ft.Column([
            new_username,
            new_email,
            new_password,
            create_error
        ], tight=True, spacing=10),
        actions=[
            ft.TextButton("Anuluj", on_click=lambda e: close_dialog()),
            ft.ElevatedButton("Utwórz", on_click=create_user_click)
        ]
    )
    
    def close_dialog():
        page.dialog.open = False
        create_error.value = ""
        page.update()
    
    def show_create_dialog(e):
        new_username.value = ""
        new_email.value = ""
        new_password.value = ""
        create_error.value = ""
        page.dialog = create_dialog
        create_dialog.open = True
        page.update()
    
    # ========== MAIN VIEW ==========
    view = ft.Column([
        ft.AppBar(
            title=ft.Text("🛡️ Panel Admina"),
            actions=[
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            text=f"👑 {user['username']} (Admin)",
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
            bgcolor=ft.colors.RED
        ),
        ft.Container(
            content=ft.Row([
                stats_text,
            ]),
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            bgcolor=ft.colors.GREY_200
        ),
        ft.Container(
            content=users_list,
            padding=20,
            expand=True
        ),
        ft.FloatingActionButton(
            icon=ft.icons.PERSON_ADD,
            on_click=show_create_dialog,
            tooltip="Dodaj użytkownika",
            bgcolor=ft.colors.RED
        )
    ], expand=True)
    
    # Załaduj userów
    load_users()
    
    return view