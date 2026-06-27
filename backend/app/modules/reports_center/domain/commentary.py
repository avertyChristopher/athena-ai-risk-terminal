from __future__ import annotations

from typing import Any

from app.modules.athena_intelligence.schemas import (
    AthenaIntelligenceRequest,
    AthenaRiskSynthesisPayloads,
    AthenaRiskSynthesisRequest,
)
from app.modules.athena_intelligence.service import AthenaIntelligenceService
from app.modules.reports_center.schemas import ReportType


def build_report_commentary(
    *,
    report_type: ReportType,
    portfolio_id: str | None,
    language: str,
    style: str,
    payloads: dict[str, Any],
    service: AthenaIntelligenceService,
) -> dict[str, Any]:
    if report_type == "full_portfolio_risk_pack":
        synthesis = service.generate_risk_synthesis(
            AthenaRiskSynthesisRequest(
                portfolio_id=portfolio_id or "portfolio",
                language=language,
                style=style if style in {"professional", "executive", "educational"} else "executive",
                payloads=AthenaRiskSynthesisPayloads(
                    portfolio_payload=payloads.get("portfolio_summary"),
                    market_data_payload=payloads.get("market_data_coverage"),
                    risk_analytics_payload=payloads.get("risk_monitor"),
                    rates_risk_payload=(payloads.get("rates") or {}).get("rates_risk_payload"),
                    options_risk_payload=(payloads.get("options") or {}).get("risk_payload"),
                    trade_impact_payload=(payloads.get("trade_simulator") or {}).get("trade_impact_payload"),
                ),
            ),
        )
        return synthesis.model_dump(mode="json")

    module_name, analysis_mode, payload = _commentary_target(report_type, payloads)
    commentary = service.generate_commentary(
        AthenaIntelligenceRequest(
            module_name=module_name,
            analysis_mode=analysis_mode,
            language=language,
            style=style,
            payload=payload,
        ),
    )
    return commentary.model_dump(mode="json")


def _commentary_target(report_type: ReportType, payloads: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
    if report_type == "risk_monitor":
        return "risk_monitor", "risk", payloads.get("risk_monitor") or {}
    if report_type == "stress_testing":
        return "risk_monitor", "risk", payloads.get("stress_testing") or {}
    if report_type == "limit_breach":
        return "limit_center", "limit", payloads.get("limit_center") or {}
    if report_type == "trade_suitability":
        return "trade_simulator", "trade", payloads.get("trade_simulator") or {}
    if report_type == "fixed_income_exposure":
        return "rates_lab", "rates", payloads.get("rates") or {}
    if report_type == "options_risk":
        return "options_pricing_lab", "options", payloads.get("options") or {}
    return "portfolio_builder", "portfolio", {
        "portfolio": payloads.get("portfolio"),
        "summary": payloads.get("portfolio_summary"),
        "concentration": payloads.get("concentration"),
        "market_data": payloads.get("market_data_coverage"),
    }
