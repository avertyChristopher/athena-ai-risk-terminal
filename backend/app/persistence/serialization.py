from __future__ import annotations

import json
from datetime import date, datetime
from typing import Any, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def to_json(value: Any) -> str:
    if isinstance(value, BaseModel):
        value = value.model_dump(mode="json")
    return json.dumps(value, default=_json_default, ensure_ascii=False, sort_keys=True)


def from_json(value: str | None, fallback: Any) -> Any:
    if not value:
        return fallback
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return fallback


def model_from_json(model: type[T], value: str) -> T:
    return model.model_validate(from_json(value, {}))


def value_to_text(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, (dict, list)):
        return to_json(value)
    return str(value)


def text_to_value(value: str | None) -> Any:
    if value is None:
        return None
    stripped = value.strip()
    if stripped.startswith("{") or stripped.startswith("["):
        return from_json(stripped, value)
    try:
        return float(value)
    except ValueError:
        return value


def coerce_datetime(value: datetime | date | str | None) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return datetime.min
    return datetime.min


def _json_default(value: Any) -> str:
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return str(value)

