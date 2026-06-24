from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_stress_testing_status_is_ready() -> None:
    response = client.get("/api/stress-testing/status")

    assert response.status_code == 200
    body = response.json()
    assert body["module"] == "stress-testing"
    assert "portfolio_impact" in body["engines_available"]
    assert "risk_monitor_payload" in body["engines_available"]


def test_stress_testing_scenarios_endpoint_returns_library() -> None:
    response = client.get("/api/stress-testing/scenarios")

    assert response.status_code == 200
    body = response.json()
    scenario_ids = {scenario["id"] for scenario in body["scenarios"]}
    assert len(scenario_ids) >= 9
    assert "equity_selloff" in scenario_ids
    assert "risk_off_combined" in scenario_ids
    for scenario in body["scenarios"]:
        assert scenario["name"]
        assert scenario["description"]
        assert "asset_class_shocks" in scenario["shocks"]


def test_stress_testing_run_returns_portfolio_impacts_and_payload() -> None:
    response = client.post(
        "/api/stress-testing/run",
        json={
            "portfolio_id": "pf_001",
            "scenario_id": "technology_shock",
            "benchmark_symbol": "SPY",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["selected_portfolio"]["portfolio_id"] == "pf_001"
    assert body["selected_scenario"]["id"] == "technology_shock"
    assert body["base_portfolio_value"] > body["stressed_portfolio_value"]
    assert body["dollar_loss"] > 0
    assert body["percent_loss"] > 0
    assert body["position_impacts"]
    assert body["asset_class_impacts"]
    assert body["sector_impacts"]
    assert body["worst_contributors"]
    assert body["risk_monitor_payload"]["scenario_id"] == "technology_shock"
    assert body["risk_monitor_payload"]["breached_limits"] == body["limit_breaches"]


def test_stress_testing_demo_endpoint_returns_complete_response() -> None:
    response = client.get("/api/stress-testing/demo")

    assert response.status_code == 200
    body = response.json()
    assert body["selected_scenario"]["id"] == "risk_off_combined"
    assert body["severity"]["severity"] in {"High", "Severe", "Critical"}
    assert body["fixed_income_stress"]["data_source"]
    assert body["options_risk"]["options_pricing_lab_ready"] is True


def test_stress_testing_missing_portfolio_returns_clean_error() -> None:
    response = client.post(
        "/api/stress-testing/run",
        json={"portfolio_id": "missing", "scenario_id": "equity_selloff"},
    )

    assert response.status_code == 422
    assert "not found" in response.json()["detail"]


def test_stress_testing_unknown_scenario_returns_clean_error() -> None:
    response = client.post(
        "/api/stress-testing/run",
        json={"portfolio_id": "pf_001", "scenario_id": "unknown"},
    )

    assert response.status_code == 422
    assert "Unknown stress scenario" in response.json()["detail"]


def test_stress_testing_invalid_custom_shock_returns_validation_error() -> None:
    response = client.post(
        "/api/stress-testing/run",
        json={
            "portfolio_id": "pf_001",
            "custom_scenario": {
                "name": "Invalid custom",
                "sector_shocks": {"Technology": -1.5},
            },
        },
    )

    assert response.status_code == 422
