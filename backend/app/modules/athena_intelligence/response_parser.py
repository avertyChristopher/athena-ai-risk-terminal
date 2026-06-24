from __future__ import annotations

import json
from typing import Any

from app.modules.athena_intelligence.domain.module_context import list_strings


def parse_commentary_response(raw: str) -> dict[str, Any] | None:
    data = _parse_json_object(raw)
    if data is None or not isinstance(data.get("summary"), str):
        return None
    return {
        "summary": data["summary"],
        "main_risks": list_strings(data.get("main_risks")),
        "risk_drivers": list_strings(data.get("risk_drivers")),
        "breaches": list_strings(data.get("breaches")),
        "suggested_actions": list_strings(data.get("suggested_actions")),
        "assumptions": list_strings(data.get("assumptions")),
        "limitations": list_strings(data.get("limitations")),
        "confidence_level": _confidence(data.get("confidence_level")),
    }


def parse_risk_synthesis_response(raw: str) -> dict[str, Any] | None:
    data = _parse_json_object(raw)
    if data is None or not isinstance(data.get("executive_summary"), str):
        return None
    return {
        "executive_summary": data["executive_summary"],
        "overall_risk_level": str(data.get("overall_risk_level") or "medium"),
        "top_risk_drivers": list_strings(data.get("top_risk_drivers")),
        "cross_module_findings": list_strings(data.get("cross_module_findings")),
        "breached_limits": list_strings(data.get("breached_limits")),
        "portfolio_vulnerabilities": list_strings(data.get("portfolio_vulnerabilities")),
        "suggested_next_actions": list_strings(data.get("suggested_next_actions")),
        "module_specific_notes": _module_notes(data.get("module_specific_notes")),
        "assumptions": list_strings(data.get("assumptions")),
        "limitations": list_strings(data.get("limitations")),
    }


def parse_metric_explanation_response(raw: str) -> dict[str, Any] | None:
    data = _parse_json_object(raw)
    if data is None or not isinstance(data.get("explanation"), str):
        return None
    return {
        "explanation": data["explanation"],
        "interpretation": str(data.get("interpretation") or ""),
        "risk_meaning": str(data.get("risk_meaning") or ""),
        "limitations": list_strings(data.get("limitations")),
        "cfa_note": data.get("cfa_note"),
    }


def _parse_json_object(raw: str) -> dict[str, Any] | None:
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, dict) else None


def _confidence(value: Any) -> str:
    normalized = str(value or "medium").lower()
    return normalized if normalized in {"low", "medium", "high"} else "medium"


def _module_notes(value: Any) -> dict[str, list[str]]:
    if not isinstance(value, dict):
        return {}
    return {str(key): list_strings(notes) for key, notes in value.items()}
