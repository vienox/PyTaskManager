import flet as ft
from components.user_navbar import create_user_navbar
from components.user_stats import create_user_stats

def create_user_view(page: ft.Page, api, user, on_logout):
    """
    Create simplified user profile view with task statistics.
    
    Args:
        page: Flet Page instance
        api: APIClient instance
        user: Dictionary containing user data
        on_logout: Callback function for logout action
    """
    
    stats_widget, load_stats_callback = create_user_stats(page, api)
    
    def go_to_tasks(e):
        """Navigate to tasks view."""
        from views.tasks_view import create_tasks_view
        page.controls.clear()
        
        def back_to_profile():
            page.controls.clear()
            page.add(create_user_view(page, api, user, on_logout))
            page.update()
        
        page.add(create_tasks_view(page, api, user, on_logout, on_back_to_profile=back_to_profile))
        page.update()
    
    navbar = create_user_navbar(page, user, on_logout)
    
    view = ft.Column([
        navbar,
        
        ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=100, color=ft.Colors.BLUE),
                
                ft.Text(user["username"], size=28, weight=ft.FontWeight.BOLD),
                ft.Text(user["email"], size=14, color=ft.Colors.GREY),
                
                ft.Divider(height=40),
                
                stats_widget,
                
                ft.Container(height=30),
                
                ft.ElevatedButton(
                    "Manage Tasks",
                    on_click=go_to_tasks,
                    width=300,
                    height=50,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10)
                    )
                ),
                
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=40,
            alignment=ft.alignment.center,
            expand=True
        )
    ], expand=True)
    
    load_stats_callback()
    
    return view