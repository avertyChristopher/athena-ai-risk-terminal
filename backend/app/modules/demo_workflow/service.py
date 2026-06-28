from __future__ import annotations

from typing import Any, Callable
from uuid import uuid4

from sqlalchemy.orm import Session

from app.modules.ai_anomaly_center.repository import AIAnomalyCenterRepository
from app.modules.ai_anomaly_center.schemas import AnomalyScanRequest
from app.modules.ai_anomaly_center.service import AIAnomalyCenterService
from app.modules.athena_intelligence.service import AthenaIntelligenceService
from app.modules.demo_workflow.domain.demo_orchestration import (
    ACTIVE_MODULE_COUNT,
    DEMO_LIMITATIONS,
    dump_payload,
    persistence_map,
    records_count,
)
from app.modules.demo_workflow.repository import DemoWorkflowRepository
from app.modules.demo_workflow.schemas import (
    DemoModuleRun,
    DemoRunHistoryResponse,
    DemoRunRequest,
    DemoRunSummary,
    DemoWorkflowStatus,
)
from app.modules.limit_center.repository import LimitCenterRepository
from app.modules.limit_center.schemas import LimitEvaluationRequest
from app.modules.limit_center.service import LimitCenterService
from app.modules.market_data.repository import MarketDataRepository
from app.modules.market_data.service import MarketDataService
from app.modules.pnl_attribution.repository import PnlAttributionRepository
from app.modules.pnl_attribution.schemas import PnlAttributionRequest
from app.modules.pnl_attribution.service import PnlAttributionService
from app.modules.portfolio_builder.repository import PortfolioRepository, PositionRepository
from app.modules.portfolio_builder.service import PortfolioService, PositionService
from app.modules.reconciliation.repository import ReconciliationRepository
from app.modules.reconciliation.schemas import ReconciliationRequest
from app.modules.reconciliation.service import ReconciliationService
from app.modules.reports_center.repository import ReportsCenterRepository
from app.modules.reports_center.schemas import ReportGenerateRequest
from app.modules.reports_center.service import ReportsCenterService
from app.modules.risk_monitor.repository import RiskMonitorRepository
from app.modules.risk_monitor.schemas import RiskMonitorAnalyzeRequest
from app.modules.risk_monitor.service import RiskMonitorService


class DemoWorkflowService:
    def __init__(
        self,
        repository: DemoWorkflowRepository,
        db: Session,
    ) -> None:
        self.repository = repository
        self.db = db
        self.athena_service = AthenaIntelligenceService()
        self.portfolio_service = PortfolioService(PortfolioRepository(db), PositionRepository(db))
        self.position_service = PositionService(PositionRepository(db), PortfolioRepository(db))
        self.market_data_service = MarketDataService(MarketDataRepository(db))
        self.risk_monitor_service = RiskMonitorService(RiskMonitorRepository(db))
        self.pnl_service = PnlAttributionService(PnlAttributionRepository(db), self.athena_service)
        self.reconciliation_service = ReconciliationService(
            ReconciliationRepository(db),
            self.pnl_service,
            self.athena_service,
        )
        self.limit_service = LimitCenterService(LimitCenterRepository(db))
        self.ai_anomaly_service = AIAnomalyCenterService(
            AIAnomalyCenterRepository(db),
            self.athena_service,
        )
        self.reports_service = ReportsCenterService(ReportsCenterRepository(db), db)

    def get_status(self) -> DemoWorkflowStatus:
        return DemoWorkflowStatus(
            detail="Runs the recruiter-ready Athena demo workflow across existing modules.",
            database_connected=self.db is not None,
            persistence=persistence_map(),
            endpoints=["GET /api/demo/status", "POST /api/demo/run-athena-demo", "GET /api/demo/history"],
            limitations=DEMO_LIMITATIONS,
        )

    def list_runs(self) -> DemoRunHistoryResponse:
        runs = self.repository.list_runs()
        return DemoRunHistoryResponse(total_runs=len(runs), items=runs)

    def run_athena_demo(self, request: DemoRunRequest) -> DemoRunSummary:
        warnings: list[str] = []
        module_results: list[DemoModuleRun] = []
        records_created: dict[str, int] = {}
        payloads: dict[str, Any] = {}
        portfolio_name: str | None = None
        symbols: list[str] = []
        benchmark_symbol = "SPY"

        portfolio = self._safe_step(
            "Portfolio Builder",
            warnings,
            module_results,
            records_created,
            lambda: self.portfolio_service.get_portfolio(request.portfolio_id),
            records_key="portfolio",
        )
        if isinstance(portfolio, dict):
            payloads["portfolio"] = portfolio
            portfolio_name = str(portfolio.get("name") or request.portfolio_id)
            benchmark_symbol = str(portfolio.get("benchmark") or benchmark_symbol)

        positions = self._safe_step(
            "Portfolio Positions",
            warnings,
            module_results,
            records_created,
            lambda: self.position_service.list_positions(request.portfolio_id),
            records_key="positions",
            record_counter=lambda value: len((value or {}).get("items", [])) if isinstance(value, dict) else 0,
        )
        if isinstance(positions, dict):
            payloads["holdings"] = positions.get("items", [])
            symbols = [str(item.get("symbol")) for item in payloads["holdings"] if item.get("symbol")]

        portfolio_summary = self._safe_step(
            "Portfolio Summary",
            warnings,
            module_results,
            records_created,
            lambda: self.portfolio_service.get_summary(request.portfolio_id),
            records_key="portfolio_summary",
        )
        if portfolio_summary is not None:
            payloads["portfolio_summary"] = dump_payload(portfolio_summary)

        market_coverage = self._safe_step(
            "Market Data",
            warnings,
            module_results,
            records_created,
            lambda: self.market_data_service.get_portfolio_coverage(symbols),
            records_key="market_data_coverage",
        )
        if market_coverage is not None:
            payloads["market_data_coverage"] = dump_payload(market_coverage)

        risk = self._safe_step(
            "Risk Monitor",
            warnings,
            module_results,
            records_created,
            lambda: self.risk_monitor_service.analyze(
                RiskMonitorAnalyzeRequest(
                    portfolio_id=request.portfolio_id,
                    benchmark_symbol=benchmark_symbol,
                ),
            ),
            records_key="risk_monitor",
        )
        risk_payload = dump_payload(risk)
        if risk is not None:
            payloads["risk_monitor"] = risk_payload

        pnl = self._safe_step(
            "P&L Attribution",
            warnings,
            module_results,
            records_created,
            lambda: self.pnl_service.analyze(
                PnlAttributionRequest(
                    portfolio_id=request.portfolio_id,
                    benchmark_symbol=benchmark_symbol,
                    attribution_method="contribution",
                    language=request.language,
                ),
            ),
            records_key="pnl_attribution",
        )
        if pnl is not None:
            payloads["pnl_attribution"] = dump_payload(pnl)

        reconciliation = self._safe_step(
            "Reconciliation Center",
            warnings,
            module_results,
            records_created,
            lambda: self.reconciliation_service.run(
                ReconciliationRequest(
                    portfolio_id=request.portfolio_id,
                    language=request.language,
                ),
            ),
            records_key="reconciliation",
            record_counter=lambda value: int((dump_payload(value) or {}).get("total_breaks") or 0),
        )
        if reconciliation is not None:
            payloads["reconciliation"] = dump_payload(reconciliation)

        limits = self._safe_step(
            "Limit Center",
            warnings,
            module_results,
            records_created,
            lambda: self.limit_service.evaluate(
                LimitEvaluationRequest(
                    portfolio_id=request.portfolio_id,
                    source_module="risk_monitor",
                    payload=risk_payload if isinstance(risk_payload, dict) else {},
                    language=request.language,
                ),
            ),
            records_key="limit_breaches",
            record_counter=lambda value: len((dump_payload(value) or {}).get("breaches") or []),
        )
        if limits is not None:
            payloads["limit_center"] = dump_payload(limits)

        anomalies = self._safe_step(
            "AI Anomaly Center",
            warnings,
            module_results,
            records_created,
            lambda: self.ai_anomaly_service.scan(
                AnomalyScanRequest(
                    portfolio_id=request.portfolio_id,
                    scan_scope="all",
                    lookback_days=60,
                    severity_threshold="low",
                    persist_results=True,
                    language=request.language,
                ),
            ),
            records_key="anomalies",
            record_counter=lambda value: int((dump_payload(value) or {}).get("anomalies_detected") or 0),
        )
        if anomalies is not None:
            payloads["ai_anomaly"] = dump_payload(anomalies)

        report = None
        if request.include_report:
            report = self._safe_step(
                "Reports Center",
                warnings,
                module_results,
                records_created,
                lambda: self.reports_service.generate_report(
                    ReportGenerateRequest(
                        report_type="full_portfolio_risk_pack",
                        portfolio_id=request.portfolio_id,
                        language=request.language,
                        style="executive",
                        source_payloads=payloads,
                    ),
                ),
                records_key="reports",
            )

        summary = DemoRunSummary(
            demo_run_id=f"demo_{uuid4().hex[:12]}",
            portfolio_id=request.portfolio_id,
            portfolio_name=portfolio_name,
            modules_run=[item.module for item in module_results if item.status in {"completed", "warning"}],
            module_results=module_results,
            records_created=records_created,
            warnings=warnings,
            generated_report_id=_get_value(report, "report_id"),
            highest_risk_status=_get_value(risk, "global_risk_status"),
            open_breaks=_get_int(reconciliation, "open_breaks"),
            limit_breaches=_get_int(limits, "summary", "breach_count") or _get_int(limits, "breaches"),
            anomalies_detected=_get_int(anomalies, "anomalies_detected"),
            total_pnl=_get_float(pnl, "total_pnl"),
            risk_score=_get_int(risk, "global_risk_score"),
            quick_links={
                "portfolio": "/portfolio-builder",
                "risk_monitor": "/risk-monitor",
                "pnl_attribution": "/pnl-attribution",
                "reconciliation": "/reconciliation",
                "limit_center": "/limit-center",
                "ai_anomaly_center": "/ai-anomaly-center",
                "reports_center": "/reports-center",
            },
            persistence=persistence_map(),
        )
        return self.repository.save(summary)

    def _safe_step(
        self,
        module: str,
        warnings: list[str],
        module_results: list[DemoModuleRun],
        records_created: dict[str, int],
        operation: Callable[[], Any],
        *,
        records_key: str,
        record_counter: Callable[[Any], int] | None = None,
    ) -> Any:
        try:
            output = operation()
            count = record_counter(output) if record_counter else records_count(output)
            records_created[records_key] = count
            module_results.append(
                DemoModuleRun(
                    module=module,
                    status="completed",
                    detail="Completed successfully.",
                    records_created=count,
                    output_id=_first_identifier(output),
                ),
            )
            return output
        except Exception as exc:  # pragma: no cover - exercised through service-level fallback tests
            message = f"{module} unavailable during demo run: {exc}"
            warnings.append(message)
            records_created[records_key] = 0
            module_results.append(
                DemoModuleRun(
                    module=module,
                    status="failed",
                    detail=message,
                    records_created=0,
                ),
            )
            return None


def _first_identifier(value: Any) -> str | None:
    payload = dump_payload(value)
    if not isinstance(payload, dict):
        return None
    for key in ("analysis_id", "run_id", "report_id", "scan_id"):
        if payload.get(key):
            return str(payload[key])
    return None


def _get_value(value: Any, *keys: str) -> str | None:
    payload = dump_payload(value)
    if not isinstance(payload, dict):
        return None
    current: Any = payload
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return str(current) if current is not None else None


def _get_int(value: Any, *keys: str) -> int | None:
    raw = _get_value(value, *keys)
    if raw is None and len(keys) == 1:
        payload = dump_payload(value)
        if isinstance(payload, dict) and isinstance(payload.get(keys[0]), list):
            return len(payload[keys[0]])
    try:
        return int(float(raw)) if raw is not None else None
    except ValueError:
        return None


def _get_float(value: Any, *keys: str) -> float | None:
    raw = _get_value(value, *keys)
    try:
        return float(raw) if raw is not None else None
    except ValueError:
        return None
