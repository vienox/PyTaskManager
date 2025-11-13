"""
Desktop application configuration.

Centralized configuration constants for the Flet desktop client.

Configuration:
    API_BASE_URL: Backend API endpoint (must match running FastAPI server)
    
Notes:
    - Ensure backend is running on this URL before starting desktop app
    - In production, load from environment variables or config file
"""

# Backend API base URL
# The FastAPI server must be running on this address
API_BASE_URL = "http://127.0.0.1:8000"