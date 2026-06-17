from app.modules.volatility_lab.domain.distribution import percentile


def classify_volatility_regime(
    latest_volatility: float | None,
    rolling_values: list[float],
) -> dict[str, object]:
    if latest_volatility is None or not rolling_values:
        return {
            "regime": "Requires Market Data",
            "latest_volatility": latest_volatility,
            "reference_percentile": None,
            "explanation": "Rolling volatility history is unavailable.",
        }

    p50 = percentile(rolling_values, 0.50)
    p75 = percentile(rolling_values, 0.75)
    p90 = percentile(rolling_values, 0.90)

    if latest_volatility >= p90:
        regime = "Extreme volatility"
    elif latest_volatility >= p75:
        regime = "Elevated volatility"
    elif latest_volatility >= p50:
        regime = "Normal volatility"
    else:
        regime = "Low volatility"

    return {
        "regime": regime,
        "latest_volatility": latest_volatility,
        "reference_percentile": _rank_percentile(latest_volatility, rolling_values),
        "explanation": (
            f"Latest rolling volatility is {latest_volatility:.1%}; "
            f"historical median is {p50:.1%} and 75th percentile is {p75:.1%}."
        ),
    }


def _rank_percentile(value: float, values: list[float]) -> float:
    if not values:
        return 0.0
    return len([item for item in values if item <= value]) / len(values)
