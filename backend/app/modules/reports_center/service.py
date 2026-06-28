from __future__ import annotations

from typing import Any

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.modules.ai_anomaly_center.repository import AIAnomalyCenterRepository
from app.modules.ai_anomaly_center.schemas import AnomalyScanRequest
from app.modules.ai_anomaly_center.service import AIAnomalyCenterService
from app.modules.athena_intelligence.service import AthenaIntelligenceService
from app.modules.limit_center.repository import LimitCenterRepository
from app.modules.limit_center.schemas import LimitEvaluationRequest
from app.modules.limit_center.service import LimitCenterService
from app.modules.market_data.repository import MarketDataRepository
from app.modules.market_data.service import MarketDataService
from app.modules.options_pricing_lab.repository import OptionsPricingLabRepository
from app.modules.options_pricing_lab.schemas import OptionPricingRequest
from app.modules.options_pricing_lab.service import OptionsPricingLabService
from app.modules.pnl_attribution.repository import PnlAttributionRepository
from app.modules.pnl_attribution.schemas import PnlAttributionRequest
from app.modules.pnl_attribution.service import PnlAttributionService
from app.modules.portfolio_builder.repository import PortfolioRepository, PositionRepository
from app.modules.portfolio_builder.service import PortfolioService, PositionService
from app.modules.rates_lab.repository import RatesLabRepository
from app.modules.rates_lab.schemas import PortfolioRatesExposureRequest
from app.modules.rates_lab.service import RatesLabService
from app.modules.reconciliation.repository import ReconciliationRepository
from app.modules.reconciliation.schemas import ReconciliationRequest
from app.modules.reconciliation.service import ReconciliationService
from app.modules.reports_center.domain.commentary import build_report_commentary
from app.modules.reports_center.domain.export_formatters import (
    report_to_csv,
    report_to_json,
    report_to_markdown,
)
from app.modules.reports_center.domain.report_builder import build_report
from app.modules.reports_center.domain.report_templates import (
    PDF_ROADMAP_NOTE,
    list_report_templates,
)
from app.modules.reports_center.repository import ReportsCenterRepository
from app.modules.reports_center.schemas import (
    CsvExportResponse,
    GeneratedReport,
    MarkdownExportResponse,
    ReportDeleteResponse,
    ReportGenerateRequest,
    ReportLibraryResponse,
    ReportListItem,
    ReportTemplateListResponse,
    ReportsCenterStatus,
)
from app.modules.risk_monitor.repository import RiskMonitorRepository
from app.modules.risk_monitor.schemas import RiskMonitorAnalyzeRequest
from app.modules.risk_monitor.service import RiskMonitorService
from app.modules.stress_testing.repository import StressTestingRepository
from app.modules.stress_testing.schemas import StressTestingRunRequest
from app.modules.stress_testing.service import StressTestingService
from app.modules.trade_simulator.repository import TradeSimulatorRepository
from app.modules.trade_simulator.schemas import TradeSimulationRequest
from app.modules.trade_simulator.service import TradeSimulatorService
from app.modules.volatility_lab.repository import VolatilityLabRepository
from app.modules.volatility_lab.schemas import VolatilityPortfolioAnalysisRequest
from app.modules.volatility_lab.service import VolatilityLabService


SOURCE_MODULES = [
    "Portfolio Builder",
    "Market Data",
    "Risk Monitor",
    "Volatility Lab",
    "Rates Lab",
    "Options Pricing Lab",
    "P&L Attribution",
    "Reconciliation Center",
    "Stress Testing",
    "Limit Center",
    "Trade Simulator",
    "AI Anomaly Center",
    "Athena Intelligence",
]


class ReportsCenterService:
    def __init__(
        self,
        repository: ReportsCenterRepository,
        db: Session,
    ) -> None:
        self.repository = repository
        self.db = db
        self.portfolio_service = PortfolioService(
            PortfolioRepository(db),
            PositionRepository(db),
        )
        self.position_service = PositionService(
            PositionRepository(db),
            PortfolioRepository(db),
        )
        self.market_data_service = MarketDataService(MarketDataRepository(db))
        self.risk_monitor_service = RiskMonitorService(RiskMonitorRepository(db))
        self.volatility_service = VolatilityLabService(VolatilityLabRepository(db))
        self.rates_service = RatesLabService(RatesLabRepository(db))
        self.stress_service = StressTestingService(StressTestingRepository(db))
        self.limit_service = LimitCenterService(LimitCenterRepository())
        self.trade_service = TradeSimulatorService(TradeSimulatorRepository(db))
        self.options_service = OptionsPricingLabService(OptionsPricingLabRepository(db))
        self.athena_service = AthenaIntelligenceService()
        self.ai_anomaly_service = AIAnomalyCenterService(
            AIAnomalyCenterRepository(db),
            self.athena_service,
        )
        self.pnl_service = PnlAttributionService(PnlAttributionRepository(db), self.athena_service)
        self.reconciliation_service = ReconciliationService(
            ReconciliationRepository(db),
            self.pnl_service,
            self.athena_service,
        )

    def get_status(self) -> ReportsCenterStatus:
        templates = list_report_templates()
        return ReportsCenterStatus(
            detail=(
            "Reports Center generates snapshot-based portfolio, P&L, risk, stress, "
                "limits, reconciliation, trade, anomaly, rates and options reports from Athena analytics."
            ),
            templates_available=len(templates),
            export_formats=["json", "markdown", "csv"],
            source_modules=SOURCE_MODULES,
            pdf_roadmap_note=PDF_ROADMAP_NOTE,
        )

    def list_templates(self) -> ReportTemplateListResponse:
        return ReportTemplateListResponse(templates=list_report_templates())

    def generate_report(self, request: ReportGenerateRequest) -> GeneratedReport:
        warnings: list[str] = []
        limitations = [
            PDF_ROADMAP_NOTE,
            "Reports are snapshot-based and do not continuously update after generation.",
        ]
        payloads = dict(request.source_payloads)
        portfolio_id = request.portfolio_id
        portfolio_name: str | None = None

        if portfolio_id:
            portfolio_payloads = self._collect_portfolio_payloads(portfolio_id, warnings)
            payloads = {**portfolio_payloads, **payloads}
            portfolio = payloads.get("portfolio") or {}
            portfolio_name = portfolio.get("name") or (payloads.get("portfolio_summary") or {}).get("name")
        elif not payloads:
            warnings.append("No portfolio_id or source_payloads were supplied; report generated with limited sections.")

        self._collect_report_specific_payloads(
            request.report_type,
            portfolio_id,
            payloads,
            warnings,
        )

        athena_commentary = None
        if request.include_athena_commentary:
            try:
                athena_commentary = build_report_commentary(
                    report_type=request.report_type,
                    portfolio_id=portfolio_id,
                    language=request.language,
                    style=request.style,
                    payloads=payloads,
                    service=self.athena_service,
                )
                payloads["athena_commentary"] = athena_commentary
            except Exception as exc:  # pragma: no cover - defensive fallback guard
                warnings.append(f"Athena Intelligence commentary unavailable: {exc}")

        if not request.include_limitations:
            limitations = []
        if not request.include_methodology:
            warnings.append("Methodology details were omitted by request.")

        report = build_report(
            report_type=request.report_type,
            portfolio_id=portfolio_id,
            portfolio_name=portfolio_name,
            language=request.language,
            style=request.style,
            payloads=payloads,
            warnings=warnings,
            limitations=limitations,
            athena_commentary=athena_commentary,
        )
        return self.repository.save_report(report)

    def list_reports(self) -> ReportLibraryResponse:
        reports = self.repository.list_reports()
        return ReportLibraryResponse(
            total_reports=len(reports),
            items=[
                ReportListItem(
                    report_id=report.report_id,
                    report_type=report.report_type,
                    title=report.title,
                    portfolio_id=report.portfolio_id,
                    portfolio_name=report.portfolio_name,
                    generated_at=report.generated_at,
                    language=report.language,
                    status=report.status,
                    warnings_count=len(report.warnings),
                    source_modules=report.snapshot.source_modules,
                )
                for report in reports
            ],
        )

    def get_report(self, report_id: str) -> GeneratedReport:
        report = self.repository.get_report(report_id)
        if report is None:
            raise HTTPException(status_code=404, detail=f"Report '{report_id}' not found.")
        return report

    def delete_report(self, report_id: str) -> ReportDeleteResponse:
        deleted = self.repository.delete_report(report_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Report '{report_id}' not found.")
        return ReportDeleteResponse(deleted=True, report_id=report_id)

    def export_json(self, report_id: str) -> dict[str, Any]:
        return report_to_json(self.get_report(report_id))

    def export_markdown(self, report_id: str) -> MarkdownExportResponse:
        report = self.get_report(report_id)
        return MarkdownExportResponse(
            report_id=report.report_id,
            markdown=report_to_markdown(report),
        )

    def export_csv(self, report_id: str) -> CsvExportResponse:
        report = self.get_report(report_id)
        content, included_tables = report_to_csv(report)
        return CsvExportResponse(
            report_id=report.report_id,
            csv=content,
            included_tables=included_tables,
        )

    def demo(self) -> GeneratedReport:
        return self.generate_report(
            ReportGenerateRequest(
                report_type="full_portfolio_risk_pack",
                portfolio_id="pf_004",
                style="executive",
            ),
        )

    def _collect_portfolio_payloads(
        self,
        portfolio_id: str,
        warnings: list[str],
    ) -> dict[str, Any]:
        payloads: dict[str, Any] = {}
        payloads["portfolio"] = self._safe_call(
            "Portfolio profile",
            warnings,
            lambda: self.portfolio_service.get_portfolio(portfolio_id),
        )
        payloads["portfolio_summary"] = self._safe_call(
            "Portfolio summary",
            warnings,
            lambda: self.portfolio_service.get_summary(portfolio_id),
        )
        positions = self._safe_call(
            "Portfolio holdings",
            warnings,
            lambda: self.position_service.list_positions(portfolio_id),
        )
        if isinstance(positions, dict):
            payloads["holdings"] = positions.get("items", [])
        payloads["allocations"] = {
            "sectors": self._allocation(portfolio_id, "sectors", warnings),
            "assets": self._allocation(portfolio_id, "assets", warnings),
            "currencies": self._allocation(portfolio_id, "currencies", warnings),
            "countries": self._allocation(portfolio_id, "countries", warnings),
            "asset_types": self._allocation(portfolio_id, "asset-types", warnings),
        }
        payloads["concentration"] = self._safe_call(
            "Concentration analysis",
            warnings,
            lambda: self.portfolio_service.get_concentration(portfolio_id),
        )
        symbols = [item.get("symbol") for item in payloads.get("holdings", []) if item.get("symbol")]
        if symbols:
            payloads["market_data_coverage"] = self._safe_call(
                "Market Data coverage",
                warnings,
                lambda: self.market_data_service.get_portfolio_coverage(symbols),
            )
        return payloads

    def _collect_report_specific_payloads(
        self,
        report_type: str,
        portfolio_id: str | None,
        payloads: dict[str, Any],
        warnings: list[str],
    ) -> None:
        if not portfolio_id:
            return
        benchmark = (payloads.get("portfolio") or {}).get("benchmark") or "SPY"
        needs_risk = report_type in {
            "risk_monitor",
            "limit_breach",
            "full_portfolio_risk_pack",
        }
        needs_volatility = report_type in {"risk_monitor", "full_portfolio_risk_pack"}
        needs_rates = report_type in {"fixed_income_exposure", "full_portfolio_risk_pack"}
        needs_stress = report_type in {"stress_testing", "full_portfolio_risk_pack"}
        needs_options = report_type in {"options_risk", "full_portfolio_risk_pack"}
        needs_trade = report_type in {"trade_suitability"}
        needs_pnl = report_type in {"pnl_attribution"}
        needs_reconciliation = report_type in {"reconciliation"}
        needs_ai_anomaly = report_type in {"ai_anomaly"}

        if needs_risk and "risk_monitor" not in payloads:
            payloads["risk_monitor"] = self._safe_call(
                "Risk Monitor",
                warnings,
                lambda: self.risk_monitor_service.analyze(
                    RiskMonitorAnalyzeRequest(
                        portfolio_id=portfolio_id,
                        benchmark_symbol=str(benchmark),
                    ),
                ),
            )
        if needs_volatility and "volatility" not in payloads:
            payloads["volatility"] = self._safe_call(
                "Volatility Lab",
                warnings,
                lambda: self.volatility_service.analyze_portfolio(
                    VolatilityPortfolioAnalysisRequest(
                        portfolio_id=portfolio_id,
                        benchmark_symbol=str(benchmark),
                        rolling_window=5,
                    ),
                ),
            )
        if needs_rates and "rates" not in payloads:
            payloads["rates"] = self._safe_call(
                "Rates Lab",
                warnings,
                lambda: self.rates_service.analyze_portfolio_exposure(
                    PortfolioRatesExposureRequest(portfolio_id=portfolio_id, shock_bps=100),
                ),
            )
        if needs_stress and "stress_testing" not in payloads:
            payloads["stress_testing"] = self._safe_call(
                "Stress Testing",
                warnings,
                lambda: self.stress_service.run(
                    StressTestingRunRequest(
                        portfolio_id=portfolio_id,
                        scenario_id="risk_off_combined",
                        benchmark_symbol=str(benchmark),
                    ),
                ),
            )
        if needs_options and "options" not in payloads:
            payloads["options"] = self._safe_call(
                "Options Pricing Lab",
                warnings,
                lambda: self.options_service.price_option(
                    OptionPricingRequest(underlying_symbol="AAPL"),
                ),
            )
        if needs_trade and "trade_simulator" not in payloads:
            payloads["trade_simulator"] = self._safe_call(
                "Trade Simulator",
                warnings,
                lambda: self.trade_service.simulate_trade(
                    TradeSimulationRequest(
                        portfolio_id=portfolio_id,
                        action="BUY",
                        symbol="AAPL",
                        asset_name="Apple Inc.",
                        asset_type="equity",
                        quantity=5,
                        estimated_price=200,
                        trade_rationale="Rebalancing",
                    ),
                ),
            )
        if needs_pnl and "pnl_attribution" not in payloads:
            payloads["pnl_attribution"] = self._safe_call(
                "P&L Attribution",
                warnings,
                lambda: self.pnl_service.analyze(
                    PnlAttributionRequest(
                        portfolio_id=portfolio_id,
                        benchmark_symbol=str(benchmark),
                        attribution_method="Brinson-lite",
                    ),
                ),
            )
        if needs_reconciliation and "reconciliation" not in payloads:
            payloads["reconciliation"] = self._safe_call(
                "Reconciliation Center",
                warnings,
                lambda: self.reconciliation_service.run(
                    ReconciliationRequest(
                        portfolio_id=portfolio_id,
                        language="en",
                    ),
                ),
            )
        if needs_ai_anomaly and "ai_anomaly" not in payloads:
            payloads["ai_anomaly"] = self._safe_call(
                "AI Anomaly Center",
                warnings,
                lambda: self.ai_anomaly_service.scan(
                    AnomalyScanRequest(
                        portfolio_id=portfolio_id,
                        scan_scope="all",
                        lookback_days=60,
                        severity_threshold="low",
                        persist_results=True,
                    ),
                ),
            )
        if report_type in {"limit_breach", "full_portfolio_risk_pack"} and "limit_center" not in payloads:
            source_payload = payloads.get("risk_monitor") or {}
            payloads["limit_center"] = self._safe_call(
                "Limit Center",
                warnings,
                lambda: self.limit_service.evaluate(
                    LimitEvaluationRequest(
                        portfolio_id=portfolio_id,
                        source_module="risk_monitor",
                        payload=source_payload,
                    ),
                ),
            )

    def _allocation(
        self,
        portfolio_id: str,
        allocation_type: str,
        warnings: list[str],
    ) -> list[dict[str, Any]]:
        allocation = self._safe_call(
            f"{allocation_type} allocation",
            warnings,
            lambda: self.portfolio_service.get_allocation(portfolio_id, allocation_type),
        )
        if isinstance(allocation, dict):
            return allocation.get("items", [])
        return []

    def _safe_call(
        self,
        label: str,
        warnings: list[str],
        operation: Any,
    ) -> Any:
        try:
            return self._dump(operation())
        except Exception as exc:
            warnings.append(f"{label} unavailable: {exc}")
            return None

    def _dump(self, value: Any) -> Any:
        if isinstance(value, BaseModel):
            return value.model_dump(mode="json")
        if isinstance(value, list):
            return [self._dump(item) for item in value]
        if isinstance(value, dict):
            return {key: self._dump(item) for key, item in value.items()}
        return value
