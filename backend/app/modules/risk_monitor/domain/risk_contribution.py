from typing import Any


def calculate_risk_contribution(
    *,
    decorated_positions: list[dict[str, Any]],
    covariance_matrix: list[list[float]],
    covariance_symbols: list[str],
) -> dict[str, object]:
    if covariance_matrix and covariance_symbols:
        realized = _realized_contribution(
            decorated_positions,
            covariance_matrix,
            covariance_symbols,
        )
        if realized is not None:
            return realized

    return _proxy_contribution(decorated_positions)


def _realized_contribution(
    decorated_positions: list[dict[str, Any]],
    covariance_matrix: list[list[float]],
    covariance_symbols: list[str],
) -> dict[str, object] | None:
    weights_by_symbol = {
        str(position["symbol"]).upper(): float(position["invested_weight"])
        for position in decorated_positions
    }
    weights = [weights_by_symbol.get(symbol.upper(), 0.0) for symbol in covariance_symbols]
    if not any(weights):
        return None

    variance = 0.0
    marginal = []
    for row_index, row in enumerate(covariance_matrix):
        marginal_value = sum(
            float(row[column_index]) * weights[column_index]
            for column_index in range(len(weights))
        )
        marginal.append(marginal_value)
        variance += weights[row_index] * marginal_value
    if variance <= 0:
        return None

    contribution_by_symbol = {
        symbol.upper(): max(0.0, weights[index] * marginal[index] / variance)
        for index, symbol in enumerate(covariance_symbols)
    }
    return _format_contribution(
        decorated_positions,
        contribution_by_symbol,
        "realized_market_data",
        "Approximate volatility contribution from realized annualized covariance.",
    )


def _proxy_contribution(decorated_positions: list[dict[str, Any]]) -> dict[str, object]:
    raw = {
        str(position["symbol"]).upper(): float(position["invested_weight"])
        * _asset_volatility(str(position["symbol"]), str(position["asset_type"]))
        for position in decorated_positions
    }
    total = sum(raw.values())
    contribution_by_symbol = {
        symbol: value / total if total else 0.0 for symbol, value in raw.items()
    }
    return _format_contribution(
        decorated_positions,
        contribution_by_symbol,
        "deterministic_demo",
        "Weight times demo asset volatility proxy; covariance unavailable.",
    )


def _format_contribution(
    decorated_positions: list[dict[str, Any]],
    contribution_by_symbol: dict[str, float],
    source: str,
    method: str,
) -> dict[str, object]:
    by_asset = []
    sector_contributions: dict[str, dict[str, float]] = {}
    for position in decorated_positions:
        symbol = str(position["symbol"]).upper()
        contribution = contribution_by_symbol.get(symbol, 0.0)
        by_asset.append(
            {
                "name": symbol,
                "weight": float(position["invested_weight"]),
                "contribution": contribution,
                "contribution_percent": contribution,
                "source": source,
            },
        )
        sector = str(position.get("sector") or "Unknown")
        sector_row = sector_contributions.setdefault(
            sector,
            {"weight": 0.0, "contribution": 0.0},
        )
        sector_row["weight"] += float(position["portfolio_weight"])
        sector_row["contribution"] += contribution

    by_asset = sorted(by_asset, key=lambda item: item["contribution"], reverse=True)
    by_sector = [
        {
            "name": sector,
            "weight": values["weight"],
            "contribution": values["contribution"],
            "contribution_percent": values["contribution"],
            "source": source,
        }
        for sector, values in sorted(
            sector_contributions.items(),
            key=lambda item: item[1]["contribution"],
            reverse=True,
        )
    ]
    largest = str(by_asset[0]["name"]) if by_asset else None
    warning = (
        f"{largest} is the largest risk contributor."
        if largest is not None and float(by_asset[0]["contribution"]) > 0.30
        else None
    )
    return {
        "contribution_source": source,
        "method": method,
        "by_asset": by_asset,
        "by_sector": by_sector,
        "largest_risk_contributor": largest,
        "diversification_warning": warning,
    }


def _asset_volatility(symbol: str, asset_type: str) -> float:
    known_volatilities = {
        "AAPL": 0.24,
        "MSFT": 0.22,
        "NVDA": 0.42,
        "SPY": 0.16,
        "QQQ": 0.22,
        "BND": 0.06,
    }
    asset_volatilities = {
        "equity": 0.22,
        "etf": 0.16,
        "fixed_income": 0.06,
        "bond": 0.06,
        "cash": 0.01,
    }
    return known_volatilities.get(
        symbol.upper(),
        asset_volatilities.get(asset_type.lower(), 0.15),
    )
