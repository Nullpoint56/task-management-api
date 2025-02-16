"""
tasks.py

This module provides a FastAPI router for task management operations.

Endpoints include:
- Creating a new task
- Retrieving a list of tasks
- Retrieving a single task by ID
- Updating a task by ID
- Deleting a task by ID
- Generating task suggestions (requires implementation)

Each endpoint interacts with the database using SQLAlchemy to perform CRUD operations on task data.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..api_models import TaskCreateDTO, TaskResponseDTO
from ..db_schemas import TaskDBSchema
from app.dependencies.database import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskResponseDTO, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreateDTO, db: Session = Depends(get_db)):
    """
    Create a new task.
    Args:
        task (TaskCreateDTO): The task data to create, including title, description, due_date, and status.
        db (Session): The SQLAlchemy database session.

    Returns:
        TaskResponseDTO: The newly created task.
    """
    db_task = TaskDBSchema(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return TaskResponseDTO.model_validate(db_task)

@router.get("/", response_model=List[TaskResponseDTO])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a list of tasks.
    Args:
        skip (int): Number of tasks to skip for pagination. Defaults to 0.
        limit (int): The maximum number of tasks to return. Defaults to 10.
        db (Session): The SQLAlchemy database session.

    Returns:
        List[TaskResponseDTO]: A list of tasks.
    """
    tasks = db.query(TaskDBSchema).offset(skip).limit(limit).all()
    return [TaskResponseDTO.model_validate(task) for task in tasks]

@router.get("/{task_id}", response_model=TaskResponseDTO)
def read_task(task_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific task by ID.
    Args:
        task_id (int): The ID of the task to retrieve.
        db (Session): The SQLAlchemy database session.

    Raises:
        HTTPException: If the task is not found.

    Returns:
        TaskResponseDTO: The task with the given ID.
    """
    task = db.query(TaskDBSchema).filter(TaskDBSchema.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponseDTO.model_validate(task)

@router.put("/{task_id}", response_model=TaskResponseDTO)
def update_task(task_id: int, updated_task: TaskCreateDTO, db: Session = Depends(get_db)):
    """
    Update an existing task by ID.

    Args:
        task_id (int): The ID of the task to update.
        updated_task (TaskCreateDTO): The data to update the task with.
        db (Session): The SQLAlchemy database session.

    Raises:
        HTTPException: If the task is not found.

    Returns:
        TaskResponseDTO: The updated task.
    """
    task = db.query(TaskDBSchema).filter(TaskDBSchema.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = updated_task.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return TaskResponseDTO.model_validate(task)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Delete a task by ID.

    Args:
        task_id (int): The ID of the task to delete.
        db (Session): The SQLAlchemy database session.

    Raises:
        HTTPException: If the task is not found.

    Returns:
        None: Indicates successful deletion.
    """
    task = db.query(TaskDBSchema).filter(TaskDBSchema.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()

@router.get("/suggestions/")
def smart_task_suggestions(db: Session = Depends(get_db)):
    """
    Provide smart task suggestions based on current task data.

    Args:
        db (Session): The SQLAlchemy database session.

    Returns:
        list: A list of suggested tasks (currently empty, implement logic).
    """
    all_tasks = db.query(TaskDBSchema).all()
    suggestions = []  # TODO: Implement task suggestion logic
    return suggestions