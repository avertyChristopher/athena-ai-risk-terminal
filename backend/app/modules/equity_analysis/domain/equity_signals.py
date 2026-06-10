def create_equity_signal(
    valuation_profile: str,
    earnings_quality: str,
    capm_signal: str,
    data_quality_score: float,
) -> str:
    if data_quality_score < 0.70:
        return "Data quality review required"
    if "discount" in valuation_profile.lower() and "high" in earnings_quality.lower():
        return "Constructive fundamental signal"
    if "below" in capm_signal.lower() or "premium" in valuation_profile.lower():
        return "Valuation risk signal"
    return "Balanced monitoring signal"


def create_portfolio_builder_bridge(
    quality_score: float,
    valuation_signal: str,
    risk_signal: str,
    expected_return: float | None,
) -> dict[str, float | str | None]:
    return {
        "quality_score": quality_score,
        "valuation_signal": valuation_signal,
        "risk_signal": risk_signal,
        "expected_return_placeholder": expected_return,
        "portfolio_use": "Candidate input for watchlist, sizing review or policy-constrained portfolio construction.",
    }
