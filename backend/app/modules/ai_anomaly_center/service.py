from __future__ import annotations

import csv
import io
from typing import Any
from uuid import uuid4

from fastapi import HTTPException

from app.modules.athena_intelligence.service import AthenaIntelligenceService
from app.modules.ai_anomaly_center.domain.anomaly_rules import (
    apply_review_action,
    count_by,
    filter_by_severity,
    highest_severity,
)
from app.modules.ai_anomaly_center.domain.commentary import build_anomaly_commentary
from app.modules.ai_anomaly_center.domain.limit_anomalies import detect_limit_anomalies
from app.modules.ai_anomaly_center.domain.market_data_anomalies import detect_market_data_anomalies
from app.modules.ai_anomaly_center.domain.pnl_anomalies import detect_pnl_anomalies
from app.modules.ai_anomaly_center.domain.portfolio_anomalies import detect_portfolio_anomalies
from app.modules.ai_anomaly_center.domain.rates_options_anomalies import detect_rates_options_anomalies
from app.modules.ai_anomaly_center.domain.reconciliation_anomalies import detect_reconciliation_anomalies
from app.modules.ai_anomaly_center.domain.risk_anomalies import detect_risk_anomalies
from app.modules.ai_anomaly_center.domain.stress_anomalies import detect_stress_anomalies
from app.modules.ai_anomaly_center.domain.trade_anomalies import detect_trade_anomalies
from app.modules.ai_anomaly_center.repository import AIAnomalyCenterRepository
from app.modules.ai_anomaly_center.schemas import (
    AIAnomalyCenterStatus,
    AnomalyCsvExportResponse,
    AnomalyDeleteResponse,
    AnomalyHistoryResponse,
    AnomalyListResponse,
    AnomalyMethodology,
    AnomalyRecord,
    AnomalyReviewRequest,
    AnomalyReviewResponse,
    AnomalyScanRequest,
    AnomalyScanResponse,
)
from app.modules.risk_monitor.repository import RiskMonitorRepository
from app.modules.risk_monitor.schemas import RiskMonitorAnalyzeRequest
from app.modules.risk_monitor.service import RiskMonitorService


CATEGORIES = [
    "market_data",
    "portfolio",
    "trades",
    "pnl",
    "risk",
    "reconciliation",
    "limits",
    "stress",
    "rates_options",
]
SOURCE_MODULES = [
    "Market Data",
    "Portfolio Builder",
    "Trade Blotter",
    "P&L Attribution",
    "Risk Monitor",
    "Reconciliation Center",
    "Limit Center",
    "Stress Testing",
    "Rates Lab",
    "Options Pricing Lab",
    "Athena Intelligence",
]
LIMITATIONS = [
    "Rule-based monitoring only; this is not production machine learning.",
    "No fraud is asserted or proven by an anomaly.",
    "Signals are based on available demo/persisted Athena records and may be incomplete.",
    "Outputs support risk and operational review and are not investment advice.",
]


class AIAnomalyCenterService:
    def __init__(
        self,
        repository: AIAnomalyCenterRepository,
        athena_service: AthenaIntelligenceService | None = None,
    ) -> None:
        self.repository = repository
        self.athena_service = athena_service or AthenaIntelligenceService()
        self.risk_monitor_service = RiskMonitorService(RiskMonitorRepository(repository.db)) if repository.db else None

    def get_status(self) -> AIAnomalyCenterStatus:
        return AIAnomalyCenterStatus(
            detail=(
                "AI Anomaly Center performs deterministic rule-based monitoring across "
                "Market Data, portfolios, trades, P&L, risk, limits, stress and reconciliation histories."
            ),
            categories=CATEGORIES,  # type: ignore[arg-type]
            source_modules=SOURCE_MODULES,
            limitations=LIMITATIONS,
        )

    def scan(self, request: AnomalyScanRequest) -> AnomalyScanResponse:
        context, warnings = self.repository.load_scan_context(request.portfolio_id, request.lookback_days)
        self._attach_live_risk_context(request.portfolio_id, context, warnings)
        records: list[AnomalyRecord] = []
        scope = request.scan_scope
        if scope in {"all", "market_data"}:
            records.extend(detect_market_data_anomalies(context, request.portfolio_id))
        if scope in {"all", "portfolio"}:
            records.extend(detect_portfolio_anomalies(context, request.portfolio_id))
        if scope in {"all", "trades"}:
            records.extend(detect_trade_anomalies(context, request.portfolio_id))
        if scope in {"all", "pnl"}:
            records.extend(detect_pnl_anomalies(context, request.portfolio_id))
        if scope in {"all", "risk"}:
            records.extend(detect_risk_anomalies(context, request.portfolio_id))
        if scope in {"all", "reconciliation"}:
            records.extend(detect_reconciliation_anomalies(context, request.portfolio_id))
        if scope in {"all", "limits"}:
            records.extend(detect_limit_anomalies(context, request.portfolio_id))
        if scope in {"all", "stress"}:
            records.extend(detect_stress_anomalies(context, request.portfolio_id))
        if scope in {"all", "rates_options"}:
            records.extend(detect_rates_options_anomalies(context, request.portfolio_id))
        records = filter_by_severity(records, request.severity_threshold)
        if request.persist_results:
            self.repository.save_many(records)
        commentary = None
        try:
            commentary = build_anomaly_commentary(
                records=records,
                language=request.language,
                service=self.athena_service,
            )
        except Exception as exc:  # pragma: no cover - defensive guard
            warnings.append(f"Athena Intelligence anomaly commentary unavailable: {exc}")
        return AnomalyScanResponse(
            scan_id=f"anom_scan_{uuid4().hex[:12]}",
            portfolio_id=request.portfolio_id,
            scan_scope=request.scan_scope,
            lookback_days=request.lookback_days,
            total_records_scanned=self._records_scanned(context),
            anomalies_detected=len(records),
            anomalies_by_category=count_by(records, "category"),
            anomalies_by_severity=count_by(records, "severity"),
            highest_severity=highest_severity(records),  # type: ignore[arg-type]
            anomaly_records=records,
            warnings=warnings,
            methodology=self._methodology(),
            limitations=LIMITATIONS,
            athena_ai_commentary=commentary,
        )

    def list_anomalies(
        self,
        *,
        portfolio_id: str | None = None,
        severity: str | None = None,
        module_name: str | None = None,
        status: str | None = None,
    ) -> AnomalyListResponse:
        records = self.repository.list_anomalies(
            portfolio_id=portfolio_id,
            severity=severity,
            module_name=module_name,
            status=status,
        )
        return AnomalyListResponse(total_anomalies=len(records), items=records)

    def get_anomaly(self, anomaly_id: str) -> AnomalyRecord:
        anomaly = self.repository.get(anomaly_id)
        if anomaly is None:
            raise HTTPException(status_code=404, detail=f"Anomaly '{anomaly_id}' not found.")
        return anomaly

    def review_anomaly(self, anomaly_id: str, request: AnomalyReviewRequest) -> AnomalyReviewResponse:
        anomaly = self.get_anomaly(anomaly_id)
        try:
            updated, event = apply_review_action(anomaly, request)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        return AnomalyReviewResponse(anomaly=self.repository.save(updated), event=event)

    def delete_anomaly(self, anomaly_id: str) -> AnomalyDeleteResponse:
        if not self.repository.delete(anomaly_id):
            raise HTTPException(status_code=404, detail=f"Anomaly '{anomaly_id}' not found.")
        return AnomalyDeleteResponse(deleted=True, anomaly_id=anomaly_id)

    def history(self) -> AnomalyHistoryResponse:
        records = self.repository.recent()
        return AnomalyHistoryResponse(recent_count=len(records), items=records)

    def demo(self) -> AnomalyScanResponse:
        return self.scan(
            AnomalyScanRequest(
                portfolio_id="pf_004",
                scan_scope="all",
                lookback_days=60,
                severity_threshold="low",
                persist_results=True,
            ),
        )

    def export_csv(self) -> AnomalyCsvExportResponse:
        records = self.repository.list_anomalies()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(
            [
                "anomaly_id",
                "portfolio_id",
                "category",
                "source_module",
                "title",
                "severity",
                "score",
                "status",
                "detected_at",
                "suggested_action",
            ],
        )
        for record in records:
            writer.writerow(
                [
                    record.anomaly_id,
                    record.portfolio_id or "",
                    record.category,
                    record.source_module,
                    record.title,
                    record.severity,
                    record.anomaly_score,
                    record.status,
                    record.detected_at.isoformat(),
                    record.suggested_action,
                ],
            )
        return AnomalyCsvExportResponse(csv=output.getvalue(), included_tables=["anomaly_register"])

    def _attach_live_risk_context(
        self,
        portfolio_id: str | None,
        context: dict[str, Any],
        warnings: list[str],
    ) -> None:
        if not portfolio_id or self.risk_monitor_service is None:
            return
        try:
            portfolio = context.get("portfolio") or {}
            benchmark = str(portfolio.get("benchmark") or "SPY")
            context["risk_monitor"] = self.risk_monitor_service.analyze(
                RiskMonitorAnalyzeRequest(
                    portfolio_id=portfolio_id,
                    benchmark_symbol=benchmark,
                ),
            ).model_dump(mode="json")
        except Exception as exc:
            warnings.append(f"Risk Monitor live scan unavailable: {exc}")

    def _records_scanned(self, context: dict[str, Any]) -> int:
        return sum(
            [
                len(context.get("positions") or []),
                sum(len(rows) for rows in (context.get("prices") or {}).values()),
                len(context.get("trade_blotter") or []),
                len(context.get("pnl_history") or []),
                len(context.get("reconciliation_breaks") or []),
                len(context.get("limit_breaches") or []),
                len(context.get("stress_runs") or []),
                1 if context.get("risk_monitor") else 0,
            ],
        )

    def _methodology(self) -> AnomalyMethodology:
        return AnomalyMethodology(
            detection_mode="deterministic rule-based monitoring",
            score_mapping={
                "0-25": "low",
                "26-50": "medium",
                "51-75": "high",
                "76-100": "critical",
            },
            factors=[
                "magnitude of deviation",
                "portfolio impact",
                "recurrence",
                "source module confidence",
                "data quality",
                "unresolved status",
                "critical rule flag",
            ],
            data_sources=SOURCE_MODULES,
            limitations=LIMITATIONS,
        )
