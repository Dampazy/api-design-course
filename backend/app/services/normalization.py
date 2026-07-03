from __future__ import annotations

import json
import re
from typing import Any


def parse_json_field(raw: str) -> Any:
    return json.loads(raw)


def normalize_text(value: str, *, case_sensitive: bool = True) -> str:
    normalized = re.sub(r"\s+", " ", value.strip())
    if not case_sensitive:
        normalized = normalized.lower()
    return normalized
