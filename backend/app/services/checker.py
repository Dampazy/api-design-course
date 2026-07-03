from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List

from app.services.normalization import normalize_text


@dataclass
class CheckResult:
    is_correct: bool
    score: float
    detail: str = ""


def check_answer(
    task_type: str,
    submitted: Any,
    correct_answer: Any,
    check_config: Dict[str, Any],
) -> CheckResult:
    strategy = _STRATEGIES.get(task_type)
    if strategy is None:
        return CheckResult(is_correct=False, score=0.0, detail=f"Unknown task type: {task_type}")
    try:
        return strategy(submitted, correct_answer, check_config)
    except Exception as exc:  # noqa: BLE001 - never let a malformed answer 500 the request
        return CheckResult(is_correct=False, score=0.0, detail=f"Could not evaluate answer: {exc}")


def _check_single_choice(submitted: Any, correct_answer: Any, _config: Dict[str, Any]) -> CheckResult:
    is_correct = int(submitted) == int(correct_answer)
    return CheckResult(is_correct=is_correct, score=1.0 if is_correct else 0.0)


def _check_multiple_choice(submitted: Any, correct_answer: Any, _config: Dict[str, Any]) -> CheckResult:
    submitted_set = {int(x) for x in submitted}
    correct_set = {int(x) for x in correct_answer}
    is_correct = submitted_set == correct_set
    return CheckResult(is_correct=is_correct, score=1.0 if is_correct else 0.0)


def _check_fill_blank(submitted: Any, correct_answer: Any, config: Dict[str, Any]) -> CheckResult:
    case_sensitive = bool(config.get("case_sensitive", True))
    submitted_text = normalize_text(str(submitted), case_sensitive=case_sensitive)
    candidates = [str(correct_answer), *config.get("alternative_answers", [])]
    normalized_candidates = {normalize_text(c, case_sensitive=case_sensitive) for c in candidates}
    is_correct = submitted_text in normalized_candidates
    return CheckResult(is_correct=is_correct, score=1.0 if is_correct else 0.0)


def _check_ordering(submitted: Any, correct_answer: Any, _config: Dict[str, Any]) -> CheckResult:
    submitted_seq: List[int] = [int(x) for x in submitted]
    correct_seq: List[int] = [int(x) for x in correct_answer]

    if not submitted_seq or set(submitted_seq) != set(correct_seq):
        return CheckResult(is_correct=False, score=0.0, detail="Submitted ordering uses different items")

    is_correct = submitted_seq == correct_seq
    score = _pairwise_order_score(submitted_seq, correct_seq)
    return CheckResult(is_correct=is_correct, score=score)


def _pairwise_order_score(submitted_seq: List[int], correct_seq: List[int]) -> float:
    position_in_correct = {item: idx for idx, item in enumerate(correct_seq)}
    n = len(submitted_seq)
    total_pairs = n * (n - 1) // 2
    if total_pairs == 0:
        return 1.0
    concordant_pairs = 0
    for i in range(n):
        for j in range(i + 1, n):
            if position_in_correct[submitted_seq[i]] < position_in_correct[submitted_seq[j]]:
                concordant_pairs += 1
    return concordant_pairs / total_pairs


def _check_matching(submitted: Any, correct_answer: Dict[str, Any], _config: Dict[str, Any]) -> CheckResult:
    submitted_map = {str(k): v for k, v in dict(submitted).items()}
    total = len(correct_answer)
    if total == 0:
        return CheckResult(is_correct=True, score=1.0)
    matched = sum(
        1
        for left_key, right_value in correct_answer.items()
        if str(submitted_map.get(str(left_key))) == str(right_value)
    )
    score = matched / total
    return CheckResult(is_correct=score == 1.0, score=score)


def _check_json_fix(submitted: Any, correct_answer: Dict[str, Any], _config: Dict[str, Any]) -> CheckResult:
    if isinstance(submitted, str):
        try:
            parsed = json.loads(submitted)
        except json.JSONDecodeError as exc:
            return CheckResult(is_correct=False, score=0.0, detail=f"invalid JSON: {exc}")
    else:
        parsed = submitted
    is_correct = parsed == correct_answer
    return CheckResult(is_correct=is_correct, score=1.0 if is_correct else 0.0)


_STRATEGIES = {
    "SINGLE_CHOICE": _check_single_choice,
    "MULTIPLE_CHOICE": _check_multiple_choice,
    "FILL_BLANK": _check_fill_blank,
    "ORDERING": _check_ordering,
    "MATCHING": _check_matching,
    "JSON_FIX": _check_json_fix,
}
