# PyTaskManager

A modern task management system with FastAPI backend and Flet desktop client.

## Architecture

**Dual-Process Architecture:**
- **Backend**: FastAPI REST API with JWT authentication
- **Desktop Client**: Flet (Flutter-based Python GUI)
- **Database**: SQLite with SQLModel ORM
- **Two separate processes**: Backend server + Desktop app as HTTP client

```
┌─────────────────┐         HTTP/REST         ┌──────────────────┐
│  Desktop Client │ ←───────────────────────→ │  FastAPI Backend │
│     (Flet)      │    JWT Bearer Tokens      │   (Port :8000)   │
└─────────────────┘                           └────────┬─────────┘
                                                       │
                                                       ▼
                                               ┌──────────────┐
                                               │   SQLite DB  │
                                               │  (tasks.db)  │
                                               └──────────────┘
```

## Features

### User Roles
- **Admin Users** (`is_admin=True`):
  - Full CRUD access to all users and tasks
  - Access to `/admin/*` endpoints
  - User management (create, delete, promote to admin)
  - System-wide task management

- **Regular Users** (`is_admin=False`):
  - Manage only their own tasks (filtered by `owner_id`)
  - Personal task dashboard with statistics
  - Cannot access other users' data

### Authentication
- JWT token-based authentication
- **Custom password hashing**: SHA256 pre-hash + bcrypt
  - Bypasses bcrypt's 72-byte limit
  - **INCOMPATIBLE with passlib** - always use direct `bcrypt` imports

### Task Management
- CRUD operations for tasks
- Task properties: title, description, completed status
- Owner-based access control
- Search and filter capabilities

##  Quick Start

### 1. Install Dependencies

```powershell
# Navigate to project directory
cd c:\Users\niewi\Desktop\PyTaskManager

# Install Python packages
pip install -r requirements.txt
```

### 2. Initialize Database

**Option A: Seed with sample data** (Recommended for testing)
```powershell
python seed_data.py
```
Creates:
- 1 admin user (`admin` / `admin123`)
- 10 regular users (all use password: `password123`)
- 40 sample tasks distributed across users

**Option B: Create admin only**
```powershell
python create_admin.py
```

### 3. Start Backend Server

```powershell
# Terminal 1: Start FastAPI backend
python -m uvicorn api.app:app --reload
```
Server runs on: `http://127.0.0.1:8000`

### 4. Launch Desktop Client

```powershell
# Terminal 2: Run desktop app
cd desktop
python main.py
```

## Project Structure

```
PyTaskManager/
├── api/                        # FastAPI Backend
│   ├── __init__.py
│   ├── app.py                 # Main FastAPI app & endpoints
│   ├── auth.py                # JWT + bcrypt password hashing
│   ├── db.py                  # Database engine & session
│   └── models.py              # SQLModel schemas (User, Task)
│
├── desktop/                   # Flet Desktop Client
│   ├── main.py               # App entry point & navigation
│   ├── api_client.py         # HTTP client for backend API
│   ├── config.py             # Configuration constants
│   ├── views/                # UI view components
│   │   ├── login_view.py    # Login screen
│   │   ├── user_view.py     # User profile dashboard
│   │   ├── tasks_view.py    # Task management (user scope)
│   │   └── admin_view.py    # Admin panel
│   └── components/           # Reusable UI components
│       ├── task_card.py     # Task display cards
│       ├── nav_bar.py       # Navigation bar
│       └── admin_task_manager.py  # Admin task CRUD
│
├── seed_data.py              # Database seeding script
├── create_admin.py           # Create admin user
├── requirements.txt          # Python dependencies
├── tasks.db                  # SQLite database (auto-created)
└── README.md                 # This file
```

## Default Credentials

### After `seed_data.py`:

**Admin Account:**
```
Username: admin
Password: admin123
```

**Regular Users:**
```
Username: john_smith, emma_johnson, michael_brown, ...
Password: password123  (for all users)
```

## Development Workflow

### Running in Development Mode

```powershell
# Terminal 1: Backend with auto-reload
python -m uvicorn api.app:app --reload

# Terminal 2: Desktop client
cd desktop
python main.py
```

### Database Operations

**Reset Database:**
```powershell
# Stop both backend and desktop app first
Remove-Item tasks.db
python seed_data.py
```

**Create New Admin:**
```powershell
python create_admin.py
```

### API Documentation

With backend running, visit:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## Flet UI Patterns

### View Creation Signature
```python
def create_<name>_view(page: ft.Page, api: APIClient, user: dict, on_logout: callable, **kwargs):
    # Build UI
    return ft.Column([...])
```

### Navigation Pattern
```python
page.controls.clear()
page.add(new_view)
page.update()
```

### Scrolling Components (Critical!)
```python
# CORRECT: Fixed height required for scrolling
ft.Container(
    content=ft.Column([...], scroll=ft.ScrollMode.ALWAYS),
    height=500  # Must specify fixed height!
)

# WRONG: expand=True won't work with scroll
ft.Container(
    content=ft.Column([...], scroll=ft.ScrollMode.ALWAYS),
    expand=True  # Scrolling won't work!
)
```

### Color Usage
```python
# RECOMMENDED: HEX codes (reliable in Flet 0.28.3)
bgcolor="#E3F2FD"

# AVOID: ft.Colors constants (API inconsistencies)
bgcolor=ft.Colors.BLUE_50
```

## 📡 API Endpoints

### Authentication
- `POST /auth/token` - Login (returns JWT token)
- `GET /auth/me` - Get current user info

### User Tasks
- `GET /tasks` - Get current user's tasks
- `POST /tasks` - Create new task
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task

### Admin Only
- `POST /admin/users` - Create user
- `GET /admin/users` - List all users
- `DELETE /admin/users/{id}` - Delete user
- `PUT /admin/users/{id}/make-admin` - Promote to admin
- `GET /admin/tasks` - Get all tasks (system-wide)
- `POST /admin/tasks` - Create task for specific user
- `PUT /admin/tasks/{id}` - Update any task
- `DELETE /admin/tasks/{id}` - Delete any task

## Important Notes

### Password Hashing Pattern
This project uses a **custom SHA256 + bcrypt pattern**:

```python
# api/auth.py
def _prepare_password(password: str) -> bytes:
    return hashlib.sha256(password.encode('utf-8')).hexdigest().encode('utf-8')

def hash_password(password: str) -> str:
    prepared = _prepare_password(password)
    return bcrypt.hashpw(prepared, bcrypt.gensalt()).decode('utf-8')
```

**CRITICAL**: 
- **NEVER use `passlib`** - it's incompatible with this pattern
- Always use direct `bcrypt` imports
- This pattern is consistent across all password operations

### Database Location
- **File**: `tasks.db` in project root
- **Format**: SQLite
- **Auto-created** on first `init_db()` call

### Public Registration
- **DISABLED** - only admins can create users
- Use `POST /admin/users` endpoint with admin token

## Testing

### Manual Testing Checklist
1. Start backend server
2. Run seed_data.py
3. Launch desktop app
4. Login as admin (admin/admin123)
5. Verify admin panel access
6. Create new user via admin panel
7. Logout and login as regular user
8. Create/edit/delete tasks
9. Verify user can only see own tasks

## Common Issues

### "Database is locked"
```powershell
# Close all running instances (backend + desktop)
# Then delete database:
Remove-Item tasks.db -Force
python seed_data.py
```

### "Connection refused" in desktop app
```
   Ensure backend is running:
   python -m uvicorn api.app:app --reload
```

### "Invalid token" errors
```
Token expired (60 min validity)
Logout and login again
```

## Version History

### v2.0.0 (Current)
- English codebase with professional documentation
- Enhanced API comments and docstrings
- Updated sample data with English names
- Improved requirements.txt with sections and notes

### v1.0.0
- Initial Polish version
- Basic task management
- Role-based access control

## Stack

- **Backend**: FastAPI 0.120.1, Python 3.8+
- **Desktop**: Flet 0.28.3 (Flutter for Python)
- **Database**: SQLite with SQLModel 0.0.27
- **Auth**: JWT (python-jose), bcrypt 5.0.0
- **HTTP Client**: requests 2.32.5

## 📄 License

This project is for educational and demonstration purposes.

## Development

**Code Style:**
- PEP 8 compliance
- Comprehensive docstrings
- Type hints where applicable
- Professional English comments

**Contribution Guidelines:**
- Maintain dual-architecture pattern
- Keep authentication pattern consistent (SHA256+bcrypt)
- Update both backend AND desktop client for feature changes
- Test with both admin and regular user roles


