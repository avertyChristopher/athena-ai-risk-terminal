import pytest

from app.modules.portfolio_builder.domain.constraints import (
    check_min_cash_limit,
    check_single_position_limit,
)
from app.modules.portfolio_builder.domain.diversification import (
    calculate_diversification_score,
    calculate_effective_number_of_holdings,
    calculate_hhi_concentration,
    calculate_top_n_holdings_weight,
    classify_concentration_level,
)
from app.modules.portfolio_builder.domain.performance import (
    calculate_holding_period_return,
    calculate_time_weighted_return,
)
from app.modules.portfolio_builder.domain.portfolio_calculator import (
    calculate_cash_weight,
    calculate_invested_value,
    calculate_portfolio_market_value,
)
from app.modules.portfolio_builder.domain.position_calculator import (
    calculate_invested_weight,
    calculate_portfolio_weight,
    calculate_position_cost_basis,
    calculate_position_market_value,
    calculate_position_unrealized_pnl,
    calculate_position_unrealized_pnl_percent,
    validate_position_input,
)
from app.modules.portfolio_builder.domain.rebalancing import (
    calculate_allocation_drift,
    create_rebalance_preview,
    detect_tolerance_band_breaches,
)
from app.modules.portfolio_builder.domain.risk_return import (
    calculate_portfolio_standard_deviation,
    calculate_portfolio_variance_from_covariance_matrix,
    calculate_weighted_expected_return,
)


def test_position_value_cost_basis_and_unrealized_pnl() -> None:
    assert calculate_position_market_value(10, 12) == 120
    assert calculate_position_cost_basis(10, 9) == 90
    assert calculate_position_unrealized_pnl(10, 9, 12) == 30
    assert calculate_position_unrealized_pnl_percent(10, 9, 12) == pytest.approx(
        1 / 3,
    )


def test_portfolio_and_invested_weights_are_distinct() -> None:
    market_values = [100.0, 300.0]
    cash = 100.0

    total = calculate_portfolio_market_value(market_values, cash)
    invested = calculate_invested_value(market_values)

    assert total == 500
    assert invested == 400
    assert calculate_cash_weight(market_values, cash) == pytest.approx(0.2)
    assert calculate_portfolio_weight(100, total) == pytest.approx(0.2)
    assert calculate_invested_weight(100, invested) == pytest.approx(0.25)


def test_concentration_and_diversification_metrics() -> None:
    weights = [0.5, 0.3, 0.2]

    assert calculate_top_n_holdings_weight(weights, 2) == pytest.approx(0.8)
    assert calculate_hhi_concentration(weights) == pytest.approx(0.38)
    assert calculate_effective_number_of_holdings(weights) == pytest.approx(1 / 0.38)
    assert calculate_diversification_score(weights) == pytest.approx(0.62)
    assert classify_concentration_level(0.5, 1.0) == "High concentration"


def test_basic_risk_return_calculations() -> None:
    weights = [0.6, 0.4]
    expected_returns = [0.08, 0.04]
    covariance = [[0.04, 0.006], [0.006, 0.01]]

    variance = calculate_portfolio_variance_from_covariance_matrix(
        weights,
        covariance,
    )

    assert calculate_weighted_expected_return(expected_returns, weights) == pytest.approx(
        0.064,
    )
    assert variance == pytest.approx(0.01888)
    assert calculate_portfolio_standard_deviation(variance) == pytest.approx(
        variance**0.5,
    )


def test_performance_measurement_foundation() -> None:
    assert calculate_holding_period_return(100, 115, 5) == pytest.approx(0.10)
    assert calculate_time_weighted_return([0.10, -0.05]) == pytest.approx(0.045)


def test_target_drift_and_rebalance_preview() -> None:
    positions = [
        {"symbol": "AAA", "market_value": 120.0, "current_price": 12.0},
        {"symbol": "BBB", "market_value": 80.0, "current_price": 8.0},
    ]
    targets = {"AAA": 0.5, "BBB": 0.5}

    preview = create_rebalance_preview(positions, 200.0, targets)

    assert calculate_allocation_drift(0.6, 0.5) == pytest.approx(0.1)
    assert preview[0]["action"] == "sell"
    assert preview[1]["action"] == "buy"
    assert detect_tolerance_band_breaches(
        {"AAA": 0.6},
        {"AAA": 0.5},
        {"AAA": 0.05},
    )[0]["status"] == "Overweight"


def test_constraints_and_position_validation() -> None:
    positions = [{"symbol": "AAA", "invested_weight": 0.4}]

    assert check_single_position_limit(positions, 0.25)[0]["name"] == "AAA"
    assert check_min_cash_limit(0.01, 0.02)[0]["constraint"] == "minimum_cash_weight"

    with pytest.raises(ValueError, match="quantity"):
        validate_position_input(
            symbol="AAA",
            asset_type="equity",
            currency="USD",
            quantity=-1,
            current_price=10,
            average_price=9,
        )

    with pytest.raises(ValueError, match="symbol"):
        validate_position_input(
            symbol="",
            asset_type="equity",
            currency="USD",
            quantity=1,
            current_price=10,
            average_price=9,
        )
