from __future__ import annotations

from collections import defaultdict
from typing import Any

from app.modules.pnl_attribution.schemas import GroupPnlContribution, PositionPnlContribution


def aggregate_group_contributions(
    positions: list[PositionPnlContribution],
    group_field: str,
    portfolio_starting_value: float,
    portfolio_ending_value: float,
    total_pnl: float,
) -> list[GroupPnlContribution]:
    grouped: dict[str, dict[str, float]] = defaultdict(
        lambda: {"starting_value": 0.0, "ending_value": 0.0, "total_pnl": 0.0},
    )
    for position in positions:
        key = str(getattr(position, group_field) or "Unclassified")
        grouped[key]["starting_value"] += position.starting_value
        grouped[key]["ending_value"] += position.ending_value
        grouped[key]["total_pnl"] += position.total_pnl

    rows = [
        GroupPnlContribution(
            name=name,
            starting_value=values["starting_value"],
            ending_value=values["ending_value"],
            total_pnl=values["total_pnl"],
            pnl_percent=_safe_div(values["total_pnl"], values["starting_value"]),
            contribution_to_total_pnl=_safe_div(values["total_pnl"], total_pnl),
            contribution_to_portfolio_return=_safe_div(values["total_pnl"], portfolio_starting_value),
            weight_start=_safe_div(values["starting_value"], portfolio_starting_value),
            weight_end=_safe_div(values["ending_value"], portfolio_ending_value),
        )
        for name, values in grouped.items()
    ]
    return sorted(rows, key=lambda row: abs(row.total_pnl), reverse=True)


def top_winners_losers(
    positions: list[PositionPnlContribution],
    limit: int = 5,
) -> tuple[list[PositionPnlContribution], list[PositionPnlContribution]]:
    winners = sorted(positions, key=lambda item: item.total_pnl, reverse=True)[:limit]
    losers = sorted(positions, key=lambda item: item.total_pnl)[:limit]
    return winners, losers


def rows_to_table(rows: list[Any]) -> list[dict[str, Any]]:
    return [row.model_dump(mode="json") if hasattr(row, "model_dump") else dict(row) for row in rows]


def _safe_div(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator
