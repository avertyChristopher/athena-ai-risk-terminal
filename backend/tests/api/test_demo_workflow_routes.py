from fastapi.testclient import TestClient

from app.main import app
from app.modules.demo_workflow.repository import DemoWorkflowRepository
from app.modules.risk_monitor.service import RiskMonitorService


client = TestClient(app)


def setup_function() -> None:
    DemoWorkflowRepository().clear()


def test_demo_workflow_status_exposes_recruiter_ready_contract() -> None:
    response = client.get("/api/demo/status")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ready"
    assert payload["demo_portfolio_id"] == "pf_004"
    assert payload["active_modules"] == 16
    assert payload["database_connected"] is True
    assert "POST /api/demo/run-athena-demo" in payload["endpoints"]
    assert {item["module"] for item in payload["persistence"]} >= {
        "Trade Blotter",
        "P&L Attribution",
        "Reconciliation Center",
        "Limit Center",
        "AI Anomaly Center",
        "Reports Center",
    }


def test_demo_workflow_run_creates_summary_and_history() -> None:
    response = client.post(
        "/api/demo/run-athena-demo",
        json={"portfolio_id": "pf_004", "language": "en", "include_report": True},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["portfolio_id"] == "pf_004"
    assert payload["demo_run_id"].startswith("demo_")
    assert payload["generated_report_id"]
    assert payload["quick_links"]["reports_center"] == "/reports-center"
    assert "Portfolio Builder" in payload["modules_run"]
    assert "Risk Monitor" in payload["modules_run"]
    assert len(payload["module_results"]) >= 8
    assert payload["records_created"]["reports"] == 1

    history = client.get("/api/demo/history")
    assert history.status_code == 200
    assert history.json()["total_runs"] == 1
    assert history.json()["items"][0]["demo_run_id"] == payload["demo_run_id"]


def test_demo_workflow_degrades_gracefully_when_a_module_fails(monkeypatch) -> None:
    def raise_risk_failure(self, payload):  # noqa: ANN001
        raise RuntimeError("forced risk monitor outage")

    monkeypatch.setattr(RiskMonitorService, "analyze", raise_risk_failure)

    response = client.post(
        "/api/demo/run-athena-demo",
        json={"portfolio_id": "pf_004", "language": "fr", "include_report": False},
    )

    assert response.status_code == 200
    payload = response.json()
    risk_step = next(item for item in payload["module_results"] if item["module"] == "Risk Monitor")
    assert risk_step["status"] == "failed"
    assert "forced risk monitor outage" in risk_step["detail"]
    assert any("Risk Monitor unavailable" in warning for warning in payload["warnings"])
    assert payload["quick_links"]["ai_anomaly_center"] == "/ai-anomaly-center"
