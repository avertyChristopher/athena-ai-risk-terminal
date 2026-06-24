from __future__ import annotations

from app.modules.limit_center.schemas import (
    ComparisonOperator,
    LimitBreach,
    LimitSeverity,
    OverallLimitStatus,
)


SEVERITY_RANK: dict[str, int] = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


def classify_breach_severity(
    *,
    current_value: float | bool,
    limit_value: float | bool,
    operator: ComparisonOperator,
    base_severity: LimitSeverity,
    metric_key: str,
) -> LimitSeverity:
    if isinstance(current_value, bool) or isinstance(limit_value, bool):
        if metric_key == "unlimited_loss" and current_value is True:
            return "critical"
        return base_severity

    magnitude = _breach_magnitude(current_value, limit_value, operator)
    severity = base_severity
    if magnitude >= 1.0:
        severity = _max_severity(severity, "critical")
    elif magnitude >= 0.50:
        severity = _max_severity(severity, "high")
    elif magnitude >= 0.15:
        severity = _max_severity(severity, "medium")
    else:
        severity = _max_severity("low", severity)
    if metric_key in {"stress_loss_severe", "unlimited_loss"}:
        severity = _max_severity(severity, "critical")
    return severity


def highest_severity(breaches: list[LimitBreach]) -> LimitSeverity | None:
    if not breaches:
        return None
    return max(
        (breach.severity for breach in breaches),
        key=lambda severity: SEVERITY_RANK[severity],
    )


def determine_overall_status(
    breaches: list[LimitBreach],
    warnings: list[str] | None = None,
) -> OverallLimitStatus:
    if not breaches:
        return "watchlist" if warnings else "within_limits"
    critical = sum(1 for breach in breaches if breach.severity == "critical")
    high = sum(1 for breach in breaches if breach.severity == "high")
    if critical:
        return "critical_breach"
    if high >= 2:
        return "severe_breach"
    if high:
        return "breached"
    if any(breach.severity == "medium" for breach in breaches):
        return "breached"
    return "watchlist"


def _breach_magnitude(
    current_value: float,
    limit_value: float,
    operator: ComparisonOperator,
) -> float:
    denominator = max(abs(limit_value), 1e-9)
    if operator.startswith("greater"):
        return max(0.0, (current_value - limit_value) / denominator)
    if operator.startswith("less"):
        return max(0.0, (limit_value - current_value) / denominator)
    return 0.0


def _max_severity(left: LimitSeverity, right: LimitSeverity) -> LimitSeverity:
    return left if SEVERITY_RANK[left] >= SEVERITY_RANK[right] else right
