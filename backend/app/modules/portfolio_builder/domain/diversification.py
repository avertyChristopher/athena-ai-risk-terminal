from collections.abc import Mapping, Sequence
from typing import Any


def calculate_largest_position_weight(weights: Sequence[float]) -> float:
    return max(weights, default=0.0)


def calculate_top_n_holdings_weight(weights: Sequence[float], n: int) -> float:
    if n <= 0:
        raise ValueError("Top holdings count must be positive.")

    return sum(sorted(weights, reverse=True)[:n])


def calculate_hhi_concentration(weights: Sequence[float]) -> float:
    return sum(weight * weight for weight in weights)


def calculate_effective_number_of_holdings(weights: Sequence[float]) -> float:
    hhi = calculate_hhi_concentration(weights)
    if hhi == 0:
        return 0.0

    return 1 / hhi


def calculate_diversification_score(weights: Sequence[float]) -> float:
    return max(0.0, 1.0 - calculate_hhi_concentration(weights))


def classify_concentration_level(largest_weight: float, top_5_weight: float) -> str:
    if largest_weight >= 0.35 or top_5_weight >= 0.85:
        return "High concentration"
    if largest_weight >= 0.20 or top_5_weight >= 0.65:
        return "Moderate concentration"
    return "Diversified"


def identify_concentration_warnings(
    positions: Sequence[Mapping[str, Any]],
    *,
    max_single_position_weight: float = 0.25,
    max_sector_weight: float = 0.50,
) -> list[str]:
    warnings: list[str] = []
    for position in positions:
        weight = float(position.get("invested_weight", position.get("weight", 0.0)))
        if weight > max_single_position_weight:
            warnings.append(
                f"{position.get('symbol', 'Position')} exceeds the single-position limit."
            )

    sector_weights: dict[str, float] = {}
    for position in positions:
        sector = str(position.get("sector") or "Unknown")
        sector_weights[sector] = sector_weights.get(sector, 0.0) + float(
            position.get("invested_weight", position.get("weight", 0.0))
        )

    for sector, weight in sector_weights.items():
        if weight > max_sector_weight:
            warnings.append(f"{sector} exceeds the sector concentration limit.")

    return warnings
