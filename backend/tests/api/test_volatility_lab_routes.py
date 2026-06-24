import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_volatility_lab_status_is_ready() -> None:
    response = client.get("/api/volatility-lab/status")

    assert response.status_code == 200
    body = response.json()
    assert body["module"] == "volatility-lab"
    assert body["status"] == "ready"
    assert "beta_capm" in body["engines_available"]


def test_volatility_lab_analyze_asset_returns_cfa_metrics() -> None:
    response = client.post(
        "/api/volatility-lab/analyze-asset",
        json={"symbol": "AAPL", "benchmark_symbol": "SPY", "rolling_window": 5},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["symbol"] == "AAPL"
    assert body["return_summary"]["observations"] > 0
    assert body["volatility_summary"]["annualized_volatility"] > 0
    assert body["benchmark_risk"]["benchmark_symbol"] == "SPY"
    assert "p5" in body["distribution"]["percentiles"]
    assert body["downside_risk"]["historical_var"] >= 0
    assert body["data_source"]["metric_source"] == "realized_market_data"
    assert body["ewma_volatility"]["latest_volatility"] > 0
    assert body["var_models"]["parametric_var"] >= 0
    assert body["var_models"]["monte_carlo_var"] >= 0
    assert body["var_models"]["horizon_days"] == 1
    assert body["risk_monitor_payload"]["annualized_volatility"] > 0
    assert body["risk_monitor_payload"]["source_module"] == "volatility_lab"
    assert body["risk_monitor_payload"]["module_name"] == "volatility_lab"
    assert body["athena_ai_commentary"]["generated_by"] == "deterministic_fallback"
    assert "not investment advice" in body["athena_ai_commentary"]["disclaimer"]
    assert body["risk_monitor_payload"]["methodology"]["ewma"].startswith("exponentially")
    assert body["risk_monitor_payload"]["assumptions"]
    assert body["risk_monitor_payload"]["limitations"]
    assert body["methodology"]["ewma"]["method"] == "ewma"
    assert body["methodology"]["parametric_var"]["method"] == "parametric_normal"
    assert body["var_backtest"]["status"] in {"acceptable", "review", "insufficient_data"}
    assert body["stress_scenarios"]
    assert body["advanced_models"]["ewma"] == "available"
    assert body["drawdown_series"]


def test_volatility_lab_analyze_asset_accepts_date_range() -> None:
    response = client.post(
        "/api/volatility-lab/analyze-asset",
        json={
            "symbol": "AAPL",
            "benchmark_symbol": "SPY",
            "start_date": "2026-01-01",
            "end_date": "2026-06-30",
            "rolling_window": 5,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["return_summary"]["observations"] > 0
    assert body["risk_monitor_payload"]["data_source"]["observations"] > 0


def test_volatility_lab_analyze_asset_falls_back_when_market_data_missing() -> None:
    response = client.post(
        "/api/volatility-lab/analyze-asset",
        json={"symbol": "UNKNOWN", "benchmark_symbol": "SPY"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["symbol"] == "UNKNOWN"
    assert body["data_source"]["fallback_used"] is True
    assert "Requires Market Data" in body["data_source"]["badges"]


def test_volatility_lab_analyze_portfolio_returns_covariance_metrics() -> None:
    response = client.post(
        "/api/volatility-lab/analyze-portfolio",
        json={"portfolio_id": "pf_001", "benchmark_symbol": "SPY", "rolling_window": 5},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["portfolio_id"] == "pf_001"
    assert body["holdings_included"]
    assert body["return_summary"]["observations"] > 0
    assert body["portfolio_risk"]["covariance_based_volatility"] > 0
    assert body["rolling_volatility"]
    assert body["covariance_matrix"]["symbols"]
    assert body["correlation_matrix"]["matrix"]
    assert body["risk_contribution"]
    assert body["athena_commentary"]["cfa_notes"]
    assert body["athena_ai_commentary"]["source_modules"] == ["volatility_lab"]
    assert body["ewma_volatility"]["latest_volatility"] > 0
    assert body["var_models"]["parametric_cvar"] >= body["var_models"]["parametric_var"]
    assert body["risk_monitor_payload"]["risk_contribution"]
    assert body["risk_monitor_payload"]["coverage_ratio"] == body["portfolio_coverage"]["coverage_ratio"]


def test_volatility_lab_analyze_portfolio_accepts_date_range() -> None:
    response = client.post(
        "/api/volatility-lab/analyze-portfolio",
        json={
            "portfolio_id": "pf_001",
            "benchmark_symbol": "SPY",
            "start_date": "2026-01-01",
            "end_date": "2026-06-30",
            "rolling_window": 5,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["portfolio_id"] == "pf_001"
    assert body["risk_monitor_payload"]["covariance_summary"]["matrix_available"] is True
    assert body["portfolio_coverage"]["coverage_ratio"] >= 0
    assert body["methodology"]["covariance"]["method"] == "sample_covariance"


def test_volatility_lab_rejects_invalid_date_range() -> None:
    response = client.post(
        "/api/volatility-lab/analyze-asset",
        json={
            "symbol": "AAPL",
            "start_date": "2026-06-30",
            "end_date": "2026-01-01",
        },
    )

    assert response.status_code == 422


def test_volatility_lab_rejects_invalid_date_format() -> None:
    response = client.post(
        "/api/volatility-lab/analyze-asset",
        json={
            "symbol": "AAPL",
            "start_date": "not-a-date",
        },
    )

    assert response.status_code == 422


def test_volatility_lab_parametric_var_scales_for_ten_day_horizon() -> None:
    one_day = client.post(
        "/api/volatility-lab/analyze-asset",
        json={"symbol": "AAPL", "benchmark_symbol": "SPY", "horizon_days": 1},
    ).json()
    ten_day = client.post(
        "/api/volatility-lab/analyze-asset",
        json={"symbol": "AAPL", "benchmark_symbol": "SPY", "horizon_days": 10},
    ).json()

    assert ten_day["var_models"]["horizon_days"] == 10
    assert ten_day["var_models"]["parametric_var"] == pytest.approx(
        one_day["var_models"]["parametric_var"] * (10**0.5),
    )
    assert "square-root-of-time" in ten_day["var_models"]["parametric_horizon_note"]


def test_volatility_lab_demo_endpoint_uses_demo_portfolio() -> None:
    response = client.get("/api/volatility-lab/demo")

    assert response.status_code == 200
    body = response.json()
    assert body["portfolio_id"] == "pf_001"
    assert body["portfolio_name"] == "Athena Demo Portfolio"
