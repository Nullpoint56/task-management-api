"""
models.py

This module defines the SQLAlchemy ORM models for the task management system.

Models defined here are used for:
- Defining table schemas in the database
- Facilitating CRUD operations through ORM queries
- Mapping Python objects to database records

Models included:
- TaskDBSchema: Represents the 'tasks' table with fields for each attribute of a task.
"""

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from app.dependencies.database import Base

class TaskDBSchema(Base):
    """
    ORM model for the 'tasks' table in the database.

    Attributes:
        id (int): The primary key identifier for the task.
        title (str): The title of the task, indexed for quick searches.
        description (str): A detailed description of the task.
        creation_date (datetime): The timestamp when the task was created, with timezone-aware UTC.
        due_date (datetime): The deadline by which the task is due.
        status (str): The current status of the task (e.g., 'pending', 'in_progress', 'completed').
    """

    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    description = Column(String)
    creation_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    due_date = Column(DateTime)
    status = Column(String)
