from collections import defaultdict
from collections.abc import Mapping, Sequence
from typing import Any


def calculate_allocation_by_asset(
    positions: Sequence[Mapping[str, Any]],
) -> list[dict[str, float | str]]:
    return _calculate_allocation(positions, "symbol")


def calculate_allocation_by_sector(
    positions: Sequence[Mapping[str, Any]],
) -> list[dict[str, float | str]]:
    return _calculate_allocation(positions, "sector")


def calculate_allocation_by_currency(
    positions: Sequence[Mapping[str, Any]],
) -> list[dict[str, float | str]]:
    return _calculate_allocation(positions, "currency")


def calculate_allocation_by_country(
    positions: Sequence[Mapping[str, Any]],
) -> list[dict[str, float | str]]:
    return _calculate_allocation(positions, "country")


def calculate_allocation_by_region(
    positions: Sequence[Mapping[str, Any]],
) -> list[dict[str, float | str]]:
    return _calculate_allocation(positions, "region")


def calculate_allocation_by_asset_type(
    positions: Sequence[Mapping[str, Any]],
) -> list[dict[str, float | str]]:
    return _calculate_allocation(positions, "asset_type")


def calculate_cash_allocation(
    positions: Sequence[Mapping[str, Any]],
    cash: float,
) -> list[dict[str, float | str]]:
    if cash < 0:
        raise ValueError("Cash cannot be negative.")

    invested_value = sum(_market_value(position) for position in positions)
    total_value = invested_value + cash
    if total_value <= 0:
        return []

    return [
        {
            "name": "Invested positions",
            "market_value": invested_value,
            "weight": invested_value / total_value,
        },
        {
            "name": "Cash",
            "market_value": cash,
            "weight": cash / total_value,
        },
    ]


def calculate_invested_allocation(
    positions: Sequence[Mapping[str, Any]],
) -> list[dict[str, float | str]]:
    return calculate_allocation_by_asset(positions)


def calculate_top_holdings(
    positions: Sequence[Mapping[str, Any]],
    limit: int = 10,
) -> list[dict[str, float | str]]:
    if limit <= 0:
        raise ValueError("Top holdings limit must be positive.")

    total_value = sum(_market_value(position) for position in positions)
    if total_value <= 0:
        return []

    holdings = [
        {
            "name": str(position.get("symbol", "Unknown")),
            "market_value": _market_value(position),
            "weight": _market_value(position) / total_value,
        }
        for position in positions
    ]

    return sorted(holdings, key=lambda item: float(item["market_value"]), reverse=True)[
        :limit
    ]


def calculate_concentration_metrics(
    positions: Sequence[Mapping[str, Any]],
) -> dict[str, float | int]:
    holdings = calculate_top_holdings(positions, limit=max(len(positions), 1))
    weights = [float(holding["weight"]) for holding in holdings]

    largest_position_weight = max(weights, default=0.0)
    top_5_holdings_weight = sum(weights[:5])
    diversification_score = max(0.0, 1.0 - sum(weight * weight for weight in weights))

    return {
        "largest_position_weight": largest_position_weight,
        "top_5_holdings_weight": top_5_holdings_weight,
        "number_of_positions": len(positions),
        "diversification_score": diversification_score,
    }


def _calculate_allocation(
    positions: Sequence[Mapping[str, Any]],
    key: str,
) -> list[dict[str, float | str]]:
    totals: dict[str, float] = defaultdict(float)

    for position in positions:
        totals[str(position.get(key) or "Unknown")] += _market_value(position)

    total_value = sum(totals.values())
    if total_value <= 0:
        return []

    return sorted(
        [
            {
                "name": name,
                "market_value": market_value,
                "weight": market_value / total_value,
            }
            for name, market_value in totals.items()
        ],
        key=lambda item: float(item["market_value"]),
        reverse=True,
    )


def _market_value(position: Mapping[str, Any]) -> float:
    if "market_value" in position:
        return float(position["market_value"])

    quantity = float(position.get("quantity", 0.0))
    current_price = float(position.get("current_price", 0.0))
    return quantity * current_price
