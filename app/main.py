"""
main.py

This is the entry point of the FastAPI application for task management.

Tasks:
- Sets up the FastAPI application
- Configures database connections and ORM models
- Includes the router for task-related operations

Upon execution, this script initializes the database schema and applies all included routers and middleware.
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager

from .routers import tasks
from app.dependencies.database import init_db


@asynccontextmanager
async def lifespan(application: FastAPI):
    """
    Async context manager to handle startup and shutdown events.
    """
    # Initialize database schema
    await init_db()

    yield

app = FastAPI(lifespan=lifespan)
app.include_router(tasks.router)
