from __future__ import annotations

import pytest

from app.services.checker import check_answer


def test_api_request_simple_get_correct():
    correct = {"method": "GET", "path": "/orders/42"}
    result = check_answer("API_REQUEST", "GET /orders/42", correct, {})
    assert result.is_correct is True
    assert result.score == 1.0


def test_api_request_wrong_method():
    correct = {"method": "DELETE", "path": "/orders/42"}
    result = check_answer("API_REQUEST", "GET /orders/42", correct, {})
    assert result.is_correct is False
    assert result.score == 0.5


def test_api_request_wrong_path():
    correct = {"method": "GET", "path": "/orders/42"}
    result = check_answer("API_REQUEST", "GET /orders/43", correct, {})
    assert result.is_correct is False
    assert result.score == 0.5


def test_api_request_case_insensitive_method():
    correct = {"method": "GET", "path": "/orders/42"}
    result = check_answer("API_REQUEST", "get /orders/42", correct, {})
    assert result.is_correct is True


def test_api_request_trailing_slash_ignored():
    correct = {"method": "GET", "path": "/orders/42"}
    result = check_answer("API_REQUEST", "GET /orders/42/", correct, {})
    assert result.is_correct is True


def test_api_request_with_body_correct():
    correct = {
        "method": "POST",
        "path": "/orders",
        "body": {"user_id": 42, "items": [{"sku": "ABC-1", "qty": 2}]},
    }
    submitted = 'POST /orders\n{"user_id": 42, "items": [{"sku": "ABC-1", "qty": 2}]}'
    result = check_answer("API_REQUEST", submitted, correct, {})
    assert result.is_correct is True
    assert result.score == 1.0


def test_api_request_with_body_key_order_does_not_matter():
    correct = {"method": "POST", "path": "/orders", "body": {"a": 1, "b": 2}}
    submitted = 'POST /orders\n{"b": 2, "a": 1}'
    result = check_answer("API_REQUEST", submitted, correct, {})
    assert result.is_correct is True


def test_api_request_missing_required_body():
    correct = {"method": "POST", "path": "/orders", "body": {"a": 1}}
    result = check_answer("API_REQUEST", "POST /orders", correct, {})
    assert result.is_correct is False
    assert result.score == pytest.approx(2 / 3)


def test_api_request_invalid_json_body_does_not_raise():
    correct = {"method": "POST", "path": "/orders", "body": {"a": 1}}
    submitted = "POST /orders\n{not valid json"
    result = check_answer("API_REQUEST", submitted, correct, {})
    assert result.is_correct is False


def test_api_request_query_params_order_independent():
    correct = {"method": "GET", "path": "/orders", "query": {"status": "paid", "limit": "10"}}
    result = check_answer("API_REQUEST", "GET /orders?limit=10&status=paid", correct, {})
    assert result.is_correct is True


def test_api_request_missing_query_param():
    correct = {"method": "GET", "path": "/orders", "query": {"status": "paid", "limit": "10"}}
    result = check_answer("API_REQUEST", "GET /orders?status=paid", correct, {})
    assert result.is_correct is False


def test_api_request_empty_submission_does_not_raise():
    correct = {"method": "GET", "path": "/orders/42"}
    result = check_answer("API_REQUEST", "", correct, {})
    assert result.is_correct is False
    assert result.score == 0.0


def test_api_request_garbage_submission_does_not_raise():
    correct = {"method": "GET", "path": "/orders/42"}
    result = check_answer("API_REQUEST", "this is not a request at all", correct, {})
    assert result.is_correct is False
