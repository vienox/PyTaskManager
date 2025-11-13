"""
Task Manager Desktop Application - Main Entry Point.

This is the primary entry point for the Flet-based desktop client.
Manages application window, navigation, and user session state.

Architecture:
    - Flet GUI framework (Flutter-based Python UI)
    - Communicates with FastAPI backend via HTTP/REST
    - Role-based routing (admin vs regular user views)
    - Stateful navigation with callbacks

Navigation Flow:
    Login → User Profile (regular) or Admin Panel (admin) → Tasks View
    
Usage:
    python main.py
    
Prerequisites:
    - Backend API must be running on http://127.0.0.1:8000
    - Database must be seeded with at least one user
"""

import flet as ft
from api_client import APIClient
from views.login_view import create_login_view
from views.userviews import create_user_view
from views.tasks_view import create_tasks_view
from views.adminviews import create_admin_view


def main(page: ft.Page):
<<<<<<< HEAD
    """
    Main application entry point and navigation controller.
    
    Initializes the Flet page with window settings and manages view navigation.
    
    Args:
        page: Flet Page object (main application window)
        
    Window Configuration:
        - Title: "Task Manager"
        - Size: 900x700 (min: 600x500)
        - Theme: Light mode
        
    State Management:
        - api: APIClient instance (shared across views)
        - current_user: Current logged-in user dict (None when logged out)
    """
    # Window configuration
=======
    """Main application entry point."""
>>>>>>> 6124b066d07b1027ac1e7848f2c94c660b46e332
    page.title = "Task Manager"
    page.window_width = 900
    page.window_height = 700
    page.window_min_width = 600
    page.window_min_height = 500
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    
    # Shared state
    api = APIClient()
    current_user = None
    
    # ============ Navigation Functions ============
    
    def show_login():
<<<<<<< HEAD
        """
        Display login screen.
        
        Clears current view and shows login form.
        On successful login, routes to appropriate view based on user role.
        """
=======
        """Display login view."""
>>>>>>> 6124b066d07b1027ac1e7848f2c94c660b46e332
        page.controls.clear()
        
        def on_login_success(user):
            """
            Callback for successful login.
            
            Args:
                user: User dict from API (id, username, email, is_admin)
            """
            nonlocal current_user
            current_user = user
<<<<<<< HEAD
            print(f"Logged in: {user}")
            
            # Role-based routing
            if user["is_admin"]:
                print("Navigating to admin panel")
                show_admin()
            else:
                print("Navigating to user profile")
=======
            if user["is_admin"]:
                show_admin()
            else:
>>>>>>> 6124b066d07b1027ac1e7848f2c94c660b46e332
                show_user_profile()
        
        page.add(create_login_view(page, api, on_login_success))
        page.update()
    
    def show_user_profile():
<<<<<<< HEAD
        """
        Display user profile dashboard (regular users only).
        
        Shows user information and task statistics.
        Provides navigation to tasks view.
        """
        print("Showing user profile")
=======
        """Display user profile view with statistics dashboard."""
>>>>>>> 6124b066d07b1027ac1e7848f2c94c660b46e332
        page.controls.clear()
        try:
            page.add(create_user_view(page, api, current_user, on_logout=show_login))
            page.update()
        except Exception as e:
<<<<<<< HEAD
            print(f"Error in user_view: {e}")
=======
>>>>>>> 6124b066d07b1027ac1e7848f2c94c660b46e332
            import traceback
            traceback.print_exc()
    
    def show_tasks():
<<<<<<< HEAD
        """
        Display tasks view (regular users).
        
        Shows task list with CRUD operations for current user's tasks.
        """
        print("Showing tasks view")
=======
        """Display tasks view for regular user."""
>>>>>>> 6124b066d07b1027ac1e7848f2c94c660b46e332
        page.controls.clear()
        try:
            page.add(create_tasks_view(page, api, current_user, on_logout=show_login, on_back_to_profile=show_user_profile))
            page.update()
        except Exception as e:
<<<<<<< HEAD
            print(f"Error in tasks_view: {e}")
=======
>>>>>>> 6124b066d07b1027ac1e7848f2c94c660b46e332
            import traceback
            traceback.print_exc()
    
    def show_admin():
<<<<<<< HEAD
        """
        Display admin panel (admins only).
        
        Shows user management and system-wide task management interface.
        Accessible only to users with is_admin=True.
        """
        print("Showing admin panel")
=======
        """Display admin panel."""
>>>>>>> 6124b066d07b1027ac1e7848f2c94c660b46e332
        page.controls.clear()
        try:
            page.add(create_admin_view(page, api, current_user, on_logout=show_login))
            page.update()
<<<<<<< HEAD
            print("Admin panel loaded")
        except Exception as e:
            print(f"Error in admin_view: {e}")
            import traceback
            traceback.print_exc()
    
    # ============ Application Start ============
    # Show login screen on startup
=======
        except Exception as e:
            import traceback
            traceback.print_exc()
    
    # Initialize application with login view
>>>>>>> 6124b066d07b1027ac1e7848f2c94c660b46e332
    show_login()


if __name__ == "__main__":
    # Launch Flet application
    ft.app(target=main)