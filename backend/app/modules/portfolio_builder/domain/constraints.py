from collections.abc import Mapping, Sequence


def check_single_position_limit(
    positions: Sequence[Mapping[str, object]],
    max_weight: float,
) -> list[dict[str, float | str]]:
    return [
        {
            "constraint": "max_single_position_weight",
            "name": str(position.get("symbol", "Unknown")),
            "actual": float(position.get("invested_weight", 0.0)),
            "limit": max_weight,
            "severity": "warning",
        }
        for position in positions
        if float(position.get("invested_weight", 0.0)) > max_weight
    ]


def check_group_limit(
    allocation: Sequence[Mapping[str, object]],
    max_weight: float,
    constraint_name: str,
) -> list[dict[str, float | str]]:
    return [
        {
            "constraint": constraint_name,
            "name": str(item.get("name", "Unknown")),
            "actual": float(item.get("weight", 0.0)),
            "limit": max_weight,
            "severity": "warning",
        }
        for item in allocation
        if float(item.get("weight", 0.0)) > max_weight
    ]


def check_sector_limit(allocation: Sequence[Mapping[str, object]], max_weight: float) -> list[dict[str, float | str]]:
    return check_group_limit(allocation, max_weight, "max_sector_weight")


def check_asset_type_limit(allocation: Sequence[Mapping[str, object]], max_weight: float) -> list[dict[str, float | str]]:
    return check_group_limit(allocation, max_weight, "max_asset_type_weight")


def check_currency_limit(allocation: Sequence[Mapping[str, object]], max_weight: float) -> list[dict[str, float | str]]:
    return check_group_limit(allocation, max_weight, "max_currency_weight")


def check_min_cash_limit(cash_weight: float, minimum_cash_weight: float) -> list[dict[str, float | str]]:
    if cash_weight >= minimum_cash_weight:
        return []

    return [
        {
            "constraint": "minimum_cash_weight",
            "name": "Cash",
            "actual": cash_weight,
            "limit": minimum_cash_weight,
            "severity": "warning",
        }
    ]


def check_allowed_asset_types(
    positions: Sequence[Mapping[str, object]],
    allowed_asset_types: Sequence[str],
) -> list[dict[str, float | str]]:
    allowed = {asset_type.lower() for asset_type in allowed_asset_types}
    breaches: list[dict[str, float | str]] = []
    for position in positions:
        asset_type = str(position.get("asset_type", "")).lower()
        if asset_type not in allowed:
            breaches.append(
                {
                    "constraint": "allowed_asset_types",
                    "name": str(position.get("symbol", "Unknown")),
                    "actual": 1.0,
                    "limit": 0.0,
                    "severity": "warning",
                }
            )
    return breaches


def summarize_constraint_breaches(
    *breach_groups: Sequence[Mapping[str, object]],
) -> list[dict[str, object]]:
    return [dict(breach) for group in breach_groups for breach in group]
