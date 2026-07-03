from __future__ import annotations

import json

from app import models  # noqa: F401  (registers models on Base)
from app.database import Base, SessionLocal, engine
from app.models.attempt import Attempt
from app.models.task import Task
from app.models.theory import TheoryBlock
from app.seed.tasks_data import TASKS
from app.seed.theory_data import THEORY_BLOCKS


def run() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Idempotent reseed: wipe dependent data first, then reinsert from
        # the seed modules. Course content lives only in theory_data.py /
        # tasks_data.py, never hardcoded in routers.
        db.query(Attempt).delete()
        db.query(Task).delete()
        db.query(TheoryBlock).delete()
        db.commit()

        slug_to_block: dict[str, TheoryBlock] = {}
        for block_data in THEORY_BLOCKS:
            block = TheoryBlock(**block_data)
            db.add(block)
            slug_to_block[block_data["slug"]] = block
        db.flush()

        for task_data in TASKS:
            theory_slug = task_data["theory_slug"]
            block = slug_to_block[theory_slug]
            task = Task(
                theory_block_id=block.id,
                order_index=task_data["order_index"],
                title=task_data["title"],
                statement_markdown=task_data["statement_markdown"],
                task_type=task_data["task_type"],
                options_json=json.dumps(task_data["options"]),
                correct_answer_json=json.dumps(task_data["correct_answer"]),
                check_config_json=json.dumps(task_data["check_config"]),
                explanation_markdown=task_data["explanation_markdown"],
                is_final_test=task_data["is_final_test"],
            )
            db.add(task)

        db.commit()

        theory_count = db.query(TheoryBlock).count()
        task_count = db.query(Task).count()
        practice_count = db.query(Task).filter(Task.is_final_test.is_(False)).count()
        final_count = db.query(Task).filter(Task.is_final_test.is_(True)).count()
        print(
            f"Seeded {theory_count} theory blocks, {task_count} tasks "
            f"({practice_count} practice + {final_count} final test)."
        )
    finally:
        db.close()


if __name__ == "__main__":
    run()
