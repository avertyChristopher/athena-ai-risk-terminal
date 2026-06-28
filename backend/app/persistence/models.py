from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


def _now() -> datetime:
    return datetime.now(UTC)


class PortfolioSnapshotModel(Base):
    __tablename__ = "portfolio_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    portfolio_id: Mapped[str] = mapped_column(String(80), index=True)
    portfolio_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    snapshot_type: Mapped[str] = mapped_column(String(80), index=True)
    payload_json: Mapped[str] = mapped_column(Text)
    source_module: Mapped[str] = mapped_column(String(120), index=True)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, index=True)


class TradeBlotterEntryModel(Base):
    __tablename__ = "trade_blotter_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    trade_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    portfolio_id: Mapped[str] = mapped_column(String(80), index=True)
    symbol: Mapped[str] = mapped_column(String(32), index=True)
    action: Mapped[str] = mapped_column(String(24), index=True)
    quantity: Mapped[float] = mapped_column(Float, default=0.0)
    price: Mapped[float] = mapped_column(Float, default=0.0)
    estimated_trade_value: Mapped[float] = mapped_column(Float, default=0.0)
    currency: Mapped[str] = mapped_column(String(8), default="USD")
    status: Mapped[str] = mapped_column(String(32), index=True, default="draft")
    trade_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    settlement_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    source_module: Mapped[str] = mapped_column(String(120), default="trade_blotter")
    cost_estimate: Mapped[float] = mapped_column(Float, default=0.0)
    slippage_estimate: Mapped[float] = mapped_column(Float, default=0.0)
    suitability_status: Mapped[str | None] = mapped_column(String(64), nullable=True)
    constraint_status: Mapped[str | None] = mapped_column(String(64), nullable=True)
    risk_summary_json: Mapped[str] = mapped_column(Text, default="{}")
    trade_payload_json: Mapped[str] = mapped_column(Text, default="{}")
    review_history_json: Mapped[str] = mapped_column(Text, default="[]")
    athena_commentary_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, index=True)
    reviewed_by: Mapped[str | None] = mapped_column(String(120), nullable=True)
    review_note: Mapped[str | None] = mapped_column(Text, nullable=True)


class ReportModel(Base):
    __tablename__ = "persistent_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    report_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    report_type: Mapped[str] = mapped_column(String(80), index=True)
    portfolio_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    portfolio_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    language: Mapped[str] = mapped_column(String(8), default="en")
    title: Mapped[str] = mapped_column(String(255))
    payload_json: Mapped[str] = mapped_column(Text)
    markdown_content: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_modules_json: Mapped[str] = mapped_column(Text, default="[]")
    warnings_json: Mapped[str] = mapped_column(Text, default="[]")
    generated_by: Mapped[str] = mapped_column(String(120), default="reports_center")
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, index=True)


class PnlAnalysisModel(Base):
    __tablename__ = "pnl_analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    analysis_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    portfolio_id: Mapped[str] = mapped_column(String(80), index=True)
    portfolio_name: Mapped[str] = mapped_column(String(255))
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    benchmark_symbol: Mapped[str | None] = mapped_column(String(32), nullable=True)
    payload_json: Mapped[str] = mapped_column(Text)
    total_pnl: Mapped[float] = mapped_column(Float, default=0.0)
    total_return: Mapped[float] = mapped_column(Float, default=0.0)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, index=True)


class ReconciliationRunModel(Base):
    __tablename__ = "reconciliation_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    run_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    portfolio_id: Mapped[str] = mapped_column(String(80), index=True)
    portfolio_name: Mapped[str] = mapped_column(String(255))
    reconciliation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    external_source: Mapped[str] = mapped_column(String(80), index=True)
    overall_status: Mapped[str] = mapped_column(String(64), index=True)
    payload_json: Mapped[str] = mapped_column(Text)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, index=True)


class ReconciliationBreakModel(Base):
    __tablename__ = "reconciliation_breaks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    break_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    run_id: Mapped[str] = mapped_column(String(80), index=True)
    portfolio_id: Mapped[str] = mapped_column(String(80), index=True)
    break_type: Mapped[str] = mapped_column(String(40), index=True)
    severity: Mapped[str] = mapped_column(String(32), index=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    symbol: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    metric: Mapped[str] = mapped_column(String(120))
    internal_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    external_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    difference: Mapped[str | None] = mapped_column(Text, nullable=True)
    tolerance: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_module: Mapped[str] = mapped_column(String(120))
    explanation: Mapped[str] = mapped_column(Text)
    suggested_action: Mapped[str] = mapped_column(Text)
    payload_json: Mapped[str] = mapped_column(Text)
    review_history_json: Mapped[str] = mapped_column(Text, default="[]")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)


class LimitBreachModel(Base):
    __tablename__ = "limit_breaches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    breach_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    portfolio_id: Mapped[str] = mapped_column(String(80), index=True)
    rule_id: Mapped[str] = mapped_column(String(120), index=True)
    rule_name: Mapped[str] = mapped_column(String(255))
    source_module: Mapped[str] = mapped_column(String(120), index=True)
    metric_key: Mapped[str] = mapped_column(String(120), index=True)
    current_value: Mapped[str] = mapped_column(Text)
    limit_value: Mapped[str] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String(32), index=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    explanation: Mapped[str] = mapped_column(Text)
    suggested_action: Mapped[str] = mapped_column(Text)
    payload_json: Mapped[str] = mapped_column(Text)
    review_history_json: Mapped[str] = mapped_column(Text, default="[]")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)


class StressRunModel(Base):
    __tablename__ = "stress_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    run_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    portfolio_id: Mapped[str] = mapped_column(String(80), index=True)
    portfolio_name: Mapped[str] = mapped_column(String(255))
    scenario_id: Mapped[str] = mapped_column(String(120), index=True)
    scenario_name: Mapped[str] = mapped_column(String(255))
    severity: Mapped[str] = mapped_column(String(32), index=True)
    estimated_loss: Mapped[float] = mapped_column(Float, default=0.0)
    estimated_loss_percent: Mapped[float] = mapped_column(Float, default=0.0)
    payload_json: Mapped[str] = mapped_column(Text)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, index=True)


class AthenaCommentaryModel(Base):
    __tablename__ = "athena_commentaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    commentary_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    module_name: Mapped[str] = mapped_column(String(120), index=True)
    portfolio_id: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    symbol: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    language: Mapped[str] = mapped_column(String(8), default="en")
    generated_by: Mapped[str] = mapped_column(String(120))
    payload_json: Mapped[str] = mapped_column(Text)
    summary: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, index=True)

