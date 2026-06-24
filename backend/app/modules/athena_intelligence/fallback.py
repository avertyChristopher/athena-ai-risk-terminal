from __future__ import annotations

from typing import Any

from app.modules.athena_intelligence.domain.commentary_rules import (
    fallback_disclaimer,
    generic_points,
    options_points,
    provider_unavailable_limitation,
    rates_points,
    risk_monitor_points,
    trade_points,
    volatility_points,
)
from app.modules.athena_intelligence.domain.module_context import (
    compact_points,
    source_modules_from_payload,
)
from app.modules.athena_intelligence.domain.risk_synthesis import synthesize_payloads
from app.modules.athena_intelligence.schemas import (
    AthenaAICommentary,
    AthenaIntelligenceRequest,
    AthenaMetricExplanationRequest,
    AthenaMetricExplanationResponse,
    AthenaRiskSynthesisRequest,
    AthenaRiskSynthesisResponse,
)


def generate_fallback_commentary(
    request: AthenaIntelligenceRequest,
) -> AthenaAICommentary:
    payload = request.payload
    points = _module_points(request)
    assumptions = compact_points(
        _payload_assumptions(payload)
        + [
            "Uses only structured module payload data."
            if request.language == "en"
            else "Utilise uniquement le payload structure du module.",
        ],
        request.max_points,
    )
    limitations = compact_points(
        _payload_limitations(payload)
        + [provider_unavailable_limitation(request.language)],
        request.max_points,
    )
    return AthenaAICommentary(
        summary=str(points["summary"]),
        main_risks=list(points["main_risks"]),
        risk_drivers=list(points["risk_drivers"]),
        breaches=list(points["breaches"]),
        suggested_actions=list(points["suggested_actions"]),
        assumptions=assumptions,
        limitations=limitations,
        confidence_level=_confidence_from_payload(payload),
        generated_by="deterministic_fallback",
        source_modules=source_modules_from_payload(payload, request.module_name),
        disclaimer=fallback_disclaimer(request.language),
    )


def generate_fallback_risk_synthesis(
    request: AthenaRiskSynthesisRequest,
) -> AthenaRiskSynthesisResponse:
    data = synthesize_payloads(
        portfolio_id=request.portfolio_id,
        payloads=request.payloads.model_dump(exclude_none=True),
        language=request.language,
        max_points=request.max_points,
    )
    return AthenaRiskSynthesisResponse(
        **data,
        generated_by="deterministic_fallback",
    )


def generate_fallback_metric_explanation(
    request: AthenaMetricExplanationRequest,
) -> AthenaMetricExplanationResponse:
    metric = request.metric_name
    value = request.metric_value
    if request.language == "fr":
        explanation = f"{metric} mesure un aspect du risque ou de la performance dans {request.module_name}."
        interpretation = (
            f"La valeur observee est {value}. Elle doit etre interpretee avec le contexte fourni."
            if value is not None
            else "La valeur n'est pas disponible dans le contexte fourni."
        )
        risk_meaning = "Une valeur plus elevee peut indiquer un risque plus important selon la metrique."
        cfa_note = "Concept utile pour relier rendement, risque et contraintes de portefeuille."
    else:
        explanation = f"{metric} measures a risk or performance dimension in {request.module_name}."
        interpretation = (
            f"The observed value is {value}. It should be interpreted with the supplied context."
            if value is not None
            else "The value is unavailable in the supplied context."
        )
        risk_meaning = "A higher value may indicate greater risk depending on the metric."
        cfa_note = "Useful for connecting return, risk and portfolio constraints."
    return AthenaMetricExplanationResponse(
        explanation=explanation,
        interpretation=interpretation,
        risk_meaning=risk_meaning,
        limitations=[provider_unavailable_limitation(request.language)],
        cfa_note=cfa_note,
        disclaimer=fallback_disclaimer(request.language),
        generated_by="deterministic_fallback",
    )


def _module_points(request: AthenaIntelligenceRequest) -> dict[str, Any]:
    if request.module_name == "risk_monitor":
        return risk_monitor_points(request.payload, request.language, request.max_points)
    if request.module_name == "volatility_lab":
        return volatility_points(request.payload, request.language, request.max_points)
    if request.module_name == "options_pricing_lab":
        return options_points(request.payload, request.language, request.max_points)
    if request.module_name == "rates_lab":
        return rates_points(request.payload, request.language, request.max_points)
    if request.module_name == "trade_simulator":
        return trade_points(request.payload, request.language, request.max_points)
    return generic_points(
        request.payload,
        request.module_name,
        request.language,
        request.max_points,
    )


def _payload_assumptions(payload: dict[str, Any]) -> list[str]:
    assumptions = payload.get("assumptions")
    if isinstance(assumptions, dict):
        values: list[str] = []
        for value in assumptions.values():
            if isinstance(value, list):
                values.extend(str(item) for item in value)
            else:
                values.append(str(value))
        return values
    if isinstance(assumptions, list):
        return [str(item) for item in assumptions]
    methodology = payload.get("methodology")
    if isinstance(methodology, dict):
        raw = methodology.get("assumptions")
        if isinstance(raw, list):
            return [str(item) for item in raw]
    return []


def _payload_limitations(payload: dict[str, Any]) -> list[str]:
    limitations = payload.get("limitations")
    if isinstance(limitations, list):
        return [str(item) for item in limitations]
    methodology = payload.get("methodology")
    if isinstance(methodology, dict):
        raw = methodology.get("limitations")
        if isinstance(raw, list):
            return [str(item) for item in raw]
    data_quality = payload.get("data_quality")
    if isinstance(data_quality, dict):
        raw = data_quality.get("limitations")
        if isinstance(raw, list):
            return [str(item) for item in raw]
    return []


def _confidence_from_payload(payload: dict[str, Any]) -> str:
    fallback_used = payload.get("fallback_used")
    coverage = payload.get("coverage_ratio")
    if isinstance(payload.get("risk_monitor_payload"), dict):
        nested = payload["risk_monitor_payload"]
        fallback_used = nested.get("fallback_used", fallback_used)
        coverage = nested.get("coverage_ratio", coverage)
    if fallback_used:
        return "low"
    if isinstance(coverage, int | float) and coverage < 0.8:
        return "medium"
    return "high"
