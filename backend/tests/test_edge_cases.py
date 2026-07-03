from __future__ import annotations

# Провокационные примеры (edge cases) — результат №6 планируемых результатов
# практики: платформа не должна падать (500) на некорректном пользовательском
# вводе, а должна безопасно возвращать понятный результат.


def test_submit_without_session_header_is_rejected(client):
    response = client.post("/api/tasks/1/submit", json={"answer": 3})
    assert response.status_code == 422


def test_submit_to_nonexistent_task_returns_404(client, session_headers):
    response = client.post(
        "/api/tasks/99999/submit", json={"answer": 3}, headers=session_headers
    )
    assert response.status_code == 404


def test_submit_empty_string_answer_to_fill_blank(client, session_headers):
    response = client.post(
        "/api/tasks/3/submit", json={"answer": ""}, headers=session_headers
    )
    assert response.status_code == 200
    assert response.json()["is_correct"] is False


def test_submit_wrong_type_answer_does_not_crash(client, session_headers):
    # Task 1 is SINGLE_CHOICE (expects an int); sending a string must not 500.
    response = client.post(
        "/api/tasks/1/submit", json={"answer": "not-an-int"}, headers=session_headers
    )
    assert response.status_code == 200
    assert response.json()["is_correct"] is False


def test_submit_invalid_json_for_json_fix_task(client, session_headers):
    # Task 6 is JSON_FIX.
    response = client.post(
        "/api/tasks/6/submit",
        json={"answer": "{this is not valid json"},
        headers=session_headers,
    )
    assert response.status_code == 200
    assert response.json()["is_correct"] is False


def test_submit_sql_injection_like_string_is_handled_safely(client, session_headers):
    malicious = "'; DROP TABLE tasks; --"
    response = client.post(
        "/api/tasks/3/submit", json={"answer": malicious}, headers=session_headers
    )
    assert response.status_code == 200
    assert response.json()["is_correct"] is False
    # confirm the table was not affected
    follow_up = client.get("/api/tasks/3")
    assert follow_up.status_code == 200


def test_submit_very_long_string_answer(client, session_headers):
    long_answer = "x" * 20000
    response = client.post(
        "/api/tasks/3/submit", json={"answer": long_answer}, headers=session_headers
    )
    assert response.status_code == 200
    assert response.json()["is_correct"] is False


def test_submit_null_answer_does_not_crash(client, session_headers):
    response = client.post(
        "/api/tasks/2/submit", json={"answer": None}, headers=session_headers
    )
    assert response.status_code == 200
    assert response.json()["is_correct"] is False


def test_submit_matching_with_extra_unexpected_keys(client, session_headers):
    # Task 4 is MATCHING; submitting extra unrecognised keys must be ignored, not crash.
    response = client.post(
        "/api/tasks/4/submit",
        json={"answer": {"0": 1, "1": 3, "2": 2, "3": 0, "99": 99}},
        headers=session_headers,
    )
    assert response.status_code == 200
    assert response.json()["is_correct"] is True
