from fastapi.testclient import TestClient

from app.main import app
from app.modules.limit_center.repository import LimitCenterRepository


client = TestClient(app)


def setup_function() -> None:
    LimitCenterRepository().reset_demo_state()


def test_limit_center_status_endpoint() -> None:
    response = client.get("/api/limit-center/status")

    assert response.status_code == 200
    body = response.json()
    assert body["module"] == "limit-center"
    assert body["status"] == "ready"
    assert "breach_detection" in body["engines_available"]


def test_limit_center_default_rules_are_returned() -> None:
    response = client.get("/api/limit-center/rules")

    assert response.status_code == 200
    body = response.json()
    assert body["total_rules"] >= 20
    assert body["active_rules"] == body["total_rules"]
    assert any(rule["rule_id"] == "max_single_position_weight" for rule in body["rules"])


def test_limit_center_create_update_disable_and_delete_rule() -> None:
    create = client.post(
        "/api/limit-center/rules",
        json={
            "rule_id": "custom_liquidity_floor",
            "name": "Custom liquidity floor",
            "category": "portfolio",
            "metric_key": "cash_weight",
            "limit_value": 0.08,
            "comparison_operator": "less_than",
            "severity_if_breached": "medium",
            "source_modules": ["portfolio_builder"],
            "description": "Custom cash floor.",
            "methodology": "Demo test rule.",
        },
    )
    assert create.status_code == 201
    assert create.json()["rule_id"] == "custom_liquidity_floor"

    update = client.put(
        "/api/limit-center/rules/custom_liquidity_floor",
        json={"enabled": False, "limit_value": 0.10},
    )
    assert update.status_code == 200
    assert update.json()["enabled"] is False
    assert update.json()["limit_value"] == 0.10

    delete = client.delete("/api/limit-center/rules/custom_liquidity_floor")
    assert delete.status_code == 200
    assert delete.json()["deleted"] is True


def test_limit_center_detects_portfolio_builder_breaches() -> None:
    response = client.post(
        "/api/limit-center/evaluate",
        json={
            "portfolio_id": "pf_001",
            "source_module": "portfolio_builder",
            "payload": {
                "concentration": {
                    "largest_position": {"weight": 0.31},
                    "top_3_weight": 0.72,
                    "sector_exposures": [{"name": "Technology", "weight": 0.64}],
                    "cash_weight": 0.03,
                }
            },
        },
    )

    assert response.status_code == 200
    body = response.json()
    rule_ids = {breach["rule_id"] for breach in body["breaches"]}
    assert "max_single_position_weight" in rule_ids
    assert "max_sector_exposure" in rule_ids
    assert body["athena_ai_commentary"]["generated_by"] == "deterministic_fallback"


def test_limit_center_detects_risk_monitor_breaches() -> None:
    response = client.post(
        "/api/limit-center/evaluate",
        json={
            "portfolio_id": "pf_001",
            "source_module": "risk_monitor",
            "payload": {
                "global_risk_score": 82,
                "risk_metrics": [
                    {"name": "VaR 95%", "value": 0.04},
                    {"name": "CVaR 95%", "value": 0.06},
                ],
            },
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert any(breach["rule_id"] == "max_var_95" for breach in body["breaches"])
    assert any(breach["rule_id"] == "max_cvar_95" for breach in body["breaches"])
    assert body["overall_status"] == "critical_breach"


def test_limit_center_detects_volatility_payload_breaches() -> None:
    response = client.post(
        "/api/limit-center/evaluate",
        json={
            "portfolio_id": "pf_001",
            "source_module": "volatility_lab",
            "payload": {
                "volatility_summary": {"annualized_volatility": 0.26},
                "var_models": {"historical_var": 0.035, "historical_cvar": 0.052},
                "benchmark_risk": {"beta": 1.6},
            },
        },
    )

    assert response.status_code == 200
    rule_ids = {breach["rule_id"] for breach in response.json()["breaches"]}
    assert "max_portfolio_volatility" in rule_ids
    assert "max_beta" in rule_ids


def test_limit_center_detects_options_unlimited_loss_breach() -> None:
    response = client.post(
        "/api/limit-center/evaluate",
        json={
            "portfolio_id": "pf_001",
            "source_module": "options_pricing_lab",
            "payload": {
                "risk_payload": {"delta_adjusted_exposure": 125000, "vega": 6100},
                "max_loss": {"type": "unlimited", "value": None},
            },
        },
    )

    assert response.status_code == 200
    breaches = response.json()["breaches"]
    assert any(breach["rule_id"] == "require_options_review_for_unlimited_loss" for breach in breaches)
    assert any(breach["severity"] == "critical" for breach in breaches)


def test_limit_center_detects_rates_duration_breach() -> None:
    response = client.post(
        "/api/limit-center/evaluate",
        json={
            "portfolio_id": "pf_001",
            "source_module": "rates_lab",
            "payload": {"modified_duration": 8.2, "dv01": 65.0},
        },
    )

    assert response.status_code == 200
    rule_ids = {breach["rule_id"] for breach in response.json()["breaches"]}
    assert "max_modified_duration" in rule_ids
    assert "max_dv01" in rule_ids


def test_limit_center_detects_stress_loss_breach() -> None:
    response = client.post(
        "/api/limit-center/evaluate",
        json={
            "portfolio_id": "pf_001",
            "source_module": "stress_testing",
            "payload": {
                "percent_loss": 0.22,
                "severity": {"severity": "critical"},
            },
        },
    )

    assert response.status_code == 200
    rule_ids = {breach["rule_id"] for breach in response.json()["breaches"]}
    assert "max_stress_loss_severe" in rule_ids
    assert "max_single_scenario_loss" in rule_ids


def test_limit_center_detects_trade_payload_breaches() -> None:
    response = client.post(
        "/api/limit-center/evaluate-module-payload",
        json={
            "portfolio_id": "pf_001",
            "source_module": "trade_simulator",
            "payload": {
                "portfolio_value": 100000,
                "trade_ticket": {
                    "gross_trade_value": 25000,
                    "estimated_cash_after_trade_weight": 0.02,
                },
                "constraints_warnings": [
                    {"name": "Post-trade sector exposure", "actual": 0.57},
                ],
            },
        },
    )

    assert response.status_code == 200
    rule_ids = {breach["rule_id"] for breach in response.json()["breaches"]}
    assert "max_trade_turnover" in rule_ids
    assert "min_cash_after_trade" in rule_ids
    assert "max_post_trade_sector_exposure" in rule_ids


def test_limit_center_returns_no_breach_when_values_are_within_limits() -> None:
    response = client.post(
        "/api/limit-center/evaluate",
        json={
            "portfolio_id": "pf_001",
            "source_module": "risk_monitor",
            "payload": {
                "global_risk_score": 40,
                "risk_metrics": [
                    {"name": "VaR 95%", "value": 0.01},
                    {"name": "CVaR 95%", "value": 0.02},
                    {"name": "Portfolio volatility", "value": 0.12},
                ],
            },
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["breaches"] == []
    assert body["overall_status"] in {"within_limits", "watchlist"}


def test_limit_center_breach_register_detail_and_review_workflow() -> None:
    evaluation = client.post(
        "/api/limit-center/evaluate",
        json={
            "portfolio_id": "pf_001",
            "source_module": "rates_lab",
            "payload": {"modified_duration": 8.2},
        },
    )
    breach_id = evaluation.json()["breaches"][0]["breach_id"]

    list_response = client.get("/api/limit-center/breaches")
    detail_response = client.get(f"/api/limit-center/breaches/{breach_id}")
    review_response = client.post(
        f"/api/limit-center/breaches/{breach_id}/review",
        json={
            "action": "mark_under_review",
            "reviewer": "risk.manager",
            "note": "Investigating duration exposure.",
        },
    )
    approve_response = client.post(
        f"/api/limit-center/breaches/{breach_id}/review",
        json={
            "action": "approve_exception",
            "reviewer": "cro",
            "note": "Temporary exception.",
        },
    )

    assert list_response.status_code == 200
    assert detail_response.status_code == 200
    assert review_response.status_code == 200
    assert review_response.json()["breach"]["status"] == "under_review"
    assert approve_response.status_code == 200
    assert approve_response.json()["breach"]["status"] == "approved_exception"


def test_limit_center_review_reject_resolve_and_reopen() -> None:
    evaluation = client.post(
        "/api/limit-center/evaluate",
        json={
            "portfolio_id": "pf_001",
            "source_module": "portfolio_builder",
            "payload": {"single_position_weight": 0.31},
        },
    )
    breach_id = evaluation.json()["breaches"][0]["breach_id"]

    under_review = client.post(
        f"/api/limit-center/breaches/{breach_id}/review",
        json={"action": "mark_under_review", "reviewer": "risk.manager"},
    )
    rejected = client.post(
        f"/api/limit-center/breaches/{breach_id}/review",
        json={"action": "reject", "reviewer": "risk.manager"},
    )
    resolved = client.post(
        f"/api/limit-center/breaches/{breach_id}/review",
        json={"action": "resolve", "reviewer": "risk.manager"},
    )
    reopened = client.post(
        f"/api/limit-center/breaches/{breach_id}/review",
        json={"action": "reopen", "reviewer": "risk.manager"},
    )

    assert under_review.status_code == 200
    assert rejected.json()["breach"]["status"] == "rejected"
    assert resolved.json()["breach"]["status"] == "resolved"
    assert reopened.json()["breach"]["status"] == "open"


def test_limit_center_demo_endpoint_returns_commentary() -> None:
    response = client.get("/api/limit-center/demo")

    assert response.status_code == 200
    body = response.json()
    assert body["portfolio_id"] == "pf_001"
    assert body["breaches"] == []
    assert body["overall_status"] in {"within_limits", "watchlist"}
    assert body["athena_ai_commentary"]["generated_by"] == "deterministic_fallback"


def test_limit_center_flags_tech_concentration_but_not_balanced_growth() -> None:
    balanced_risk = client.post(
        "/api/risk-monitor/analyze",
        json={"portfolio_id": "pf_001", "benchmark_symbol": "SPY"},
    ).json()
    tech_risk = client.post(
        "/api/risk-monitor/analyze",
        json={"portfolio_id": "pf_003", "benchmark_symbol": "SPY"},
    ).json()

    balanced = client.post(
        "/api/limit-center/evaluate",
        json={
            "portfolio_id": "pf_001",
            "source_module": "risk_monitor",
            "payload": balanced_risk,
        },
    ).json()
    tech = client.post(
        "/api/limit-center/evaluate",
        json={
            "portfolio_id": "pf_003",
            "source_module": "risk_monitor",
            "payload": tech_risk,
        },
    ).json()

    tech_rule_ids = {breach["rule_id"] for breach in tech["breaches"]}
    assert balanced["overall_status"] in {"within_limits", "watchlist"}
    assert balanced["breaches"] == []
    assert tech["overall_status"] == "critical_breach"
    assert {"max_single_position_weight", "max_sector_exposure", "max_risk_score"} <= tech_rule_ids


def test_limit_center_missing_payload_fields_warn_without_crashing() -> None:
    response = client.post(
        "/api/limit-center/evaluate",
        json={
            "portfolio_id": "pf_001",
            "source_module": "rates_lab",
            "payload": {"module_name": "rates_lab"},
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["breaches"] == []
    assert body["warnings"]
