from math import sqrt


def weighted_portfolio_returns(
    aligned_returns: dict[str, list[float]],
    weights: dict[str, float],
) -> list[float]:
    if not aligned_returns:
        return []
    length = min(len(series) for series in aligned_returns.values())
    return [
        sum(
            aligned_returns[symbol][index] * weights.get(symbol, 0.0)
            for symbol in aligned_returns
        )
        for index in range(length)
    ]


def portfolio_variance(weights: list[float], covariance_matrix: list[list[float]]) -> float:
    if not weights or not covariance_matrix:
        return 0.0
    return sum(
        weights[row] * weights[column] * covariance_matrix[row][column]
        for row in range(len(weights))
        for column in range(len(weights))
    )


def portfolio_volatility(
    weights: list[float],
    covariance_matrix: list[list[float]],
    periods_per_year: int = 252,
) -> float:
    return sqrt(max(portfolio_variance(weights, covariance_matrix), 0.0)) * sqrt(periods_per_year)


def risk_contribution(
    symbols: list[str],
    weights: list[float],
    covariance_matrix: list[list[float]],
) -> list[dict[str, float | str]]:
    variance_value = portfolio_variance(weights, covariance_matrix)
    if variance_value <= 0:
        return [
            {"symbol": symbol, "weight": weights[index], "contribution": 0.0}
            for index, symbol in enumerate(symbols)
        ]
    contributions = []
    for row, symbol in enumerate(symbols):
        marginal = sum(
            covariance_matrix[row][column] * weights[column]
            for column in range(len(weights))
        )
        contribution = weights[row] * marginal / variance_value
        contributions.append(
            {
                "symbol": symbol,
                "weight": weights[row],
                "contribution": contribution,
            },
        )
    return contributions


def diversification_benefit(
    weighted_average_volatility: float,
    portfolio_volatility_value: float,
) -> float:
    if weighted_average_volatility == 0:
        return 0.0
    return max(0.0, (weighted_average_volatility - portfolio_volatility_value) / weighted_average_volatility)
