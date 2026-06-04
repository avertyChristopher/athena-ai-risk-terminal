from collections import Counter
from collections.abc import Mapping, Sequence
from statistics import mean, stdev
from typing import Any


def detect_missing_prices(
    rows: Sequence[Mapping[str, Any]],
    price_column: str = "close",
) -> list[str]:
    missing_dates = []

    for row in rows:
        price = row.get(price_column)
        if price in (None, ""):
            missing_dates.append(str(row.get("date", "")))

    return missing_dates


def detect_duplicate_dates(rows: Sequence[Mapping[str, Any]]) -> list[str]:
    date_counts = Counter(str(row.get("date", "")) for row in rows)

    return [date for date, count in date_counts.items() if date and count > 1]


def detect_outliers(values: Sequence[float], threshold: float = 3.0) -> list[int]:
    if threshold <= 0:
        raise ValueError("Outlier threshold must be positive.")

    if len(values) < 3:
        return []

    sample_stdev = stdev(values)
    if sample_stdev == 0:
        return []

    sample_mean = mean(values)

    return [
        index
        for index, value in enumerate(values)
        if abs((value - sample_mean) / sample_stdev) > threshold
    ]
