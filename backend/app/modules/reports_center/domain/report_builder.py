from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from app.modules.reports_center.domain.report_sections import build_report_sections
from app.modules.reports_center.domain.report_snapshots import create_snapshot
from app.modules.reports_center.domain.report_templates import get_report_template
from app.modules.reports_center.schemas import (
    GeneratedReport,
    ReportStyle,
    ReportType,
)


def build_report(
    *,
    report_type: ReportType,
    portfolio_id: str | None,
    portfolio_name: str | None,
    language: str,
    style: ReportStyle,
    payloads: dict[str, Any],
    warnings: list[str],
    limitations: list[str],
    athena_commentary: dict[str, Any] | None,
) -> GeneratedReport:
    template = get_report_template(report_type)
    report_id = f"rpt_{uuid4().hex[:12]}"
    snapshot = create_snapshot(
        report_id=report_id,
        report_type=report_type,
        portfolio_id=portfolio_id,
        portfolio_name=portfolio_name,
        language=language,
        payloads=payloads,
        warnings=warnings,
        limitations=limitations,
    )
    generated_at = datetime.now(UTC)
    executive_summary = _executive_summary(
        template.name,
        portfolio_name,
        payloads,
        athena_commentary,
    )
    return GeneratedReport(
        report_id=report_id,
        report_type=report_type,
        title=template.name,
        portfolio_id=portfolio_id,
        portfolio_name=portfolio_name,
        generated_at=generated_at,
        language=language,
        style=style,
        status="generated_with_warnings" if warnings else "generated",
        executive_summary=executive_summary,
        sections=build_report_sections(report_type, payloads),
        snapshot=snapshot,
        athena_commentary=athena_commentary,
        assumptions=[
            "Reports are generated from point-in-time Athena module snapshots.",
            "Demo data and deterministic fallback analytics may be used when live feeds are unavailable.",
        ],
        limitations=limitations,
        warnings=warnings,
    )


def _executive_summary(
    report_name: str,
    portfolio_name: str | None,
    payloads: dict[str, Any],
    athena_commentary: dict[str, Any] | None,
) -> str:
    commentary_summary = ""
    if athena_commentary:
        commentary_summary = (
            athena_commentary.get("summary")
            or athena_commentary.get("executive_summary")
            or ""
        )
    if commentary_summary:
        return commentary_summary
    if portfolio_name:
        return f"{report_name} generated for {portfolio_name} from Athena module snapshots."
    if payloads:
        return f"{report_name} generated from supplied Athena source payloads."
    return f"{report_name} generated with limited source data."
