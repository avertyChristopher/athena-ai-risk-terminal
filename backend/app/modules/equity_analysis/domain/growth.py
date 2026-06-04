from app.modules.equity_analysis.domain.fundamentals import (
    calculate_eps_growth,
    calculate_operating_income_growth,
    calculate_revenue_growth,
)
from app.modules.equity_analysis.domain.ratios import (
    calculate_retention_ratio,
    calculate_sustainable_growth_rate,
)


def classify_growth_profile(
    revenue_growth: float | None,
    eps_growth: float | None,
    sustainable_growth_rate: float | None,
) -> str:
    available_growth = [
        value
        for value in (revenue_growth, eps_growth, sustainable_growth_rate)
        if value is not None
    ]
    if not available_growth:
        return "Insufficient data"

    average_growth = sum(available_growth) / len(available_growth)
    if average_growth >= 0.15:
        return "High growth"
    if average_growth >= 0.06:
        return "Moderate growth"
    if average_growth >= 0:
        return "Low growth"
    return "Contracting"


__all__ = [
    "calculate_eps_growth",
    "calculate_operating_income_growth",
    "calculate_retention_ratio",
    "calculate_revenue_growth",
    "calculate_sustainable_growth_rate",
    "classify_growth_profile",
]
