from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from app.modules.reports_center.schemas import ReportSnapshot, ReportType


def create_snapshot(
    *,
    report_id: str,
    report_type: ReportType,
    portfolio_id: str | None,
    portfolio_name: str | None,
    language: str,
    payloads: dict[str, Any],
    warnings: list[str],
    limitations: list[str],
) -> ReportSnapshot:
    return ReportSnapshot(
        snapshot_id=f"snap_{uuid4().hex[:12]}",
        report_id=report_id,
        portfolio_id=portfolio_id,
        portfolio_name=portfolio_name,
        report_type=report_type,
        generated_at=datetime.now(UTC),
        source_modules=sorted(_source_modules(payloads)),
        data_sources=_data_sources(payloads),
        payloads_used=payloads,
        warnings=warnings,
        limitations=limitations,
        language=language,
    )


def _source_modules(payloads: dict[str, Any]) -> set[str]:
    mapping = {
        "portfolio": "Portfolio Builder",
        "portfolio_summary": "Portfolio Builder",
        "holdings": "Portfolio Builder",
        "allocations": "Portfolio Builder",
        "concentration": "Portfolio Builder",
        "market_data_coverage": "Market Data",
        "risk_monitor": "Risk Monitor",
        "volatility": "Volatility Lab",
        "rates": "Rates Lab",
        "options": "Options Pricing Lab",
        "pnl_attribution": "P&L Attribution",
        "reconciliation": "Reconciliation Center",
        "stress_testing": "Stress Testing",
        "limit_center": "Limit Center",
        "trade_simulator": "Trade Simulator",
        "athena_commentary": "Athena Intelligence",
        "athena_synthesis": "Athena Intelligence",
    }
    return {module for key, module in mapping.items() if payloads.get(key) is not None}


def _data_sources(payloads: dict[str, Any]) -> list[str]:
    sources = ["snapshot_store", "deterministic_demo_fallback"]
    if payloads.get("market_data_coverage") is not None:
        sources.append("market_data")
    if payloads.get("portfolio") is not None:
        sources.append("portfolio_builder")
    if payloads.get("pnl_attribution") is not None:
        sources.append("pnl_attribution")
    if payloads.get("reconciliation") is not None:
        sources.append("reconciliation")
    return sources
