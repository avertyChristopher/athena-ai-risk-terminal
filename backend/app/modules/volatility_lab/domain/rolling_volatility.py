from app.modules.volatility_lab.domain.volatility import annualized_volatility


def rolling_volatility(
    returns: list[float],
    dates: list[str],
    window: int = 20,
    periods_per_year: int = 252,
) -> list[dict[str, float | str]]:
    if window <= 1:
        return []
    return [
        {
            "date": dates[index],
            "volatility": annualized_volatility(
                returns[index - window + 1 : index + 1],
                periods_per_year,
            ),
        }
        for index in range(window - 1, len(returns))
    ]


def rolling_summary(points: list[dict[str, float | str]]) -> dict[str, float | None]:
    values = [float(point["volatility"]) for point in points]
    if not values:
        return {"latest": None, "minimum": None, "maximum": None, "average": None}
    return {
        "latest": values[-1],
        "minimum": min(values),
        "maximum": max(values),
        "average": sum(values) / len(values),
    }
