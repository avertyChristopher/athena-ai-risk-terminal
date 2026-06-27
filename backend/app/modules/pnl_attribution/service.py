from __future__ import annotations

import csv
import io
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from fastapi import HTTPException

from app.modules.athena_intelligence.service import AthenaIntelligenceService
from app.modules.pnl_attribution.domain.attribution import (
    build_benchmark_comparison,
    build_position_contributions,
    finalize_contributions,
    portfolio_totals,
)
from app.modules.pnl_attribution.domain.commentary import build_pnl_commentary
from app.modules.pnl_attribution.domain.contribution import aggregate_group_contributions
from app.modules.pnl_attribution.domain.fixed_income_pnl import estimate_fixed_income_effects
from app.modules.pnl_attribution.domain.fx import estimate_fx_effects
from app.modules.pnl_attribution.domain.options_pnl import estimate_options_effects
from app.modules.pnl_attribution.domain.pnl_calculation import calculate_total_pnl_percent
from app.modules.pnl_attribution.domain.trade_effects import calculate_trade_effects
from app.modules.pnl_attribution.repository import PnlAttributionRepository
from app.modules.pnl_attribution.schemas import (
    PnlAttributionRequest,
    PnlAttributionResult,
    PnlAttributionStatus,
    PnlCsvExportResponse,
    PnlDeleteResponse,
    PnlHistoryItem,
    PnlHistoryResponse,
    PnlMethodology,
    PnlPeriod,
)


SOURCE_MODULES = [
    "Portfolio Builder",
    "Market Data",
    "Trade Simulator",
    "Rates Lab",
    "Options Pricing Lab",
    "Risk Monitor",
    "Reports Center",
    "Athena Intelligence",
]


class PnlAttributionService:
    def __init__(
        self,
        repository: PnlAttributionRepository,
        athena_service: AthenaIntelligenceService | None = None,
    ) -> None:
        self.repository = repository
        self.athena_service = athena_service or AthenaIntelligenceService()

    def get_status(self) -> PnlAttributionStatus:
        return PnlAttributionStatus(
            detail=(
                "P&L Attribution explains portfolio gains and losses by position, "
                "asset class, sector, income, trades, rates, options and benchmark drivers."
            ),
            source_modules=SOURCE_MODULES,
        )

    def analyze(self, request: PnlAttributionRequest) -> PnlAttributionResult:
        portfolio = self.repository.get_portfolio(request.portfolio_id)
        if portfolio is None:
            raise HTTPException(status_code=404, detail=f"Portfolio '{request.portfolio_id}' not found.")
        raw_positions = self.repository.list_positions(request.portfolio_id)
        if not raw_positions:
            raise HTTPException(status_code=404, detail=f"Portfolio '{request.portfolio_id}' has no positions.")

        warnings: list[str] = []
        period_days = max((request.end_date - request.start_date).days, 1)
        price_lookup = {
            str(position.get("symbol", "")).upper(): self.repository.get_price_snapshot(
                str(position.get("symbol", "")),
                request.start_date,
                request.end_date,
            )
            for position in raw_positions
        }
        for symbol, snapshot in price_lookup.items():
            warnings.extend(str(item) for item in snapshot.get("warnings", []))

        cash = _as_float(portfolio.get("cash")) or 0.0
        preliminary_start = sum(
            (_as_float(price_lookup.get(str(position.get("symbol", "")).upper(), {}).get("starting_price"))
             or _as_float(position.get("average_price"))
             or 0.0)
            * (_as_float(position.get("quantity")) or 0.0)
            for position in raw_positions
        ) + cash
        transactions = [
            trade
            for trade in portfolio.get("transaction_history", [])
            if isinstance(trade, dict)
        ]
        trade_effects = calculate_trade_effects(
            transactions,
            preliminary_start,
            request.include_trades,
        )
        positions = build_position_contributions(
            positions=raw_positions,
            price_lookup=price_lookup,
            transactions=transactions,
            period_days=period_days,
            include_income=request.include_income,
            portfolio_starting_value=preliminary_start,
        )
        preliminary_totals = portfolio_totals(
            positions,
            cash,
            trade_effects.total_trade_costs + trade_effects.estimated_slippage,
            0.0,
        )
        fx_pnl, fx_effects, fx_warnings = estimate_fx_effects(
            positions,
            str(portfolio.get("base_currency") or "USD"),
            request.include_fx,
        )
        totals = portfolio_totals(
            positions,
            cash,
            trade_effects.total_trade_costs + trade_effects.estimated_slippage,
            fx_pnl,
        )
        positions = finalize_contributions(
            positions,
            totals["total_pnl"],
            trade_effects.total_trade_costs + trade_effects.estimated_slippage,
            totals["starting_value"],
        )
        asset_class_contributions = aggregate_group_contributions(
            positions,
            "asset_class",
            totals["starting_value"],
            totals["ending_value"],
            totals["total_pnl"],
        )
        sector_contributions = aggregate_group_contributions(
            positions,
            "sector",
            totals["starting_value"],
            totals["ending_value"],
            totals["total_pnl"],
        )
        currency_contributions = aggregate_group_contributions(
            positions,
            "currency",
            totals["starting_value"],
            totals["ending_value"],
            totals["total_pnl"],
        )
        fixed_income_effects, rates_warnings = estimate_fixed_income_effects(
            positions,
            raw_positions,
            request.include_rates,
        )
        options_effects, options_warnings = estimate_options_effects(
            positions,
            request.include_options,
        )
        benchmark_return, benchmark_warning = self._benchmark_return(request)
        if benchmark_warning:
            warnings.append(benchmark_warning)
        benchmark = build_benchmark_comparison(
            request,
            totals["total_pnl_percent"],
            benchmark_return,
            asset_class_contributions,
        )
        top_winners = sorted(positions, key=lambda item: item.total_pnl, reverse=True)[:5]
        top_losers = sorted(positions, key=lambda item: item.total_pnl)[:5]
        warnings.extend(rates_warnings + options_warnings + fx_warnings + trade_effects.warnings)
        limitations = [
            "Demo P&L uses point-in-time portfolio holdings and deterministic fallback assumptions.",
            "No live broker execution or custodial tax lot feed is connected.",
            "Market Data history is demo data; do not interpret as real historical performance.",
        ]
        methodology = PnlMethodology(
            attribution_method=request.attribution_method,
            assumptions=[
                "Position P&L = ending value - starting value + income - allocated costs.",
                "Realized P&L uses supplied sell transactions when present; otherwise it is zero.",
                "Unrealized P&L uses remaining price movement from demo Market Data or Portfolio Builder prices.",
                "Fixed income P&L uses duration and convexity approximations.",
                "Options Greeks attribution is prepared and falls back to zero when no option positions exist.",
            ],
            data_sources=[
                "Portfolio Builder positions",
                "Market Data demo prices",
                "Portfolio transaction_history when supplied",
                "Deterministic rates, FX and options fallback assumptions",
            ],
            limitations=limitations,
        )
        result_without_commentary = PnlAttributionResult(
            analysis_id=f"pnl_{uuid4().hex[:12]}",
            portfolio_id=str(portfolio["id"]),
            portfolio_name=str(portfolio["name"]),
            period=PnlPeriod(
                start_date=request.start_date,
                end_date=request.end_date,
                days=period_days,
            ),
            starting_value=totals["starting_value"],
            ending_value=totals["ending_value"],
            total_pnl=totals["total_pnl"],
            total_pnl_percent=totals["total_pnl_percent"],
            realized_pnl=totals["realized_pnl"],
            unrealized_pnl=totals["unrealized_pnl"],
            income_pnl=totals["income_pnl"],
            fees_and_costs=totals["fees_and_costs"],
            fx_pnl=fx_pnl,
            price_pnl=totals["price_pnl"],
            position_contributions=positions,
            asset_class_contributions=asset_class_contributions,
            sector_contributions=sector_contributions,
            currency_contributions=currency_contributions,
            trade_effects=trade_effects,
            fixed_income_effects=fixed_income_effects,
            options_effects=options_effects,
            fx_effects=fx_effects,
            benchmark_comparison=benchmark,
            top_winners=top_winners,
            top_losers=top_losers,
            warnings=warnings,
            methodology=methodology,
            limitations=limitations,
            status="generated_with_warnings" if warnings else "generated",
            generated_at=datetime.now(UTC),
        )
        commentary_payload = result_without_commentary.model_dump(mode="json")
        try:
            commentary = build_pnl_commentary(
                payload=commentary_payload,
                language=request.language,
                service=self.athena_service,
            )
        except Exception as exc:  # pragma: no cover - defensive guard
            warnings.append(f"Athena Intelligence commentary unavailable: {exc}")
            commentary = None

        result = result_without_commentary.model_copy(
            update={
                "athena_ai_commentary": commentary,
                "warnings": warnings,
                "status": "generated_with_warnings" if warnings else "generated",
            },
        )
        return self.repository.save(result)

    def demo(self) -> PnlAttributionResult:
        return self.analyze(
            PnlAttributionRequest(
                portfolio_id="pf_004",
                attribution_method="Brinson-lite",
                benchmark_symbol="SPY",
            ),
        )

    def list_history(self) -> PnlHistoryResponse:
        analyses = self.repository.list_history()
        return PnlHistoryResponse(
            total_analyses=len(analyses),
            items=[
                PnlHistoryItem(
                    analysis_id=analysis.analysis_id,
                    portfolio_id=analysis.portfolio_id,
                    portfolio_name=analysis.portfolio_name,
                    start_date=analysis.period.start_date,
                    end_date=analysis.period.end_date,
                    total_pnl=analysis.total_pnl,
                    total_pnl_percent=analysis.total_pnl_percent,
                    generated_at=analysis.generated_at,
                    status=analysis.status,
                    warnings_count=len(analysis.warnings),
                )
                for analysis in analyses
            ],
        )

    def get_history_item(self, analysis_id: str) -> PnlAttributionResult:
        analysis = self.repository.get(analysis_id)
        if analysis is None:
            raise HTTPException(status_code=404, detail=f"P&L analysis '{analysis_id}' not found.")
        return analysis

    def delete_history_item(self, analysis_id: str) -> PnlDeleteResponse:
        if not self.repository.delete(analysis_id):
            raise HTTPException(status_code=404, detail=f"P&L analysis '{analysis_id}' not found.")
        return PnlDeleteResponse(deleted=True, analysis_id=analysis_id)

    def export_csv(self, analysis_id: str) -> PnlCsvExportResponse:
        analysis = self.get_history_item(analysis_id)
        output = io.StringIO()
        writer = csv.writer(output)
        included = ["position_contributions", "asset_class_contributions", "sector_contributions", "currency_contributions"]
        _write_table(writer, "Position P&L", [row.model_dump(mode="json") for row in analysis.position_contributions])
        _write_table(writer, "Asset Class Attribution", [row.model_dump(mode="json") for row in analysis.asset_class_contributions])
        _write_table(writer, "Sector Attribution", [row.model_dump(mode="json") for row in analysis.sector_contributions])
        _write_table(writer, "Currency Attribution", [row.model_dump(mode="json") for row in analysis.currency_contributions])
        return PnlCsvExportResponse(
            analysis_id=analysis.analysis_id,
            csv=output.getvalue(),
            included_tables=included,
        )

    def _benchmark_return(self, request: PnlAttributionRequest) -> tuple[float | None, str | None]:
        snapshot = self.repository.get_price_snapshot(
            request.benchmark_symbol,
            request.start_date,
            request.end_date,
        )
        warnings = snapshot.get("warnings", [])
        start = _as_float(snapshot.get("starting_price"))
        end = _as_float(snapshot.get("ending_price"))
        if start is None or end is None or start == 0:
            return None, f"{request.benchmark_symbol}: benchmark return unavailable."
        warning = str(warnings[0]) if warnings else None
        return calculate_total_pnl_percent(end - start, start), warning


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


def _as_float(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
