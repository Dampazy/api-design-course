from __future__ import annotations

from app.services.checker import check_answer


def test_single_choice_correct():
    result = check_answer("SINGLE_CHOICE", 3, 3, {})
    assert result.is_correct is True
    assert result.score == 1.0


def test_single_choice_incorrect():
    result = check_answer("SINGLE_CHOICE", 1, 3, {})
    assert result.is_correct is False
    assert result.score == 0.0


def test_multiple_choice_exact_match():
    result = check_answer("MULTIPLE_CHOICE", [0, 2, 3], [3, 0, 2], {})
    assert result.is_correct is True


def test_multiple_choice_partial_selection_is_wrong():
    result = check_answer("MULTIPLE_CHOICE", [0, 2], [0, 2, 3], {})
    assert result.is_correct is False
    assert result.score == 0.0


def test_multiple_choice_extra_selection_is_wrong():
    result = check_answer("MULTIPLE_CHOICE", [0, 1, 2, 3], [0, 2, 3], {})
    assert result.is_correct is False


def test_multiple_choice_empty_submission():
    result = check_answer("MULTIPLE_CHOICE", [], [0, 2, 3], {})
    assert result.is_correct is False
    assert result.score == 0.0
