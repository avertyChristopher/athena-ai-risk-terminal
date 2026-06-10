from collections.abc import Sequence


def calculate_portfolio_market_value(
    position_market_values: Sequence[float],
    cash: float = 0.0,
) -> float:
    if cash < 0:
        raise ValueError("Cash cannot be negative.")

    if any(market_value < 0 for market_value in position_market_values):
        raise ValueError("Position market values cannot be negative.")

    return sum(position_market_values) + cash


def calculate_invested_value(position_market_values: Sequence[float]) -> float:
    if any(market_value < 0 for market_value in position_market_values):
        raise ValueError("Position market values cannot be negative.")

    return sum(position_market_values)


def calculate_portfolio_weights(
    position_market_values: Sequence[float],
    cash: float = 0.0,
) -> list[float]:
    total_value = calculate_portfolio_market_value(position_market_values, cash)
    if total_value == 0:
        return [0.0 for _ in position_market_values]

    return [market_value / total_value for market_value in position_market_values]


def calculate_cash_weight(
    position_market_values: Sequence[float],
    cash: float = 0.0,
) -> float:
    total_value = calculate_portfolio_market_value(position_market_values, cash)
    if total_value == 0:
        return 0.0

    return cash / total_value


def calculate_portfolio_return(
    position_returns: Sequence[float],
    position_weights: Sequence[float],
) -> float:
    if len(position_returns) != len(position_weights):
        raise ValueError("Returns and weights must have the same length.")

    return sum(
        position_return * position_weight
        for position_return, position_weight in zip(position_returns, position_weights)
    )
