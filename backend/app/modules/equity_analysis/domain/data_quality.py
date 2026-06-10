from collections.abc import Mapping, Sequence
from typing import Any


REQUIRED_FUNDAMENTAL_FIELDS = [
    "revenue",
    "eps",
    "assets",
    "liabilities",
    "equity",
    "debt",
    "cash",
    "operating_cash_flow",
    "capital_expenditures",
    "free_cash_flow",
]


def detect_missing_fundamental_fields(
    fundamentals: Mapping[str, Any],
    required_fields: Sequence[str] = REQUIRED_FUNDAMENTAL_FIELDS,
) -> list[str]:
    return [
        field
        for field in required_fields
        if fundamentals.get(field) is None
    ]


def validate_fundamental_completeness(fundamentals: Mapping[str, Any]) -> bool:
    return not detect_missing_fundamental_fields(fundamentals)


def validate_market_cap_consistency(
    reported_market_cap: float,
    price: float | None,
    shares_outstanding: float | None,
    tolerance: float = 0.02,
) -> bool:
    if price is None or shares_outstanding in (None, 0):
        return False
    implied_market_cap = price * shares_outstanding
    if implied_market_cap == 0:
        return False
    return abs(reported_market_cap - implied_market_cap) / implied_market_cap <= tolerance


def validate_fcf_consistency(
    free_cash_flow: float | None,
    operating_cash_flow: float | None,
    capital_expenditures: float | None,
    tolerance: float = 0.02,
) -> bool:
    if free_cash_flow is None or operating_cash_flow is None or capital_expenditures is None:
        return False
    expected_fcf = operating_cash_flow - capital_expenditures
    base = max(abs(expected_fcf), 1.0)
    return abs(free_cash_flow - expected_fcf) / base <= tolerance


def create_equity_data_quality_score(warnings: Sequence[str], missing_fields: Sequence[str]) -> float:
    penalty = min(1.0, 0.08 * len(warnings) + 0.10 * len(missing_fields))
    return max(0.0, 1.0 - penalty)


def create_equity_data_quality_report(
    fundamentals: Mapping[str, Any],
    warnings: Sequence[str],
) -> dict[str, Any]:
    missing_fields = detect_missing_fundamental_fields(fundamentals)
    return {
        "missing_fields": missing_fields,
        "warnings": list(warnings),
        "quality_score": create_equity_data_quality_score(warnings, missing_fields),
        "is_usable": not missing_fields,
    }
