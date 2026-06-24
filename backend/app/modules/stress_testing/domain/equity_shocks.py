from __future__ import annotations


def apply_symbol_shock(symbol: str, symbol_shocks: dict[str, float]) -> float:
    return float(symbol_shocks.get(symbol.upper(), 0.0))


def apply_sector_shock(sector: str | None, sector_shocks: dict[str, float]) -> float:
    if not sector:
        return 0.0
    normalized = sector.strip().lower()
    for sector_name, shock in sector_shocks.items():
        if sector_name.strip().lower() == normalized:
            return float(shock)
    return 0.0


def apply_asset_class_shock(
    asset_type: str | None,
    asset_class_shocks: dict[str, float],
) -> float:
    if not asset_type:
        return 0.0
    normalized = asset_type.strip().lower()
    return float(asset_class_shocks.get(normalized, 0.0))


def combined_equity_shock(
    symbol: str,
    sector: str | None,
    asset_type: str | None,
    symbol_shocks: dict[str, float],
    sector_shocks: dict[str, float],
    asset_class_shocks: dict[str, float],
) -> tuple[float, str]:
    shocks = [
        (apply_asset_class_shock(asset_type, asset_class_shocks), "asset class"),
        (apply_sector_shock(sector, sector_shocks), "sector"),
        (apply_symbol_shock(symbol, symbol_shocks), "symbol"),
    ]
    selected_shock, source = min(shocks, key=lambda item: item[0])
    return selected_shock, source
