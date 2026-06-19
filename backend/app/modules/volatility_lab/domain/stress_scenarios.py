def build_volatility_stress_scenarios(
    *,
    base_volatility: float,
    historical_var: float,
    historical_cvar: float,
    mode: str,
    largest_holding: str | None = None,
) -> list[dict[str, float | str]]:
    scenarios = [
        _scenario(
            "Volatility +25%",
            base_volatility,
            historical_var,
            historical_cvar,
            1.25,
            "Deterministic volatility shock.",
        ),
        _scenario(
            "Volatility +50%",
            base_volatility,
            historical_var,
            historical_cvar,
            1.50,
            "Deterministic volatility shock.",
        ),
        _scenario(
            "Volatility +100%",
            base_volatility,
            historical_var,
            historical_cvar,
            2.00,
            "Deterministic volatility shock.",
        ),
    ]

    if mode == "portfolio":
        scenarios.extend(
            [
                _scenario(
                    "Correlation shock",
                    base_volatility,
                    historical_var,
                    historical_cvar,
                    1.15,
                    "Correlations are assumed to move toward 1 during stress.",
                ),
                _scenario(
                    "Benchmark drawdown shock",
                    base_volatility,
                    historical_var,
                    historical_cvar,
                    1.20,
                    "Benchmark drawdown shock is proxied through higher realized risk.",
                ),
                _scenario(
                    "Largest holding volatility shock",
                    base_volatility,
                    historical_var,
                    historical_cvar,
                    1.10,
                    f"{largest_holding or 'Largest holding'} volatility shock.",
                ),
            ],
        )

    return scenarios


def _scenario(
    name: str,
    base_volatility: float,
    historical_var: float,
    historical_cvar: float,
    multiplier: float,
    note: str,
) -> dict[str, float | str]:
    stressed_volatility = base_volatility * multiplier
    return {
        "name": name,
        "volatility_multiplier": multiplier,
        "stressed_volatility": stressed_volatility,
        "stressed_var": historical_var * multiplier,
        "stressed_cvar": historical_cvar * multiplier,
        "risk_status": _risk_status(stressed_volatility),
        "note": note,
    }


def _risk_status(volatility: float) -> str:
    if volatility >= 0.35:
        return "critical"
    if volatility >= 0.25:
        return "high"
    if volatility >= 0.18:
        return "elevated"
    return "watch"
