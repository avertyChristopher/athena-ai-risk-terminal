from math import isclose

from fastapi.testclient import TestClient

from app.main import app
from app.modules.pnl_attribution.repository import PnlAttributionRepository
from app.modules.reports_center.repository import ReportsCenterRepository


client = TestClient(app)


def setup_function() -> None:
    PnlAttributionRepository().clear()
    ReportsCenterRepository().clear()


def test_pnl_attribution_status_endpoint() -> None:
    response = client.get("/api/pnl-attribution/status")

    assert response.status_code == 200
    body = response.json()
    assert body["module"] == "pnl-attribution"
    assert body["status"] == "ready"
    assert body["attribution_ready"] is True
    assert "Portfolio Builder" in body["source_modules"]


def test_pnl_attribution_analyze_default_portfolio_calculation_coherence() -> None:
    response = client.post(
        "/api/pnl-attribution/analyze",
        json={
            "portfolio_id": "pf_001",
            "start_date": "2026-05-13",
            "end_date": "2026-06-03",
            "attribution_method": "Brinson-lite",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["portfolio_name"] == "Athena Balanced Growth Portfolio"
    assert body["position_contributions"]
    assert body["athena_ai_commentary"]["generated_by"] == "deterministic_fallback"
    assert isclose(
        body["total_pnl"],
        body["ending_value"] - body["starting_value"],
        rel_tol=1e-9,
        abs_tol=1e-6,
    )
    assert isclose(
        sum(row["total_pnl"] for row in body["position_contributions"]),
        body["total_pnl"],
        rel_tol=1e-9,
        abs_tol=1e-6,
    )
    assert isclose(
        sum(row["total_pnl"] for row in body["asset_class_contributions"]),
        body["total_pnl"],
        rel_tol=1e-9,
        abs_tol=1e-6,
    )
    assert isclose(
        sum(row["total_pnl"] for row in body["sector_contributions"]),
        body["total_pnl"],
        rel_tol=1e-9,
        abs_tol=1e-6,
    )
    assert isclose(
        body["realized_pnl"] + body["unrealized_pnl"],
        body["price_pnl"],
        rel_tol=1e-9,
        abs_tol=1e-6,
    )
    assert body["income_pnl"] >= 0
    assert body["fees_and_costs"] >= 0
    assert body["benchmark_comparison"]["benchmark_symbol"] == "SPY"


def test_pnl_attribution_demo_portfolios_work() -> None:
    for portfolio_id in ["pf_001", "pf_003", "pf_004"]:
        response = client.post(
            "/api/pnl-attribution/analyze",
            json={"portfolio_id": portfolio_id},
        )

        assert response.status_code == 200
        body = response.json()
        assert body["portfolio_id"] == portfolio_id
        assert body["top_winners"]
        assert body["top_losers"]


def test_pnl_attribution_missing_market_data_returns_warning_not_crash() -> None:
    portfolio_response = client.post(
        "/api/portfolios",
        json={
            "name": "P&L Missing Data Test",
            "base_currency": "USD",
            "benchmark": "SPY",
            "cash": 1000,
        },
    )
    portfolio_id = portfolio_response.json()["id"]
    position_response = client.post(
        f"/api/portfolios/{portfolio_id}/positions",
        json={
            "symbol": "ZZZZ",
            "asset_name": "Missing Market Data Asset",
            "asset_type": "equity",
            "quantity": 10,
            "average_price": 100,
            "current_price": 105,
            "currency": "USD",
            "sector": "Test",
            "country": "United States",
        },
    )
    assert position_response.status_code == 201

    response = client.post(
        "/api/pnl-attribution/analyze",
        json={"portfolio_id": portfolio_id},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "generated_with_warnings"
    assert any("ZZZZ" in warning for warning in body["warnings"])


def test_pnl_attribution_rates_options_trade_and_history_export_workflow() -> None:
    generated = client.post(
        "/api/pnl-attribution/analyze",
        json={"portfolio_id": "pf_004", "include_options": True, "include_rates": True},
    ).json()
    analysis_id = generated["analysis_id"]

    history = client.get("/api/pnl-attribution/history")
    detail = client.get(f"/api/pnl-attribution/history/{analysis_id}")
    csv_export = client.get(f"/api/pnl-attribution/history/{analysis_id}/export/csv")
    delete_response = client.delete(f"/api/pnl-attribution/history/{analysis_id}")
    missing = client.get(f"/api/pnl-attribution/history/{analysis_id}")

    assert generated["fixed_income_effects"]
    assert generated["options_effects"]["status"] in {"prepared", "demo_estimate"}
    assert generated["trade_effects"]["status"] in {"available", "unavailable"}
    assert history.status_code == 200
    assert history.json()["total_analyses"] == 1
    assert detail.status_code == 200
    assert csv_export.status_code == 200
    assert "position_contributions" in csv_export.json()["included_tables"]
    assert delete_response.status_code == 200
    assert missing.status_code == 404


def test_reports_center_includes_and_generates_pnl_report() -> None:
    templates = client.get("/api/reports-center/templates")
    template_types = {template["report_type"] for template in templates.json()["templates"]}

    response = client.post(
        "/api/reports-center/generate",
        json={"report_type": "pnl_attribution", "portfolio_id": "pf_001"},
    )

    assert "pnl_attribution" in template_types
    assert response.status_code == 200
    body = response.json()
    assert body["report_type"] == "pnl_attribution"
    assert any(section["section_id"] == "position_pnl" for section in body["sections"])
