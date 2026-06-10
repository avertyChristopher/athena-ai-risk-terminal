from collections.abc import Sequence


def calculate_utility_score(
    expected_return: float,
    variance: float,
    risk_aversion_coefficient: float,
) -> float:
    return expected_return - 0.5 * risk_aversion_coefficient * variance


def classify_risk_aversion(risk_aversion_coefficient: float) -> str:
    if risk_aversion_coefficient < 2:
        return "Low risk aversion"
    if risk_aversion_coefficient <= 5:
        return "Moderate risk aversion"
    return "High risk aversion"


def rank_portfolio_by_utility(
    portfolios: Sequence[dict[str, float | str]],
) -> list[dict[str, float | str]]:
    return sorted(
        portfolios,
        key=lambda portfolio: float(portfolio.get("utility_score", 0.0)),
        reverse=True,
    )
