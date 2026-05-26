from typing import Any


def classify_valuation_status(
    margin_of_safety: float,
    pe_ratio: float,
    sector_pe_ratio: float | None = None,
) -> str:
    if margin_of_safety >= 0.15:
        return "Potentially undervalued"
    if margin_of_safety <= -0.15:
        return "Potentially expensive"
    if sector_pe_ratio and pe_ratio > sector_pe_ratio * 1.25:
        return "Premium multiple"
    return "Near fair value"


def classify_profitability_quality(
    net_margin: float,
    return_on_equity: float,
) -> str:
    if net_margin >= 0.20 and return_on_equity >= 0.25:
        return "High quality"
    if net_margin >= 0.10 and return_on_equity >= 0.12:
        return "Solid"
    return "Needs review"


def classify_balance_sheet_quality(
    debt_to_equity: float,
    current_ratio: float,
    interest_coverage: float,
) -> str:
    if debt_to_equity <= 1.0 and current_ratio >= 1.0 and interest_coverage >= 8.0:
        return "Conservative"
    if debt_to_equity <= 2.0 and current_ratio >= 0.8 and interest_coverage >= 4.0:
        return "Manageable"
    return "Levered"


def create_equity_diagnostics_summary(
    *,
    company_name: str,
    valuation_status: str,
    profitability_quality: str,
    balance_sheet_quality: str,
    strengths: list[str],
    risks: list[str],
    metrics: dict[str, Any],
) -> str:
    strength_text = "; ".join(strengths[:2]).lower()
    risk_text = "; ".join(risks[:2]).lower()
    margin = metrics.get("margin_of_safety")
    margin_text = ""
    if isinstance(margin, int | float):
        margin_text = f" with a margin of safety of {margin:.1%}"

    return (
        f"{company_name} screens as {valuation_status.lower()}{margin_text}. "
        f"Profitability is classified as {profitability_quality.lower()} and "
        f"balance sheet quality is {balance_sheet_quality.lower()}. "
        f"Key strengths include {strength_text}. Main risks to monitor include "
        f"{risk_text}. This output is educational analysis, not investment advice."
    )
