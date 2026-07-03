from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.task import Task
from app.schemas.progress import TaskStatOut
from app.services import progress_service

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("", response_model=List[TaskStatOut])
def get_stats(db: Session = Depends(get_db)) -> List[TaskStatOut]:
    return progress_service.get_stats(db)


@router.get("/tasks/{task_id}", response_model=TaskStatOut)
def get_task_stat(task_id: int, db: Session = Depends(get_db)) -> TaskStatOut:
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return progress_service.get_task_stat(db, task)
