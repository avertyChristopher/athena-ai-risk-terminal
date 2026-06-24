from __future__ import annotations

from collections import defaultdict


def rank_worst_contributors(
    position_impacts: list[dict[str, object]],
    limit: int = 5,
) -> list[dict[str, object]]:
    losses = [
        {
            "name": str(impact["symbol"]),
            "label": str(impact["name"]),
            "dollar_loss": max(-float(impact["dollar_impact"]), 0.0),
            "percent_impact": float(impact["percent_impact"]),
            "contribution_to_loss": float(impact["contribution_to_loss"]),
        }
        for impact in position_impacts
    ]
    return sorted(losses, key=lambda item: item["dollar_loss"], reverse=True)[:limit]


def aggregate_impacts(
    position_impacts: list[dict[str, object]],
    group_key: str,
) -> list[dict[str, object]]:
    groups: dict[str, dict[str, float]] = defaultdict(
        lambda: {"base_value": 0.0, "stressed_value": 0.0, "dollar_impact": 0.0}
    )
    for impact in position_impacts:
        name = str(impact.get(group_key) or "Unknown")
        groups[name]["base_value"] += float(impact["base_value"])
        groups[name]["stressed_value"] += float(impact["stressed_value"])
        groups[name]["dollar_impact"] += float(impact["dollar_impact"])

    rows = []
    for name, values in groups.items():
        base_value = values["base_value"]
        rows.append(
            {
                "name": name,
                "base_value": base_value,
                "stressed_value": values["stressed_value"],
                "dollar_impact": values["dollar_impact"],
                "percent_impact": values["dollar_impact"] / base_value if base_value else 0.0,
                "loss_contribution": 0.0,
            }
        )

    total_loss = sum(max(-row["dollar_impact"], 0.0) for row in rows)
    for row in rows:
        row["loss_contribution"] = max(-row["dollar_impact"], 0.0) / total_loss if total_loss > 0 else 0.0

    return sorted(rows, key=lambda item: item["dollar_impact"])
