from __future__ import annotations

import csv
import io
from datetime import UTC, date, datetime
from typing import Any
from uuid import uuid4

from fastapi import HTTPException

from app.modules.athena_intelligence.service import AthenaIntelligenceService
from app.modules.pnl_attribution.repository import PnlAttributionRepository
from app.modules.pnl_attribution.schemas import PnlAttributionRequest
from app.modules.pnl_attribution.service import PnlAttributionService
from app.modules.reconciliation.domain.break_classification import (
    apply_review_action,
    overall_status_from_breaks,
    summarize_by_severity,
    summarize_by_type,
)
from app.modules.reconciliation.domain.cash_reconciliation import reconcile_cash
from app.modules.reconciliation.domain.commentary import build_reconciliation_commentary
from app.modules.reconciliation.domain.fx_reconciliation import reconcile_fx
from app.modules.reconciliation.domain.pnl_reconciliation import reconcile_pnl
from app.modules.reconciliation.domain.position_reconciliation import reconcile_positions
from app.modules.reconciliation.domain.price_reconciliation import reconcile_prices
from app.modules.reconciliation.domain.trade_reconciliation import reconcile_trades
from app.modules.reconciliation.repository import ReconciliationRepository
from app.modules.reconciliation.schemas import (
    BreakRegisterResponse,
    ReconciliationBreak,
    ReconciliationCsvExportResponse,
    ReconciliationDeleteResponse,
    ReconciliationHistoryItem,
    ReconciliationHistoryResponse,
    ReconciliationMethodology,
    ReconciliationRequest,
    ReconciliationRunResult,
    ReconciliationStatus,
    ReviewRequest,
)


CHECKS = ["positions", "cash", "prices", "trades", "pnl", "fx"]
SOURCE_MODULES = [
    "Portfolio Builder",
    "Market Data",
    "Trade Simulator",
    "P&L Attribution",
    "Reports Center",
    "Athena Intelligence",
]


class ReconciliationService:
    def __init__(
        self,
        repository: ReconciliationRepository,
        pnl_service: PnlAttributionService | None = None,
        athena_service: AthenaIntelligenceService | None = None,
    ) -> None:
        self.repository = repository
        self.athena_service = athena_service or AthenaIntelligenceService()
        self.pnl_service = pnl_service or PnlAttributionService(
            PnlAttributionRepository(repository.db),
            self.athena_service,
        )

    def get_status(self) -> ReconciliationStatus:
        return ReconciliationStatus(
            detail=(
                "Reconciliation Center compares Athena internal portfolio, market data, "
                "trade and P&L records with deterministic demo custodian reference data."
            ),
            checks_available=CHECKS,
            source_modules=SOURCE_MODULES,
            external_sources=["demo_custodian", "uploaded_file_placeholder", "manual_reference"],
        )

    def run(self, request: ReconciliationRequest) -> ReconciliationRunResult:
        portfolio = self.repository.get_portfolio(request.portfolio_id)
        if portfolio is None:
            raise HTTPException(status_code=404, detail=f"Portfolio '{request.portfolio_id}' not found.")
        raw_positions = self.repository.list_positions(request.portfolio_id)
        if not raw_positions:
            raise HTTPException(status_code=404, detail=f"Portfolio '{request.portfolio_id}' has no positions.")

        run_id = f"recon_{uuid4().hex[:12]}"
        warnings: list[str] = []
        checks = _clean_checks(request.checks)
        internal_positions = self._internal_positions(raw_positions)
        pnl_result = None
        if "pnl" in checks:
            pnl_result = self.pnl_service.analyze(
                PnlAttributionRequest(
                    portfolio_id=request.portfolio_id,
                    end_date=request.reconciliation_date,
                    language=request.language,
                ),
            )
        external, source_warnings = self.repository.build_demo_external_data(
            portfolio=portfolio,
            positions=raw_positions,
            reconciliation_date=request.reconciliation_date,
            source=request.external_source,
            internal_total_pnl=pnl_result.total_pnl if pnl_result else None,
        )
        warnings.extend(source_warnings)

        breaks: list[ReconciliationBreak] = []
        position_rows = []
        cash_rows = []
        price_rows = []
        trade_rows = []
        pnl_rows = []
        fx_rows = []

        if "positions" in checks:
            position_rows, position_breaks = reconcile_positions(
                run_id=run_id,
                portfolio_id=request.portfolio_id,
                internal_positions=internal_positions,
                external_positions=external["positions"],
                tolerance=request.tolerance,
            )
            breaks.extend(position_breaks)
        if "cash" in checks:
            cash_rows, cash_breaks, cash_warnings = reconcile_cash(
                run_id=run_id,
                portfolio_id=request.portfolio_id,
                currency=str(portfolio.get("base_currency") or "USD"),
                internal_cash=float(portfolio.get("cash") or 0.0),
                external_cash=external.get("cash"),
                tolerance=request.tolerance,
            )
            breaks.extend(cash_breaks)
            warnings.extend(cash_warnings)
        if "prices" in checks:
            price_rows, price_breaks, price_warnings = reconcile_prices(
                run_id=run_id,
                portfolio_id=request.portfolio_id,
                internal_prices=self._internal_price_map(raw_positions),
                external_positions=external["positions"],
                tolerance=request.tolerance,
            )
            breaks.extend(price_breaks)
            warnings.extend(price_warnings)
        if "trades" in checks:
            trade_rows, trade_breaks, trade_warnings = reconcile_trades(
                run_id=run_id,
                portfolio_id=request.portfolio_id,
                internal_trades=self._internal_trade_candidates(portfolio),
                external_trades=external.get("pending_trades", []),
            )
            breaks.extend(trade_breaks)
            warnings.extend(trade_warnings)
        if "pnl" in checks:
            pnl_rows, pnl_breaks, pnl_warnings = reconcile_pnl(
                run_id=run_id,
                portfolio_id=request.portfolio_id,
                internal_total_pnl=pnl_result.total_pnl if pnl_result else None,
                external_total_pnl=external.get("total_pnl"),
                starting_value=pnl_result.starting_value if pnl_result else None,
                tolerance=request.tolerance,
            )
            breaks.extend(pnl_breaks)
            warnings.extend(pnl_warnings)
        if "fx" in checks:
            fx_rows, fx_breaks, fx_warnings = reconcile_fx(
                run_id=run_id,
                portfolio_id=request.portfolio_id,
                base_currency=str(portfolio.get("base_currency") or "USD"),
                internal_rates=self._internal_fx_rates(),
                external_rates=external.get("fx_rates", {}),
                external_positions=external.get("positions", []),
            )
            breaks.extend(fx_breaks)
            warnings.extend(fx_warnings)

        limitations = [
            "External reference data is deterministic demo custodian data, not a real broker or custodian feed.",
            "Trade reconciliation uses portfolio transaction history and demo pending trades only.",
            "P&L reconciliation uses P&L Attribution demo calculations and deterministic external value movement.",
        ]
        unresolved_items = [
            item.explanation
            for item in breaks
            if item.status == "open" and item.severity in {"high", "critical"}
        ]
        run = ReconciliationRunResult(
            run_id=run_id,
            portfolio_id=request.portfolio_id,
            portfolio_name=str(portfolio["name"]),
            reconciliation_date=request.reconciliation_date,
            external_source=request.external_source,
            overall_status=overall_status_from_breaks(breaks),
            total_breaks=len(breaks),
            open_breaks=len([item for item in breaks if item.status == "open"]),
            critical_breaks=len([item for item in breaks if item.severity == "critical"]),
            breaks_by_type=summarize_by_type(breaks),
            breaks_by_severity=summarize_by_severity(breaks),
            checks_performed=checks,
            position_breaks=position_rows,
            cash_breaks=cash_rows,
            price_breaks=price_rows,
            trade_breaks=trade_rows,
            pnl_breaks=pnl_rows,
            fx_breaks=fx_rows,
            breaks=breaks,
            unresolved_items=unresolved_items,
            warnings=warnings,
            methodology=ReconciliationMethodology(
                checks_performed=checks,
                tolerances=request.tolerance,
                data_sources=[
                    "Portfolio Builder internal positions and cash",
                    "Market Data latest demo prices",
                    "P&L Attribution calculated P&L",
                    "Demo custodian external reference data",
                ],
                assumptions=[
                    "Position market value equals quantity times price.",
                    "Break severity escalates with tolerance multiple and market value materiality.",
                    "Review workflow state is stored in memory for this demo build.",
                ],
                limitations=limitations,
            ),
            limitations=limitations,
            generated_at=datetime.now(UTC),
        )
        try:
            commentary = build_reconciliation_commentary(
                payload=run.model_dump(mode="json"),
                language=request.language,
                service=self.athena_service,
            )
            run = run.model_copy(update={"athena_ai_commentary": commentary})
        except Exception as exc:  # pragma: no cover - defensive fallback guard
            warnings.append(f"Athena Intelligence commentary unavailable: {exc}")
            run = run.model_copy(update={"warnings": warnings})
        return self.repository.save_run(run)

    def demo(self) -> ReconciliationRunResult:
        return self.run(
            ReconciliationRequest(
                portfolio_id="pf_004",
                external_source="demo_custodian",
            ),
        )

    def list_breaks(self) -> BreakRegisterResponse:
        items = self.repository.list_breaks()
        return BreakRegisterResponse(total_breaks=len(items), items=items)

    def get_break(self, break_id: str) -> ReconciliationBreak:
        item = self.repository.get_break(break_id)
        if item is None:
            raise HTTPException(status_code=404, detail=f"Break '{break_id}' not found.")
        return item

    def review_break(self, break_id: str, request: ReviewRequest) -> ReconciliationBreak:
        item = self.get_break(break_id)
        updated = apply_review_action(item, request)
        return self.repository.save_break(updated)

    def list_history(self) -> ReconciliationHistoryResponse:
        runs = self.repository.list_runs()
        return ReconciliationHistoryResponse(
            total_runs=len(runs),
            items=[
                ReconciliationHistoryItem(
                    run_id=run.run_id,
                    portfolio_id=run.portfolio_id,
                    portfolio_name=run.portfolio_name,
                    reconciliation_date=run.reconciliation_date,
                    external_source=run.external_source,
                    overall_status=run.overall_status,
                    total_breaks=run.total_breaks,
                    critical_breaks=run.critical_breaks,
                    generated_at=run.generated_at,
                )
                for run in runs
            ],
        )

    def get_history_item(self, run_id: str) -> ReconciliationRunResult:
        run = self.repository.get_run(run_id)
        if run is None:
            raise HTTPException(status_code=404, detail=f"Reconciliation run '{run_id}' not found.")
        return run

    def delete_history_item(self, run_id: str) -> ReconciliationDeleteResponse:
        if not self.repository.delete_run(run_id):
            raise HTTPException(status_code=404, detail=f"Reconciliation run '{run_id}' not found.")
        return ReconciliationDeleteResponse(deleted=True, run_id=run_id)

    def export_csv(self, run_id: str) -> ReconciliationCsvExportResponse:
        run = self.get_history_item(run_id)
        output = io.StringIO()
        writer = csv.writer(output)
        _write_table(writer, "Break Register", [item.model_dump(mode="json") for item in run.breaks])
        _write_table(writer, "Position Reconciliation", [item.model_dump(mode="json") for item in run.position_breaks])
        _write_table(writer, "Price Reconciliation", [item.model_dump(mode="json") for item in run.price_breaks])
        return ReconciliationCsvExportResponse(
            run_id=run.run_id,
            csv=output.getvalue(),
            included_tables=["breaks", "position_breaks", "price_breaks"],
        )

    def _internal_positions(self, positions: list[dict[str, Any]]) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for position in positions:
            quantity = float(position.get("quantity") or 0.0)
            symbol = str(position.get("symbol", "")).upper()
            market = self.repository.latest_market_price(symbol)
            price = float(market.get("price") or position.get("current_price") or position.get("average_price") or 0.0)
            rows.append({**position, "market_value": quantity * price, "price": price})
        return rows

    def _internal_trade_candidates(self, portfolio: dict[str, Any]) -> list[dict[str, Any]]:
        trades = portfolio.get("pending_trades") or portfolio.get("trade_blotter") or []
        if trades and isinstance(trades, list):
            return [item for item in trades if isinstance(item, dict)]
        candidates: list[dict[str, Any]] = []
        for item in portfolio.get("transaction_history", []):
            if not isinstance(item, dict):
                continue
            status = str(item.get("status") or item.get("settlement_status") or "").lower()
            source = str(item.get("source_module") or item.get("source") or "").lower()
            if status in {"pending", "simulated", "unsettled"} or source == "trade_simulator":
                candidates.append(item)
        return candidates

    def _internal_price_map(self, positions: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
        prices: dict[str, dict[str, Any]] = {}
        for position in positions:
            symbol = str(position.get("symbol", "")).upper()
            market = self.repository.latest_market_price(symbol)
            prices[symbol] = {
                "price": market.get("price") or float(position.get("current_price") or position.get("average_price") or 0.0),
                "timestamp": market.get("timestamp") or "portfolio_builder_current_price",
            }
        return prices

    def _internal_fx_rates(self) -> dict[str, float]:
        return {"EUR": 1.085, "CAD": 0.733, "GBP": 1.263, "JPY": 0.0068}


def _clean_checks(checks: list[str]) -> list[Any]:
    valid = [check for check in checks if check in CHECKS]
    return valid or list(CHECKS)


def _write_table(writer: Any, title: str, rows: list[dict[str, Any]]) -> None:
    writer.writerow([title])
    if not rows:
        writer.writerow(["No rows"])
        writer.writerow([])
        return
    keys = sorted({key for row in rows for key in row})
    writer.writerow(keys)
    for row in rows:
        writer.writerow([_stringify(row.get(key)) for key in keys])
    writer.writerow([])


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    return str(value).replace("\n", " ")
