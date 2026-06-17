from math import sqrt


def ewma_volatility(
    returns: list[float],
    lambda_decay: float = 0.94,
    annualization_factor: int = 252,
) -> dict[str, float | int | str | None]:
    if not returns:
        return {
            "latest_volatility": None,
            "lambda_decay": lambda_decay,
            "annualization_factor": annualization_factor,
            "observations": 0,
            "metric_source": "requires_market_data",
            "badge": "Requires Market Data",
            "explanation": (
                "EWMA volatility requires return observations and gives more "
                "weight to recent returns."
            ),
        }

    ewma_variance = returns[0] ** 2
    for value in returns[1:]:
        ewma_variance = lambda_decay * ewma_variance + (1.0 - lambda_decay) * value**2

    return {
        "latest_volatility": sqrt(max(ewma_variance, 0.0)) * sqrt(annualization_factor),
        "lambda_decay": lambda_decay,
        "annualization_factor": annualization_factor,
        "observations": len(returns),
        "metric_source": "realized_market_data",
        "badge": "Realized",
        "explanation": (
            "EWMA gives more weight to recent returns, making it more responsive "
            "to changing volatility regimes."
        ),
    }
