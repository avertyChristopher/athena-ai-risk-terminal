import pytest

from app.modules.volatility_lab.domain.beta import calculate_beta, jensen_alpha
from app.modules.volatility_lab.domain.correlation import correlation
from app.modules.volatility_lab.domain.covariance import covariance
from app.modules.volatility_lab.domain.downside_risk import (
    downside_deviation,
    historical_cvar,
    historical_var,
    max_drawdown_from_returns,
    semi_deviation,
    semi_variance,
)
from app.modules.volatility_lab.domain.ewma import ewma_volatility
from app.modules.volatility_lab.domain.portfolio_volatility import (
    portfolio_volatility,
    weighted_portfolio_returns,
)
from app.modules.volatility_lab.domain.risk_adjusted import (
    information_ratio,
    sharpe_ratio,
    tracking_error,
    treynor_ratio,
)
from app.modules.volatility_lab.domain.rolling_volatility import rolling_volatility
from app.modules.volatility_lab.domain.volatility import (
    annualized_volatility,
    standard_deviation,
    variance,
)
from app.modules.volatility_lab.domain.var_models import (
    monte_carlo_cvar,
    monte_carlo_var,
    parametric_cvar,
    parametric_var,
)


RETURNS = [0.01, -0.02, 0.03, 0.04]
BENCHMARK_RETURNS = [0.0, -0.01, 0.02, 0.03]


def test_standard_deviation_and_annualized_volatility_are_sample_based() -> None:
    assert variance(RETURNS) == pytest.approx(0.0007)
    assert standard_deviation(RETURNS) == pytest.approx(0.0264575, rel=1e-5)
    assert annualized_volatility(RETURNS) == pytest.approx(0.4200, rel=1e-3)


def test_rolling_volatility_uses_windowed_returns() -> None:
    points = rolling_volatility(
        RETURNS,
        ["2026-01-02", "2026-01-03", "2026-01-04", "2026-01-05"],
        window=2,
    )

    assert len(points) == 3
    assert points[0]["date"] == "2026-01-03"
    assert float(points[0]["volatility"]) > 0


def test_downside_risk_var_cvar_and_drawdown() -> None:
    assert semi_variance(RETURNS) == pytest.approx(0.0004)
    assert semi_deviation(RETURNS) == pytest.approx(0.02)
    assert downside_deviation(RETURNS) == pytest.approx(0.31749, rel=1e-4)
    assert max_drawdown_from_returns(RETURNS) == pytest.approx(-0.02)
    assert historical_var(RETURNS, 0.95) == pytest.approx(0.02)
    assert historical_cvar(RETURNS, 0.95) == pytest.approx(0.02)


def test_covariance_correlation_and_beta() -> None:
    assert covariance(RETURNS, BENCHMARK_RETURNS) == pytest.approx(0.0004667, rel=1e-4)
    assert correlation(RETURNS, BENCHMARK_RETURNS) == pytest.approx(0.9661, rel=1e-3)
    assert calculate_beta(RETURNS, BENCHMARK_RETURNS) == pytest.approx(1.4)


def test_portfolio_weighted_returns_and_covariance_volatility() -> None:
    aligned_returns = {
        "AAPL": [0.01, 0.02, -0.01],
        "MSFT": [0.00, 0.01, 0.02],
    }
    weights = {"AAPL": 0.6, "MSFT": 0.4}
    portfolio_returns = weighted_portfolio_returns(aligned_returns, weights)

    assert portfolio_returns == pytest.approx([0.006, 0.016, 0.002])
    assert portfolio_volatility([0.6, 0.4], [[0.0004, 0.0001], [0.0001, 0.0002]]) > 0


def test_risk_adjusted_metrics_are_available() -> None:
    beta = calculate_beta(RETURNS, BENCHMARK_RETURNS)

    assert sharpe_ratio(RETURNS, 0.02) is not None
    assert treynor_ratio(RETURNS, beta, 0.02) is not None
    assert tracking_error(RETURNS, BENCHMARK_RETURNS) is not None
    assert information_ratio(RETURNS, BENCHMARK_RETURNS) is not None
    assert jensen_alpha(RETURNS, BENCHMARK_RETURNS, 0.02) is not None


def test_ewma_volatility_weights_recent_returns() -> None:
    summary = ewma_volatility(RETURNS, lambda_decay=0.94)

    assert summary["latest_volatility"] == pytest.approx(0.2515, rel=1e-3)
    assert summary["lambda_decay"] == 0.94
    assert summary["badge"] == "Realized"


def test_parametric_var_and_cvar_use_normal_assumption() -> None:
    var_value = parametric_var(RETURNS, 0.95)
    cvar_value = parametric_cvar(RETURNS, 0.95)

    assert var_value == pytest.approx(0.0285, rel=1e-2)
    assert cvar_value > var_value


def test_monte_carlo_var_is_deterministic_with_seed() -> None:
    first_var = monte_carlo_var(RETURNS, 0.95, simulations=500, seed=7)
    second_var = monte_carlo_var(RETURNS, 0.95, simulations=500, seed=7)
    first_cvar = monte_carlo_cvar(RETURNS, 0.95, simulations=500, seed=7)
    second_cvar = monte_carlo_cvar(RETURNS, 0.95, simulations=500, seed=7)

    assert first_var == pytest.approx(second_var)
    assert first_cvar == pytest.approx(second_cvar)
    assert first_cvar >= first_var
