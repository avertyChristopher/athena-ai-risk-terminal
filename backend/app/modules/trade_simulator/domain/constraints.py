from typing import Any


def build_constraint_warnings(
    *,
    action: str,
    symbol: str,
    requested_quantity: float,
    available_quantity: float,
    gross_trade_value: float,
    portfolio_value_after: float,
    metrics_after: dict[str, float | str],
    sector_name: str,
    asset_type: str,
    turnover_limit: float = 0.10,
) -> list[dict[str, Any]]:
    warnings: list[dict[str, Any]] = []

    _append_weight_warning(
        warnings,
        name="Max single position",
        actual=float(metrics_after["position_weight"]),
        limit=0.25,
        message=(
            f"Max single position breached: {symbol.upper()} "
            f"{float(metrics_after['position_weight']) * 100:.1f}% / limit 25.0%."
        ),
    )
    _append_weight_warning(
        warnings,
        name="Max sector weight",
        actual=float(metrics_after["sector_exposure"]),
        limit=0.50,
        message=(
            f"{sector_name} sector overweight: "
            f"{float(metrics_after['sector_exposure']) * 100:.1f}% / limit 50.0%."
        ),
    )
    _append_weight_warning(
        warnings,
        name="Minimum cash reserve",
        actual=float(metrics_after["cash_weight"]),
        limit=0.02,
        message="Cash below reserve requirement.",
        breach_when="below",
    )

    if asset_type.lower() == "etf":
        _append_weight_warning(
            warnings,
            name="Max ETF allocation",
            actual=float(metrics_after["asset_type_allocation"]),
            limit=0.80,
            message=(
                "ETF allocation overweight: "
                f"{float(metrics_after['asset_type_allocation']) * 100:.1f}% / limit 80.0%."
            ),
        )

    if asset_type.lower() == "equity":
        _append_weight_warning(
            warnings,
            name="Max single-stock exposure",
            actual=float(metrics_after["asset_type_allocation"]),
            limit=0.70,
            message=(
                "Single-stock exposure overweight: "
                f"{float(metrics_after['asset_type_allocation']) * 100:.1f}% / limit 70.0%."
            ),
        )

    turnover = gross_trade_value / portfolio_value_after if portfolio_value_after > 0 else 0.0
    _append_weight_warning(
        warnings,
        name="Max turnover",
        actual=turnover,
        limit=turnover_limit,
        message=(
            f"Turnover impact is {turnover * 100:.1f}% / limit "
            f"{turnover_limit * 100:.1f}%."
        ),
    )

    if float(metrics_after["top_3_holdings_concentration"]) > 0.80:
        warnings.append(
            {
                "name": "Concentration risk",
                "severity": "medium",
                "actual": float(metrics_after["top_3_holdings_concentration"]),
                "limit": 0.80,
                "status": "warning",
                "message": "Top 3 holdings concentration remains elevated.",
            },
        )

    if action == "SELL" and requested_quantity > available_quantity:
        warnings.append(
            {
                "name": "Sell quantity",
                "severity": "high",
                "actual": requested_quantity,
                "limit": available_quantity,
                "status": "breach",
                "message": (
                    f"Sell quantity exceeds available holdings: "
                    f"{requested_quantity:.2f} / available {available_quantity:.2f}."
                ),
            },
        )

    return warnings


def _append_weight_warning(
    warnings: list[dict[str, Any]],
    *,
    name: str,
    actual: float,
    limit: float,
    message: str,
    breach_when: str = "above",
) -> None:
    breached = actual > limit if breach_when == "above" else actual < limit
    if not breached:
        return

    warnings.append(
        {
            "name": name,
            "severity": "high" if name in {"Max single position", "Minimum cash reserve"} else "medium",
            "actual": actual,
            "limit": limit,
            "status": "breach",
            "message": message,
        },
    )
