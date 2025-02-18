"""
schemas.py

This module defines the Pydantic data models (schemas) for task management.

These schemas are used for:
- Validating incoming data for task creation and updates
- Serializing task data for responses
- Ensuring consistent data structures throughout the application

Includes:
- TaskBaseDTO: Common fields for tasks
- TaskCreateDTO: Used when creating a new task
- TaskResponseDTO: Extends TaskBaseDTO for responses, adding ID and creation date
"""

from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Literal, Annotated

class TaskBaseDTO(BaseModel):
    """
    Base Data Transfer Object for tasks, containing the common attributes.
    Attributes:
        title (str): The task title, constrained to 1-100 characters.
        description (str): A detailed description, limited to 500 characters.
        due_date (datetime): The due date for task completion, expected as a valid ISO8601 datetime string with timezone awareness.
        status (Literal): The current status of the task ('pending', 'in_progress', 'completed').
    """
    title: Annotated[
        str,
        Field(
            ..., min_length=1, max_length=100,
            description="The title of the task. Must be between 1 and 100 characters."
        )
    ]
    description: Annotated[
        str,
        Field(
            ..., min_length=1, max_length=500,
            description="A detailed description of the task, limited to 500 characters."
        )
    ]
    due_date: Annotated[
        datetime,
        Field(
            ..., description="The due date by which the task should be completed. Must be a valid ISO8601 datetime string with timezone."
        )
    ]
    status: Annotated[
        Literal['pending', 'in_progress', 'completed'],
        Field(
            ..., description="The current status of the task. Options: 'pending', 'in_progress', 'completed'."
        )
    ]

class TaskCreateDTO(TaskBaseDTO):
    """
    Data Transfer Object for creating a new task.

    Inherits all fields from TaskBaseDTO. Used specifically for validating data when a user creates a new task.
    """
    pass

class TaskResponseDTO(TaskBaseDTO):
    """
    Response Data Transfer Object for task information.

    Extends TaskBaseDTO by adding:
        id (int): A unique identifier for the task.
        creation_date (datetime): Timestamp of when the task was created.

    This model is used for sending task information back to clients.
    """
    id: int = Field(..., description="The unique identifier of the task.")
    creation_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp indicating when the task was created."
    )

    class Config:
        """
        Configuration for Pydantic model.

        Enables ORM mode to allow the model to read data from ORM models directly.
        """
        from_attributes = True  # Replace `orm_mode` with `from_attributes`
