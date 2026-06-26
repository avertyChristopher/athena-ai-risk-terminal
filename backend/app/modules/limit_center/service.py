from __future__ import annotations

from datetime import UTC, datetime

from app.modules.athena_intelligence.integration import build_athena_ai_commentary
from app.modules.limit_center.domain.breach_detection import evaluate_limit_payload
from app.modules.limit_center.domain.commentary import commentary_payload
from app.modules.limit_center.domain.review_workflow import apply_review_action
from app.modules.limit_center.domain.severity import (
    determine_overall_status,
    highest_severity,
)
from app.modules.limit_center.domain.source_mapping import source_module_cards
from app.modules.limit_center.repository import LimitCenterRepository
from app.modules.limit_center.schemas import (
    BreachListResponse,
    BreachReviewRequest,
    BreachReviewResponse,
    LimitBreach,
    LimitCenterStatus,
    LimitEvaluationRequest,
    LimitEvaluationResponse,
    LimitEvaluationSummary,
    LimitRule,
    LimitRuleCreate,
    LimitRuleListResponse,
    LimitRuleUpdate,
    SourceModuleCard,
)


SUPPORTED_SOURCE_MODULES = [
    "portfolio_builder",
    "risk_monitor",
    "volatility_lab",
    "options_pricing_lab",
    "rates_lab",
    "stress_testing",
    "trade_simulator",
]


class LimitCenterService:
    def __init__(self, repository: LimitCenterRepository) -> None:
        self.repository = repository

    def get_status(self) -> LimitCenterStatus:
        rules = self.repository.list_rules()
        return LimitCenterStatus(
            detail="Limit Center centralizes risk limits, breach detection, exception workflow and Athena Intelligence commentary.",
            engines_available=[
                "rules_library",
                "breach_detection",
                "severity_engine",
                "review_workflow",
                "source_module_mapping",
                "athena_intelligence_commentary",
            ],
            active_rules=sum(1 for rule in rules if rule.enabled),
            supported_source_modules=SUPPORTED_SOURCE_MODULES,
        )

    def list_rules(self) -> LimitRuleListResponse:
        rules = self.repository.list_rules()
        return LimitRuleListResponse(
            total_rules=len(rules),
            active_rules=sum(1 for rule in rules if rule.enabled),
            rules=rules,
        )

    def create_rule(self, payload: LimitRuleCreate) -> LimitRule:
        return self.repository.create_rule(payload)

    def update_rule(self, rule_id: str, payload: LimitRuleUpdate) -> LimitRule:
        rule = self.repository.update_rule(rule_id, payload)
        if rule is None:
            raise ValueError(f"Limit rule '{rule_id}' was not found.")
        return rule

    def delete_rule(self, rule_id: str) -> bool:
        return self.repository.delete_rule(rule_id)

    def evaluate(self, request: LimitEvaluationRequest) -> LimitEvaluationResponse:
        rules = request.ruleset if request.ruleset is not None else self.repository.list_rules()
        evaluated, breaches, warnings = evaluate_limit_payload(
            portfolio_id=request.portfolio_id,
            source_module=request.source_module,
            payload=request.payload,
            rules=rules,
        )
        saved_breaches = self.repository.save_breaches(breaches)
        summary = self._summary(
            portfolio_id=request.portfolio_id,
            source_module=request.source_module,
            evaluated_count=len(evaluated),
            breaches=saved_breaches,
        )
        overall_status = determine_overall_status(saved_breaches, warnings)
        summary.overall_status = overall_status
        summary.highest_severity = highest_severity(saved_breaches)
        ai_commentary = build_athena_ai_commentary(
            module_name="limit_center",
            analysis_mode="limit",
            payload=commentary_payload(summary, saved_breaches, warnings),
            language=request.language,
            style="professional",
        )
        return LimitEvaluationResponse(
            portfolio_id=request.portfolio_id,
            source_module=request.source_module,
            evaluated_rules=evaluated,
            breaches=saved_breaches,
            warnings=warnings,
            summary=summary,
            highest_severity=summary.highest_severity,
            overall_status=overall_status,
            athena_ai_commentary=ai_commentary,
            generated_at=datetime.now(UTC),
        )

    def list_breaches(self) -> BreachListResponse:
        breaches = self.repository.list_breaches()
        return self._breach_list_response(breaches)

    def get_breach(self, breach_id: str) -> LimitBreach:
        breach = self.repository.get_breach(breach_id)
        if breach is None:
            raise ValueError(f"Limit breach '{breach_id}' was not found.")
        return breach

    def review_breach(
        self,
        breach_id: str,
        payload: BreachReviewRequest,
    ) -> BreachReviewResponse:
        breach = self.get_breach(breach_id)
        event = apply_review_action(
            breach.status,
            payload.action,
            payload.reviewer,
            payload.note,
        )
        updated = self.repository.update_breach_status(
            breach_id,
            event.to_status,
            event,
        )
        if updated is None:
            raise ValueError(f"Limit breach '{breach_id}' was not found.")
        return BreachReviewResponse(breach=updated, event=event)

    def source_modules(self) -> list[SourceModuleCard]:
        return [SourceModuleCard(**card) for card in source_module_cards()]

    def demo(self) -> LimitEvaluationResponse:
        return self.evaluate(
            LimitEvaluationRequest(
                portfolio_id="pf_001",
                source_module="risk_monitor",
                payload={
                    "source_module": "risk_monitor",
                    "global_risk_score": 45,
                    "concentration": {
                        "largest_position": {"name": "SPY", "weight": 0.21},
                        "top_3_weight": 0.55,
                        "sector_exposures": [
                            {"name": "Fixed Income", "weight": 0.30},
                            {"name": "Technology", "weight": 0.29},
                            {"name": "International Equity", "weight": 0.12},
                        ],
                        "cash_weight": 0.05,
                    },
                    "risk_metrics": [
                        {"name": "Portfolio volatility", "value": 0.12},
                        {"name": "VaR 95%", "value": 0.014},
                        {"name": "CVaR 95%", "value": 0.018},
                        {"name": "Max drawdown", "value": 0.08},
                    ],
                    "benchmark_risk": {
                        "tracking_error": 0.03,
                        "beta": 0.88,
                    },
                    "assumptions": {
                        "ruleset": "Default deterministic demo ruleset.",
                    },
                    "limitations": [
                        "Demo payload is used when live governance data is unavailable.",
                    ],
                },
            )
        )

    def _summary(
        self,
        *,
        portfolio_id: str,
        source_module: str,
        evaluated_count: int,
        breaches: list[LimitBreach],
    ) -> LimitEvaluationSummary:
        return LimitEvaluationSummary(
            portfolio_id=portfolio_id,
            source_module=source_module,
            evaluated_rule_count=evaluated_count,
            breach_count=len(breaches),
            open_breach_count=sum(1 for breach in breaches if breach.status == "open"),
            critical_breach_count=sum(1 for breach in breaches if breach.severity == "critical"),
            highest_severity=highest_severity(breaches),
            overall_status=determine_overall_status(breaches),
            source_modules=[source_module],
        )

    def _breach_list_response(self, breaches: list[LimitBreach]) -> BreachListResponse:
        return BreachListResponse(
            total_breaches=len(breaches),
            open_breaches=sum(1 for breach in breaches if breach.status == "open"),
            critical_breaches=sum(1 for breach in breaches if breach.severity == "critical"),
            approved_exceptions=sum(
                1 for breach in breaches if breach.status == "approved_exception"
            ),
            resolved_breaches=sum(1 for breach in breaches if breach.status == "resolved"),
            breaches=breaches,
        )
