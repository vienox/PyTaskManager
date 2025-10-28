"""
Skrypt do wypełnienia bazy danych przykładowymi danymi
"""
from sqlmodel import Session, select
from api.models import User, Task
from api.db import engine, init_db
from api.auth import hash_password

def seed_database():
    """Wypełnia bazę danych przykładowymi użytkownikami i taskami"""
    
    print("🌱 Rozpoczynam seedowanie bazy danych...")
    
    # Inicjalizuj bazę
    init_db()
    
    with Session(engine) as session:
        # Sprawdź czy admin już istnieje
        existing_admin = session.exec(select(User).where(User.username == "admin")).first()
        
        if not existing_admin:
            print("➕ Tworzę administratora...")
            admin = User(
                username="admin",
                email="admin@taskmanager.com",
                hashed_password=hash_password("admin123"),
                is_admin=True
            )
            session.add(admin)
            session.commit()
            session.refresh(admin)
            print(f"✅ Admin utworzony (ID: {admin.id})")
        else:
            admin = existing_admin
            print(f"✅ Admin już istnieje (ID: {admin.id})")
        
        # Usuń starych użytkowników (oprócz admina)
        print("🗑️ Czyszczę starych użytkowników...")
        old_users = session.exec(select(User).where(User.is_admin == False)).all()
        for user in old_users:
            session.delete(user)
        session.commit()
        
        # Usuń stare taski
        print("🗑️ Czyszczę stare taski...")
        old_tasks = session.exec(select(Task)).all()
        for task in old_tasks:
            session.delete(task)
        session.commit()
        
        # Twórz nowych użytkowników
        print("\n👥 Tworzę użytkowników...")
        
        users_data = [
            {"username": "jan_kowalski", "email": "jan.kowalski@firma.pl", "password": "haslo123"},
            {"username": "anna_nowak", "email": "anna.nowak@firma.pl", "password": "haslo123"},
            {"username": "piotr_wisniewski", "email": "piotr.wisniewski@firma.pl", "password": "haslo123"},
            {"username": "maria_wojcik", "email": "maria.wojcik@firma.pl", "password": "haslo123"},
            {"username": "krzysztof_kowalczyk", "email": "krzysztof.kowalczyk@firma.pl", "password": "haslo123"},
            {"username": "magdalena_kaminska", "email": "magdalena.kaminska@firma.pl", "password": "haslo123"},
            {"username": "tomasz_lewandowski", "email": "tomasz.lewandowski@firma.pl", "password": "haslo123"},
            {"username": "agnieszka_zielinska", "email": "agnieszka.zielinska@firma.pl", "password": "haslo123"},
            {"username": "marcin_szymanski", "email": "marcin.szymanski@firma.pl", "password": "haslo123"},
            {"username": "katarzyna_wozniak", "email": "katarzyna.wozniak@firma.pl", "password": "haslo123"},
        ]
        
        created_users = []
        for user_data in users_data:
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                hashed_password=hash_password(user_data["password"]),
                is_admin=False
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            created_users.append(user)
            print(f"  ✅ {user.username} (ID: {user.id})")
        
        print(f"\n✅ Utworzono {len(created_users)} użytkowników")
        
        # Twórz taski
        print("\n📝 Tworzę taski...")
        
        tasks_data = [
            # Taski dla Jan Kowalski
            {"title": "Przygotować prezentację dla klienta", "description": "Prezentacja powinna zawierać analizę wyników Q4", "completed": True, "owner": created_users[0]},
            {"title": "Sprawdzić raporty miesięczne", "description": "Zweryfikować wszystkie faktury i rozliczenia", "completed": False, "owner": created_users[0]},
            {"title": "Zaktualizować dokumentację projektu", "description": "Dodać nowe funkcjonalności do README", "completed": False, "owner": created_users[0]},
            {"title": "Spotkanie z zespołem o 14:00", "description": "Sprint planning na następny tydzień", "completed": True, "owner": created_users[0]},
            
            # Taski dla Anna Nowak
            {"title": "Code review Pull Request #245", "description": "Sprawdzić zmiany w module autentykacji", "completed": False, "owner": created_users[1]},
            {"title": "Naprawić bug w formularzu logowania", "description": "Users zgłaszają problem z walidacją email", "completed": True, "owner": created_users[1]},
            {"title": "Napisać testy jednostkowe dla API", "description": "Pokrycie minimum 80% kodu", "completed": False, "owner": created_users[1]},
            {"title": "Zaktualizować biblioteki projektu", "description": "npm audit fix i aktualizacja dependencies", "completed": False, "owner": created_users[1]},
            {"title": "Zoptymalizować zapytania do bazy", "description": "Dodać indeksy do najczęściej używanych kolumn", "completed": True, "owner": created_users[1]},
            
            # Taski dla Piotr Wiśniewski
            {"title": "Przygotować środowisko deweloperskie", "description": "Docker compose dla lokalnego developmentu", "completed": True, "owner": created_users[2]},
            {"title": "Wdrożyć CI/CD pipeline", "description": "GitHub Actions dla automatycznych testów", "completed": False, "owner": created_users[2]},
            {"title": "Konfiguracja monitoring production", "description": "Prometheus i Grafana dashboardy", "completed": False, "owner": created_users[2]},
            {"title": "Backup bazy danych", "description": "Automatyczne daily backupy", "completed": True, "owner": created_users[2]},
            
            # Taski dla Maria Wojcik
            {"title": "Zaprojektować nowy interfejs użytkownika", "description": "Figma mockupy dla dashboardu", "completed": False, "owner": created_users[3]},
            {"title": "Przeprowadzić testy UX", "description": "Zebrać feedback od 10 użytkowników", "completed": False, "owner": created_users[3]},
            {"title": "Stworzyć style guide", "description": "Dokumentacja komponentów i kolorystyki", "completed": True, "owner": created_users[3]},
            {"title": "Optymalizacja responsywności", "description": "Mobile-first approach dla wszystkich widoków", "completed": False, "owner": created_users[3]},
            
            # Taski dla Krzysztof Kowalczyk
            {"title": "Analiza wymagań nowego modułu", "description": "Spotkanie z Product Ownerem", "completed": True, "owner": created_users[4]},
            {"title": "Napisać specyfikację techniczną", "description": "Architecture Decision Records", "completed": False, "owner": created_users[4]},
            {"title": "Estymacja zadań w Jira", "description": "Story points dla sprintu #15", "completed": False, "owner": created_users[4]},
            
            # Taski dla Magdalena Kamińska
            {"title": "Integracja z systemem płatności", "description": "Stripe API implementation", "completed": False, "owner": created_users[5]},
            {"title": "Testowanie procesu checkout", "description": "E2E testy dla całego flow zakupowego", "completed": True, "owner": created_users[5]},
            {"title": "Implementacja webhooków", "description": "Obsługa powiadomień o płatnościach", "completed": False, "owner": created_users[5]},
            {"title": "Dodać logi transakcji", "description": "Audit trail dla wszystkich operacji", "completed": False, "owner": created_users[5]},
            
            # Taski dla Tomasz Lewandowski
            {"title": "Migracja bazy danych", "description": "PostgreSQL 14 -> 15 upgrade", "completed": True, "owner": created_users[6]},
            {"title": "Optymalizacja wydajności SQL", "description": "Analyze slow queries", "completed": False, "owner": created_users[6]},
            {"title": "Konfiguracja replikacji", "description": "Master-slave setup dla high availability", "completed": False, "owner": created_users[6]},
            
            # Taski dla Agnieszka Zielińska
            {"title": "Przygotować kampanię marketingową", "description": "Social media content calendar", "completed": False, "owner": created_users[7]},
            {"title": "Analiza konkurencji", "description": "Benchmark report Q1 2025", "completed": True, "owner": created_users[7]},
            {"title": "Newsletter do klientów", "description": "Informacja o nowych funkcjach", "completed": False, "owner": created_users[7]},
            {"title": "Aktualizacja strony www", "description": "Nowe case studies i referencje", "completed": False, "owner": created_users[7]},
            
            # Taski dla Marcin Szymański
            {"title": "Code refactoring modułu auth", "description": "Clean code principles", "completed": False, "owner": created_users[8]},
            {"title": "Dokumentacja API endpoints", "description": "Swagger/OpenAPI specification", "completed": True, "owner": created_users[8]},
            {"title": "Implementacja rate limiting", "description": "Zabezpieczenie przed DDoS", "completed": False, "owner": created_users[8]},
            {"title": "Security audit", "description": "OWASP Top 10 compliance check", "completed": False, "owner": created_users[8]},
            
            # Taski dla Katarzyna Woźniak
            {"title": "Szkolenie nowych pracowników", "description": "Onboarding session dla juniorów", "completed": True, "owner": created_users[9]},
            {"title": "Przygotować prezentację tech talk", "description": "Temat: Best practices w React", "completed": False, "owner": created_users[9]},
            {"title": "Code review guidelines", "description": "Standardy dla zespołu", "completed": False, "owner": created_users[9]},
            {"title": "Mentoring sesja z juniorami", "description": "Pair programming Friday", "completed": True, "owner": created_users[9]},
        ]
        
        for task_data in tasks_data:
            task = Task(
                title=task_data["title"],
                description=task_data["description"],
                completed=task_data["completed"],
                owner_id=task_data["owner"].id
            )
            session.add(task)
        
        session.commit()
        print(f"✅ Utworzono {len(tasks_data)} tasków")
        
        # Podsumowanie
        total_users = session.exec(select(User)).all()
        total_tasks = session.exec(select(Task)).all()
        completed_tasks = session.exec(select(Task).where(Task.completed == True)).all()
        
        print("\n" + "="*50)
        print("📊 PODSUMOWANIE:")
        print("="*50)
        print(f"👥 Użytkownicy: {len(total_users)} (w tym 1 admin)")
        print(f"📝 Wszystkie taski: {len(total_tasks)}")
        print(f"✅ Ukończone: {len(completed_tasks)}")
        print(f"⏳ Do zrobienia: {len(total_tasks) - len(completed_tasks)}")
        print("="*50)
        print("\n✨ Seedowanie zakończone pomyślnie!")
        print("\n🔑 Dane logowania:")
        print("   Admin: admin / admin123")
        print("   Użytkownicy: [nazwa_użytkownika] / haslo123")
        print("   Przykład: jan_kowalski / haslo123")

if __name__ == "__main__":
    seed_database()
