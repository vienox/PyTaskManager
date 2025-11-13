# PyTaskManager - AI Coding Agent Instructions

## Architecture Overview

This is a **dual-architecture** task management system with separate backend (FastAPI) and desktop client (Flet):

- **Backend**: `api/` - FastAPI REST API with JWT auth, SQLite database (SQLModel ORM)
- **Desktop Client**: `desktop/` - Flet (Python GUI framework) consuming the REST API
- **Two processes**: Backend server runs on `http://127.0.0.1:8000`, desktop app connects as HTTP client

## Critical Authentication Pattern

**IMPORTANT**: Password hashing uses SHA256 pre-hash before bcrypt to bypass bcrypt's 72-byte limit:

```python
# api/auth.py - DO NOT modify this pattern
def _prepare_password(password: str) -> bytes:
    return hashlib.sha256(password.encode('utf-8')).hexdigest().encode('utf-8')

def hash_password(password: str) -> str:
    prepared = _prepare_password(password)
    return bcrypt.hashpw(prepared, bcrypt.gensalt()).decode('utf-8')
```

This is incompatible with `passlib`. Always use direct `bcrypt` imports, never `passlib.hash.bcrypt`.

## User Roles & Permissions

- **Admin users** (`is_admin=True`): Full CRUD on all users and tasks, access to `/admin/*` endpoints
- **Regular users** (`is_admin=False`): Can only view/edit their own tasks (`owner_id` filtered)
- **No public registration**: Only admins can create users via `POST /admin/users`

## Development Workflow

### Starting the Application

```powershell
# Terminal 1: Start FastAPI backend
cd c:\Users\niewi\Desktop\PyTaskManager
python -m uvicorn api.app:app --reload

# Terminal 2: Run desktop client
cd c:\Users\niewi\Desktop\PyTaskManager\desktop
python main.py
```

### Database Operations

```powershell
# Seed database with sample data (10 users + 40 tasks)
python seed_data.py

# Create standalone admin user
python create_admin.py
```

**Database location**: `tasks.db` in project root (SQLite, auto-created on first run)

## Flet UI Architecture Patterns

### View Creation Functions

All views follow this signature pattern:

```python
def create_<name>_view(page: ft.Page, api: APIClient, user: dict, on_logout: callable, **kwargs):
    # Build UI components
    # Define event handlers
    # Return ft.Column with complete view
    return view
```

### Navigation Flow

```
main.py (show_login/show_admin/show_user_profile/show_tasks)
  ↓
page.controls.clear() + page.add(view) + page.update()
```

**Pattern**: Navigation always clears page, adds new view, calls `page.update()`. Callbacks passed as `on_logout`, `on_back_to_profile`, etc.

### Scrolling Components

**CRITICAL**: Flet's `Column(scroll=ft.ScrollMode.ALWAYS)` requires parent Container with **fixed height**, not `expand=True`:

```python
# CORRECT
ft.Container(
    content=ft.Column([...], scroll=ft.ScrollMode.ALWAYS),
    height=500  # Fixed height required!
)

# WRONG - scrolling won't work
ft.Container(
    content=ft.Column([...], scroll=ft.ScrollMode.ALWAYS),
    expand=True
)
```

### Color Usage

Use **HEX codes**, not `ft.Colors` constants (API inconsistencies in Flet 0.28.3):

```python
bgcolor="#E3F2FD"  # ✅ Works reliably
bgcolor=ft.Colors.BLUE_50  # ⚠️ May fail
```

### Emoji/Icon Convention

- **Keep functional icons**: 📝 (tasks), 🔍 (search), ✅/❌ (status indicators)
- **Remove decorative emoji**: No 👤, 📊, 🛡️, ➕ in button labels or titles
- Use `ft.Icons.*` for UI controls instead

## API Client Patterns

`desktop/api_client.py` maintains session state:

```python
api = APIClient()
api.login(username, password)  # Sets self.token
api.get_tasks()  # Uses Bearer token automatically
```

All API methods raise `requests.HTTPError` on failure. Views should catch and display error messages:

```python
try:
    api.create_user(username, email, password)
except requests.HTTPException as e:
    if e.response.status_code == 400:
        # Handle specific errors (duplicate username/email)
```

## Form Validation Patterns

Real-time validation in TextFields:

```python
username_field = ft.TextField(
    label="Username",
    on_change=lambda e: validate_username_field()
)

def validate_username_field():
    if username_field.value and len(username_field.value) < 3:
        username_field.error_text = "Min. 3 characters"
    else:
        username_field.error_text = None
    page.update()
```

**Validation rules**:
- Username: min 3 chars, unique
- Email: regex `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`, unique
- Password: min 6 chars

## Component Architecture

Reusable components in `desktop/components/`:

- `task_card.py`: Task display with checkbox, edit, delete buttons
- `nav_bar.py`: Top navigation bar with user info and menu
- `admin_task_manager.py`: Full task management panel for admins

Components accept callbacks for actions (e.g., `on_toggle`, `on_edit`, `on_delete`).

## Testing Credentials

After running `seed_data.py`:
- Admin: `admin` / `admin123`
- Users: `john_smith`, `emma_johnson`, etc. / `password123` (all users)

## Common Pitfalls

1. **AppBar Error**: Never add `ft.AppBar` to `ft.Column`. Use custom Container-based navbar instead.
2. **Scrolling Not Working**: Check parent Container has `height=500`, not `expand=True`
3. **Auth Errors**: Ensure backend is running before starting desktop client
4. **Import Errors**: Desktop code uses relative imports (`from views.login_view import ...`), run from `desktop/` directory

## Code Style Guidelines

- **Language**: All code, comments, and documentation in **English**
- **Docstrings**: Use Google-style docstrings with Args, Returns, Raises sections
- **Comments**: Professional, concise explanations of WHY, not WHAT
- **Type Hints**: Use where applicable for better IDE support
- **Error Messages**: User-friendly English messages in UI, technical details in logs

## Sample Data

Seed script creates realistic English names and professional task descriptions:
- Users: John Smith, Emma Johnson, Michael Brown, etc.
- Tasks: Professional work items (code reviews, meetings, development tasks)
- Emails: `firstname.lastname@company.com`

