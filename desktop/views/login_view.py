import flet as ft
from api_client import APIClient

def create_login_view(page: ft.Page, api, on_login_success):
    """
    Widok logowania
    
    Args:
        page: Flet Page
        api: APIClient instance
        on_login_success: callback(user) - wywołany po udanym logowaniu
    """
    
    username_field = ft.TextField(
        label="Username",
        width=300,
        autofocus=True,
        prefix_icon=ft.Icons.PERSON
    )
    
    password_field = ft.TextField(
        label="Password",
        password=True,
        width=300,
        prefix_icon=ft.Icons.LOCK,
        can_reveal_password=True
    )
    
    error_text = ft.Text(color="red", size=12)
    loading = ft.ProgressRing(visible=False, width=30, height=30)
    
    def login_click(e):
        # Walidacja
        if not username_field.value or not password_field.value:
            error_text.value = "⚠️ Wypełnij wszystkie pola"
            page.update()
            return
        
        # Pokaż loading
        loading.visible = True
        error_text.value = ""
        page.update()
        
        try:
            # Logowanie przez API
            api.login(username_field.value, password_field.value)
            
            # Pobierz dane usera
            user = api.get_me()
            
            # Callback - przekaż dane usera
            on_login_success(user)
            
        except Exception as err:
            loading.visible = False
            error_msg = str(err)
            
            # Szczegółowe komunikaty błędów
            if "404" in error_msg or "User not found" in error_msg:
                error_text.value = f"❌ Nie znaleziono użytkownika '{username_field.value}'"
            elif "401" in error_msg or "Invalid password" in error_msg:
                error_text.value = "❌ Nieprawidłowe hasło"
            elif "500" in error_msg:
                error_text.value = "❌ Błąd serwera. Sprawdź czy backend działa."
            else:
                error_text.value = f"❌ Błąd logowania: {error_msg}"
            
            page.update()
    
    # Enter key = login
    def on_key_press(e: ft.KeyboardEvent):
        if e.key == "Enter":
            login_click(None)
    
    page.on_keyboard_event = on_key_press
    
    return ft.Container(
        content=ft.Column([
            ft.Container(height=50),  # spacer
            ft.Icon(ft.Icons.TASK_ALT, size=80, color=ft.Colors.BLUE),
            ft.Text(
                "Task Manager",
                size=32,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Text(
                "Zaloguj się aby kontynuować",
                size=14,
                color=ft.Colors.GREY,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Container(height=30),
            username_field,
            password_field,
            ft.Container(height=10),
            ft.ElevatedButton(
                "Zaloguj",
                on_click=login_click,
                width=300,
                height=45,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10)
                )
            ),
            loading,
            error_text,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center,
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#e3f2fd", "#ffffff"]
        )
    )