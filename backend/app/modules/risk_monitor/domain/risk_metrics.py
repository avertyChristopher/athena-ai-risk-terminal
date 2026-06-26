from math import sqrt
from statistics import mean
from typing import Any

TRADING_DAYS_PER_YEAR = 252


def decorate_positions(
    positions: list[dict[str, Any]],
    cash: float,
) -> list[dict[str, Any]]:
    market_values = [_market_value(position) for position in positions]
    invested_value = sum(market_values)
    total_value = invested_value + cash

    return [
        {
            **position,
            "market_value": market_value,
            "portfolio_weight": _safe_divide(market_value, total_value),
            "invested_weight": _safe_divide(market_value, invested_value),
        }
        for position, market_value in zip(positions, market_values)
    ]


def calculate_total_value(
    decorated_positions: list[dict[str, Any]],
    cash: float,
) -> float:
    return sum(float(position["market_value"]) for position in decorated_positions) + cash


def calculate_weight_by_symbol(
    decorated_positions: list[dict[str, Any]],
    weight_key: str = "invested_weight",
) -> dict[str, float]:
    weights: dict[str, float] = {}
    for position in decorated_positions:
        symbol = str(position["symbol"]).upper()
        weights[symbol] = weights.get(symbol, 0.0) + float(position[weight_key])
    return weights


def calculate_exposure_by_key(
    decorated_positions: list[dict[str, Any]],
    key: str,
    weight_key: str = "portfolio_weight",
) -> dict[str, float]:
    exposures: dict[str, float] = {}
    for position in decorated_positions:
        name = str(position.get(key) or "Unknown")
        exposures[name] = exposures.get(name, 0.0) + float(position[weight_key])
    return exposures


def calculate_top_n_weight(
    decorated_positions: list[dict[str, Any]],
    count: int,
    weight_key: str = "invested_weight",
) -> float:
    weights = sorted(
        [float(position[weight_key]) for position in decorated_positions],
        reverse=True,
    )
    return sum(weights[:count])


def calculate_demo_expected_return(
    decorated_positions: list[dict[str, Any]],
    cash_weight: float,
) -> float:
    expected_return = cash_weight * 0.02
    for position in decorated_positions:
        expected_return += float(position["portfolio_weight"]) * _asset_expected_return(
            str(position["asset_type"]),
        )
    return expected_return


def calculate_demo_volatility(
    decorated_positions: list[dict[str, Any]],
    cash_weight: float,
) -> float:
    weighted_volatility = cash_weight * 0.01
    for position in decorated_positions:
        weighted_volatility += float(position["portfolio_weight"]) * _asset_volatility(
            str(position["symbol"]),
            str(position["asset_type"]),
        )
    return weighted_volatility * 0.72


def calculate_demo_beta(decorated_positions: list[dict[str, Any]]) -> float:
    return sum(
        float(position["portfolio_weight"])
        * _asset_beta(str(position["symbol"]), str(position["asset_type"]))
        for position in decorated_positions
    )


def calculate_demo_var(volatility: float, confidence_multiplier: float = 1.65) -> float:
    return volatility / sqrt(TRADING_DAYS_PER_YEAR) * confidence_multiplier


def calculate_demo_cvar(volatility: float, tail_multiplier: float = 2.06) -> float:
    return volatility / sqrt(TRADING_DAYS_PER_YEAR) * tail_multiplier


def calculate_demo_max_drawdown(volatility: float) -> float:
    return -min(0.65, volatility * 2.4)


def calculate_sharpe_ratio(
    expected_return: float,
    risk_free_rate: float,
    volatility: float,
) -> float | None:
    if volatility <= 0:
        return None
    return (expected_return - risk_free_rate) / volatility


def calculate_sortino_ratio(
    returns: list[float],
    expected_return: float,
    risk_free_rate: float,
    volatility: float,
) -> float | None:
    if returns:
        downside_returns = [period_return for period_return in returns if period_return < 0]
        if len(downside_returns) >= 2:
            downside_mean = mean(downside_returns)
            downside_deviation = sqrt(
                sum((period_return - downside_mean) ** 2 for period_return in downside_returns)
                / (len(downside_returns) - 1),
            ) * sqrt(TRADING_DAYS_PER_YEAR)
            if downside_deviation > 0:
                return (expected_return - risk_free_rate) / downside_deviation

    downside_proxy = volatility * 0.75
    if downside_proxy <= 0:
        return None
    return (expected_return - risk_free_rate) / downside_proxy


def calculate_tracking_error_fallback(
    expected_return: float,
    largest_position_weight: float,
) -> float:
    return max(0.015, abs(expected_return - 0.06) * 0.65 + largest_position_weight * 0.035)


def calculate_information_ratio(
    expected_return: float,
    tracking_error: float | None,
    benchmark_return: float = 0.06,
) -> float | None:
    if tracking_error is None or tracking_error <= 0:
        return None
    return (expected_return - benchmark_return) / tracking_error


def calculate_active_exposure(
    decorated_positions: list[dict[str, Any]],
    benchmark_symbol: str,
) -> float:
    benchmark_weight = 0.0
    for position in decorated_positions:
        if str(position["symbol"]).upper() == benchmark_symbol.upper():
            benchmark_weight += float(position["portfolio_weight"])
    return max(0.0, 1.0 - benchmark_weight)


def calculate_risk_score(
    *,
    volatility: float,
    var_95: float,
    cvar_95: float,
    max_drawdown: float,
    top_3_weight: float,
    cash_weight: float,
    active_exposure: float,
    breach_severities: list[str],
) -> int:
    score = 15
    score += min(20, int((volatility / 0.20) * 16))
    score += min(12, int((var_95 / 0.03) * 10))
    score += min(12, int((cvar_95 / 0.05) * 10))
    score += min(12, int((abs(max_drawdown) / 0.15) * 10))
    score += min(16, int((top_3_weight / 0.65) * 12))
    score += 8 if cash_weight < 0.05 else 0
    score += min(10, int(active_exposure * 8))
    severity_points = {"low": 2, "medium": 5, "high": 9, "critical": 14}
    score += sum(severity_points.get(severity, 0) for severity in breach_severities)
    return min(100, max(0, score))


def classify_global_risk_status(score: int) -> str:
    if score >= 90:
        return "Critical Risk"
    if score >= 70:
        return "High Risk"
    if score >= 50:
        return "Elevated Risk"
    if score >= 30:
        return "Moderate Risk"
    return "Low Risk"


def _asset_expected_return(asset_type: str) -> float:
    return {
        "equity": 0.08,
        "etf": 0.06,
        "fixed_income": 0.035,
        "bond": 0.035,
        "bond_etf": 0.035,
        "treasury_etf": 0.032,
        "commodity_etf": 0.04,
        "cash": 0.02,
    }.get(asset_type.lower(), 0.05)


def _asset_volatility(symbol: str, asset_type: str) -> float:
    known_volatilities = {
        "AAPL": 0.24,
        "MSFT": 0.22,
        "NVDA": 0.42,
        "SPY": 0.16,
        "QQQ": 0.22,
        "VXUS": 0.18,
        "BND": 0.06,
        "IEF": 0.075,
        "TLT": 0.14,
        "GLD": 0.17,
    }
    asset_volatilities = {
        "equity": 0.22,
        "etf": 0.16,
        "fixed_income": 0.06,
        "bond": 0.06,
        "bond_etf": 0.06,
        "treasury_etf": 0.08,
        "commodity_etf": 0.17,
        "cash": 0.01,
    }
    return known_volatilities.get(
        symbol.upper(),
        asset_volatilities.get(asset_type.lower(), 0.15),
    )


def _asset_beta(symbol: str, asset_type: str) -> float:
    known_betas = {
        "AAPL": 1.20,
        "MSFT": 1.05,
        "NVDA": 1.60,
        "SPY": 1.00,
        "QQQ": 1.15,
        "VXUS": 0.95,
        "BND": 0.20,
        "IEF": 0.10,
        "TLT": -0.05,
        "GLD": 0.05,
    }
    asset_betas = {
        "equity": 1.05,
        "etf": 0.95,
        "fixed_income": 0.20,
        "bond": 0.20,
        "bond_etf": 0.20,
        "treasury_etf": 0.10,
        "commodity_etf": 0.05,
        "cash": 0.0,
    }
    return known_betas.get(symbol.upper(), asset_betas.get(asset_type.lower(), 1.0))


def _market_value(position: dict[str, Any]) -> float:
    return float(position["quantity"]) * float(position["current_price"])


def _safe_divide(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator
