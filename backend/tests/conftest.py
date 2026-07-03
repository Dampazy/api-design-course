from __future__ import annotations

import json

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models  # noqa: F401
from app.database import Base, get_db
from app.main import app
from app.models.task import Task
from app.models.theory import TheoryBlock
from app.seed.tasks_data import TASKS
from app.seed.theory_data import THEORY_BLOCKS


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    slug_to_block = {}
    for block_data in THEORY_BLOCKS:
        block = TheoryBlock(**block_data)
        session.add(block)
        slug_to_block[block_data["slug"]] = block
    session.flush()

    for task_data in TASKS:
        block = slug_to_block[task_data["theory_slug"]]
        session.add(
            Task(
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
        )
    session.commit()

    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def session_headers():
    return {"X-Session-Id": "test-session-abc123"}
