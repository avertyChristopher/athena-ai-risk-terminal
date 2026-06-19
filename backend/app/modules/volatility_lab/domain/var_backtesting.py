def var_backtest(
    returns: list[float],
    static_var: float,
    confidence_level: float = 0.95,
    minimum_observations: int = 30,
) -> dict[str, float | int | str]:
    observations = len(returns)
    expected_exception_rate = 1.0 - confidence_level
    if observations < minimum_observations:
        return {
            "observations": observations,
            "exceptions": 0,
            "exception_rate": 0.0,
            "expected_exception_rate": expected_exception_rate,
            "status": "insufficient_data",
            "note": "Insufficient observations for meaningful VaR backtesting.",
        }

    exceptions = len([value for value in returns if value < -abs(static_var)])
    exception_rate = exceptions / observations if observations else 0.0
    status = (
        "acceptable"
        if exception_rate <= expected_exception_rate * 1.5
        else "review"
    )
    return {
        "observations": observations,
        "exceptions": exceptions,
        "exception_rate": exception_rate,
        "expected_exception_rate": expected_exception_rate,
        "status": status,
        "note": (
            "Static VaR backtest compares realized one-period losses with the "
            "current VaR threshold."
        ),
    }
