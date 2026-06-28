from fastapi.testclient import TestClient

from app.main import app
from app.modules.reconciliation.repository import ReconciliationRepository
from app.modules.reports_center.repository import ReportsCenterRepository
from app.modules.trade_blotter.repository import TradeBlotterRepository


client = TestClient(app)


def setup_function() -> None:
    ReconciliationRepository().clear()
    ReportsCenterRepository().clear()
    TradeBlotterRepository().clear()


def test_reconciliation_status_endpoint() -> None:
    response = client.get("/api/reconciliation/status")

    assert response.status_code == 200
    body = response.json()
    assert body["module"] == "reconciliation"
    assert body["status"] == "ready"
    assert body["review_workflow_enabled"] is True
    assert {"positions", "cash", "prices", "trades", "pnl", "fx"} <= set(body["checks_available"])
    assert "Portfolio Builder" in body["source_modules"]


def test_reconciliation_run_default_portfolio_returns_minor_demo_breaks() -> None:
    response = client.post("/api/reconciliation/run", json={"portfolio_id": "pf_001"})

    assert response.status_code == 200
    body = response.json()
    assert body["portfolio_name"] == "Athena Balanced Growth Portfolio"
    assert body["overall_status"] == "minor_breaks"
    assert body["breaks_by_type"]["cash"] == 1
    assert body["breaks_by_type"]["price"] == 1
    assert body["critical_breaks"] == 0
    assert body["athena_ai_commentary"]["generated_by"] == "deterministic_fallback"
    assert any("No internal or external trades available" in warning for warning in body["warnings"])


def test_reconciliation_run_handles_placeholder_source_with_warning() -> None:
    response = client.post(
        "/api/reconciliation/run",
        json={
            "portfolio_id": "pf_001",
            "external_source": "uploaded_file_placeholder",
            "checks": ["positions", "cash"],
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["external_source"] == "uploaded_file_placeholder"
    assert any("uploaded_file_placeholder" in warning for warning in body["warnings"])
    assert body["checks_performed"] == ["positions", "cash"]


def test_reconciliation_demo_portfolios_have_expected_break_profiles() -> None:
    conservative = client.post("/api/reconciliation/run", json={"portfolio_id": "pf_002"}).json()
    tech = client.post("/api/reconciliation/run", json={"portfolio_id": "pf_003"}).json()
    institutional = client.get("/api/reconciliation/demo").json()

    assert conservative["overall_status"] == "material_breaks"
    assert conservative["breaks_by_type"]["price"] >= 1
    assert tech["breaks_by_type"]["position"] >= 1
    assert tech["breaks_by_type"]["trade"] == 1
    assert institutional["portfolio_id"] == "pf_004"
    assert institutional["breaks_by_type"]["pnl"] == 1


def test_reconciliation_review_workflow_history_export_and_delete() -> None:
    generated = client.post("/api/reconciliation/run", json={"portfolio_id": "pf_003"}).json()
    run_id = generated["run_id"]
    break_id = generated["breaks"][0]["break_id"]

    under_review = client.post(
        f"/api/reconciliation/breaks/{break_id}/review",
        json={"action": "mark_under_review", "reviewer": "ops", "note": "Investigating settlement."},
    )
    explained = client.post(
        f"/api/reconciliation/breaks/{break_id}/review",
        json={"action": "explain", "reviewer": "ops", "note": "Likely settlement timing."},
    )
    resolved = client.post(
        f"/api/reconciliation/breaks/{break_id}/review",
        json={"action": "resolve", "reviewer": "ops", "decision": "Confirmed with custodian."},
    )
    reopened = client.post(
        f"/api/reconciliation/breaks/{break_id}/review",
        json={"action": "reopen", "reviewer": "ops", "note": "Reopened for regression test."},
    )
    register = client.get("/api/reconciliation/breaks")
    detail = client.get(f"/api/reconciliation/breaks/{break_id}")
    history = client.get("/api/reconciliation/history")
    history_detail = client.get(f"/api/reconciliation/history/{run_id}")
    csv_export = client.get(f"/api/reconciliation/history/{run_id}/export/csv")
    delete_response = client.delete(f"/api/reconciliation/history/{run_id}")
    missing = client.get(f"/api/reconciliation/history/{run_id}")

    assert under_review.status_code == 200
    assert under_review.json()["status"] == "under_review"
    assert explained.json()["status"] == "explained"
    assert resolved.json()["status"] == "resolved"
    assert reopened.json()["status"] == "open"
    assert len(reopened.json()["review_history"]) == 4
    assert register.status_code == 200
    assert register.json()["total_breaks"] >= 1
    assert detail.status_code == 200
    assert history.status_code == 200
    assert history.json()["total_runs"] == 1
    assert history_detail.status_code == 200
    assert csv_export.status_code == 200
    assert {"breaks", "position_breaks", "price_breaks"} <= set(csv_export.json()["included_tables"])
    assert "Break Register" in csv_export.json()["csv"]
    assert delete_response.status_code == 200
    assert missing.status_code == 404


def test_reports_center_includes_and_generates_reconciliation_report() -> None:
    templates = client.get("/api/reports-center/templates")
    template_types = {template["report_type"] for template in templates.json()["templates"]}

    response = client.post(
        "/api/reports-center/generate",
        json={"report_type": "reconciliation", "portfolio_id": "pf_001"},
    )

    assert "reconciliation" in template_types
    assert response.status_code == 200
    body = response.json()
    assert body["report_type"] == "reconciliation"
    assert "Reconciliation Center" in body["snapshot"]["source_modules"]
    assert any(section["section_id"] == "break_register" for section in body["sections"])
    assert body["athena_commentary"]["generated_by"] == "deterministic_fallback"
