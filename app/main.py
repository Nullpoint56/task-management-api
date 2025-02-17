"""
main.py

This is the entry point of the FastAPI application for task management.

Tasks:
- Sets up the FastAPI application
- Configures database connections and ORM models
- Initializes in-memory caching for performance improvement
- Includes the router for task-related operations

Upon execution, this script initializes the database schema and applies all included routers and middleware.
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from .routers import tasks
from app.dependencies.database import get_db



@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Async context manager to handle startup and shutdown events.
    """
    # Initialize database schema
    get_db()

    # Initialize in-memory cache
    FastAPICache.init(InMemoryBackend(), prefix="api-cache")

    yield

    # Cleanup logic if needed (currently no cleanup in this example)

app = FastAPI(lifespan=lifespan)
app.include_router(tasks.router)
