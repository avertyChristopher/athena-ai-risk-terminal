from fastapi.testclient import TestClient

from app.main import app
from app.modules.ai_anomaly_center.repository import AIAnomalyCenterRepository
from app.modules.reports_center.repository import ReportsCenterRepository


client = TestClient(app)


def setup_function() -> None:
    AIAnomalyCenterRepository().clear()
    ReportsCenterRepository().clear()


def test_ai_anomaly_center_status_endpoint() -> None:
    response = client.get("/api/ai-anomaly-center/status")

    assert response.status_code == 200
    body = response.json()
    assert body["module"] == "ai-anomaly-center"
    assert body["status"] == "ready"
    assert body["detection_mode"] == "deterministic_rule_based"
    assert body["persistence_enabled"] is True
    assert "market_data" in body["categories"]


def test_ai_anomaly_scan_all_scope_returns_summary_and_commentary() -> None:
    response = client.post(
        "/api/ai-anomaly-center/scan",
        json={
            "portfolio_id": "pf_003",
            "scan_scope": "all",
            "lookback_days": 60,
            "severity_threshold": "low",
            "persist_results": True,
            "language": "en",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["scan_id"].startswith("anom_scan_")
    assert body["portfolio_id"] == "pf_003"
    assert body["scan_scope"] == "all"
    assert body["total_records_scanned"] >= 0
    assert body["anomalies_by_category"] == {
        key: body["anomalies_by_category"][key]
        for key in body["anomalies_by_category"]
    }
    assert body["methodology"]["detection_mode"] == "deterministic rule-based monitoring"
    assert body["athena_ai_commentary"]["generated_by"] == "deterministic_fallback"
    assert "not investment advice" in body["athena_ai_commentary"]["disclaimer"].lower()


def test_ai_anomaly_scan_persists_list_get_review_delete_and_export() -> None:
    scan = client.post(
        "/api/ai-anomaly-center/scan",
        json={
            "portfolio_id": "pf_003",
            "scan_scope": "portfolio",
            "lookback_days": 30,
            "severity_threshold": "low",
            "persist_results": True,
        },
    )

    assert scan.status_code == 200
    scan_body = scan.json()
    assert scan_body["anomalies_detected"] > 0
    anomaly = scan_body["anomaly_records"][0]
    anomaly_id = anomaly["anomaly_id"]

    listed = client.get("/api/ai-anomaly-center/anomalies?portfolio_id=pf_003")
    detail = client.get(f"/api/ai-anomaly-center/anomalies/{anomaly_id}")
    under_review = client.post(
        f"/api/ai-anomaly-center/anomalies/{anomaly_id}/review",
        json={"action": "mark_under_review", "reviewer": "risk", "note": "Initial review."},
    )
    explained = client.post(
        f"/api/ai-anomaly-center/anomalies/{anomaly_id}/review",
        json={"action": "explain", "reviewer": "risk", "note": "Concentration expected."},
    )
    resolved = client.post(
        f"/api/ai-anomaly-center/anomalies/{anomaly_id}/review",
        json={"action": "resolve", "reviewer": "risk", "decision": "Documented exception."},
    )
    reopened = client.post(
        f"/api/ai-anomaly-center/anomalies/{anomaly_id}/review",
        json={"action": "reopen", "reviewer": "risk"},
    )
    csv_export = client.get("/api/ai-anomaly-center/anomalies/export/csv")
    deleted = client.delete(f"/api/ai-anomaly-center/anomalies/{anomaly_id}")
    missing = client.get(f"/api/ai-anomaly-center/anomalies/{anomaly_id}")

    assert listed.status_code == 200
    assert listed.json()["total_anomalies"] >= 1
    assert detail.status_code == 200
    assert detail.json()["anomaly_id"] == anomaly_id
    assert under_review.status_code == 200
    assert under_review.json()["anomaly"]["status"] == "under_review"
    assert explained.status_code == 200
    assert explained.json()["anomaly"]["status"] == "explained"
    assert resolved.status_code == 200
    assert resolved.json()["anomaly"]["status"] == "resolved"
    assert reopened.status_code == 200
    assert reopened.json()["anomaly"]["status"] == "open"
    assert csv_export.status_code == 200
    assert "anomaly_id" in csv_export.json()["csv"]
    assert deleted.status_code == 200
    assert deleted.json()["deleted"] is True
    assert missing.status_code == 404


def test_ai_anomaly_scan_handles_empty_history_without_crashing() -> None:
    response = client.post(
        "/api/ai-anomaly-center/scan",
        json={
            "portfolio_id": "unknown_portfolio",
            "scan_scope": "market_data",
            "lookback_days": 7,
            "severity_threshold": "low",
            "persist_results": False,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["portfolio_id"] == "unknown_portfolio"
    assert body["warnings"]
    assert body["anomaly_records"]
    assert body["anomaly_records"][0]["anomaly_type"] == "coverage_drop"


def test_ai_anomaly_history_and_demo_endpoints() -> None:
    demo = client.get("/api/ai-anomaly-center/demo")
    history = client.get("/api/ai-anomaly-center/history")

    assert demo.status_code == 200
    assert demo.json()["portfolio_id"] == "pf_004"
    assert history.status_code == 200
    assert history.json()["recent_count"] >= 0


def test_reports_center_includes_and_generates_ai_anomaly_report() -> None:
    templates = client.get("/api/reports-center/templates")
    template_types = {template["report_type"] for template in templates.json()["templates"]}

    generated = client.post(
        "/api/reports-center/generate",
        json={"report_type": "ai_anomaly", "portfolio_id": "pf_003"},
    )

    assert templates.status_code == 200
    assert "ai_anomaly" in template_types
    assert generated.status_code == 200
    body = generated.json()
    assert body["report_type"] == "ai_anomaly"
    assert body["report_id"].startswith("rpt_")
    assert any(section["section_id"] == "top_anomalies" for section in body["sections"])
    assert "AI Anomaly Center" in body["snapshot"]["source_modules"]
