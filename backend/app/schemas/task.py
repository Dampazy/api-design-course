from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

from app.services.normalization import parse_json_field


class TaskOut(BaseModel):
    """Public task representation. Deliberately excludes the correct answer
    (correct_answer_json) so it can never leak to the client before the
    user submits.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    theory_block_id: int
    order_index: int
    title: str
    statement_markdown: str
    task_type: str
    options: Optional[Any] = None
    is_final_test: bool

    @classmethod
    def from_task(cls, task) -> "TaskOut":  # noqa: ANN001
        return cls(
            id=task.id,
            theory_block_id=task.theory_block_id,
            order_index=task.order_index,
            title=task.title,
            statement_markdown=task.statement_markdown,
            task_type=task.task_type,
            options=parse_json_field(task.options_json),
            is_final_test=task.is_final_test,
        )
