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
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from contextlib import asynccontextmanager
from .routers import tasks
from app.dependencies.database import engine
from .db_schemas import Base

# Initialize database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize In-Memory Cache
    FastAPICache.init(InMemoryBackend(), prefix="api-cache")
    yield
app = FastAPI(lifespan=lifespan)
app.include_router(tasks.router)