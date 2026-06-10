from collections.abc import Mapping, Sequence


def calculate_market_risk_premium(
    expected_market_return: float,
    risk_free_rate: float,
) -> float:
    return expected_market_return - risk_free_rate


def calculate_capm_required_return(
    risk_free_rate: float,
    beta: float,
    market_risk_premium: float,
) -> float:
    return risk_free_rate + beta * market_risk_premium


def calculate_weighted_portfolio_beta(
    positions: Sequence[Mapping[str, object]],
    beta_by_symbol: Mapping[str, float],
) -> float:
    return sum(
        float(position.get("invested_weight", 0.0))
        * beta_by_symbol.get(str(position.get("symbol", "")).upper(), 1.0)
        for position in positions
    )


def compare_expected_return_to_required_return(
    expected_return: float,
    required_return: float,
) -> str:
    spread = expected_return - required_return
    if spread > 0.005:
        return "Expected return is above CAPM required return."
    if spread < -0.005:
        return "Expected return is below CAPM required return."
    return "Expected return is broadly in line with CAPM required return."
