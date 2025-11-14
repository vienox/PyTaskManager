from typing import List
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import select, Session
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from .models import User, UserCreate, UserRead, Task, TaskCreate, TaskUpdate
from .db import init_db, get_session
from .auth import hash_password, verify_password, create_access_token, decode_token

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

# Rate limiter configuration
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Tasks API", version="2.0", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware for future web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React/Vite dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> User:
    username = decode_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")
    return current_user


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/auth/token")
@limiter.limit("5/minute")  # Max 5 login attempts per minute per IP
def login(request: Request, form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == form.username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    token = create_access_token(user.username)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/auth/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/tasks", response_model=List[Task])
def get_tasks(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    tasks = session.exec(select(Task).where(Task.owner_id == current_user.id)).all()
    return tasks


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(data: TaskCreate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    task = Task(**data.model_dump(), owner_id=current_user.id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, data: TaskUpdate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    session.delete(task)
    session.commit()
    return None


# Admin endpoints
@app.post("/admin/users", response_model=UserRead, status_code=201)
def create_user_admin(data: UserCreate, admin: User = Depends(get_admin_user), session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.username == data.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    existing_email = session.exec(select(User).where(User.email == data.email)).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password),
        is_admin=False
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.get("/admin/users", response_model=List[UserRead])
def get_all_users(admin: User = Depends(get_admin_user), session: Session = Depends(get_session)):
    return session.exec(select(User)).all()


@app.get("/admin/tasks", response_model=List[Task])
def get_all_tasks(admin: User = Depends(get_admin_user), session: Session = Depends(get_session)):
    return session.exec(select(Task)).all()


@app.post("/admin/tasks", response_model=Task, status_code=201)
def create_task_admin(data: TaskCreate, owner_id: int, admin: User = Depends(get_admin_user), session: Session = Depends(get_session)):
    owner = session.get(User, owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="User not found")
    
    task = Task(**data.model_dump(), owner_id=owner_id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.put("/admin/tasks/{task_id}", response_model=Task)
def update_task_admin(task_id: int, data: TaskUpdate, admin: User = Depends(get_admin_user), session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.delete("/admin/tasks/{task_id}", status_code=204)
def delete_task_admin(task_id: int, admin: User = Depends(get_admin_user), session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    session.delete(task)
    session.commit()
    return None


@app.delete("/admin/users/{user_id}", status_code=204)
def delete_user(user_id: int, admin: User = Depends(get_admin_user), session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    
    session.delete(user)
    session.commit()
    return None


@app.put("/admin/users/{user_id}/make-admin", response_model=UserRead)
def make_admin(user_id: int, admin: User = Depends(get_admin_user), session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_admin = True
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
