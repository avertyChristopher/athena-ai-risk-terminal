from __future__ import annotations

import csv
import io
import json
from typing import Any

from app.modules.reports_center.schemas import GeneratedReport


def report_to_json(report: GeneratedReport) -> dict[str, Any]:
    return report.model_dump(mode="json")


def report_to_markdown(report: GeneratedReport) -> str:
    lines = [
        f"# {report.title}",
        "",
        f"**Report ID:** `{report.report_id}`",
        f"**Portfolio:** {report.portfolio_name or 'Unavailable'}",
        f"**Generated at:** {report.generated_at.isoformat()}",
        f"**Status:** {report.status}",
        "",
        "## Executive Summary",
        report.executive_summary,
        "",
    ]
    if report.athena_commentary:
        lines.extend(
            [
                "## Athena Intelligence Commentary",
                str(report.athena_commentary.get("summary") or "No commentary available."),
                "",
            ],
        )
    for section in report.sections:
        lines.extend([f"## {section.title}", section.summary, ""])
        if section.metrics:
            lines.extend(_dict_to_lines(section.metrics))
            lines.append("")
        if section.table:
            lines.extend(_table_to_markdown(section.table))
            lines.append("")
        if section.warnings:
            lines.append("**Warnings:** " + "; ".join(section.warnings))
            lines.append("")
    lines.extend(["## Assumptions", *[f"- {item}" for item in report.assumptions], ""])
    lines.extend(["## Limitations", *[f"- {item}" for item in report.limitations], ""])
    lines.extend(["## Disclaimer", report.disclaimer, ""])
    lines.extend(["## PDF Export Roadmap", report.pdf_roadmap_note, ""])
    return "\n".join(lines)


def report_to_csv(report: GeneratedReport) -> tuple[str, list[str]]:
    output = io.StringIO()
    writer = csv.writer(output)
    included: list[str] = []
    for section in report.sections:
        if not section.table:
            continue
        included.append(section.title)
        keys = sorted({key for row in section.table for key in row})
        writer.writerow([section.title])
        writer.writerow(keys)
        for row in section.table:
            writer.writerow([_stringify(row.get(key)) for key in keys])
        writer.writerow([])
    if not included:
        writer.writerow(["No tabular sections available for CSV export."])
    return output.getvalue(), included


def _dict_to_lines(data: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for key, value in data.items():
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        lines.append(f"- **{key}:** {value}")
    return lines


def _table_to_markdown(rows: list[dict[str, Any]]) -> list[str]:
    keys = sorted({key for row in rows for key in row})
    if not keys:
        return []
    lines = [
        "| " + " | ".join(keys) + " |",
        "| " + " | ".join("---" for _ in keys) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(_stringify(row.get(key)) for key in keys) + " |")
    return lines


def _stringify(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    if value is None:
        return ""
    return str(value).replace("\n", " ")
