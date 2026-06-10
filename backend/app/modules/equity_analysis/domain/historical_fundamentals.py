from collections.abc import Sequence


def calculate_cagr(beginning_value: float | None, ending_value: float | None, periods: int) -> float | None:
    if beginning_value in (None, 0) or ending_value is None or periods <= 0:
        return None
    if beginning_value <= 0 or ending_value <= 0:
        return None
    return (ending_value / beginning_value) ** (1 / periods) - 1


def calculate_year_over_year_growth(
    history: Sequence[dict[str, float | int | None]],
    field_name: str,
) -> list[dict[str, float | int | None]]:
    rows = []
    ordered = sorted(history, key=lambda row: int(row["year"]))
    for previous, current in zip(ordered, ordered[1:]):
        previous_value = previous.get(field_name)
        current_value = current.get(field_name)
        growth = None
        if previous_value not in (None, 0) and current_value is not None:
            growth = (float(current_value) / float(previous_value)) - 1.0
        rows.append({"year": current["year"], "growth": growth})
    return rows


def calculate_margin_trends(
    history: Sequence[dict[str, float | int | None]],
    numerator_field: str,
    denominator_field: str = "revenue",
) -> list[dict[str, float | int | None]]:
    return [
        {
            "year": row["year"],
            "margin": _safe_divide(row.get(numerator_field), row.get(denominator_field)),
        }
        for row in sorted(history, key=lambda item: int(item["year"]))
    ]


def calculate_ratio_trends(
    history: Sequence[dict[str, float | int | None]],
    numerator_field: str,
    denominator_field: str,
) -> list[dict[str, float | int | None]]:
    return [
        {
            "year": row["year"],
            "ratio": _safe_divide(row.get(numerator_field), row.get(denominator_field)),
        }
        for row in sorted(history, key=lambda item: int(item["year"]))
    ]


def calculate_historical_average(values: Sequence[float | None]) -> float | None:
    clean_values = [value for value in values if value is not None]
    if not clean_values:
        return None
    return sum(clean_values) / len(clean_values)


def detect_trend_improvement(values: Sequence[float | None]) -> bool:
    clean_values = [value for value in values if value is not None]
    return len(clean_values) >= 2 and clean_values[-1] > clean_values[0]


def detect_trend_deterioration(values: Sequence[float | None]) -> bool:
    clean_values = [value for value in values if value is not None]
    return len(clean_values) >= 2 and clean_values[-1] < clean_values[0]


def _safe_divide(numerator: float | int | None, denominator: float | int | None) -> float | None:
    if numerator is None or denominator in (None, 0):
        return None
    return float(numerator) / float(denominator)
