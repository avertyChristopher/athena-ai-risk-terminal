from __future__ import annotations

from typing import Any


def nested_get(data: dict[str, Any], *keys: str) -> Any:
    current: Any = data
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def first_present(data: dict[str, Any], paths: list[tuple[str, ...]]) -> Any:
    for path in paths:
        value = nested_get(data, *path)
        if value is not None:
            return value
    return None


def as_float(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def list_strings(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value else []
    if isinstance(value, list):
        return [str(item) for item in value if item is not None and str(item)]
    return [str(value)]


def compact_points(points: list[str], max_points: int) -> list[str]:
    unique: list[str] = []
    for point in points:
        cleaned = " ".join(str(point).split())
        if cleaned and cleaned not in unique:
            unique.append(cleaned)
        if len(unique) >= max_points:
            break
    return unique


def source_modules_from_payload(payload: dict[str, Any], fallback: str) -> list[str]:
    modules = [
        str(value)
        for value in [
            payload.get("source_module"),
            payload.get("module_name"),
            payload.get("module"),
        ]
        if value
    ]
    if not modules:
        modules.append(fallback)
    return compact_points(modules, 5)
