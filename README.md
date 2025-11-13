# PyTaskManager

Simple task management system with FastAPI backend and Flet desktop GUI.

## Stack

- **Backend**: FastAPI + SQLite + JWT auth
- **Desktop**: Flet (Python GUI framework)
- **Database**: SQLite with SQLModel ORM
- **Auth**: JWT tokens + bcrypt password hashing

## Quick Start

### 1. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Initialize Database

```powershell
python scripts/seed_data.py
```

Creates:
- Admin user: `admin` / `admin123`
- 10 regular users: password `password123`
- 40 sample tasks

### 3. Start Backend

```powershell
python -m uvicorn api.app:app --reload
```

Backend runs on `http://127.0.0.1:8000`

### 4. Launch Desktop App

```powershell
cd desktop
python main.py
```

## Features

### User Roles

**Admin**:
- Manage all users (create, delete, promote)
- View and manage all tasks system-wide
- Access admin panel

**Regular User**:
- Manage own tasks only
- View personal statistics
- Task CRUD operations

### Authentication

- JWT token-based (60min expiry)
- SHA256 + bcrypt password hashing
- Role-based access control


## Project Structure

```
PyTaskManager/
├── api/
│   ├── app.py          # FastAPI endpoints
│   ├── auth.py         # JWT + password hashing
│   ├── db.py           # Database connection
│   └── models.py       # User & Task models
├── desktop/
│   ├── main.py         # App entry point
│   ├── api_client.py   # HTTP client
│   └── views/          # UI components
│       ├── auth/       # Login view
│       ├── user/       # User dashboard & tasks
│       ├── admin/      # Admin panel & management
│       └── ui/         # Shared components
├── scripts/
│   ├── seed_data.py    # Database seeding
│   └── create_admin.py # Create admin user
└── tests/
    └── api/
        └── test_endpoints.py  # API tests
```

## API Endpoints

### Auth
- `POST /auth/token` - Login
- `GET /auth/me` - Current user info

### Tasks (User)
- `GET /tasks` - My tasks
- `POST /tasks` - Create task
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task

### Admin
- `GET /admin/users` - All users
- `POST /admin/users` - Create user
- `DELETE /admin/users/{id}` - Delete user
- `PUT /admin/users/{id}/make-admin` - Promote to admin
- `GET /admin/tasks` - All tasks
- `POST /admin/tasks?owner_id={id}` - Create task for user
- `PUT /admin/tasks/{id}` - Update any task
- `DELETE /admin/tasks/{id}` - Delete any task

## Testing

Run tests:
```powershell
pytest tests/ -v
```

Test coverage:
- Authentication (login, token validation)
- Task CRUD (user scope)
- Admin operations (users & tasks)
- Authorization (role-based access)

## Development

### API Documentation

With backend running:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### Reset Database

```powershell
Remove-Item tasks.db -Force
python scripts/seed_data.py
```

## Common Issues

**"Database is locked"**
- Stop all processes (backend + desktop)
- Delete `tasks.db` and re-seed

**"Connection refused"**
- Ensure backend is running on port 8000

**"Invalid token"**
- Token expired (logout and login again)



