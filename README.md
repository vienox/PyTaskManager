# PyTaskManager

A modern desktop task management application built with Python, featuring a Flask REST API backend and Flet GUI frontend.

## Features

### User Features
- **User Authentication**: Secure login system with JWT tokens
- **Task Management**: Create, edit, delete, and mark tasks as completed
- **Task Search**: Real-time search filtering for tasks
- **Task Statistics**: Dashboard showing total, completed, and pending tasks
- **User Profile**: View and manage personal information

### Admin Features
- **User Management**: Create, view, and delete users
- **Global Task Management**: View and manage tasks for all users
- **User Search & Filtering**: Search users by username or email
- **Task Filtering**: Filter tasks by user
- **Bulk Operations**: Manage multiple users and tasks efficiently

## Technology Stack

### Backend
- **Flask**: Lightweight WSGI web application framework
- **SQLModel**: SQL databases in Python with type hints
- **SQLite**: Embedded relational database
- **JWT**: Secure token-based authentication
- **Passlib**: Password hashing library

### Frontend
- **Flet**: Modern Python framework for building desktop applications
- **Material Design**: Clean and intuitive user interface

## Project Structure

```
PyTaskManager/
├── api/                    # Backend API
│   ├── __init__.py
│   ├── app.py             # Flask application entry point
│   ├── auth.py            # Authentication utilities
│   ├── db.py              # Database configuration
│   └── models.py          # SQLModel database models
├── desktop/               # Desktop GUI application
│   ├── components/        # Reusable UI components
│   │   ├── admin_navbar.py
│   │   ├── admin_task_manager.py
│   │   ├── task_card.py
│   │   ├── user_manager.py
│   │   ├── user_navbar.py
│   │   ├── user_stats.py
│   │   └── user_task_manager.py
│   ├── views/             # Application views
│   │   ├── admin_view.py
│   │   ├── login_view.py
│   │   ├── tasks_view.py
│   │   └── user_view.py
│   ├── api_client.py      # API client for backend communication
│   ├── config.py          # Configuration settings
│   └── main.py            # Desktop application entry point
├── scripts/               # Database management scripts
│   ├── create_admin.py    # Create admin user
│   └── seed_data.py       # Populate database with sample data
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone https://github.com/vienox/PyTaskManager.git
cd PyTaskManager
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database

**Option 1: Create Admin Only**
```bash
python scripts/create_admin.py
```

**Option 2: Populate with Sample Data** (recommended for testing)
```bash
python scripts/seed_data.py
```

This will create:
- 1 admin user
- 10 regular users
- 39 sample tasks

##  Usage

### Running the Application

**Terminal 1: Start Backend API**
```bash
cd api
python app.py
```
API will be available at: `http://127.0.0.1:8000`

**Terminal 2: Start Desktop Application**
```bash
cd desktop
python main.py
```

### Default Login Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**Sample User Accounts:**
- Username: `john_smith` / Password: `pass123`
- Username: `anna_johnson` / Password: `pass123`
- Username: `peter_williams` / Password: `pass123`
- _(see full list in seed_data.py)_

## API Endpoints

### Authentication
- `POST /auth/token` - Login and get JWT token
- `GET /auth/me` - Get current user information

### User Tasks
- `GET /tasks` - Get user's tasks
- `POST /tasks` - Create new task
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task

### Admin Endpoints
- `GET /admin/users` - Get all users
- `POST /admin/users` - Create new user
- `DELETE /admin/users/{id}` - Delete user
- `GET /admin/tasks` - Get all tasks
- `POST /admin/tasks` - Create task for user
- `PUT /admin/tasks/{id}` - Update any task
- `DELETE /admin/tasks/{id}` - Delete any task

## Architecture

### Component-Based Design
The desktop application uses a modular component architecture:
- **Separation of Concerns**: Views orchestrate components
- **Reusable Components**: Shared UI elements across views
- **Clean Callbacks**: Event handling with callback pattern
- **State Management**: Local state in components

### Authentication Flow
1. User enters credentials in login view
2. Desktop app sends credentials to Flask API
3. API validates and returns JWT token
4. Token stored in APIClient for subsequent requests
5. All API calls include Bearer token in headers

### Database Schema

**Users Table:**
- `id`: Integer (Primary Key)
- `username`: String (Unique)
- `email`: String (Unique)
- `hashed_password`: String
- `is_admin`: Boolean

**Tasks Table:**
- `id`: Integer (Primary Key)
- `title`: String
- `description`: String (Optional)
- `completed`: Boolean
- `owner_id`: Integer (Foreign Key → Users)

## Dependencies

### Core
- `flet>=0.24.1` - Desktop GUI framework
- `flask>=3.0.0` - Web framework
- `sqlmodel>=0.0.22` - SQL ORM with type hints

### Authentication & Security
- `pyjwt>=2.9.0` - JWT token handling
- `passlib>=1.7.4` - Password hashing
- `bcrypt>=4.2.0` - Password encryption

### API & HTTP
- `requests>=2.32.0` - HTTP library
- `python-multipart>=0.0.12` - Form data parsing

### Development
- `python-dotenv>=1.0.0` - Environment variable management

## 🧪 Testing the Application

1. **Start Backend**: Run `python api/app.py`
2. **Start Desktop App**: Run `python desktop/main.py`
3. **Login as Admin**: Use `admin` / `admin123`
4. **Explore Admin Panel**:
   - View all users
   - Manage tasks for any user
   - Create new users
5. **Login as Regular User**: Use `john_smith` / `pass123`
6. **Test User Features**:
   - Create personal tasks
   - Mark tasks as completed
   - Edit and delete tasks
   - View task statistics

## Security Features

- **Password Hashing**: Bcrypt with salt
- **JWT Authentication**: Secure token-based auth
- **Role-Based Access**: Admin vs regular user permissions
- **Input Validation**: Form validation on client and server
- **SQL Injection Protection**: SQLModel ORM prevents SQL injection

## UI Features

- **Material Design**: Modern, clean interface
- **Responsive Layout**: Adapts to different window sizes
- **Real-time Search**: Instant filtering of tasks and users
- **Visual Feedback**: Loading states and error messages
- **Status Indicators**: Color-coded task completion
- **Empty States**: Helpful messages when no data available

## Development

### Adding New Features

1. **Backend**: Add endpoints in `api/app.py`
2. **Models**: Update models in `api/models.py`
3. **Frontend**: Create components in `desktop/components/`
4. **Views**: Compose views from components in `desktop/views/`

### Code Style

- **Type Hints**: Use Python type annotations
- **Docstrings**: Document all functions and classes
- **Clean Code**: Follow PEP 8 guidelines
- **Modular Design**: Keep components focused and reusable

## Troubleshooting

### Backend Not Starting
```bash
# Check if port 8000 is available
netstat -ano | findstr :8000

# Kill process if needed (Windows)
taskkill /PID <process_id> /F
```

### Database Issues
```bash
# Delete database and reinitialize
rm taskmanager.db
python scripts/seed_data.py
```

### Import Errors
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```


## 👥 Authors

- **vienox** - *Initial work* - [GitHub](https://github.com/vienox)

## 🙏 Acknowledgments

- [Flet](https://flet.dev/) - For the amazing desktop framework
- [Flask](https://flask.palletsprojects.com/) - For the lightweight web framework
- [SQLModel](https://sqlmodel.tiangolo.com/) - For the elegant ORM


