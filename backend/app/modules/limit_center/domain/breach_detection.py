from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from app.modules.limit_center.domain.limit_rules import compare_values
from app.modules.limit_center.domain.severity import classify_breach_severity
from app.modules.limit_center.domain.source_mapping import extract_limit_metrics
from app.modules.limit_center.schemas import (
    EvaluatedLimitRule,
    LimitBreach,
    LimitRule,
    LimitSourceModule,
)


def evaluate_limit_payload(
    *,
    portfolio_id: str,
    source_module: LimitSourceModule,
    payload: dict[str, object],
    rules: list[LimitRule],
) -> tuple[list[EvaluatedLimitRule], list[LimitBreach], list[str]]:
    metrics, warnings = extract_limit_metrics(source_module, payload)
    evaluated: list[EvaluatedLimitRule] = []
    breaches: list[LimitBreach] = []
    now = datetime.now(UTC)

    for rule in rules:
        if not rule.enabled:
            evaluated.append(
                _evaluated_rule(rule, source_module, None, breached=False, warning="Rule disabled.")
            )
            continue
        if source_module not in rule.source_modules:
            continue
        current = metrics.get(rule.metric_key)
        if current is None:
            warning = f"Metric '{rule.metric_key}' was not available in {source_module} payload."
            warnings.append(warning)
            evaluated.append(_evaluated_rule(rule, source_module, None, breached=False, warning=warning))
            continue

        breached = compare_values(current, rule.limit_value, rule.comparison_operator)
        severity = (
            classify_breach_severity(
                current_value=current,
                limit_value=rule.limit_value,
                operator=rule.comparison_operator,
                base_severity=rule.severity_if_breached,
                metric_key=rule.metric_key,
            )
            if breached
            else None
        )
        evaluated.append(
            _evaluated_rule(
                rule,
                source_module,
                current,
                breached=breached,
                severity=severity,
            )
        )
        if breached and severity is not None:
            breaches.append(
                LimitBreach(
                    breach_id=_breach_id(rule.rule_id),
                    rule_id=rule.rule_id,
                    rule_name=rule.name,
                    portfolio_id=portfolio_id,
                    source_module=source_module,
                    metric_key=rule.metric_key,
                    current_value=current,
                    limit_value=rule.limit_value,
                    comparison_operator=rule.comparison_operator,
                    severity=severity,
                    status="open",
                    explanation=_explanation(rule, current),
                    suggested_action=_suggested_action(rule),
                    created_at=now,
                    updated_at=now,
                )
            )

    return evaluated, breaches, _dedupe(warnings)


def _evaluated_rule(
    rule: LimitRule,
    source_module: LimitSourceModule,
    current_value: float | bool | None,
    *,
    breached: bool,
    severity: str | None = None,
    warning: str | None = None,
) -> EvaluatedLimitRule:
    return EvaluatedLimitRule(
        rule_id=rule.rule_id,
        rule_name=rule.name,
        category=rule.category,
        source_module=source_module,
        metric_key=rule.metric_key,
        current_value=current_value,
        limit_value=rule.limit_value,
        comparison_operator=rule.comparison_operator,
        breached=breached,
        severity=severity,
        enabled=rule.enabled,
        warning=warning,
    )


def _explanation(rule: LimitRule, current: float | bool) -> str:
    return (
        f"{rule.name} breached: metric '{rule.metric_key}' is {current}, "
        f"limit is {rule.limit_value} with operator {rule.comparison_operator}."
    )


def _suggested_action(rule: LimitRule) -> str:
    if rule.category == "portfolio":
        return "Review concentration, diversification and policy constraints before adding risk."
    if rule.category == "risk":
        return "Review risk drivers and consider whether exposure remains within mandate."
    if rule.category == "stress":
        return "Escalate the stress scenario result and document mitigation or exception rationale."
    if rule.category == "fixed_income":
        return "Review duration, DV01 and rate-shock sensitivity before approving fixed-income exposure."
    if rule.category == "options":
        return "Route the options exposure to risk governance review before approving the strategy."
    if rule.category == "trade":
        return "Review the simulated trade ticket and post-trade constraints before approval."
    return "Review the limit breach and document the governance decision."


def _breach_id(rule_id: str) -> str:
    return f"br_{rule_id}_{uuid4().hex[:8]}"


def _dedupe(values: list[str]) -> list[str]:
    unique: list[str] = []
    for value in values:
        if value and value not in unique:
            unique.append(value)
    return unique
