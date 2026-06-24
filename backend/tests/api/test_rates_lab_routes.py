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
    assert body["rates_risk_payload"]["module_name"] == "rates_lab"
    assert body["rates_risk_payload"]["clean_price"] == pytest.approx(body["clean_price"])
    assert body["rates_risk_payload"]["ytm"] == 0.05


def test_rates_lab_dated_bond_price_and_data_quality() -> None:
    response = client.post(
        "/api/rates-lab/bond-price",
        json={
            "face_value": 1000,
            "coupon_rate": 0.05,
            "coupon_frequency": "semiannual",
            "years_to_maturity": 5,
            "yield_to_maturity": 0.05,
            "settlement_date": "2026-03-01",
            "maturity_date": "2030-12-31",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["clean_price"] == pytest.approx(1000, abs=0.15)
    assert body["dirty_price"] == pytest.approx(
        body["clean_price"] + body["accrued_interest"]
    )
    assert body["methodology"]["details"]["pricing_mode"] == "dated"
    assert body["data_quality"]["simplified_pricing_used"] is False


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
    assert body["rates_risk_payload"]["modified_duration"] == pytest.approx(body["modified_duration"])
    assert body["rates_risk_payload"]["dv01"] == pytest.approx(body["dv01"])


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
    assert body["rates_risk_payload"]["curve_scenario_impact"] == pytest.approx(body["price_change"])
    assert body["rates_risk_payload"]["rate_shock_bps"] == pytest.approx(body["effective_shock_bps"])


def test_rates_lab_nonparallel_scenario_curve_matches_repricing_shock() -> None:
    response = client.post(
        "/api/rates-lab/rate-scenarios",
        json={"scenario_type": "steepener", "shock_bps": 100},
    )

    assert response.status_code == 200
    body = response.json()
    base_five_year = next(point["rate"] for point in body["base_curve"] if point["maturity"] == 5)
    stressed_five_year = next(point["rate"] for point in body["stressed_curve"] if point["maturity"] == 5)
    assert body["base_yield_at_maturity"] == pytest.approx(base_five_year)
    assert body["shocked_yield_at_maturity"] == pytest.approx(stressed_five_year)
    assert body["effective_shock_bps"] == pytest.approx(
        (stressed_five_year - base_five_year) * 10_000
    )
    assert body["stressed_price"] != pytest.approx(body["base_price"])


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
    assert body["rates_risk_payload"]["portfolio_id"] == "pf_001"
    assert body["rates_risk_payload"]["dv01"] == pytest.approx(body["estimated_portfolio_dv01"])


def test_rates_lab_demo_endpoint() -> None:
    response = client.get("/api/rates-lab/demo")

    assert response.status_code == 200
    assert response.json()["cash_flow_schedule"]


@pytest.mark.parametrize(
    ("path", "payload"),
    [
        ("/api/rates-lab/yield-curve", {"requested_maturities": [-1, 1, 5]}),
        ("/api/rates-lab/bond-price", {"coupon_frequency": "weekly"}),
        (
            "/api/rates-lab/rate-scenarios",
            {
                "yield_to_maturity": -0.9,
                "coupon_frequency": "annual",
                "scenario_type": "parallel_down",
                "shock_bps": 5000,
            },
        ),
        ("/api/rates-lab/bond-price", {"settlement_date": "2026-01-01"}),
    ],
)
def test_rates_lab_invalid_financial_inputs_return_422(
    path: str,
    payload: dict[str, object],
) -> None:
    response = client.post(path, json=payload)

    assert response.status_code == 422


def test_rates_lab_extreme_but_calculable_yield_request_does_not_return_500() -> None:
    response = client.post(
        "/api/rates-lab/yield-analysis",
        json={
            "price": 1000,
            "face_value": 1000,
            "coupon_rate": 0.05,
            "coupon_frequency": "monthly",
            "years_to_maturity": 100,
        },
    )

    assert response.status_code == 200


def test_rates_lab_commentary_defaults_to_english_and_supports_french() -> None:
    english = client.post("/api/rates-lab/bond-price", json={}).json()
    french = client.post(
        "/api/rates-lab/bond-price",
        json={"language": "fr"},
    ).json()

    assert english["athena_commentary"]["summary"].startswith("The bond")
    assert french["athena_commentary"]["summary"].startswith("L'obligation")
