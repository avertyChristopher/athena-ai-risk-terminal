def create_efficient_frontier_demo_points(
    expected_return: float,
    standard_deviation: float | None,
) -> list[dict[str, float | str]]:
    base_risk = standard_deviation or 0.12
    return [
        {"label": "Defensive mix", "expected_return": max(0.0, expected_return - 0.02), "risk": base_risk * 0.70},
        {"label": "Current portfolio", "expected_return": expected_return, "risk": base_risk},
        {"label": "Growth mix", "expected_return": expected_return + 0.02, "risk": base_risk * 1.30},
    ]
