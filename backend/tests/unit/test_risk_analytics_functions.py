import pytest

from app.modules.risk_analytics.domain import (
    calculate_annualized_volatility,
    calculate_covariance_matrix,
    calculate_historical_cvar,
    calculate_historical_var,
    calculate_tracking_error,
    calculate_weighted_portfolio_returns,
)
from app.modules.risk_analytics.service import RiskAnalyticsService


class FakeMarketDataRepository:
    def get_supported_symbols(self) -> list[str]:
        return ["AAA", "BBB", "SPY"]

    def get_prices(self, symbol: str) -> list[dict[str, object]]:
        prices = {
            "AAA": [100.0, 101.0, 99.0, 102.0],
            "BBB": [50.0, 50.5, 51.0, 50.0],
            "SPY": [400.0, 402.0, 401.0, 404.0],
        }
        return [
            {
                "date": f"2026-01-0{index + 1}",
                "symbol": symbol,
                "close": price,
            }
            for index, price in enumerate(prices[symbol])
        ]


def test_weighted_portfolio_returns() -> None:
    returns = {
        "AAA": [0.01, -0.02, 0.03],
        "BBB": [0.00, 0.01, -0.01],
    }

    weighted = calculate_weighted_portfolio_returns(
        returns,
        {"AAA": 0.6, "BBB": 0.4},
    )

    assert weighted == pytest.approx([0.006, -0.008, 0.014])


def test_annualized_volatility_and_covariance_matrix() -> None:
    returns = {
        "AAA": [0.01, -0.02, 0.03],
        "BBB": [0.00, 0.01, -0.01],
    }

    volatility = calculate_annualized_volatility(returns["AAA"])
    covariance = calculate_covariance_matrix(returns, ["AAA", "BBB"])

    assert volatility > 0
    assert len(covariance) == 2
    assert covariance[0][0] > 0
    assert covariance[0][1] == pytest.approx(covariance[1][0])


def test_historical_var_cvar_and_tracking_error() -> None:
    portfolio_returns = [0.01, -0.03, 0.02, -0.01, 0.015]
    benchmark_returns = [0.005, -0.01, 0.012, -0.004, 0.01]

    assert calculate_historical_var(portfolio_returns) > 0
    assert calculate_historical_cvar(portfolio_returns) >= calculate_historical_var(
        portfolio_returns,
    )
    assert calculate_tracking_error(portfolio_returns, benchmark_returns) > 0


def test_risk_analytics_service_uses_aligned_market_returns() -> None:
    service = RiskAnalyticsService(FakeMarketDataRepository())

    result = service.calculate_realized_portfolio_risk(
        {"AAA": 0.6, "BBB": 0.4},
        benchmark_symbol="SPY",
    )

    assert result.metric_source == "realized_market_data"
    assert result.fallback_used is False
    assert result.observations == 3
    assert result.realized_volatility is not None
    assert result.portfolio_var_95 is not None
    assert result.tracking_error is not None


def test_risk_analytics_service_falls_back_when_returns_missing() -> None:
    service = RiskAnalyticsService(FakeMarketDataRepository())

    result = service.calculate_realized_portfolio_risk(
        {"AAA": 0.6, "MISSING": 0.4},
        benchmark_symbol="SPY",
    )

    assert result.metric_source == "deterministic_demo"
    assert result.fallback_used is True
    assert "MISSING" in result.symbols_missing
    assert result.fallback_reason is not None
