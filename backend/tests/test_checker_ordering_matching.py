from __future__ import annotations

from app.services.checker import check_answer


def test_ordering_fully_correct():
    result = check_answer("ORDERING", [1, 3, 0, 4, 2], [1, 3, 0, 4, 2], {})
    assert result.is_correct is True
    assert result.score == 1.0


def test_ordering_fully_reversed_scores_zero_concordance():
    result = check_answer("ORDERING", [2, 4, 0, 3, 1], [1, 3, 0, 4, 2], {})
    assert result.is_correct is False
    assert result.score == 0.0


def test_ordering_partial_credit_between_zero_and_one():
    result = check_answer("ORDERING", [1, 0, 3, 4, 2], [1, 3, 0, 4, 2], {})
    assert result.is_correct is False
    assert 0.0 < result.score < 1.0


def test_ordering_with_different_items_is_invalid():
    result = check_answer("ORDERING", [1, 3, 0, 4, 99], [1, 3, 0, 4, 2], {})
    assert result.is_correct is False
    assert result.score == 0.0


def test_matching_fully_correct():
    correct = {"0": 1, "1": 3, "2": 2, "3": 0}
    submitted = {"0": 1, "1": 3, "2": 2, "3": 0}
    result = check_answer("MATCHING", submitted, correct, {})
    assert result.is_correct is True
    assert result.score == 1.0


def test_matching_partial_credit():
    correct = {"0": 1, "1": 3, "2": 2, "3": 0}
    submitted = {"0": 1, "1": 3, "2": 0, "3": 0}
    result = check_answer("MATCHING", submitted, correct, {})
    assert result.is_correct is False
    assert result.score == 0.75


def test_matching_missing_keys_does_not_raise():
    correct = {"0": 1, "1": 3, "2": 2, "3": 0}
    submitted = {"0": 1}
    result = check_answer("MATCHING", submitted, correct, {})
    assert result.is_correct is False
    assert result.score == 0.25
