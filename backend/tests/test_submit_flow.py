from __future__ import annotations


def test_submit_correct_answer(client, session_headers):
    response = client.post(
        "/api/tasks/1/submit",
        json={"answer": 3, "response_time_ms": 5000},
        headers=session_headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["is_correct"] is True
    assert body["score"] == 1.0
    assert body["attempts_count"] == 1


def test_submit_incorrect_answer(client, session_headers):
    response = client.post(
        "/api/tasks/1/submit",
        json={"answer": 0, "response_time_ms": 3000},
        headers=session_headers,
    )
    body = response.json()
    assert body["is_correct"] is False
    assert body["attempts_count"] == 1


def test_submit_twice_increments_attempts_count(client, session_headers):
    client.post("/api/tasks/1/submit", json={"answer": 0}, headers=session_headers)
    response = client.post("/api/tasks/1/submit", json={"answer": 3}, headers=session_headers)
    assert response.json()["attempts_count"] == 2


def test_progress_reflects_solved_task(client, session_headers):
    before = client.get("/api/progress", headers=session_headers).json()
    assert before["solved"] == 0

    client.post("/api/tasks/1/submit", json={"answer": 3}, headers=session_headers)

    after = client.get("/api/progress", headers=session_headers).json()
    assert after["solved"] == 1
    assert after["total_tasks"] == 30
    block_1 = next(b for b in after["by_block"] if b["theory_block_id"] == 1)
    assert block_1["solved"] == 1
    assert block_1["total"] == 5


def test_progress_is_isolated_per_session(client):
    client.post(
        "/api/tasks/1/submit",
        json={"answer": 3},
        headers={"X-Session-Id": "session-a"},
    )
    progress_a = client.get("/api/progress", headers={"X-Session-Id": "session-a"}).json()
    progress_b = client.get("/api/progress", headers={"X-Session-Id": "session-b"}).json()
    assert progress_a["solved"] == 1
    assert progress_b["solved"] == 0


def test_stats_updates_after_submission(client, session_headers):
    client.post(
        "/api/tasks/1/submit",
        json={"answer": 3, "response_time_ms": 4000},
        headers=session_headers,
    )
    stats = client.get("/api/stats/tasks/1").json()
    assert stats["total_attempts"] == 1
    assert stats["correct_rate"] == 100.0
    assert stats["avg_response_time_ms"] == 4000.0
