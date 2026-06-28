from fastapi.testclient import TestClient

from app.main import app
from app.modules.ai_anomaly_center.repository import AIAnomalyCenterRepository
from app.modules.reports_center.repository import ReportsCenterRepository


client = TestClient(app)


def setup_function() -> None:
    AIAnomalyCenterRepository().clear()
    ReportsCenterRepository().clear()


def test_reports_center_status_endpoint() -> None:
    response = client.get("/api/reports-center/status")

    assert response.status_code == 200
    body = response.json()
    assert body["module"] == "reports-center"
    assert body["status"] == "ready"
    assert body["snapshot_based"] is True
    assert "markdown" in body["export_formats"]


def test_reports_center_templates_endpoint_returns_required_templates() -> None:
    response = client.get("/api/reports-center/templates")

    assert response.status_code == 200
    template_types = {template["report_type"] for template in response.json()["templates"]}
    assert {
        "portfolio_overview",
        "risk_monitor",
        "stress_testing",
        "limit_breach",
        "trade_suitability",
        "fixed_income_exposure",
        "options_risk",
        "ai_anomaly",
        "full_portfolio_risk_pack",
    } <= template_types


def test_reports_center_generates_portfolio_overview_snapshot() -> None:
    response = client.post(
        "/api/reports-center/generate",
        json={"report_type": "portfolio_overview", "portfolio_id": "pf_001"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["report_type"] == "portfolio_overview"
    assert body["portfolio_id"] == "pf_001"
    assert body["portfolio_name"] == "Athena Balanced Growth Portfolio"
    assert body["snapshot"]["portfolio_id"] == "pf_001"
    assert body["snapshot"]["generated_at"]
    assert "Portfolio Builder" in body["snapshot"]["source_modules"]
    assert "Market Data" in body["snapshot"]["source_modules"]
    assert any(section["section_id"] == "holdings" for section in body["sections"])
    assert body["athena_commentary"]["generated_by"] == "deterministic_fallback"


def test_reports_center_generates_risk_stress_limit_and_full_pack_reports() -> None:
    report_types = [
        "risk_monitor",
        "stress_testing",
        "limit_breach",
        "fixed_income_exposure",
        "options_risk",
        "trade_suitability",
        "ai_anomaly",
        "full_portfolio_risk_pack",
    ]

    for report_type in report_types:
        response = client.post(
            "/api/reports-center/generate",
            json={"report_type": report_type, "portfolio_id": "pf_003"},
        )

        assert response.status_code == 200
        body = response.json()
        assert body["report_type"] == report_type
        assert body["report_id"].startswith("rpt_")
        assert body["snapshot"]["source_modules"]
        assert body["sections"]
        assert body["disclaimer"]


def test_reports_center_missing_payloads_generate_warnings_not_crashes() -> None:
    response = client.post(
        "/api/reports-center/generate",
        json={"report_type": "options_risk", "portfolio_id": None, "source_payloads": {}},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "generated_with_warnings"
    assert body["warnings"]
    assert any(section["status"] == "unavailable" for section in body["sections"])


def test_reports_center_library_get_exports_and_delete_workflow() -> None:
    generated = client.post(
        "/api/reports-center/generate",
        json={"report_type": "full_portfolio_risk_pack", "portfolio_id": "pf_004"},
    ).json()
    report_id = generated["report_id"]

    list_response = client.get("/api/reports-center/reports")
    detail_response = client.get(f"/api/reports-center/reports/{report_id}")
    json_export = client.get(f"/api/reports-center/reports/{report_id}/export/json")
    markdown_export = client.get(f"/api/reports-center/reports/{report_id}/export/markdown")
    csv_export = client.get(f"/api/reports-center/reports/{report_id}/export/csv")
    delete_response = client.delete(f"/api/reports-center/reports/{report_id}")
    missing_response = client.get(f"/api/reports-center/reports/{report_id}")

    assert list_response.status_code == 200
    assert list_response.json()["total_reports"] == 1
    assert detail_response.status_code == 200
    assert detail_response.json()["report_id"] == report_id
    assert json_export.status_code == 200
    assert json_export.json()["report_id"] == report_id
    assert markdown_export.status_code == 200
    assert "# Full Portfolio Risk Pack" in markdown_export.json()["markdown"]
    assert csv_export.status_code == 200
    assert csv_export.json()["included_tables"]
    assert delete_response.status_code == 200
    assert delete_response.json()["deleted"] is True
    assert missing_response.status_code == 404


def test_reports_center_demo_endpoint_generates_full_risk_pack() -> None:
    response = client.get("/api/reports-center/demo")

    assert response.status_code == 200
    body = response.json()
    assert body["report_type"] == "full_portfolio_risk_pack"
    assert body["portfolio_id"] == "pf_004"
    assert "Athena" in body["title"] or "Risk Pack" in body["title"]
