import pytest

from app.modules.portfolio_builder.domain.behavioral import (
    create_behavioral_bias_summary,
    detect_concentration_overconfidence_warning,
    detect_home_bias_placeholder,
    detect_loss_aversion_placeholder,
)
from app.modules.portfolio_builder.domain.capm import (
    calculate_capm_required_return,
    calculate_market_risk_premium,
    calculate_weighted_portfolio_beta,
    compare_expected_return_to_required_return,
)
from app.modules.portfolio_builder.domain.efficient_frontier import (
    create_efficient_frontier_demo_points,
)
from app.modules.portfolio_builder.domain.performance_ratios import (
    calculate_active_return,
    calculate_information_ratio,
    calculate_jensen_alpha,
    calculate_sharpe_ratio,
    calculate_tracking_error,
    calculate_treynor_ratio,
)
from app.modules.portfolio_builder.domain.pooled_vehicles import (
    calculate_etf_exposure,
    calculate_pooled_vehicle_exposure,
    calculate_single_stock_exposure,
    classify_pooled_vehicle_usage,
)
from app.modules.portfolio_builder.domain.risk_tolerance import (
    classify_overall_risk_tolerance,
    create_risk_tolerance_summary,
    detect_ability_willingness_conflict,
)
from app.modules.portfolio_builder.domain.utility import (
    calculate_utility_score,
    classify_risk_aversion,
    rank_portfolio_by_utility,
)


def test_risk_tolerance_uses_lower_of_ability_and_willingness() -> None:
    assert classify_overall_risk_tolerance("High", "Moderate") == "Moderate"
    assert detect_ability_willingness_conflict("High", "Low") is True
    assert "conflict" in create_risk_tolerance_summary("High", "Low").lower()


def test_utility_and_risk_aversion_calculations() -> None:
    assert calculate_utility_score(0.08, 0.04, 3.0) == pytest.approx(0.02)
    assert classify_risk_aversion(6.0) == "High risk aversion"
    ranked = rank_portfolio_by_utility(
        [
            {"name": "A", "utility_score": 0.01},
            {"name": "B", "utility_score": 0.03},
        ],
    )
    assert ranked[0]["name"] == "B"


def test_capm_and_portfolio_beta_calculations() -> None:
    positions = [
        {"symbol": "AAA", "invested_weight": 0.6},
        {"symbol": "BBB", "invested_weight": 0.4},
    ]
    premium = calculate_market_risk_premium(0.08, 0.04)
    beta = calculate_weighted_portfolio_beta(positions, {"AAA": 1.2, "BBB": 0.5})

    assert premium == pytest.approx(0.04)
    assert beta == pytest.approx(0.92)
    assert calculate_capm_required_return(0.04, beta, premium) == pytest.approx(
        0.0768,
    )
    assert "above" in compare_expected_return_to_required_return(0.09, 0.0768)


def test_risk_adjusted_performance_ratios() -> None:
    active_returns = [0.02, 0.01, -0.01]
    tracking_error = calculate_tracking_error(active_returns)

    assert calculate_sharpe_ratio(0.08, 0.04, 0.20) == pytest.approx(0.20)
    assert calculate_treynor_ratio(0.08, 0.04, 1.25) == pytest.approx(0.032)
    assert calculate_jensen_alpha(0.09, 0.075) == pytest.approx(0.015)
    assert calculate_active_return(0.08, 0.06) == pytest.approx(0.02)
    assert tracking_error is not None
    assert calculate_information_ratio(0.02, tracking_error) is not None


def test_behavioral_bias_heuristics() -> None:
    positions = [{"country": "Canada", "invested_weight": 0.8}]

    assert "home bias" in detect_home_bias_placeholder(positions, "Canada").lower()
    assert detect_concentration_overconfidence_warning(0.35) is not None
    assert detect_loss_aversion_placeholder(-0.20) is not None
    assert "home bias" in create_behavioral_bias_summary(["home bias warning"])


def test_pooled_vehicle_exposure_calculations() -> None:
    positions = [
        {"asset_type": "etf", "portfolio_weight": 0.30},
        {"asset_type": "equity", "portfolio_weight": 0.60},
        {"asset_type": "cash", "portfolio_weight": 0.10},
    ]

    assert calculate_etf_exposure(positions) == pytest.approx(0.30)
    assert calculate_single_stock_exposure(positions) == pytest.approx(0.60)
    assert calculate_pooled_vehicle_exposure(positions) == pytest.approx(0.30)
    assert classify_pooled_vehicle_usage(0.30) == "Satellite pooled-vehicle allocation"


def test_efficient_frontier_demo_points_include_current_portfolio() -> None:
    points = create_efficient_frontier_demo_points(0.07, 0.15)

    assert len(points) == 3
    assert points[1]["label"] == "Current portfolio"
    assert points[1]["expected_return"] == pytest.approx(0.07)
