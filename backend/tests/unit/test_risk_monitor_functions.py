from app.modules.risk_monitor.domain.risk_contribution import (
    calculate_risk_contribution,
)
from app.modules.risk_monitor.domain.risk_limits import evaluate_limit_breaches
from app.modules.risk_monitor.domain.risk_metrics import (
    calculate_exposure_by_key,
    calculate_risk_score,
    classify_global_risk_status,
    decorate_positions,
)
from app.modules.risk_monitor.domain.stress_testing import run_stress_scenarios
from app.modules.risk_monitor.schemas import RiskMonitorAnalyzeRequest
from app.modules.risk_monitor.service import RiskMonitorService


def _sample_positions() -> list[dict[str, object]]:
    return [
        {
            "symbol": "NVDA",
            "asset_name": "NVIDIA Corporation",
            "asset_type": "equity",
            "quantity": 40,
            "current_price": 900,
            "sector": "Technology",
        },
        {
            "symbol": "AAPL",
            "asset_name": "Apple Inc.",
            "asset_type": "equity",
            "quantity": 20,
            "current_price": 190,
            "sector": "Technology",
        },
        {
            "symbol": "BND",
            "asset_name": "Vanguard Total Bond Market ETF",
            "asset_type": "etf",
            "quantity": 100,
            "current_price": 72,
            "sector": "Fixed Income",
        },
    ]


def test_risk_score_classifies_high_risk_with_severe_inputs() -> None:
    score = calculate_risk_score(
        volatility=0.24,
        var_95=0.04,
        cvar_95=0.06,
        max_drawdown=-0.20,
        top_3_weight=0.90,
        cash_weight=0.02,
        active_exposure=0.80,
        breach_severities=["high", "medium"],
    )

    assert score >= 70
    assert classify_global_risk_status(score) in {"High Risk", "Critical Risk"}


def test_limit_engine_detects_concentration_and_cash_breaches() -> None:
    decorated = decorate_positions(_sample_positions(), cash=500)
    breaches = evaluate_limit_breaches(
        decorated_positions=decorated,
        sector_exposures=calculate_exposure_by_key(decorated, "sector"),
        asset_type_exposures=calculate_exposure_by_key(decorated, "asset_type"),
        cash_weight=0.01,
        top_3_weight=0.95,
        volatility=0.22,
        var_95=0.02,
        cvar_95=0.03,
        max_drawdown=-0.10,
        tracking_error=0.04,
        active_exposure=0.65,
    )

    rule_names = {str(breach["rule_name"]) for breach in breaches}
    assert "Max single position weight" in rule_names
    assert "Max sector exposure" in rule_names
    assert "Minimum cash reserve" in rule_names
    assert "Max top 3 concentration" in rule_names


def test_stress_scenarios_estimate_negative_portfolio_impacts() -> None:
    decorated = decorate_positions(_sample_positions(), cash=500)
    total_value = sum(float(position["market_value"]) for position in decorated) + 500

    scenarios = run_stress_scenarios(decorated, total_value)
    tech_scenario = next(
        scenario
        for scenario in scenarios
        if str(scenario["name"]) == "Technology sector shock -15%"
    )

    assert len(scenarios) == 6
    assert float(tech_scenario["estimated_impact_percent"]) < 0
    assert "NVDA" in tech_scenario["most_affected_holdings"]


def test_risk_contribution_falls_back_to_demo_proxy_without_covariance() -> None:
    decorated = decorate_positions(_sample_positions(), cash=500)

    contribution = calculate_risk_contribution(
        decorated_positions=decorated,
        covariance_matrix=[],
        covariance_symbols=[],
    )

    assert contribution["contribution_source"] == "deterministic_demo"
    assert contribution["largest_risk_contributor"] == "NVDA"
    assert len(contribution["by_asset"]) == 3


class MissingReturnRepository:
    db = None

    def get_portfolio(self, portfolio_id: str) -> dict[str, object] | None:
        return {
            "id": portfolio_id,
            "name": "Missing Return Portfolio",
            "base_currency": "USD",
            "benchmark": "SPY",
            "cash": 1000,
        }

    def list_positions(self, portfolio_id: str) -> list[dict[str, object]]:
        return [
            {
                "symbol": "XYZ",
                "asset_name": "Missing Return Series Corp.",
                "asset_type": "equity",
                "quantity": 10,
                "current_price": 100,
                "sector": "Technology",
            }
        ]


def test_risk_monitor_uses_demo_fallback_when_returns_are_missing() -> None:
    service = RiskMonitorService(MissingReturnRepository())

    response = service.analyze(RiskMonitorAnalyzeRequest(portfolio_id="pf_missing"))

    assert response.risk_source.metric_source == "deterministic_demo"
    assert response.risk_source.fallback_used is True
    assert "XYZ" in response.risk_source.symbols_missing
