from __future__ import annotations

from app.services.checker import check_answer


def test_fill_blank_exact_match():
    result = check_answer("FILL_BLANK", "GET", "GET", {"case_sensitive": False})
    assert result.is_correct is True


def test_fill_blank_case_insensitive():
    result = check_answer("FILL_BLANK", "get", "GET", {"case_sensitive": False})
    assert result.is_correct is True


def test_fill_blank_case_sensitive_rejects_wrong_case():
    result = check_answer("FILL_BLANK", "get", "GET", {"case_sensitive": True})
    assert result.is_correct is False


def test_fill_blank_ignores_surrounding_whitespace():
    result = check_answer("FILL_BLANK", "  GET  ", "GET", {"case_sensitive": False})
    assert result.is_correct is True


def test_fill_blank_alternative_answers():
    result = check_answer(
        "FILL_BLANK",
        "users/42/orders",
        "/users/42/orders",
        {"case_sensitive": False, "alternative_answers": ["users/42/orders"]},
    )
    assert result.is_correct is True


def test_fill_blank_completely_wrong_answer():
    result = check_answer("FILL_BLANK", "POST", "GET", {"case_sensitive": False})
    assert result.is_correct is False


def test_fill_blank_empty_string():
    result = check_answer("FILL_BLANK", "", "GET", {"case_sensitive": False})
    assert result.is_correct is False


def test_json_fix_valid_and_correct():
    correct = {"type": "https://x/conflict", "title": "t", "status": 409}
    submitted = '{"type": "https://x/conflict", "status": 409, "title": "t"}'
    result = check_answer("JSON_FIX", submitted, correct, {})
    assert result.is_correct is True, "key order must not matter for JSON equality"


def test_json_fix_missing_field():
    correct = {"type": "https://x/conflict", "title": "t", "status": 409}
    submitted = '{"type": "https://x/conflict", "title": "t"}'
    result = check_answer("JSON_FIX", submitted, correct, {})
    assert result.is_correct is False


def test_json_fix_invalid_json_does_not_raise():
    correct = {"type": "https://x/conflict", "title": "t", "status": 409}
    result = check_answer("JSON_FIX", "{not valid json", correct, {})
    assert result.is_correct is False
    assert "invalid JSON" in result.detail
