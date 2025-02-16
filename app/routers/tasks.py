from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..api_models import TaskCreateDTO, TaskResponseDTO
from ..db_schemas import TaskDBSchema
from ..database import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskResponseDTO, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreateDTO, db: Session = Depends(get_db)):
    db_task = TaskDBSchema(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return TaskResponseDTO.model_validate(db_task)

@router.get("/", response_model=List[TaskResponseDTO])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tasks = db.query(TaskDBSchema).offset(skip).limit(limit).all()
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
    all_tasks = db.query(TaskDBSchema).all()
    suggestions = []  # Implement smart suggestions logic
    return suggestions