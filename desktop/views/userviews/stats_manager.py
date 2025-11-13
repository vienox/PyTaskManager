"""
Statistics management for user profile view.

Handles fetching and updating task statistics.
"""

import flet as ft
from typing import Callable


def create_stats_loader(api, total_text: ft.Text, completed_text: ft.Text, pending_text: ft.Text, page: ft.Page) -> Callable:
    """
    Create function to load and update task statistics.
    
    Args:
        api: API client instance
        total_text: Text component for total count
        completed_text: Text component for completed count
        pending_text: Text component for pending count
        page: Flet Page for updates
        
    Returns:
        callable: Function to call for loading stats
    """
    def load_stats():
        """Fetch and display task statistics from API."""
        try:
            tasks = api.get_tasks()
            total = len(tasks)
            completed = len([t for t in tasks if t["completed"]])
            pending = total - completed
            
            total_text.value = str(total)
            completed_text.value = str(completed)
            pending_text.value = str(pending)
            
            page.update()
        except Exception as e:
            print(f"Error loading stats: {e}")
    
    return load_stats
