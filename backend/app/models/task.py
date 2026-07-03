from __future__ import annotations

import enum
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class TaskType(str, enum.Enum):
    SINGLE_CHOICE = "SINGLE_CHOICE"
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    FILL_BLANK = "FILL_BLANK"
    ORDERING = "ORDERING"
    MATCHING = "MATCHING"
    JSON_FIX = "JSON_FIX"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    theory_block_id: Mapped[int] = mapped_column(ForeignKey("theory_blocks.id"))
    order_index: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(200))
    statement_markdown: Mapped[str] = mapped_column(Text)
    task_type: Mapped[str] = mapped_column(String(30))
    options_json: Mapped[str] = mapped_column(Text)
    correct_answer_json: Mapped[str] = mapped_column(Text)
    check_config_json: Mapped[str] = mapped_column(Text, default="{}")
    explanation_markdown: Mapped[str] = mapped_column(Text)
    is_final_test: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    theory_block: Mapped["TheoryBlock"] = relationship(back_populates="tasks")
