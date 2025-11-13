"""
Standalone script to create the first admin user.

This utility creates an initial administrator account for the Task Manager system.
Use this when you need to create an admin without running the full seed script.

Usage:
    python scripts/create_admin.py
    
    OR from project root:
    cd scripts && python create_admin.py

Default Credentials:
    Username: admin
    Password: admin123
    Email: admin@example.com
    
Notes:
    - Safe to run multiple times (checks if admin already exists)
    - Creates database tables if they don't exist
    - Only creates admin, doesn't modify other data
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from api.models import User
from api.db import engine, init_db
from api.auth import hash_password
from sqlmodel import Session, select


def create_first_admin():
    """
    Create the first admin user in the database.
    
    Creates:
        - Database tables (if they don't exist)
        - Admin user with default credentials (if doesn't exist)
        
    Returns:
        None
        
    Side Effects:
        - Initializes database schema
        - Commits admin user to database
    """
    # Initialize database tables
    init_db()
    
    with Session(engine) as session:
        # Check if admin already exists
        existing = session.exec(select(User).where(User.username == "admin")).first()
        if existing:
            print("✅ Admin user already exists!")
            print(f"   Username: {existing.username}")
            print(f"   Email: {existing.email}")
            return
        
        # Create new admin user
        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=hash_password("admin123"),
            is_admin=True
        )
        session.add(admin)
        session.commit()
        
        print("✅ Admin user created successfully!")
        print("   Username: admin")
        print("   Password: admin123")
        print("   Email: admin@example.com")
        print("\n⚠️  IMPORTANT: Change the default password after first login!")


if __name__ == "__main__":
    create_first_admin()