"""
main.py

This is the entry point of the FastAPI application for task management.

Functions:
- Sets up the FastAPI application
- Configures database connections and ORM models
- Includes the router for task-related operations

Upon execution, initializes the database schema and applies all included routers and middleware.
"""

from fastapi import FastAPI
from .routers import tasks
from app.dependencies.database import engine
from .db_schemas import Base


# Initialize database tables
Base.metadata.create_all(bind=engine)

# Instantiate the FastAPI app
app = FastAPI()

# Include the router module that contains task management endpoints
app.include_router(tasks.router)