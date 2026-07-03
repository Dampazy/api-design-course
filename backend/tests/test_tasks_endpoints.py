from __future__ import annotations


def test_list_tasks_returns_18_practice_plus_7_final(client):
    practice = client.get("/api/tasks", params={"is_final_test": False}).json()
    final_test = client.get("/api/tasks", params={"is_final_test": True}).json()
    assert len(practice) == 18
    assert len(final_test) == 7


def test_task_response_never_leaks_correct_answer(client):
    response = client.get("/api/tasks/1")
    assert response.status_code == 200
    body = response.json()
    assert "correct_answer" not in body
    assert "correct_answer_json" not in body


def test_get_task_404_for_unknown_id(client):
    response = client.get("/api/tasks/99999")
    assert response.status_code == 404


def test_filter_tasks_by_theory_block(client):
    response = client.get("/api/tasks", params={"theory_block_id": 1, "is_final_test": False})
    tasks = response.json()
    assert len(tasks) == 3
    assert all(t["theory_block_id"] == 1 for t in tasks)
