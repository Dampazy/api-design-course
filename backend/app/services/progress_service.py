from __future__ import annotations

from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.attempt import Attempt
from app.models.task import Task
from app.models.theory import TheoryBlock
from app.schemas.progress import (
    BlockProgressOut,
    FinalTestProgressOut,
    ProgressOut,
    TaskStatOut,
)

FINAL_TEST_PASS_THRESHOLD = 0.7


def _solved_task_ids(db: Session, session_id: str, task_ids: List[int]) -> set:
    if not task_ids:
        return set()
    rows = (
        db.query(Attempt.task_id)
        .filter(
            Attempt.session_id == session_id,
            Attempt.task_id.in_(task_ids),
            Attempt.is_correct.is_(True),
        )
        .distinct()
        .all()
    )
    return {row[0] for row in rows}


def get_progress(db: Session, session_id: str) -> ProgressOut:
    blocks = db.query(TheoryBlock).order_by(TheoryBlock.order_index).all()
    practice_tasks = db.query(Task).filter(Task.is_final_test.is_(False)).all()
    solved_ids = _solved_task_ids(db, session_id, [t.id for t in practice_tasks])

    by_block: List[BlockProgressOut] = []
    for block in blocks:
        block_task_ids = [t.id for t in practice_tasks if t.theory_block_id == block.id]
        block_solved = len(solved_ids.intersection(block_task_ids))
        by_block.append(
            BlockProgressOut(
                theory_block_id=block.id,
                title=block.title,
                solved=block_solved,
                total=len(block_task_ids),
            )
        )

    total_tasks = len(practice_tasks)
    solved = len(solved_ids)
    percent = round(100 * solved / total_tasks, 1) if total_tasks else 0.0

    final_test = get_final_test_progress(db, session_id)

    return ProgressOut(
        total_tasks=total_tasks,
        solved=solved,
        percent=percent,
        by_block=by_block,
        final_test_passed=final_test.passed,
        solved_task_ids=sorted(solved_ids),
    )


def get_final_test_progress(db: Session, session_id: str) -> FinalTestProgressOut:
    final_tasks = db.query(Task).filter(Task.is_final_test.is_(True)).all()
    solved_ids = _solved_task_ids(db, session_id, [t.id for t in final_tasks])

    total = len(final_tasks)
    solved = len(solved_ids)
    percent = round(100 * solved / total, 1) if total else 0.0
    passed = total > 0 and (solved / total) >= FINAL_TEST_PASS_THRESHOLD

    return FinalTestProgressOut(
        total=total,
        solved=solved,
        percent=percent,
        passed=passed,
        solved_task_ids=sorted(solved_ids),
    )


def get_stats(db: Session) -> List[TaskStatOut]:
    tasks = (
        db.query(Task)
        .join(TheoryBlock, Task.theory_block_id == TheoryBlock.id)
        .order_by(TheoryBlock.order_index, Task.order_index)
        .all()
    )
    results: List[TaskStatOut] = []
    for task in tasks:
        results.append(get_task_stat(db, task))
    return results


def get_task_stat(db: Session, task: Task) -> TaskStatOut:
    total_attempts = db.query(func.count(Attempt.id)).filter(Attempt.task_id == task.id).scalar() or 0
    correct_attempts = (
        db.query(func.count(Attempt.id))
        .filter(Attempt.task_id == task.id, Attempt.is_correct.is_(True))
        .scalar()
        or 0
    )
    avg_response_time_ms = (
        db.query(func.avg(Attempt.response_time_ms))
        .filter(Attempt.task_id == task.id, Attempt.response_time_ms.isnot(None))
        .scalar()
    )
    correct_rate = round(100 * correct_attempts / total_attempts, 1) if total_attempts else 0.0

    return TaskStatOut(
        task_id=task.id,
        title=task.title,
        theory_block_title=task.theory_block.title,
        total_attempts=total_attempts,
        correct_rate=correct_rate,
        avg_response_time_ms=round(avg_response_time_ms, 1) if avg_response_time_ms is not None else None,
    )
