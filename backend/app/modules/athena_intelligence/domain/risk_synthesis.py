from __future__ import annotations

from typing import Any

from app.modules.athena_intelligence.domain.commentary_rules import (
    fallback_disclaimer,
    provider_unavailable_limitation,
    risk_level_from_score,
)
from app.modules.athena_intelligence.domain.module_context import (
    as_float,
    compact_points,
)


def synthesize_payloads(
    *,
    portfolio_id: str,
    payloads: dict[str, Any],
    language: str,
    max_points: int,
) -> dict[str, Any]:
    risk_payload = payloads.get("risk_analytics_payload") or {}
    options_payload = payloads.get("options_risk_payload") or {}
    rates_payload = payloads.get("rates_risk_payload") or {}
    trade_payload = payloads.get("trade_impact_payload") or {}
    score = as_float(risk_payload.get("global_risk_score"))
    volatility = as_float(risk_payload.get("annualized_volatility"))
    cvar_value = as_float(risk_payload.get("historical_cvar"))
    dv01 = as_float(rates_payload.get("dv01"))
    duration = as_float(rates_payload.get("modified_duration"))
    delta_exposure = as_float(options_payload.get("delta_adjusted_exposure"))
    suitability = trade_payload.get("suitability_status")
    overall = risk_level_from_score(score)

    if language == "fr":
        executive_summary = (
            f"Synthese Athena pour {portfolio_id}: le risque global est classe {overall} "
            "selon les payloads disponibles."
        )
        drivers = [
            f"Volatilite annualisee: {volatility:.2%}." if volatility is not None else "",
            f"CVaR historique: {cvar_value:.2%}." if cvar_value is not None else "",
            f"Duration taux: {duration:.2f}." if duration is not None else "",
            f"DV01: {dv01:.2f}." if dv01 is not None else "",
            f"Exposition delta options: {delta_exposure:.2f}." if delta_exposure is not None else "",
        ]
        findings = [
            "Les risques marche, taux et options doivent etre lus ensemble.",
            f"Suitability pre-trade: {suitability}." if suitability else "",
        ]
        actions = [
            "Prioriser les limites depassees et la concentration.",
            "Verifier les donnees manquantes avant une decision de portefeuille.",
        ]
    else:
        executive_summary = (
            f"Athena synthesis for {portfolio_id}: overall risk is classified as {overall} "
            "based on available payloads."
        )
        drivers = [
            f"Annualized volatility: {volatility:.2%}." if volatility is not None else "",
            f"Historical CVaR: {cvar_value:.2%}." if cvar_value is not None else "",
            f"Rates duration: {duration:.2f}." if duration is not None else "",
            f"DV01: {dv01:.2f}." if dv01 is not None else "",
            f"Options delta-adjusted exposure: {delta_exposure:.2f}." if delta_exposure is not None else "",
        ]
        findings = [
            "Market, rates and options risks should be reviewed together.",
            f"Pre-trade suitability: {suitability}." if suitability else "",
        ]
        actions = [
            "Prioritize breached limits and concentration drivers.",
            "Check missing data before portfolio decisions.",
        ]

    return {
        "executive_summary": executive_summary,
        "overall_risk_level": overall,
        "top_risk_drivers": compact_points(drivers, max_points),
        "cross_module_findings": compact_points(findings, max_points),
        "breached_limits": compact_points(
            [
                str(item.get("explanation") or item.get("rule_name"))
                for item in risk_payload.get("limit_breaches", [])
                if isinstance(item, dict)
            ],
            max_points,
        ),
        "portfolio_vulnerabilities": compact_points(
            [
                "Concentration risk" if score and score >= 65 else "",
                "Interest-rate sensitivity" if duration and duration >= 7 else "",
                "Options convexity/volatility exposure" if delta_exposure else "",
            ],
            max_points,
        ),
        "suggested_next_actions": compact_points(actions, max_points),
        "module_specific_notes": {
            "risk_monitor": compact_points([str(risk_payload.get("global_risk_status") or overall)], max_points),
            "rates_lab": compact_points([f"DV01 {dv01:.2f}" if dv01 is not None else ""], max_points),
            "options_pricing_lab": compact_points([f"Delta exposure {delta_exposure:.2f}" if delta_exposure is not None else ""], max_points),
            "trade_simulator": compact_points([str(suitability)] if suitability else [], max_points),
        },
        "assumptions": [
            "Cross-module synthesis uses only supplied structured payloads.",
        ],
        "limitations": [provider_unavailable_limitation(language)],
        "disclaimer": fallback_disclaimer(language),
    }
