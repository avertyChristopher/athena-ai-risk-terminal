import pytest

from app.modules.stress_testing.domain.contributors import (
    aggregate_impacts,
    rank_worst_contributors,
)
from app.modules.stress_testing.domain.portfolio_impact import (
    calculate_portfolio_stress_value,
)
from app.modules.stress_testing.domain.rates_shocks import (
    duration_assumption,
    estimate_bond_price_impact_from_duration,
)
from app.modules.stress_testing.domain.risk_impact import (
    build_risk_metric_snapshot,
    estimate_stress_severity,
)
from app.modules.stress_testing.domain.scenarios import (
    get_predefined_scenario,
    list_predefined_scenarios,
)


POSITIONS = [
    {
        "id": "pos_a",
        "symbol": "AAPL",
        "asset_name": "Apple Inc.",
        "asset_type": "equity",
        "quantity": 10,
        "current_price": 200,
        "sector": "Technology",
        "currency": "USD",
    },
    {
        "id": "pos_b",
        "symbol": "BND",
        "asset_name": "Vanguard Total Bond Market ETF",
        "asset_type": "fixed_income",
        "quantity": 20,
        "current_price": 75,
        "sector": "Fixed Income",
        "currency": "USD",
    },
]


def test_scenario_library_contains_required_institutional_scenarios() -> None:
    scenarios = list_predefined_scenarios()
    scenario_ids = {scenario["id"] for scenario in scenarios}

    assert "equity_selloff" in scenario_ids
    assert "technology_shock" in scenario_ids
    assert "rates_shock_up" in scenario_ids
    assert "rates_shock_down" in scenario_ids
    assert "volatility_spike" in scenario_ids
    assert "usd_shock" in scenario_ids
    assert "credit_spread_widening" in scenario_ids
    assert "risk_off_combined" in scenario_ids
    assert "liquidity_shock" in scenario_ids


def test_portfolio_stress_calculates_base_stressed_loss_and_contributions() -> None:
    scenario = get_predefined_scenario("equity_selloff")
    assert scenario is not None

    result = calculate_portfolio_stress_value(POSITIONS, 500.0, scenario, "USD")

    assert result["base_portfolio_value"] == pytest.approx(4000.0)
    assert result["stressed_portfolio_value"] < result["base_portfolio_value"]
    assert result["dollar_loss"] > 0
    assert result["percent_loss"] > 0
    contribution_sum = sum(
        impact["contribution_to_loss"] for impact in result["position_impacts"]
    )
    assert contribution_sum == pytest.approx(1.0)


def test_technology_shock_impacts_technology_more_than_broad_market() -> None:
    scenario = get_predefined_scenario("technology_shock")
    assert scenario is not None

    result = calculate_portfolio_stress_value(POSITIONS, 0.0, scenario, "USD")
    impacts = {impact["symbol"]: impact for impact in result["position_impacts"]}

    assert impacts["AAPL"]["percent_impact"] < -0.25
    assert impacts["AAPL"]["percent_impact"] < impacts["BND"]["percent_impact"]


def test_rates_shock_up_creates_negative_fixed_income_duration_impact() -> None:
    duration, source = duration_assumption("BND", "fixed_income")

    assert duration == pytest.approx(6.0)
    assert source == "Demo Duration"
    assert estimate_bond_price_impact_from_duration(1000.0, duration, 100.0) == pytest.approx(-60.0)


def test_volatility_spike_increases_stressed_var_and_cvar() -> None:
    snapshot = build_risk_metric_snapshot(
        portfolio_value=100_000.0,
        base_volatility=0.18,
        volatility_shock=0.75,
        percent_loss=0.10,
        confidence_level=0.95,
    )

    assert snapshot["stressed_volatility"] > snapshot["before_volatility"]
    assert snapshot["stressed_var"] > snapshot["before_var"]
    assert snapshot["stressed_cvar"] > snapshot["before_cvar"]


def test_stress_severity_framework_classifies_low_and_critical_losses() -> None:
    low = estimate_stress_severity(0.01, 1000.0, 0, 0.0, 0.1, False)
    critical = estimate_stress_severity(0.40, 40_000.0, 3, 1.5, 0.6, True)

    assert low["severity"] == "Low"
    assert critical["severity"] == "Critical"
    assert critical["score"] > low["score"]


def test_worst_contributors_and_group_impacts_are_ranked() -> None:
    scenario = get_predefined_scenario("risk_off_combined")
    assert scenario is not None
    result = calculate_portfolio_stress_value(POSITIONS, 0.0, scenario, "USD")

    worst = rank_worst_contributors(result["position_impacts"])
    sectors = aggregate_impacts(result["position_impacts"], "sector")

    assert worst[0]["dollar_loss"] >= worst[-1]["dollar_loss"]
    assert sectors[0]["dollar_impact"] <= 0
