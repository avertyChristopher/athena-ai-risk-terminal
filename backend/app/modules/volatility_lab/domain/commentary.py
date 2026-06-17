def build_asset_commentary(
    symbol: str,
    regime: str,
    beta: float,
    correlation: float,
    annualized_volatility: float,
    max_drawdown: float,
) -> list[str]:
    beta_note = (
        "above 1, indicating above-market systematic risk"
        if beta > 1
        else "below 1, indicating below-market systematic risk"
    )
    correlation_note = (
        "highly correlated with the benchmark"
        if correlation >= 0.75
        else "not tightly correlated with the benchmark"
    )
    return [
        (
            f"{symbol} is in a {regime.lower()} regime with annualized "
            f"volatility of {annualized_volatility:.1%}."
        ),
        f"Beta is {beta:.2f}, {beta_note}.",
        f"Correlation is {correlation:.2f}; the asset is {correlation_note}.",
        f"Maximum drawdown in the analyzed sample is {max_drawdown:.1%}.",
    ]


def build_portfolio_commentary(
    portfolio_name: str,
    annualized_volatility: float,
    diversification_benefit: float,
    largest_risk_contributor: str | None,
    tracking_error: float | None,
) -> list[str]:
    return [
        (
            f"{portfolio_name} has realized annualized volatility of "
            f"{annualized_volatility:.1%}."
        ),
        (
            f"Diversification benefit is estimated at {diversification_benefit:.1%}, "
            "showing how correlations reduce weighted average standalone risk."
        ),
        (
            f"{largest_risk_contributor} is the largest risk contributor."
            if largest_risk_contributor
            else "No single largest risk contributor is available."
        ),
        (
            f"Tracking error versus benchmark is {tracking_error:.1%}."
            if tracking_error is not None
            else "Tracking error requires aligned benchmark return history."
        ),
    ]
