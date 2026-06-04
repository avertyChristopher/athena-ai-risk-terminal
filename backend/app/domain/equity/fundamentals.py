from typing import Any

from app.domain.equity.instruments import (
    calculate_book_value_per_share,
    calculate_market_cap,
)


def calculate_free_cash_flow(
    operating_cash_flow: float | None,
    capital_expenditures: float | None,
) -> float | None:
    if operating_cash_flow is None or capital_expenditures is None:
        return None
    return operating_cash_flow - abs(capital_expenditures)


def calculate_revenue_growth(
    current_revenue: float | None,
    prior_revenue: float | None,
) -> float | None:
    return _calculate_growth(current_revenue, prior_revenue)


def calculate_eps_growth(
    current_eps: float | None,
    prior_eps: float | None,
) -> float | None:
    return _calculate_growth(current_eps, prior_eps)


def calculate_operating_income_growth(
    current_operating_income: float | None,
    prior_operating_income: float | None,
) -> float | None:
    return _calculate_growth(current_operating_income, prior_operating_income)


def calculate_working_capital(
    current_assets: float | None,
    current_liabilities: float | None,
) -> float | None:
    if current_assets is None or current_liabilities is None:
        return None
    return current_assets - current_liabilities


def calculate_enterprise_value(
    market_cap: float,
    total_debt: float,
    cash_and_equivalents: float,
) -> float:
    _validate_positive(market_cap, "market_cap")
    return market_cap + total_debt - cash_and_equivalents


def normalize_fundamentals_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(snapshot)
    if "operating_income" not in normalized and "ebit" in normalized:
        normalized["operating_income"] = normalized["ebit"]
    if "shareholders_equity" not in normalized and "equity" in normalized:
        normalized["shareholders_equity"] = normalized["equity"]
    if "total_debt" not in normalized and "debt" in normalized:
        normalized["total_debt"] = normalized["debt"]
    if "total_assets" not in normalized and "assets" in normalized:
        normalized["total_assets"] = normalized["assets"]
    if "total_liabilities" not in normalized and "liabilities" in normalized:
        normalized["total_liabilities"] = normalized["liabilities"]
    if normalized.get("free_cash_flow") is None:
        normalized["free_cash_flow"] = calculate_free_cash_flow(
            normalized.get("operating_cash_flow"),
            normalized.get("capital_expenditures"),
        )
    return normalized


def _calculate_growth(
    current_value: float | None,
    prior_value: float | None,
) -> float | None:
    if current_value is None or prior_value in (None, 0):
        return None
    return (current_value / prior_value) - 1.0


def _validate_positive(value: float, field_name: str) -> None:
    if value <= 0:
        raise ValueError(f"{field_name} must be positive.")
