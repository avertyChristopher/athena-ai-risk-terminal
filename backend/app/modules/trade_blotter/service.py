from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any
from uuid import uuid4

from fastapi import HTTPException

from app.modules.trade_blotter.domain.commentary import build_trade_blotter_summary
from app.modules.trade_blotter.domain.review_workflow import apply_review_action
from app.modules.trade_blotter.domain.trade_validation import estimated_trade_value, normalize_trade_payload
from app.modules.trade_blotter.repository import TradeBlotterRepository
from app.modules.trade_blotter.schemas import (
    TradeBlotterDemoResponse,
    TradeBlotterDeleteResponse,
    TradeBlotterEntry,
    TradeBlotterEntryCreate,
    TradeBlotterEntryUpdate,
    TradeBlotterFromSimulationRequest,
    TradeBlotterListResponse,
    TradeBlotterReviewRequest,
    TradeBlotterReviewResponse,
    TradeBlotterStatus,
)


SOURCE_MODULES = ["Trade Simulator", "P&L Attribution", "Reconciliation", "Risk Monitor"]


class TradeBlotterService:
    def __init__(self, repository: TradeBlotterRepository) -> None:
        self.repository = repository

    def get_status(self) -> TradeBlotterStatus:
        entries = self.repository.list()
        return TradeBlotterStatus(
            detail=(
                "Trade Blotter stores simulated, reviewed and approved trades for downstream "
                "P&L Attribution, Reconciliation and Risk Monitor workflows. "
                "No real market execution occurs."
            ),
            entries_count=len(entries),
            source_modules=SOURCE_MODULES,
        )

    def list_entries(
        self,
        portfolio_id: str | None = None,
        symbol: str | None = None,
        status: str | None = None,
    ) -> TradeBlotterListResponse:
        entries = self.repository.list()
        if portfolio_id:
            entries = [entry for entry in entries if entry.portfolio_id == portfolio_id]
        if symbol:
            entries = [entry for entry in entries if entry.symbol == symbol.upper()]
        if status:
            entries = [entry for entry in entries if entry.status == status]
        return TradeBlotterListResponse(total_entries=len(entries), entries=entries)

    def get_entry(self, trade_id: str) -> TradeBlotterEntry:
        entry = self.repository.get(trade_id)
        if entry is None:
            raise HTTPException(status_code=404, detail=f"Trade '{trade_id}' not found.")
        return entry

    def create_entry(self, payload: TradeBlotterEntryCreate) -> TradeBlotterEntry:
        now = datetime.now(UTC)
        data = normalize_trade_payload(payload.model_dump(mode="json"))
        entry = TradeBlotterEntry(
            **data,
            trade_id=f"trd_{uuid4().hex[:12]}",
            estimated_trade_value=estimated_trade_value(payload.quantity, payload.price),
            created_at=now,
            updated_at=now,
        )
        return self.repository.save(entry)

    def update_entry(self, trade_id: str, payload: TradeBlotterEntryUpdate) -> TradeBlotterEntry:
        existing = self.get_entry(trade_id)
        update = normalize_trade_payload(payload.model_dump(mode="json", exclude_none=True))
        if "quantity" in update or "price" in update:
            quantity = float(update.get("quantity", existing.quantity))
            price = float(update.get("price", existing.price))
            update["estimated_trade_value"] = estimated_trade_value(quantity, price)
        update["updated_at"] = datetime.now(UTC)
        entry = existing.model_copy(update=update)
        return self.repository.save(entry)

    def review_entry(
        self,
        trade_id: str,
        payload: TradeBlotterReviewRequest,
    ) -> TradeBlotterReviewResponse:
        entry = self.get_entry(trade_id)
        try:
            updated, event = apply_review_action(entry, payload)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        return TradeBlotterReviewResponse(entry=self.repository.save(updated), event=event)

    def delete_entry(self, trade_id: str) -> TradeBlotterDeleteResponse:
        if not self.repository.delete(trade_id):
            raise HTTPException(status_code=404, detail=f"Trade '{trade_id}' not found.")
        return TradeBlotterDeleteResponse(deleted=True, trade_id=trade_id)

    def create_from_simulation(self, payload: TradeBlotterFromSimulationRequest) -> TradeBlotterEntry:
        ticket = dict(payload.simulation.get("trade_ticket") or {})
        if not ticket:
            raise HTTPException(status_code=422, detail="Simulation payload must include trade_ticket.")
        costs = dict(payload.simulation.get("transaction_cost_analysis") or {})
        suitability = dict(payload.simulation.get("suitability_review") or {})
        constraints = list(payload.simulation.get("constraints_warnings") or [])
        risk_impact = dict(payload.simulation.get("risk_impact") or {})
        commentary = payload.simulation.get("athena_ai_commentary") or payload.simulation.get("athena_commentary")
        create_payload = TradeBlotterEntryCreate(
            portfolio_id=str(ticket.get("portfolio_id") or "pf_001"),
            symbol=str(ticket.get("symbol") or ""),
            action=str(ticket.get("action") or "BUY").upper(),
            quantity=float(ticket.get("quantity") or 0.0),
            price=float(ticket.get("estimated_price") or 0.0),
            currency=str(ticket.get("currency") or "USD"),
            status=payload.initial_status,
            trade_date=date.today(),
            source_module="trade_simulator",
            cost_estimate=float(costs.get("total_estimated_cost") or ticket.get("estimated_total_implementation_cost") or 0.0),
            slippage_estimate=float(ticket.get("estimated_slippage") or 0.0),
            suitability_status=suitability.get("status"),
            constraint_status="warnings" if constraints else "clear",
            risk_summary={
                "metric_source": risk_impact.get("metric_source"),
                "fallback_used": risk_impact.get("fallback_used"),
                "warnings_count": len(constraints),
                "summary": build_trade_blotter_summary_from_ticket(ticket),
            },
            source_payload=payload.simulation,
            athena_ai_commentary=commentary if isinstance(commentary, dict) else None,
        )
        entry = self.create_entry(create_payload)
        if payload.note:
            reviewed = TradeBlotterReviewRequest(
                action="submit_for_review" if payload.initial_status == "draft" else "reopen",
                reviewer=payload.reviewer,
                note=payload.note,
            )
            if entry.status == "draft":
                return self.review_entry(entry.trade_id, reviewed).entry
        return entry

    def demo(self) -> TradeBlotterDemoResponse:
        entries = [
            self._upsert_demo_entry(
                trade_id="demo_trd_aapl_buy",
                portfolio_id="pf_001",
                symbol="AAPL",
                action="BUY",
                quantity=5,
                price=195.25,
                status="approved",
            ),
            self._upsert_demo_entry(
                trade_id="demo_trd_msft_sell",
                portfolio_id="pf_001",
                symbol="MSFT",
                action="SELL",
                quantity=2,
                price=422.10,
                status="pending_review",
            ),
        ]
        return TradeBlotterDemoResponse(entries=entries)

    def _upsert_demo_entry(
        self,
        *,
        trade_id: str,
        portfolio_id: str,
        symbol: str,
        action: str,
        quantity: float,
        price: float,
        status: str,
    ) -> TradeBlotterEntry:
        existing = self.repository.get(trade_id)
        now = datetime.now(UTC)
        if existing:
            return existing
        entry = TradeBlotterEntry(
            trade_id=trade_id,
            portfolio_id=portfolio_id,
            symbol=symbol,
            action=action,
            quantity=quantity,
            price=price,
            estimated_trade_value=estimated_trade_value(quantity, price),
            status=status,
            trade_date=date(2026, 6, 3),
            source_module="demo_trade_blotter",
            cost_estimate=estimated_trade_value(quantity, price) * 0.0005,
            slippage_estimate=estimated_trade_value(quantity, price) * 0.0003,
            suitability_status="Suitable" if status == "approved" else "Requires Review",
            constraint_status="clear" if status == "approved" else "warnings",
            risk_summary={"summary": build_trade_blotter_summary_from_ticket({"action": action, "quantity": quantity, "symbol": symbol})},
            source_payload={"demo": True},
            created_at=now,
            updated_at=now,
        )
        return self.repository.save(entry)


def build_trade_blotter_summary_from_ticket(ticket: dict[str, Any]) -> dict[str, str]:
    synthetic = TradeBlotterEntry(
        trade_id="preview",
        portfolio_id=str(ticket.get("portfolio_id") or "pf_001"),
        symbol=str(ticket.get("symbol") or "UNKNOWN").upper(),
        action=str(ticket.get("action") or "BUY").upper(),
        quantity=float(ticket.get("quantity") or 0.0),
        price=float(ticket.get("estimated_price") or ticket.get("price") or 0.0),
        estimated_trade_value=estimated_trade_value(
            float(ticket.get("quantity") or 0.0),
            float(ticket.get("estimated_price") or ticket.get("price") or 0.0),
        ),
        status="simulated",
        trade_date=date.today(),
        source_module="trade_simulator",
    )
    return build_trade_blotter_summary(synthetic)
