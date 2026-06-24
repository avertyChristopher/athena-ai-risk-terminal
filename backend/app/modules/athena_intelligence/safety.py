from __future__ import annotations

import re
from typing import Any

from app.modules.athena_intelligence.domain.commentary_rules import fallback_disclaimer


UNSAFE_REPLACEMENTS = {
    r"\bstrong buy\b": "review candidate",
    r"\bbuy recommendation\b": "risk review",
    r"\bsell recommendation\b": "risk review",
    r"\bhold recommendation\b": "risk review",
    r"\brecommend(?:s|ed|ing)? buying\b": "suggests reviewing exposure to",
    r"\brecommend(?:s|ed|ing)? selling\b": "suggests reviewing risk in",
    r"\brecommend(?:s|ed|ing)? holding\b": "suggests monitoring",
    r"\byou should buy\b": "the exposure should be reviewed",
    r"\byou should sell\b": "the exposure should be reviewed",
    r"\byou should hold\b": "the exposure should be monitored",
}


def sanitize_text(value: str) -> str:
    cleaned = value
    for pattern, replacement in UNSAFE_REPLACEMENTS.items():
        cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)
    return cleaned


def sanitize_list(values: list[str]) -> list[str]:
    return [sanitize_text(value) for value in values]


def sanitize_commentary_data(data: dict[str, Any], language: str) -> dict[str, Any]:
    sanitized = dict(data)
    for key in [
        "summary",
        "executive_summary",
        "overall_risk_level",
        "explanation",
        "interpretation",
        "risk_meaning",
    ]:
        if isinstance(sanitized.get(key), str):
            sanitized[key] = sanitize_text(sanitized[key])

    for key in [
        "main_risks",
        "risk_drivers",
        "breaches",
        "suggested_actions",
        "assumptions",
        "limitations",
        "top_risk_drivers",
        "cross_module_findings",
        "breached_limits",
        "portfolio_vulnerabilities",
        "suggested_next_actions",
    ]:
        if isinstance(sanitized.get(key), list):
            sanitized[key] = sanitize_list(sanitized[key])

    module_notes = sanitized.get("module_specific_notes")
    if isinstance(module_notes, dict):
        sanitized["module_specific_notes"] = {
            str(module): sanitize_list([str(note) for note in notes])
            for module, notes in module_notes.items()
            if isinstance(notes, list)
        }

    sanitized["disclaimer"] = fallback_disclaimer(language)
    return sanitized
