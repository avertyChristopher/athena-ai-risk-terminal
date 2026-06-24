from __future__ import annotations

from app.modules.limit_center.schemas import LimitBreach, LimitEvaluationSummary


def commentary_payload(
    summary: LimitEvaluationSummary,
    breaches: list[LimitBreach],
    warnings: list[str],
) -> dict[str, object]:
    return {
        "source_module": "limit_center",
        "module_name": "limit_center",
        "analysis_mode": "limit",
        "portfolio_id": summary.portfolio_id,
        "breach_count": summary.breach_count,
        "open_breach_count": summary.open_breach_count,
        "critical_breach_count": summary.critical_breach_count,
        "highest_severity": summary.highest_severity,
        "overall_status": summary.overall_status,
        "source_modules": summary.source_modules,
        "breaches": [
            {
                "rule_name": breach.rule_name,
                "severity": breach.severity,
                "source_module": breach.source_module,
                "metric_key": breach.metric_key,
                "current_value": breach.current_value,
                "limit_value": breach.limit_value,
                "suggested_action": breach.suggested_action,
            }
            for breach in breaches[:8]
        ],
        "warnings": warnings,
        "assumptions": [
            "Limit Center evaluates structured module payloads against deterministic governance rules.",
            "In-memory demo persistence is used until durable workflow storage is added.",
        ],
        "limitations": [
            "Missing payload fields are reported as warnings and do not crash evaluation.",
            "Outputs are risk governance analytics and are not investment advice.",
        ],
    }
