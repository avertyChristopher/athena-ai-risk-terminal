import math

import pytest

from app.domain.market_data import (
    calculate_cumulative_returns,
    calculate_drawdown,
    calculate_log_returns,
    calculate_simple_returns,
    detect_duplicate_dates,
    detect_missing_prices,
    detect_outliers,
)
from app.domain.portfolios import (
    calculate_allocation_by_sector,
    calculate_cash_weight,
    calculate_portfolio_market_value,
    calculate_portfolio_weights,
    calculate_position_market_value,
)
from app.domain.volatility import (
    calculate_annualized_volatility,
    calculate_daily_volatility,
    rolling_volatility,
)


def test_calculate_simple_returns() -> None:
    prices = [100.0, 105.0, 102.9, 108.045]

    returns = calculate_simple_returns(prices)

    assert returns == pytest.approx([0.05, -0.02, 0.05])


def test_calculate_log_returns() -> None:
    prices = [100.0, 105.0, 102.9]

    returns = calculate_log_returns(prices)

    assert returns == pytest.approx([math.log(1.05), math.log(0.98)])


def test_returns_reject_invalid_prices() -> None:
    with pytest.raises(ValueError, match="strictly positive"):
        calculate_simple_returns([100.0, 0.0, 101.0])


def test_calculate_cumulative_returns() -> None:
    returns = [0.10, -0.05, 0.02]

    cumulative_returns = calculate_cumulative_returns(returns)

    assert cumulative_returns == pytest.approx([0.10, 0.045, 0.0659])


def test_calculate_drawdown() -> None:
    values = [100.0, 120.0, 90.0, 108.0, 130.0, 117.0]

    drawdowns = calculate_drawdown(values)

    assert drawdowns == pytest.approx([0.0, 0.0, -0.25, -0.10, 0.0, -0.10])


def test_drawdown_rejects_invalid_values() -> None:
    with pytest.raises(ValueError, match="strictly positive"):
        calculate_drawdown([100.0, -95.0])


def test_missing_prices_are_detected() -> None:
    rows = [
        {"date": "2026-05-01", "close": 100.0},
        {"date": "2026-05-02", "close": None},
        {"date": "2026-05-03", "close": ""},
    ]

    assert detect_missing_prices(rows) == ["2026-05-02", "2026-05-03"]


def test_duplicate_dates_are_detected() -> None:
    rows = [
        {"date": "2026-05-01", "close": 100.0},
        {"date": "2026-05-01", "close": 101.0},
        {"date": "2026-05-02", "close": 102.0},
    ]

    assert detect_duplicate_dates(rows) == ["2026-05-01"]


def test_outliers_are_flagged() -> None:
    values = [10.0, 11.0, 12.0, 100.0]

    assert detect_outliers(values, threshold=1.0) == [3]


def test_daily_and_annualized_volatility() -> None:
    returns = [0.01, 0.02, -0.01, 0.0]

    daily = calculate_daily_volatility(returns)
    annualized = calculate_annualized_volatility(returns)

    assert daily == pytest.approx(0.012909944487358056)
    assert annualized == pytest.approx(daily * math.sqrt(252))


def test_rolling_volatility() -> None:
    returns = [0.01, 0.02, -0.01, 0.0]

    values = rolling_volatility(returns, window=2)

    assert values == pytest.approx(
        [
            0.007071067811865475,
            0.021213203435596427,
            0.007071067811865475,
        ]
    )


def test_volatility_rejects_too_few_returns() -> None:
    with pytest.raises(ValueError, match="At least 2 returns"):
        calculate_daily_volatility([0.01])


def test_position_market_value() -> None:
    assert calculate_position_market_value(quantity=10, current_price=200) == 2000


def test_portfolio_value_and_weights() -> None:
    market_values = [2000.0, 3000.0]
    cash = 1000.0

    total_value = calculate_portfolio_market_value(market_values, cash)
    weights = calculate_portfolio_weights(market_values, cash)
    cash_weight = calculate_cash_weight(market_values, cash)

    assert total_value == 6000
    assert weights == pytest.approx([1 / 3, 1 / 2])
    assert cash_weight == pytest.approx(1 / 6)
    assert sum(weights) + cash_weight == pytest.approx(1.0)


def test_empty_portfolio_returns_total_value_zero() -> None:
    assert calculate_portfolio_market_value([]) == 0
    assert calculate_portfolio_weights([]) == []


def test_position_rejects_negative_quantity() -> None:
    with pytest.raises(ValueError, match="quantity"):
        calculate_position_market_value(quantity=-1, current_price=200)


def test_position_rejects_negative_price() -> None:
    with pytest.raises(ValueError, match="price"):
        calculate_position_market_value(quantity=1, current_price=-200)


def test_allocation_by_sector() -> None:
    positions = [
        {"sector": "Technology", "market_value": 700.0},
        {"sector": "Technology", "market_value": 300.0},
        {"sector": "Fixed Income", "market_value": 1000.0},
    ]

    allocation = calculate_allocation_by_sector(positions)

    assert allocation == [
        {"name": "Technology", "market_value": 1000.0, "weight": 0.5},
        {"name": "Fixed Income", "market_value": 1000.0, "weight": 0.5},
    ]
