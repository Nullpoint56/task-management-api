"""
tasks.py

This module provides a FastAPI router for task management operations.
Endpoints include:
- Creating a new task
- Retrieving a list of tasks with filtering and sorting
- Retrieving a single task by ID
- Updating a task by ID
- Deleting a task by ID
- Generating smart task suggestions

Each endpoint interacts with the database using SQLAlchemy to perform CRUD operations on task data.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from typing import List, Optional
from ..api_models import TaskCreateDTO, TaskResponseDTO
from ..db_schemas import TaskDBSchema
from app.dependencies.database import get_db
from app.services.suggestions import analyze_task_data

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskResponseDTO, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreateDTO, db: Session = Depends(get_db)):
    db_task = TaskDBSchema(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return TaskResponseDTO.model_validate(db_task)

@router.get("/", response_model=List[TaskResponseDTO])
def read_tasks(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = Query(None, description="Filter by task status"),
    sort_by: Optional[str] = Query("creation_date", description="Sort by 'creation_date' or 'due_date'"),
    sort_order: Optional[str] = Query("asc", description="Sort order 'asc' or 'desc'")
):
    query = db.query(TaskDBSchema)

    if status:
        query = query.filter(TaskDBSchema.status == status)

    if sort_by not in ["creation_date", "due_date"]:
        raise HTTPException(status_code=400, detail="Invalid sort_by value. Must be 'creation_date' or 'due_date'.")

    if sort_order == "asc":
        query = query.order_by(asc(getattr(TaskDBSchema, sort_by)))
    else:
        query = query.order_by(desc(getattr(TaskDBSchema, sort_by)))

    tasks = query.offset(skip).limit(limit).all()
    return [TaskResponseDTO.model_validate(task) for task in tasks]

@router.get("/{task_id}", response_model=TaskResponseDTO)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDBSchema).filter(TaskDBSchema.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponseDTO.model_validate(task)

@router.put("/{task_id}", response_model=TaskResponseDTO)
def update_task(task_id: int, updated_task: TaskCreateDTO, db: Session = Depends(get_db)):
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
    task = db.query(TaskDBSchema).filter(TaskDBSchema.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()

@router.get("/suggestions/")
def smart_task_suggestions(db: Session = Depends(get_db)):
    """
    Generate task suggestions based on their titles, descriptions, and common completion patterns.

    Args:
        db (Session): The SQLAlchemy database session.

    Returns:
        List[str]: A list of suggested task ideas.
    """
    word_counter, completed_sequences = analyze_task_data(db)

    # Generate suggestions from frequency and sequence analysis
    common_words = word_counter.most_common(5)
    task_suggestions = [
        f"Consider tasks related to '{word}'"
        for word, _ in common_words
    ]
    for task, sequenced_tasks in completed_sequences.items():
        task_suggestions.extend(
            f"Consider a follow-up task like '{seq_task}' often completed after '{task}'"
            for seq_task in sequenced_tasks
        )
    return task_suggestions