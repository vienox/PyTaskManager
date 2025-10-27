import flet as ft
from api_client import APIClient
from components.nav_bar import create_nav_bar

def create_admin_view(page: ft.Page, api, user, on_logout):
    """Panel admina - zarządzanie użytkownikami"""
    
    users_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=10)
    stats_text = ft.Text("", size=14, color=ft.Colors.GREY)
    
    def load_users():
        try:
            all_users = api.get_all_users()  # Endpoint admina
            users_list.controls.clear()
            
            for u in all_users:
                users_list.controls.append(create_user_card(u))
            
            stats_text.value = f"👥 Łącznie użytkowników: {len(all_users)}"
            page.update()
        except Exception as e:
            print(f"❌ Błąd ładowania userów: {e}")
    
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
    
    # Załaduj userów przy starcie
    load_users()
    
    # ✅ NAVBAR
    navbar = create_nav_bar(page, user, on_logout=on_logout)
    
    return ft.Column([
        navbar,  # ✅ Dodaj navbar
        ft.Container(
            content=ft.Column([
                ft.Text("🛡️ Panel Administratora", size=24, weight=ft.FontWeight.BOLD),
                stats_text,
                ft.Divider(),
                users_list
            ], spacing=15),
            padding=20,
            expand=True
        )
    ], spacing=0)