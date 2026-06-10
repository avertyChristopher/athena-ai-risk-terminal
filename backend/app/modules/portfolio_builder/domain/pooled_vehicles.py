from collections.abc import Mapping, Sequence


def calculate_etf_exposure(positions: Sequence[Mapping[str, object]]) -> float:
    return sum(
        float(position.get("portfolio_weight", 0.0))
        for position in positions
        if str(position.get("asset_type", "")).lower() == "etf"
    )


def calculate_single_stock_exposure(positions: Sequence[Mapping[str, object]]) -> float:
    return sum(
        float(position.get("portfolio_weight", 0.0))
        for position in positions
        if str(position.get("asset_type", "")).lower() == "equity"
    )


def calculate_pooled_vehicle_exposure(positions: Sequence[Mapping[str, object]]) -> float:
    pooled_types = {"etf", "mutual_fund", "fund"}
    return sum(
        float(position.get("portfolio_weight", 0.0))
        for position in positions
        if str(position.get("asset_type", "")).lower() in pooled_types
    )


def classify_pooled_vehicle_usage(pooled_vehicle_exposure: float) -> str:
    if pooled_vehicle_exposure >= 0.50:
        return "Core pooled-vehicle allocation"
    if pooled_vehicle_exposure >= 0.15:
        return "Satellite pooled-vehicle allocation"
    return "Single-security oriented allocation"
