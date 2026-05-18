from collections.abc import Mapping, Sequence
from typing import Any


def sort_price_series(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return sorted((dict(row) for row in rows), key=lambda row: str(row.get("date", "")))


def extract_close_prices(rows: Sequence[Mapping[str, Any]]) -> list[float]:
    prices = []

    for row in sort_price_series(rows):
        close = row.get("close")
        if close not in (None, ""):
            prices.append(float(close))

    return prices
