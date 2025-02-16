"""
database.py

This module sets up the database connection and configuration for the application.

Components:
- SQLAlchemy Engine: Configures the connection to the SQLite database.
- SessionLocal: A SQLAlchemy database session that will be used for dependency injection.
- Base: Declarative base class for ORM models.
- get_db: Dependency function to provide a database session to endpoints.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Connection string for the SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create a new SQLAlchemy engine instance
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models
Base = declarative_base()

def get_db():
    """
    Provides a transactional scope around a series of operations.

    Yields:
        SessionLocal: A SQLAlchemy database session.

    Automatically handles closing the session after use, ensuring the session lifecycle
    is properly managed for each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
