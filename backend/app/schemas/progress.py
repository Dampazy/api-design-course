from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class BlockProgressOut(BaseModel):
    theory_block_id: int
    title: str
    solved: int
    total: int


class ProgressOut(BaseModel):
    total_tasks: int
    solved: int
    percent: float
    by_block: List[BlockProgressOut]
    final_test_passed: bool
    solved_task_ids: List[int]


class FinalTestProgressOut(BaseModel):
    total: int
    solved: int
    percent: float
    passed: bool
    solved_task_ids: List[int]


class TaskStatOut(BaseModel):
    task_id: int
    title: str
    theory_block_title: str
    total_attempts: int
    correct_rate: float
    avg_response_time_ms: Optional[float] = None
