from collections.abc import Mapping, Sequence
from typing import Any

REQUIRED_OHLCV_COLUMNS = {"date", "symbol", "open", "high", "low", "close", "volume"}


def validate_price_data(
    rows: Sequence[Mapping[str, Any]],
    required_columns: set[str] | None = None,
) -> bool:
    if not rows:
        raise ValueError("At least one price row is required.")

    required = required_columns or REQUIRED_OHLCV_COLUMNS
    missing_columns = required - set(rows[0].keys())

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required price columns: {missing}.")

    for row in rows:
        close = row.get("close")
        if close in (None, ""):
            continue

        if float(close) <= 0:
            raise ValueError("Close prices must be strictly positive.")

    return True
