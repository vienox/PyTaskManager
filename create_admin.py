"""Skrypt do stworzenia pierwszego admina"""
from api.models import User
from api.db import engine, init_db
from api.auth import hash_password
from sqlmodel import Session, select

def create_first_admin():
    # Najpierw utwórz tabele w bazie danych
    init_db()
    
    with Session(engine) as session:
        # Sprawdź czy admin już istnieje
        existing = session.exec(select(User).where(User.username == "admin")).first()
        if existing:
            print("⚠️ Admin już istnieje!")
            return
        
        # Utwórz admina
        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=hash_password("admin123"),
            is_admin=True
        )
        session.add(admin)
        session.commit()
        print("✅ Admin utworzony!")
        print("   Username: admin")
        print("   Password: admin123")

if __name__ == "__main__":
    create_first_admin()