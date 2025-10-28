"""
Script to populate database with sample data
"""
import sys
from pathlib import Path

# Add parent directory to path to enable imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session, select
from api.models import User, Task
from api.db import engine, init_db
from api.auth import hash_password

def seed_database():
    init_db()
    
    with Session(engine) as session:
        existing_admin = session.exec(select(User).where(User.username == "admin")).first()
        
        if not existing_admin:
            admin = User(
                username="admin",
                email="admin@taskmanager.com",
                hashed_password=hash_password("admin123"),
                is_admin=True
            )
            session.add(admin)
            session.commit()
            session.refresh(admin)
        else:
            admin = existing_admin
        
        old_users = session.exec(select(User).where(User.is_admin == False)).all()
        for user in old_users:
            session.delete(user)
        session.commit()
        
        old_tasks = session.exec(select(Task)).all()
        for task in old_tasks:
            session.delete(task)
        session.commit()
        
        # Create new users
        print("\n Creating users...")
        
        users_data = [
            {"username": "john_smith", "email": "john.smith@company.com", "password": "pass123"},
            {"username": "anna_johnson", "email": "anna.johnson@company.com", "password": "pass123"},
            {"username": "peter_williams", "email": "peter.williams@company.com", "password": "pass123"},
            {"username": "mary_brown", "email": "mary.brown@company.com", "password": "pass123"},
            {"username": "chris_jones", "email": "chris.jones@company.com", "password": "pass123"},
            {"username": "maggie_davis", "email": "maggie.davis@company.com", "password": "pass123"},
            {"username": "tom_miller", "email": "tom.miller@company.com", "password": "pass123"},
            {"username": "alice_wilson", "email": "alice.wilson@company.com", "password": "pass123"},
            {"username": "mark_moore", "email": "mark.moore@company.com", "password": "pass123"},
            {"username": "kate_taylor", "email": "kate.taylor@company.com", "password": "pass123"},
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
            print(f"  Created: {user.username} (ID: {user.id})")
        
        print(f"\nCreated {len(created_users)} users")
        
        # Create tasks
        print("\n Creating tasks...")
        
        tasks_data = [
            # Tasks for John Smith
            {"title": "Prepare client presentation", "description": "Presentation should include Q4 results analysis", "completed": True, "owner": created_users[0]},
            {"title": "Review monthly reports", "description": "Verify all invoices and settlements", "completed": False, "owner": created_users[0]},
            {"title": "Update project documentation", "description": "Add new features to README", "completed": False, "owner": created_users[0]},
            {"title": "Team meeting at 2:00 PM", "description": "Sprint planning for next week", "completed": True, "owner": created_users[0]},
            
            # Tasks for Anna Johnson
            {"title": "Code review Pull Request #245", "description": "Check changes in authentication module", "completed": False, "owner": created_users[1]},
            {"title": "Fix bug in login form", "description": "Users report email validation issue", "completed": True, "owner": created_users[1]},
            {"title": "Write unit tests for API", "description": "Minimum 80% code coverage", "completed": False, "owner": created_users[1]},
            {"title": "Update project libraries", "description": "npm audit fix and dependencies update", "completed": False, "owner": created_users[1]},
            {"title": "Optimize database queries", "description": "Add indexes to most frequently used columns", "completed": True, "owner": created_users[1]},
            
            # Tasks for Peter Williams
            {"title": "Setup development environment", "description": "Docker compose for local development", "completed": True, "owner": created_users[2]},
            {"title": "Deploy CI/CD pipeline", "description": "GitHub Actions for automated tests", "completed": False, "owner": created_users[2]},
            {"title": "Configure production monitoring", "description": "Prometheus and Grafana dashboards", "completed": False, "owner": created_users[2]},
            {"title": "Database backup", "description": "Automatic daily backups", "completed": True, "owner": created_users[2]},
            
            # Tasks for Mary Brown
            {"title": "Design new user interface", "description": "Figma mockups for dashboard", "completed": False, "owner": created_users[3]},
            {"title": "Conduct UX testing", "description": "Gather feedback from 10 users", "completed": False, "owner": created_users[3]},
            {"title": "Create style guide", "description": "Component and color scheme documentation", "completed": True, "owner": created_users[3]},
            {"title": "Optimize responsiveness", "description": "Mobile-first approach for all views", "completed": False, "owner": created_users[3]},
            
            # Tasks for Chris Jones
            {"title": "Analyze new module requirements", "description": "Meeting with Product Owner", "completed": True, "owner": created_users[4]},
            {"title": "Write technical specification", "description": "Architecture Decision Records", "completed": False, "owner": created_users[4]},
            {"title": "Estimate tasks in Jira", "description": "Story points for sprint #15", "completed": False, "owner": created_users[4]},
            
            # Tasks for Maggie Davis
            {"title": "Integrate payment system", "description": "Stripe API implementation", "completed": False, "owner": created_users[5]},
            {"title": "Test checkout process", "description": "E2E tests for entire purchase flow", "completed": True, "owner": created_users[5]},
            {"title": "Implement webhooks", "description": "Handle payment notifications", "completed": False, "owner": created_users[5]},
            {"title": "Add transaction logs", "description": "Audit trail for all operations", "completed": False, "owner": created_users[5]},
            
            # Tasks for Tom Miller
            {"title": "Database migration", "description": "PostgreSQL 14 -> 15 upgrade", "completed": True, "owner": created_users[6]},
            {"title": "Optimize SQL performance", "description": "Analyze slow queries", "completed": False, "owner": created_users[6]},
            {"title": "Configure replication", "description": "Master-slave setup for high availability", "completed": False, "owner": created_users[6]},
            
            # Tasks for Alice Wilson
            {"title": "Prepare marketing campaign", "description": "Social media content calendar", "completed": False, "owner": created_users[7]},
            {"title": "Competitor analysis", "description": "Benchmark report Q1 2025", "completed": True, "owner": created_users[7]},
            {"title": "Customer newsletter", "description": "Information about new features", "completed": False, "owner": created_users[7]},
            {"title": "Website update", "description": "New case studies and references", "completed": False, "owner": created_users[7]},
            
            # Tasks for Mark Moore
            {"title": "Code refactoring auth module", "description": "Clean code principles", "completed": False, "owner": created_users[8]},
            {"title": "API endpoints documentation", "description": "Swagger/OpenAPI specification", "completed": True, "owner": created_users[8]},
            {"title": "Implement rate limiting", "description": "DDoS protection", "completed": False, "owner": created_users[8]},
            {"title": "Security audit", "description": "OWASP Top 10 compliance check", "completed": False, "owner": created_users[8]},
            
            # Tasks for Kate Taylor
            {"title": "Train new employees", "description": "Onboarding session for juniors", "completed": True, "owner": created_users[9]},
            {"title": "Prepare tech talk presentation", "description": "Topic: Best practices in React", "completed": False, "owner": created_users[9]},
            {"title": "Code review guidelines", "description": "Team standards", "completed": False, "owner": created_users[9]},
            {"title": "Mentoring session with juniors", "description": "Pair programming Friday", "completed": True, "owner": created_users[9]},
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
        print(f"Created {len(tasks_data)} tasks")
        
        # Summary
        total_users = session.exec(select(User)).all()
        total_tasks = session.exec(select(Task)).all()
        completed_tasks = session.exec(select(Task).where(Task.completed == True)).all()
        
        print("\n" + "="*50)
        print("SUMMARY:")
        print("="*50)
        print(f" Users: {len(total_users)} (including 1 admin)")
        print(f" All tasks: {len(total_tasks)}")
        print(f" Completed: {len(completed_tasks)}")
        print(f" Pending: {len(total_tasks) - len(completed_tasks)}")
        print("="*50)
        print("\nSeeding completed successfully!")
        print("\nLogin credentials:")
        print("   Admin: admin / admin123")
        print("   Users: [username] / pass123")
        print("   Example: john_smith / pass123")

if __name__ == "__main__":
    seed_database()
