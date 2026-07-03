from __future__ import annotations

import json
from typing import List, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.attempt import Attempt
from app.models.task import Task
from app.schemas.submission import SubmitRequest, SubmitResult
from app.schemas.task import TaskOut
from app.services.checker import check_answer

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=List[TaskOut])
def list_tasks(
    theory_block_id: Optional[int] = Query(default=None),
    is_final_test: Optional[bool] = Query(default=None),
    db: Session = Depends(get_db),
) -> List[TaskOut]:
    query = db.query(Task)
    if theory_block_id is not None:
        query = query.filter(Task.theory_block_id == theory_block_id)
    if is_final_test is not None:
        query = query.filter(Task.is_final_test == is_final_test)
    tasks = query.order_by(Task.theory_block_id, Task.order_index).all()
    return [TaskOut.from_task(t) for t in tasks]


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)) -> TaskOut:
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskOut.from_task(task)


@router.post("/{task_id}/submit", response_model=SubmitResult)
def submit_answer(
    task_id: int,
    payload: SubmitRequest,
    x_session_id: str = Header(...),
    db: Session = Depends(get_db),
) -> SubmitResult:
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    correct_answer = json.loads(task.correct_answer_json)
    check_config = json.loads(task.check_config_json)
    result = check_answer(task.task_type, payload.answer, correct_answer, check_config)

    attempt = Attempt(
        session_id=x_session_id,
        task_id=task.id,
        submitted_answer_json=json.dumps(payload.answer),
        is_correct=result.is_correct,
        score=result.score,
        response_time_ms=payload.response_time_ms,
    )
    db.add(attempt)
    db.commit()

    attempts_count = (
        db.query(Attempt)
        .filter(Attempt.session_id == x_session_id, Attempt.task_id == task.id)
        .count()
    )

    return SubmitResult(
        is_correct=result.is_correct,
        score=result.score,
        correct_answer=correct_answer,
        explanation_markdown=task.explanation_markdown,
        attempts_count=attempts_count,
    )
