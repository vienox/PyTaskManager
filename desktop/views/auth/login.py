import flet as ft


def create_login_view(page, api, on_login_success):
    username_field = ft.TextField(label="Username", width=300, autofocus=True)
    password_field = ft.TextField(label="Password", password=True, width=300, can_reveal_password=True)
    error_text = ft.Text(color="red", size=12)
    loading = ft.ProgressRing(visible=False, width=30, height=30)
    
    def login_click(e):
        if not username_field.value or not password_field.value:
            error_text.value = "Fill all fields"
            page.update()
            return
        
        loading.visible = True
        error_text.value = ""
        page.update()
        
        try:
            api.login(username_field.value, password_field.value)
            user = api.get_me()
            on_login_success(user)
        except Exception as err:
            loading.visible = False
            error_msg = str(err)
            if "404" in error_msg:
                error_text.value = f"User '{username_field.value}' not found"
            elif "401" in error_msg:
                error_text.value = "Invalid password"
            elif "500" in error_msg:
                error_text.value = "Server error. Check if backend is running."
            else:
                error_text.value = f"Error: {error_msg}"
            page.update()
    
    page.on_keyboard_event = lambda e: login_click(None) if e.key == "Enter" else None
    
    return ft.Container(
        content=ft.Column([
            ft.Container(height=50),
            ft.Icon(ft.Icons.TASK_ALT, size=80, color=ft.Colors.BLUE),
            ft.Text("Task Manager", size=32, weight=ft.FontWeight.BOLD),
            ft.Text("Log in to continue", size=14, color=ft.Colors.GREY),
            ft.Container(height=30),
            username_field,
            password_field,
            ft.Container(height=10),
            ft.ElevatedButton("Log In", on_click=login_click, width=300, height=45),
            loading,
            error_text
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        alignment=ft.alignment.center,
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#e3f2fd", "#ffffff"]
        )
    )
