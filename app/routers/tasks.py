import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import asc, desc
from typing import List, Optional
from ..api_models import TaskCreateDTO, TaskResponseDTO
from ..db_schemas import TaskDBSchema
from app.dependencies.database import get_db
from ..services.smart_task_suggestion import get_semantically_similar_tasks

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreateDTO, db: AsyncSession = Depends(get_db)):
    db_task = TaskDBSchema(**task.model_dump())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return TaskResponseDTO.model_validate(db_task)

@router.get("/", response_model=List[TaskResponseDTO])
async def read_tasks(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    task_status: Optional[str] = Query(None, description="Filter by task status"),
    sort_by: Optional[str] = Query("creation_date", description="Sort by 'creation_date' or 'due_date'"),
    sort_order: Optional[str] = Query("asc", description="Sort order 'asc' or 'desc'")
):
    query = select(TaskDBSchema)

    if task_status:
        query = query.filter(TaskDBSchema.status == task_status)

    if sort_by not in ["creation_date", "due_date"]:
        raise HTTPException(status_code=400, detail="Invalid sort_by value. Must be 'creation_date' or 'due_date'.")

    if sort_order == "asc":
        query = query.order_by(asc(getattr(TaskDBSchema, sort_by)))
    else:
        query = query.order_by(desc(getattr(TaskDBSchema, sort_by)))

    result = await db.execute(query.offset(skip).limit(limit))
    tasks = result.scalars().all()
    return [TaskResponseDTO.model_validate(task) for task in tasks]

@router.get("/{task_id}", response_model=TaskResponseDTO)
async def read_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskDBSchema).filter(TaskDBSchema.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponseDTO.model_validate(task)

@router.put("/{task_id}", response_model=TaskResponseDTO)
async def update_task(task_id: int, updated_task: TaskCreateDTO, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskDBSchema).filter(TaskDBSchema.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = updated_task.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
    await db.commit()
    await db.refresh(task)
    return TaskResponseDTO.model_validate(task)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskDBSchema).filter(TaskDBSchema.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.delete(task)
    await db.commit()

@router.get("/suggestions/")
async def smart_task_suggestions(db: AsyncSession = Depends(get_db)):
    text_similarity_threshold = 0.5
    top_k_clusters = 5
    time_similarity_threshold = datetime.timedelta(days=1)
    suggested_task_amount = 5
    tasks = await db.execute(select(TaskDBSchema))
    semantically_similar_tasks = get_semantically_similar_tasks(tasks, text_similarity_threshold, top_k_clusters)
    completion_time_similar_tasks = get_completion_time_similar_tasks(tasks, time_similarity_threshold, top_k_clusters)
    suggested_tasks = generate_new_tasks(semantically_similar_tasks, completion_time_similar_tasks, suggested_task_amount)
    return suggested_tasks