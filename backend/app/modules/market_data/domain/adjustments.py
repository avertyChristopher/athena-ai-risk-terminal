from collections.abc import Mapping, Sequence
from typing import Any


def calculate_price_return(previous_close: float, current_close: float) -> float:
    return (current_close / previous_close) - 1.0


def calculate_total_return(
    previous_adjusted_close: float,
    current_adjusted_close: float,
) -> float:
    return (current_adjusted_close / previous_adjusted_close) - 1.0


def adjust_prices_for_splits(
    rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    adjusted_rows = []
    cumulative_split_factor = 1.0
    for row in reversed(list(rows)):
        split_factor = float(row.get("split_factor", 1.0))
        cumulative_split_factor *= split_factor
        adjusted_row = dict(row)
        adjusted_row["adjusted_close"] = float(row["close"]) / cumulative_split_factor
        adjusted_rows.append(adjusted_row)
    return list(reversed(adjusted_rows))


def validate_adjusted_close(rows: Sequence[Mapping[str, Any]]) -> bool:
    return all(float(row.get("adjusted_close", row["close"])) > 0 for row in rows)
