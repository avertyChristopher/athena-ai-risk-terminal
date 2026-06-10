from collections.abc import Mapping
from typing import Any


def calculate_allocation_drift(current_weight: float, target_weight: float) -> float:
    return current_weight - target_weight


def classify_overweight_underweight(
    current_weight: float,
    target_weight: float,
    tolerance_band: float,
) -> str:
    drift = calculate_allocation_drift(current_weight, target_weight)
    if drift > tolerance_band:
        return "Overweight"
    if drift < -tolerance_band:
        return "Underweight"
    return "Within tolerance"


def detect_tolerance_band_breaches(
    allocations: Mapping[str, float],
    targets: Mapping[str, float],
    tolerance_bands: Mapping[str, float],
) -> list[dict[str, float | str]]:
    breaches: list[dict[str, float | str]] = []
    for name, target_weight in targets.items():
        current_weight = allocations.get(name, 0.0)
        tolerance = tolerance_bands.get(name, 0.0)
        drift = calculate_allocation_drift(current_weight, target_weight)
        status = classify_overweight_underweight(current_weight, target_weight, tolerance)
        if status != "Within tolerance":
            breaches.append(
                {
                    "name": name,
                    "current_weight": current_weight,
                    "target_weight": target_weight,
                    "drift": drift,
                    "tolerance_band": tolerance,
                    "status": status,
                }
            )

    return breaches


def calculate_target_market_values(
    total_market_value: float,
    target_weights: Mapping[str, float],
) -> dict[str, float]:
    if total_market_value < 0:
        raise ValueError("Total market value cannot be negative.")

    return {name: total_market_value * weight for name, weight in target_weights.items()}


def calculate_rebalance_value_differences(
    current_market_values: Mapping[str, float],
    target_market_values: Mapping[str, float],
) -> dict[str, float]:
    return {
        name: target_value - current_market_values.get(name, 0.0)
        for name, target_value in target_market_values.items()
    }


def calculate_rebalance_quantity_differences(
    value_differences: Mapping[str, float],
    current_prices: Mapping[str, float],
) -> dict[str, float]:
    differences: dict[str, float] = {}
    for name, value_difference in value_differences.items():
        price = current_prices.get(name, 0.0)
        differences[name] = value_difference / price if price > 0 else 0.0
    return differences


def create_rebalance_preview(
    positions: list[Mapping[str, Any]],
    total_market_value: float,
    target_weights: Mapping[str, float],
) -> list[dict[str, float | str]]:
    current_values = {
        str(position["symbol"]): float(position.get("market_value", 0.0))
        for position in positions
    }
    prices = {
        str(position["symbol"]): float(position.get("current_price", 0.0))
        for position in positions
    }
    target_values = calculate_target_market_values(total_market_value, target_weights)
    value_differences = calculate_rebalance_value_differences(current_values, target_values)
    quantity_differences = calculate_rebalance_quantity_differences(value_differences, prices)

    rows: list[dict[str, float | str]] = []
    for name, target_value in target_values.items():
        value_difference = value_differences[name]
        action = "hold"
        if value_difference > 0:
            action = "buy"
        elif value_difference < 0:
            action = "sell"
        rows.append(
            {
                "name": name,
                "current_market_value": current_values.get(name, 0.0),
                "target_market_value": target_value,
                "value_difference": value_difference,
                "estimated_quantity_difference": quantity_differences[name],
                "action": action,
            }
        )

    return rows


def estimate_turnover(value_differences: Mapping[str, float], total_market_value: float) -> float:
    if total_market_value <= 0:
        return 0.0

    return sum(abs(value) for value in value_differences.values()) / (2 * total_market_value)
