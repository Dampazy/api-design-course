from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel


class SubmitRequest(BaseModel):
    answer: Any
    response_time_ms: Optional[int] = None


class SubmitResult(BaseModel):
    is_correct: bool
    score: float
    correct_answer: Any
    explanation_markdown: str
    attempts_count: int
