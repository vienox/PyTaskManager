"""
Database seeding script for Task Manager application.

This script populates the database with sample users and tasks for testing and demonstration.
It creates:
    - 1 admin user (admin/admin123)
    - 10 regular users with realistic names and emails
    - 40 tasks distributed across users with varied content

Usage:
    python seed_data.py
    
Warning:
    This script clears existing users (except admin) and all tasks before seeding.
    Do NOT run in production environments with real data.
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlmodel import Session, select
from api.models import User, Task
from api.db import engine, init_db
from api.auth import hash_password


def seed_database():
    """
    Populate database with sample users and tasks.
    
    Creates:
        - 1 admin user (if doesn't exist)
        - 10 regular users (clears existing non-admin users first)
        - 40 tasks distributed across users (clears all existing tasks first)
        
    Returns:
        None
    
    Side Effects:
        - Deletes all existing non-admin users
        - Deletes all existing tasks
        - Commits new data to database
    """
    
    print("🌱 Starting database seeding...")
    
    # Initialize database tables
    init_db()
    
    with Session(engine) as session:
        # ============ Create Admin User ============
        existing_admin = session.exec(select(User).where(User.username == "admin")).first()
        
        if not existing_admin:
            print("Creating administrator...")
            admin = User(
                username="admin",
                email="admin@taskmanager.com",
                hashed_password=hash_password("admin123"),
                is_admin=True
            )
            session.add(admin)
            session.commit()
            session.refresh(admin)
            print(f"Admin created (ID: {admin.id})")
        else:
            admin = existing_admin
            print(f" Admin already exists (ID: {admin.id})")
        
        # ============ Clear Existing Data ============
        print("🗑️ Clearing existing users (keeping admin)...")
        old_users = session.exec(select(User).where(User.is_admin == False)).all()
        for user in old_users:
            session.delete(user)
        session.commit()
        
        print("Clearing existing tasks...")
        old_tasks = session.exec(select(Task)).all()
        for task in old_tasks:
            session.delete(task)
        session.commit()
        
        # ============ Create Regular Users ============
        print("\n👥 Creating users...")
        
        users_data = [
            {"username": "john_smith", "email": "john.smith@company.com", "password": "password123"},
            {"username": "emma_johnson", "email": "emma.johnson@company.com", "password": "password123"},
            {"username": "michael_brown", "email": "michael.brown@company.com", "password": "password123"},
            {"username": "sarah_davis", "email": "sarah.davis@company.com", "password": "password123"},
            {"username": "david_wilson", "email": "david.wilson@company.com", "password": "password123"},
            {"username": "lisa_anderson", "email": "lisa.anderson@company.com", "password": "password123"},
            {"username": "robert_taylor", "email": "robert.taylor@company.com", "password": "password123"},
            {"username": "jennifer_thomas", "email": "jennifer.thomas@company.com", "password": "password123"},
            {"username": "william_martinez", "email": "william.martinez@company.com", "password": "password123"},
            {"username": "amanda_garcia", "email": "amanda.garcia@company.com", "password": "password123"},
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
        
        print(f"\n✅ Created {len(created_users)} users")
        
        # ============ Create Tasks ============
        print("\n📝 Creating tasks...")
        
        tasks_data = [
            # Tasks for John Smith
            {"title": "Prepare client presentation", "description": "Create Q4 performance analysis slides", "completed": True, "owner": created_users[0]},
            {"title": "Review monthly reports", "description": "Verify all invoices and reconciliations", "completed": False, "owner": created_users[0]},
            {"title": "Update project documentation", "description": "Add new features to README file", "completed": False, "owner": created_users[0]},
            {"title": "Team meeting at 2:00 PM", "description": "Sprint planning for next week", "completed": True, "owner": created_users[0]},
            
            # Tasks for Emma Johnson
            {"title": "Code review Pull Request #245", "description": "Review authentication module changes", "completed": False, "owner": created_users[1]},
            {"title": "Fix login form bug", "description": "Users reporting email validation issues", "completed": True, "owner": created_users[1]},
            {"title": "Write unit tests for API", "description": "Minimum 80% code coverage required", "completed": False, "owner": created_users[1]},
            {"title": "Update project dependencies", "description": "Run npm audit fix and update packages", "completed": False, "owner": created_users[1]},
            {"title": "Optimize database queries", "description": "Add indexes to frequently queried columns", "completed": True, "owner": created_users[1]},
            
            # Tasks for Michael Brown
            {"title": "Setup development environment", "description": "Docker compose for local development", "completed": True, "owner": created_users[2]},
            {"title": "Implement CI/CD pipeline", "description": "GitHub Actions for automated testing", "completed": False, "owner": created_users[2]},
            {"title": "Configure production monitoring", "description": "Setup Prometheus and Grafana dashboards", "completed": False, "owner": created_users[2]},
            {"title": "Database backup automation", "description": "Implement daily backup scripts", "completed": True, "owner": created_users[2]},
            
            # Tasks for Sarah Davis
            {"title": "Design new user interface", "description": "Create Figma mockups for dashboard", "completed": False, "owner": created_users[3]},
            {"title": "Conduct UX testing", "description": "Gather feedback from 10 users", "completed": False, "owner": created_users[3]},
            {"title": "Create style guide", "description": "Document UI components and color schemes", "completed": True, "owner": created_users[3]},
            {"title": "Improve mobile responsiveness", "description": "Mobile-first approach for all views", "completed": False, "owner": created_users[3]},
            
            # Tasks for David Wilson
            {"title": "Analyze new module requirements", "description": "Meeting with Product Owner scheduled", "completed": True, "owner": created_users[4]},
            {"title": "Write technical specification", "description": "Create Architecture Decision Records", "completed": False, "owner": created_users[4]},
            {"title": "Estimate Jira tasks", "description": "Story points for sprint #15", "completed": False, "owner": created_users[4]},
            
            # Tasks for Lisa Anderson
            {"title": "Integrate payment system", "description": "Implement Stripe API integration", "completed": False, "owner": created_users[5]},
            {"title": "Test checkout process", "description": "End-to-end tests for purchase flow", "completed": True, "owner": created_users[5]},
            {"title": "Implement webhooks", "description": "Handle payment notification callbacks", "completed": False, "owner": created_users[5]},
            {"title": "Add transaction logging", "description": "Audit trail for all payment operations", "completed": False, "owner": created_users[5]},
            
            # Tasks for Robert Taylor
            {"title": "Database migration", "description": "Upgrade PostgreSQL 14 to 15", "completed": True, "owner": created_users[6]},
            {"title": "Optimize SQL performance", "description": "Analyze and fix slow queries", "completed": False, "owner": created_users[6]},
            {"title": "Configure database replication", "description": "Master-slave setup for high availability", "completed": False, "owner": created_users[6]},
            
            # Tasks for Jennifer Thomas
            {"title": "Prepare marketing campaign", "description": "Create social media content calendar", "completed": False, "owner": created_users[7]},
            {"title": "Competitor analysis", "description": "Q1 2025 benchmark report", "completed": True, "owner": created_users[7]},
            {"title": "Customer newsletter", "description": "Announce new product features", "completed": False, "owner": created_users[7]},
            {"title": "Update company website", "description": "Add new case studies and testimonials", "completed": False, "owner": created_users[7]},
            
            # Tasks for William Martinez
            {"title": "Refactor authentication module", "description": "Apply clean code principles", "completed": False, "owner": created_users[8]},
            {"title": "Document API endpoints", "description": "Create Swagger/OpenAPI specification", "completed": True, "owner": created_users[8]},
            {"title": "Implement rate limiting", "description": "DDoS protection for public endpoints", "completed": False, "owner": created_users[8]},
            {"title": "Security audit", "description": "OWASP Top 10 compliance check", "completed": False, "owner": created_users[8]},
            
            # Tasks for Amanda Garcia
            {"title": "New employee training", "description": "Onboarding session for junior developers", "completed": True, "owner": created_users[9]},
            {"title": "Prepare tech talk presentation", "description": "Topic: React best practices", "completed": False, "owner": created_users[9]},
            {"title": "Code review guidelines", "description": "Establish team coding standards", "completed": False, "owner": created_users[9]},
            {"title": "Junior mentoring session", "description": "Pair programming Friday afternoon", "completed": True, "owner": created_users[9]},
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
        print(f"✅ Created {len(tasks_data)} tasks")
        
        # ============ Summary Statistics ============
        total_users = session.exec(select(User)).all()
        total_tasks = session.exec(select(Task)).all()
        completed_tasks = session.exec(select(Task).where(Task.completed == True)).all()
        
        print("\n" + "="*50)
        print("📊 SUMMARY:")
        print("="*50)
        print(f"👥 Users: {len(total_users)} (including 1 admin)")
        print(f"📝 Total tasks: {len(total_tasks)}")
        print(f"✅ Completed: {len(completed_tasks)}")
        print(f"⏳ Pending: {len(total_tasks) - len(completed_tasks)}")
        print("="*50)
        print("\n✨ Database seeding completed successfully!")
        print("\n🔑 Login credentials:")
        print("   Admin: admin / admin123")
        print("   Users: [username] / password123")
        print("   Example: john_smith / password123")


if __name__ == "__main__":
    seed_database()
