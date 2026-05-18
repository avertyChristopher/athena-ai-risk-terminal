import math

import pytest

from app.domain.market_data import calculate_log_returns, calculate_simple_returns
from app.domain.volatility import annualized_volatility, daily_volatility, rolling_volatility


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


def test_daily_and_annualized_volatility() -> None:
    returns = [0.01, 0.02, -0.01, 0.0]

    daily = daily_volatility(returns)
    annualized = annualized_volatility(returns)

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
        daily_volatility([0.01])
