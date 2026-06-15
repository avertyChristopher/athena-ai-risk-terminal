from copy import deepcopy
from typing import Any


def decorate_positions(
    positions: list[dict[str, Any]],
    cash: float,
) -> list[dict[str, Any]]:
    market_values = [_market_value(position) for position in positions]
    total_value = sum(market_values) + cash
    invested_value = sum(market_values)

    return [
        {
            **position,
            "market_value": market_value,
            "portfolio_weight": _safe_divide(market_value, total_value),
            "invested_weight": _safe_divide(market_value, invested_value),
        }
        for position, market_value in zip(positions, market_values)
    ]


def apply_trade_to_positions(
    positions: list[dict[str, Any]],
    *,
    action: str,
    symbol: str,
    quantity: float,
    estimated_price: float,
    asset_name: str,
    asset_type: str,
    currency: str,
    sector: str,
    country: str,
) -> list[dict[str, Any]]:
    simulated_positions = deepcopy(positions)
    normalized_symbol = symbol.upper()
    existing_position = next(
        (
            position
            for position in simulated_positions
            if str(position["symbol"]).upper() == normalized_symbol
        ),
        None,
    )

    if action == "BUY":
        if existing_position is None:
            simulated_positions.append(
                {
                    "id": f"sim_{normalized_symbol}",
                    "portfolio_id": "",
                    "symbol": normalized_symbol,
                    "asset_name": asset_name,
                    "name": asset_name,
                    "asset_type": asset_type,
                    "quantity": quantity,
                    "average_price": estimated_price,
                    "current_price": estimated_price,
                    "currency": currency,
                    "sector": sector,
                    "country": country,
                },
            )
            return simulated_positions

        previous_quantity = float(existing_position["quantity"])
        previous_cost = previous_quantity * float(existing_position["average_price"])
        added_cost = quantity * estimated_price
        new_quantity = previous_quantity + quantity
        existing_position["quantity"] = new_quantity
        existing_position["average_price"] = (previous_cost + added_cost) / new_quantity
        existing_position["current_price"] = estimated_price
        return simulated_positions

    if existing_position is None:
        return simulated_positions

    existing_position["quantity"] = max(
        0.0,
        float(existing_position["quantity"]) - quantity,
    )
    existing_position["current_price"] = estimated_price
    return [
        position
        for position in simulated_positions
        if float(position["quantity"]) > 0
    ]


def calculate_cash_after_trade(
    *,
    cash_before: float,
    action: str,
    gross_trade_value: float,
    total_implementation_cost: float,
) -> float:
    if action == "BUY":
        return cash_before - gross_trade_value - total_implementation_cost

    return cash_before + gross_trade_value - total_implementation_cost


def calculate_portfolio_metrics(
    positions: list[dict[str, Any]],
    cash: float,
    symbol: str,
) -> dict[str, float | str]:
    decorated_positions = decorate_positions(positions, cash)
    market_values = [float(position["market_value"]) for position in decorated_positions]
    total_value = sum(market_values) + cash
    cash_weight = _safe_divide(cash, total_value)
    normalized_symbol = symbol.upper()
    symbol_position = next(
        (
            position
            for position in decorated_positions
            if str(position["symbol"]).upper() == normalized_symbol
        ),
        None,
    )
    weights = [float(position["portfolio_weight"]) for position in decorated_positions]
    top_weights = sorted(weights, reverse=True)
    sector_exposures = _allocation_weight_by_key(decorated_positions, "sector", total_value)
    asset_type_exposures = _allocation_weight_by_key(
        decorated_positions,
        "asset_type",
        total_value,
    )
    currency_exposures = _allocation_weight_by_key(
        decorated_positions,
        "currency",
        total_value,
    )
    expected_return, volatility, beta = calculate_demo_risk_metrics(
        decorated_positions,
        cash_weight,
    )

    return {
        "portfolio_value": total_value,
        "cash": cash,
        "cash_weight": cash_weight,
        "position_weight": float(symbol_position["portfolio_weight"]) if symbol_position else 0.0,
        "sector_exposure": float(
            sector_exposures.get(str(symbol_position["sector"]), 0.0)
            if symbol_position
            else 0.0,
        ),
        "asset_type_allocation": float(
            asset_type_exposures.get(str(symbol_position["asset_type"]), 0.0)
            if symbol_position
            else 0.0,
        ),
        "currency_exposure": float(
            currency_exposures.get(str(symbol_position["currency"]), 0.0)
            if symbol_position
            else 0.0,
        ),
        "largest_position_weight": max(weights, default=0.0),
        "top_3_holdings_concentration": sum(top_weights[:3]),
        "diversification_score": max(0.0, 1.0 - sum(weight * weight for weight in weights)),
        "expected_return": expected_return,
        "portfolio_volatility": volatility,
        "portfolio_beta": beta,
    }


def calculate_demo_risk_metrics(
    positions: list[dict[str, Any]],
    cash_weight: float,
) -> tuple[float, float, float]:
    expected_return = cash_weight * 0.02
    weighted_average_volatility = cash_weight * 0.01
    beta = 0.0

    for position in positions:
        asset_type = str(position["asset_type"]).lower()
        weight = float(position["portfolio_weight"])
        expected_return += weight * _expected_return_for_asset_type(asset_type)
        weighted_average_volatility += weight * _volatility_for_asset_type(asset_type)
        beta += weight * _beta_for_asset(str(position["symbol"]), asset_type)

    volatility = weighted_average_volatility * 0.72
    return expected_return, volatility, beta


def estimate_var_95(portfolio_value: float, volatility: float) -> float:
    return portfolio_value * volatility * 1.65


def estimate_cvar_95(portfolio_value: float, volatility: float) -> float:
    return portfolio_value * volatility * 2.06


def estimate_max_drawdown(volatility: float) -> float:
    return -min(0.65, volatility * 2.4)


def estimate_tracking_error(expected_return: float, concentration: float) -> float:
    return max(0.015, abs(expected_return - 0.06) * 0.65 + concentration * 0.035)


def calculate_information_ratio(
    expected_return: float,
    tracking_error: float,
) -> float | None:
    if tracking_error <= 0:
        return None

    return (expected_return - 0.06) / tracking_error


def _allocation_weight_by_key(
    positions: list[dict[str, Any]],
    key: str,
    total_value: float,
) -> dict[str, float]:
    exposures: dict[str, float] = {}
    for position in positions:
        name = str(position.get(key) or "Unknown")
        exposures[name] = exposures.get(name, 0.0) + _safe_divide(
            float(position["market_value"]),
            total_value,
        )
    return exposures


def _expected_return_for_asset_type(asset_type: str) -> float:
    return {
        "equity": 0.08,
        "etf": 0.06,
        "fixed_income": 0.035,
        "bond": 0.035,
        "cash": 0.02,
    }.get(asset_type, 0.05)


def _volatility_for_asset_type(asset_type: str) -> float:
    return {
        "equity": 0.22,
        "etf": 0.16,
        "fixed_income": 0.06,
        "bond": 0.06,
        "cash": 0.01,
    }.get(asset_type, 0.15)


def _beta_for_asset(symbol: str, asset_type: str) -> float:
    known_betas = {
        "AAPL": 1.20,
        "MSFT": 1.05,
        "NVDA": 1.60,
        "SPY": 1.00,
        "QQQ": 1.15,
        "BND": 0.20,
    }
    beta_by_asset_type = {
        "equity": 1.05,
        "etf": 0.95,
        "fixed_income": 0.20,
        "bond": 0.20,
        "cash": 0.0,
    }
    return known_betas.get(symbol.upper(), beta_by_asset_type.get(asset_type, 1.0))


def _market_value(position: dict[str, Any]) -> float:
    return float(position["quantity"]) * float(position["current_price"])


def _safe_divide(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0

    return numerator / denominator
