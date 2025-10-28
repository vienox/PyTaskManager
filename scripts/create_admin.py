"""Script to create first admin user"""
import sys
from pathlib import Path

# Add parent directory to path to enable imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.models import User
from api.db import engine, init_db
from api.auth import hash_password
from sqlmodel import Session, select

def create_first_admin():
    # First create tables in database
    init_db()
    
    with Session(engine) as session:
        # Check if admin already exists
        existing = session.exec(select(User).where(User.username == "admin")).first()
        if existing:
            print("Admin already exists!")
            return
        
        # Create admin
        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=hash_password("admin123"),
            is_admin=True
        )
        session.add(admin)
        session.commit()
        print("  Admin created!")
        print("   Username: admin")
        print("   Password: admin123")

if __name__ == "__main__":
    create_first_admin()