# PyTaskManager 📋

> Modern task management system with FastAPI backend and Flet desktop GUI

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.120-009688?logo=fastapi)
![Flet](https://img.shields.io/badge/Flet-0.28-blue?logo=flutter)
![Tests](https://img.shields.io/badge/tests-19%20passing-success)
![Docker](https://img.shields.io/badge/docker-ready-2496ED?logo=docker)

</div>

---

## 📸 Demo

<div align="center">

![App Demo](screenshots/demo.gif)

*Complete walkthrough: Login → User Dashboard → Task Management → Admin Panel*

</div>

## ✨ Features

<table>
<tr>
<td width="50%">

### 👤 User Features
- ✅ **Personal Dashboard** with task statistics
- ✅ **Task Management** (Create, Edit, Delete)
- ✅ **Real-time Search** across tasks
- ✅ **Task Completion** tracking
- ✅ **Secure Authentication** (JWT)

</td>
<td width="50%">

### 👨‍💼 Admin Features
- ✅ **User Management** (Create, Delete, Promote)
- ✅ **System-wide Task View**
- ✅ **Advanced Filtering** by user
- ✅ **Task Assignment** to users
- ✅ **Role-based Access Control**

</td>
</tr>
</table>

## 🏗️ Architecture

```mermaid
graph TB
    subgraph "Desktop Client"
        A[Flet UI] --> B[API Client]
    end
    
    subgraph "Backend API"
        C[FastAPI] --> D[Auth JWT]
        C --> E[SQLModel ORM]
    end
    
    subgraph "Database"
        F[(SQLite/PostgreSQL)]
    end
    
    B -->|HTTP/REST| C
    E --> F
    
    style A fill:#42A5F5
    style C fill:#009688
    style F fill:#FF6F00
```

## 🚀 Tech Stack

<div align="center">

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | ![Flet](https://img.shields.io/badge/Flet-0.28-blue?logo=flutter) | Cross-platform desktop GUI |
| **Backend** | ![FastAPI](https://img.shields.io/badge/FastAPI-0.120-009688?logo=fastapi) | High-performance REST API |
| **ORM** | ![SQLModel](https://img.shields.io/badge/SQLModel-0.0.27-red) | Type-safe database operations |
| **Auth** | ![JWT](https://img.shields.io/badge/JWT-Auth-000000?logo=jsonwebtokens) | Secure token-based authentication |
| **Database** | ![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite) / ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?logo=postgresql) | Flexible database options |
| **Container** | ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker) | Easy deployment |

</div>

## ⚡ Quick Start

### Option 1: 🐍 Local Development (SQLite)

```powershell
# 1️⃣ Clone repository
git clone https://github.com/vienox/PyTaskManager.git
cd PyTaskManager

# 2️⃣ Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Configure environment
cp .env.example .env
# ✏️ Edit .env if needed (default SQLite works out of the box)

# 5️⃣ Initialize database with sample data
python scripts/seed_data.py

# 6️⃣ Start backend API
python -m uvicorn api.app:app --reload
# 🌐 API running at: http://localhost:8000

# 7️⃣ Launch desktop app (in new terminal)
python desktop/main.py
```

### Option 2: 🐳 Docker (PostgreSQL)

```powershell
# 1️⃣ Clone repository
git clone https://github.com/vienox/PyTaskManager.git
cd PyTaskManager

# 2️⃣ Copy environment file
cp .env.example .env

# 3️⃣ Start with Docker Compose
docker-compose up
# 🐘 PostgreSQL + FastAPI running

# 4️⃣ Launch desktop app (in new terminal)
python desktop/main.py
```

### 🔑 Default Credentials

After running `seed_data.py`:

| Role | Username | Password |
|------|----------|----------|
| 🔴 **Admin** | `admin` | `admin123` |
| 🔵 **User** | `john_smith` | `password123` |
| 🔵 **User** | `emma_johnson` | `password123` |

> 💡 **Tip:** Seed script creates 10 sample users + 40 tasks for testing

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


## 📂 Project Structure

```
PyTaskManager/
│
├── 🔧 api/                    # Backend (FastAPI)
│   ├── app.py                # Main API endpoints
│   ├── auth.py               # JWT & password hashing
│   ├── config.py             # Environment configuration
│   ├── db.py                 # Database connection
│   └── models.py             # SQLModel schemas
│
├── 🖥️ desktop/                # Desktop Client (Flet)
│   ├── main.py               # App entry point
│   ├── api_client.py         # HTTP client wrapper
│   ├── config.py             # Desktop configuration
│   ├── constants.py          # UI constants & colors
│   └── views/                # UI components
│       ├── auth/             # Login view
│       ├── user/             # User dashboard & tasks
│       ├── admin/            # Admin panel & management
│       └── ui/               # Shared components (navbar, cards)
│
├── 🧪 tests/                  # Test suite (19 tests)
│   ├── conftest.py           # Pytest fixtures
│   └── api/
│       └── test_endpoints.py # API integration tests
│
├── 📜 scripts/                # Database utilities
│   ├── seed_data.py          # Sample data seeding
│   └── create_admin.py       # Create admin user
│
├── 🐳 Docker/                 # Deployment
│   ├── Dockerfile            # Backend container
│   └── docker-compose.yml    # PostgreSQL + backend
│
├── ⚙️ Configuration
│   ├── .env                  # Environment variables (gitignored)
│   ├── .env.example          # Environment template
│   ├── requirements.txt      # Python dependencies
│   └── .gitignore            # Git ignore rules
│
└── 📸 screenshots/            # Demo assets
    └── demo.gif              # Application walkthrough
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# 🖥️ Desktop Application
API_URL=http://localhost:8000

# 🔐 Backend Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=60

# 🗄️ Database Connection
DATABASE_URL=sqlite:///tasks.db  # or postgresql://user:pass@host/db
```

### Database Options

<table>
<tr>
<td width="50%">

**🔹 SQLite (Default)**
```bash
DATABASE_URL=sqlite:///tasks.db
```

✅ **Pros:**
- Zero configuration
- Perfect for development
- Single file database

</td>
<td width="50%">

**🔹 PostgreSQL (Production)**
```bash
DATABASE_URL=postgresql://taskuser:taskpass@localhost/tasks
```

✅ **Pros:**
- Production-ready
- Better concurrency
- Docker support included

</td>
</tr>
</table>

> 💡 **Tip:** Switch databases by changing `DATABASE_URL` - no code changes needed!

## 📡 API Endpoints

<details>
<summary><b>🔐 Authentication</b></summary>

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/auth/token` | Login and get JWT token | 🔓 Public |
| `GET` | `/auth/me` | Get current user info | ✅ Required |

</details>

<details>
<summary><b>📝 User Tasks</b></summary>

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/tasks` | Get my tasks | ✅ User |
| `POST` | `/tasks` | Create new task | ✅ User |
| `GET` | `/tasks/{id}` | Get specific task | ✅ User |
| `PUT` | `/tasks/{id}` | Update task | ✅ User |
| `DELETE` | `/tasks/{id}` | Delete task | ✅ User |

</details>

<details>
<summary><b>👨‍💼 Admin - Users</b></summary>

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/admin/users` | Get all users | ✅ Admin |
| `POST` | `/admin/users` | Create user | ✅ Admin |
| `DELETE` | `/admin/users/{id}` | Delete user | ✅ Admin |
| `PUT` | `/admin/users/{id}/make-admin` | Promote to admin | ✅ Admin |

</details>

<details>
<summary><b>👨‍💼 Admin - Tasks</b></summary>

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/admin/tasks` | Get all tasks (system-wide) | ✅ Admin |
| `POST` | `/admin/tasks?owner_id={id}` | Create task for user | ✅ Admin |
| `PUT` | `/admin/tasks/{id}` | Update any task | ✅ Admin |
| `DELETE` | `/admin/tasks/{id}` | Delete any task | ✅ Admin |

</details>

### 📚 Interactive API Docs

With backend running, explore the API:

```bash
🌐 Swagger UI:  http://localhost:8000/docs
📖 ReDoc:       http://localhost:8000/redoc
```

## 🧪 Testing

Run all tests:
```powershell
pytest tests/ -v
```

### Test Coverage (19 tests passing ✅)

```mermaid
pie title Test Distribution
    "Authentication" : 4
    "User Tasks CRUD" : 6
    "Admin Users" : 4
    "Admin Tasks" : 3
    "Authorization" : 2
```

<details>
<summary><b>📊 Test Breakdown</b></summary>

| Category | Tests | Coverage |
|----------|-------|----------|
| 🔐 **Authentication** | 4 | Login, token validation, user info |
| 📝 **Task CRUD** | 6 | Create, read, update, delete, list |
| 👥 **Admin Users** | 4 | User management, role promotion |
| 📋 **Admin Tasks** | 3 | System-wide task operations |
| 🔒 **Authorization** | 2 | Permission checks, role-based access |

**Test Environment:** In-memory SQLite for complete isolation

</details>

## 🛠️ Development

### 📚 Interactive API Documentation

With backend running, explore the API interactively:

```bash
🌐 Swagger UI:  http://localhost:8000/docs
📖 ReDoc:       http://localhost:8000/redoc
🏥 Health Check: http://localhost:8000/health
```

### 🔄 Reset Database

<table>
<tr>
<td width="50%">

**SQLite:**
```powershell
Remove-Item tasks.db -Force
python scripts/seed_data.py
```

</td>
<td width="50%">

**Docker (PostgreSQL):**
```powershell
docker-compose down -v
docker-compose up
```

</td>
</tr>
</table>

### 🐳 Docker Commands

```powershell
# 🚀 Build and start
docker-compose up --build

# 🌙 Run in background
docker-compose up -d

# 📋 View logs
docker-compose logs -f backend

# 🛑 Stop all
docker-compose down

# 🗑️ Remove volumes (reset database)
docker-compose down -v

# 🔍 Check running containers
docker-compose ps
```

## 🐛 Common Issues

<details>
<summary><b>❌ "ModuleNotFoundError: pydantic_settings"</b></summary>

```powershell
pip install pydantic-settings
```

</details>

<details>
<summary><b>🔒 "Database is locked" (SQLite)</b></summary>

**Solution:**
1. Stop all processes (backend + desktop)
2. Delete database and re-seed:
   ```powershell
   Remove-Item tasks.db -Force
   python scripts/seed_data.py
   ```

</details>

<details>
<summary><b>🔌 "Connection refused"</b></summary>

**Checklist:**
- ✅ Ensure backend is running on port 8000
- ✅ Check `API_URL` in `.env`
- ✅ Verify no firewall blocking localhost

</details>

<details>
<summary><b>⏰ "Invalid token"</b></summary>

**Cause:** Token expired (60min default)

**Solution:** Logout and login again

</details>

<details>
<summary><b>🐳 Docker: "port 5432 already in use"</b></summary>

**Solution:**
- Stop existing PostgreSQL instance, or
- Change port in `docker-compose.yml`:
  ```yaml
  ports:
    - "5433:5432"  # Changed from 5432
  ```

</details>

---

## 📝 License

MIT License - feel free to use this project for learning or production!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📧 Contact

**Project Link:** [https://github.com/vienox/PyTaskManager](https://github.com/vienox/PyTaskManager)

---




