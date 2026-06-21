import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_rates_lab_status_endpoint() -> None:
    response = client.get("/api/rates-lab/status")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ready"
    assert body["module"] == "rates-lab"
    assert "duration" in body["engines_available"]


def test_rates_lab_bond_price_endpoint() -> None:
    response = client.post(
        "/api/rates-lab/bond-price",
        json={
            "face_value": 1000,
            "coupon_rate": 0.05,
            "coupon_frequency": "semiannual",
            "years_to_maturity": 5,
            "yield_to_maturity": 0.05,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["clean_price"] == pytest.approx(1000)
    assert body["price_status"] == "par"
    assert len(body["cash_flow_schedule"]) == 10


def test_rates_lab_yield_analysis_endpoint() -> None:
    response = client.post(
        "/api/rates-lab/yield-analysis",
        json={
            "price": 950,
            "face_value": 1000,
            "coupon_rate": 0.05,
            "coupon_frequency": "annual",
            "years_to_maturity": 5,
            "beginning_price": 940,
            "ending_price": 950,
            "coupon_received": 50,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["yield_to_maturity"] > 0.05
    assert body["current_yield"] > 0.05
    assert body["holding_period_return"] > 0
    assert body["price_status"] == "discount"


def test_rates_lab_duration_convexity_endpoint() -> None:
    response = client.post(
        "/api/rates-lab/duration-convexity",
        json={"rate_shock_bps": 100},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["macaulay_duration"] > body["modified_duration"] > 0
    assert body["convexity"] > 0
    assert body["dv01"] > 0
    assert body["estimated_price_change_duration"] < 0
    assert body["risk_monitor_payload"]["module"] == "rates_lab"


def test_rates_lab_yield_curve_endpoint() -> None:
    response = client.post("/api/rates-lab/yield-curve", json={})

    assert response.status_code == 200
    body = response.json()
    assert body["interpolated_curve"]
    assert body["forward_rates"]
    assert body["curve_shape"] in {"normal", "steep", "flat", "inverted"}
    assert body["data_source"]["curve_source"] == "demo_curve"


def test_rates_lab_rate_scenario_endpoint() -> None:
    response = client.post(
        "/api/rates-lab/rate-scenarios",
        json={"scenario_type": "parallel_up", "shock_bps": 100},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["stressed_price"] < body["base_price"]
    assert body["price_change"] < 0
    assert body["stressed_curve"]
    assert body["stress_testing_payload"]["status"] == "ready_for_future_stress_testing"


def test_rates_lab_portfolio_exposure_identifies_demo_bond_etf() -> None:
    response = client.post(
        "/api/rates-lab/portfolio-exposure",
        json={"portfolio_id": "pf_001", "shock_bps": 100},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["portfolio_id"] == "pf_001"
    assert any(item["symbol"] == "BND" for item in body["fixed_income_holdings"])
    assert body["weighted_average_duration"] > 0
    assert body["estimated_portfolio_dv01"] > 0
    assert body["estimated_rate_shock_loss"] < 0
    assert body["risk_monitor_payload"]["status"] == "risk_monitor_ready"


def test_rates_lab_demo_endpoint() -> None:
    response = client.get("/api/rates-lab/demo")

    assert response.status_code == 200
    assert response.json()["cash_flow_schedule"]
