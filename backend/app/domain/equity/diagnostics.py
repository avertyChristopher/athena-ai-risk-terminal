from typing import Any


def classify_valuation_status(
    margin_of_safety: float,
    pe_ratio: float,
    sector_pe_ratio: float | None = None,
) -> str:
    if margin_of_safety >= 0.15:
        return "Model-implied discount"
    if margin_of_safety <= -0.15:
        return "Model-implied premium"
    if sector_pe_ratio and pe_ratio > sector_pe_ratio * 1.25:
        return "Premium multiple"
    return "Near model fair value"


def classify_valuation_profile(
    margin_of_safety: float | None,
    multiple_level: str,
) -> str:
    if margin_of_safety is None:
        return "Insufficient data"
    if margin_of_safety >= 0.15 and multiple_level != "Premium":
        return "Dividend-model discount signal"
    if margin_of_safety <= -0.15 or multiple_level == "Premium":
        return "Valuation sensitivity elevated"
    return "Balanced model signal"


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


def classify_growth_profile(
    revenue_growth: float | None,
    eps_growth: float | None,
    sustainable_growth_rate: float | None,
) -> str:
    growth_values = [
        value
        for value in (revenue_growth, eps_growth, sustainable_growth_rate)
        if value is not None
    ]
    if not growth_values:
        return "Insufficient data"

    average_growth = sum(growth_values) / len(growth_values)
    if average_growth >= 0.15:
        return "High growth"
    if average_growth >= 0.06:
        return "Moderate growth"
    if average_growth >= 0:
        return "Low growth"
    return "Contracting"


def classify_dividend_profile(
    dividend_yield: float | None,
    payout_ratio: float | None,
) -> str:
    if dividend_yield is None or dividend_yield == 0:
        return "Non-dividend or minimal dividend"
    if payout_ratio is not None and payout_ratio > 0.75:
        return "High payout"
    if dividend_yield >= 0.02:
        return "Income-oriented"
    return "Modest dividend"


def classify_equity_risk_profile(
    beta: float | None,
    debt_to_equity: float | None,
    valuation_profile: str,
) -> str:
    if beta is None:
        return "Insufficient data"
    if beta >= 1.4 or (debt_to_equity is not None and debt_to_equity >= 2.0):
        return "Elevated equity risk"
    if beta <= 0.9 and "elevated" not in valuation_profile.lower():
        return "Moderate equity risk"
    return "Market-like equity risk"


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
        f"{company_name} has a {valuation_status.lower()} under demo assumptions"
        f"{margin_text}. "
        f"Profitability is classified as {profitability_quality.lower()} and "
        f"balance sheet quality is {balance_sheet_quality.lower()}. "
        f"Key strengths include {strength_text}. Main risks to monitor include "
        f"{risk_text}. Dividend-based valuation is a simplified model signal, "
        f"not a complete fair-value estimate or investment advice."
    )


def create_bull_base_bear_case_summary(
    *,
    strengths: list[str],
    risks: list[str],
    growth_profile: str,
    valuation_profile: str,
) -> dict[str, str]:
    bull_strength = strengths[0] if strengths else "Business quality improves."
    bear_risk = risks[0] if risks else "Execution risk rises."
    return {
        "bull_case": f"{bull_strength} Growth profile remains {growth_profile.lower()}.",
        "base_case": (
            f"Business fundamentals remain stable while valuation is classified as "
            f"{valuation_profile.lower()}."
        ),
        "bear_case": f"{bear_risk} Multiple compression or slower growth pressures returns.",
    }


def create_watchlist_flags(
    *,
    valuation_profile: str,
    balance_sheet_quality: str,
    growth_profile: str,
    risk_profile: str,
) -> list[str]:
    flags = []
    if "sensitivity elevated" in valuation_profile.lower():
        flags.append("Monitor valuation multiple compression")
    if balance_sheet_quality == "Levered":
        flags.append("Monitor leverage and refinancing risk")
    if growth_profile in {"Low growth", "Contracting"}:
        flags.append("Monitor revenue and EPS growth trajectory")
    if risk_profile == "Elevated equity risk":
        flags.append("Monitor beta, drawdowns and business volatility")
    return flags or ["No major demo watchlist flag triggered"]
