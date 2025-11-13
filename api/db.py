"""
Database configuration and session management.

This module provides SQLite database engine and session management utilities
using SQLModel (built on top of SQLAlchemy).

Database Details:
    - SQLite file: tasks.db (created in project root)
    - ORM: SQLModel
    - Auto-creates tables on first init_db() call
"""

from sqlmodel import SQLModel, create_engine, Session

# SQLite database engine
# echo=False disables SQL query logging for production
engine = create_engine("sqlite:///tasks.db", echo=False)


def init_db():
    """
    Initialize the database by creating all tables.
    
    This function creates all tables defined in models.py if they don't exist.
    Safe to call multiple times - won't recreate existing tables.
    
    Called automatically on application startup via FastAPI event.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Dependency for getting database sessions in FastAPI endpoints.
    
    Yields:
        Session: SQLModel database session with automatic cleanup
        
    Usage:
        @app.get("/endpoint")
        def endpoint(session: Session = Depends(get_session)):
            # Use session for database operations
            pass
    
    Note:
        Session is automatically closed after request completion.
    """
    with Session(engine) as session:
        yield session
