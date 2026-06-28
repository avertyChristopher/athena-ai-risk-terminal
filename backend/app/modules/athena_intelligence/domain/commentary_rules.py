from __future__ import annotations

from typing import Any

from app.modules.athena_intelligence.domain.module_context import (
    as_float,
    compact_points,
    first_present,
    list_strings,
    nested_get,
)


def fallback_disclaimer(language: str) -> str:
    if language == "fr":
        return (
            "Ce commentaire est genere a des fins educatives et analytiques "
            "et ne constitue pas un conseil en investissement."
        )
    return (
        "This commentary is generated for educational and analytical purposes "
        "and is not investment advice."
    )


def provider_unavailable_limitation(language: str) -> str:
    if language == "fr":
        return (
            "Fournisseur IA indisponible. Commentaire genere avec les regles "
            "deterministes Athena."
        )
    return (
        "AI provider unavailable. Commentary generated with deterministic Athena rules."
    )


def risk_level_from_score(score: float | None) -> str:
    if score is None:
        return "medium"
    if score >= 80:
        return "critical"
    if score >= 65:
        return "high"
    if score >= 45:
        return "medium"
    return "low"


def metric_value(payload: dict[str, Any], metric_name: str) -> float | None:
    for metric in payload.get("risk_metrics", []):
        if str(metric.get("name", "")).lower() == metric_name.lower():
            return as_float(metric.get("value"))
    return None


def risk_monitor_points(
    payload: dict[str, Any],
    language: str,
    max_points: int,
) -> dict[str, list[str] | str]:
    score = as_float(payload.get("global_risk_score"))
    status = str(payload.get("global_risk_status") or risk_level_from_score(score))
    var_value = metric_value(payload, "VaR 95%")
    cvar_value = metric_value(payload, "CVaR 95%")
    volatility = metric_value(payload, "Portfolio volatility")
    max_drawdown = metric_value(payload, "Max drawdown")
    top_3 = as_float(nested_get(payload, "concentration", "top_3_weight"))
    largest = nested_get(payload, "concentration", "largest_position", "name")
    breaches = [
        str(item.get("explanation") or item.get("rule_name"))
        for item in payload.get("limit_breaches", [])
        if isinstance(item, dict)
    ]
    missing_symbols = list_strings(nested_get(payload, "risk_source", "symbols_missing"))

    if language == "fr":
        summary = f"Le portefeuille presente un profil de risque {status} avec un score de {score or 0:.0f}/100."
        drivers = [
            f"VaR 95% observee a {var_value:.2%}." if var_value is not None else "",
            f"CVaR 95% observee a {cvar_value:.2%}." if cvar_value is not None else "",
            f"Volatilite annuelle estimee a {volatility:.2%}." if volatility is not None else "",
            f"Top 3 holdings a {top_3:.2%}." if top_3 is not None else "",
            f"Plus grande ligne: {largest}." if largest else "",
        ]
        actions = [
            "Revoir les limites depassees avant toute decision de portefeuille.",
            "Surveiller la concentration et les scenarios de stress les plus defavorables.",
        ]
        risks = [
            "Risque de concentration eleve." if top_3 and top_3 > 0.65 else "",
            "Risque de perte extreme a surveiller." if cvar_value and cvar_value > 0.03 else "",
            "Couverture de donnees partielle." if missing_symbols else "",
        ]
    else:
        summary = f"The portfolio shows a {status} risk profile with a score of {score or 0:.0f}/100."
        drivers = [
            f"VaR 95% is {var_value:.2%}." if var_value is not None else "",
            f"CVaR 95% is {cvar_value:.2%}." if cvar_value is not None else "",
            f"Annualized volatility is {volatility:.2%}." if volatility is not None else "",
            f"Top 3 holdings weight is {top_3:.2%}." if top_3 is not None else "",
            f"Largest holding is {largest}." if largest else "",
        ]
        actions = [
            "Review breached limits before changing portfolio exposure.",
            "Monitor concentration and the most adverse stress scenarios.",
        ]
        risks = [
            "Elevated concentration risk." if top_3 and top_3 > 0.65 else "",
            "Tail-loss risk should be monitored." if cvar_value and cvar_value > 0.03 else "",
            "Partial market-data coverage affects confidence." if missing_symbols else "",
        ]

    return {
        "summary": summary,
        "main_risks": compact_points(risks, max_points),
        "risk_drivers": compact_points(drivers, max_points),
        "breaches": compact_points(breaches, max_points),
        "suggested_actions": compact_points(actions, max_points),
    }


def volatility_points(
    payload: dict[str, Any],
    language: str,
    max_points: int,
) -> dict[str, list[str] | str]:
    risk_payload = payload.get("risk_monitor_payload") if isinstance(payload.get("risk_monitor_payload"), dict) else payload
    symbol = risk_payload.get("symbol") or risk_payload.get("portfolio_id") or "portfolio"
    annualized_vol = as_float(risk_payload.get("annualized_volatility"))
    ewma = as_float(risk_payload.get("ewma_volatility"))
    beta = as_float(risk_payload.get("beta"))
    correlation = as_float(risk_payload.get("correlation"))
    coverage = as_float(risk_payload.get("coverage_ratio"))
    missing = list_strings(risk_payload.get("missing_symbols"))
    var_value = as_float(risk_payload.get("historical_var"))
    cvar_value = as_float(risk_payload.get("historical_cvar"))

    if language == "fr":
        summary = f"Volatility Lab signale un risque de marche pour {symbol} base sur les donnees disponibles."
        drivers = [
            f"Volatilite annualisee: {annualized_vol:.2%}." if annualized_vol is not None else "",
            f"Volatilite EWMA: {ewma:.2%}." if ewma is not None else "",
            f"Beta: {beta:.2f}." if beta is not None else "",
            f"Correlation: {correlation:.2f}." if correlation is not None else "",
            f"Couverture portefeuille: {coverage:.2%}." if coverage is not None else "",
        ]
        risks = [
            "Volatilite elevee a surveiller." if annualized_vol and annualized_vol > 0.25 else "",
            "Couverture de donnees partielle." if missing else "",
        ]
        actions = ["Comparer EWMA, VaR/CVaR et drawdown avant de valider le niveau de risque."]
    else:
        summary = f"Volatility Lab identifies market risk for {symbol} using the available return history."
        drivers = [
            f"Annualized volatility is {annualized_vol:.2%}." if annualized_vol is not None else "",
            f"EWMA volatility is {ewma:.2%}." if ewma is not None else "",
            f"Beta is {beta:.2f}." if beta is not None else "",
            f"Correlation is {correlation:.2f}." if correlation is not None else "",
            f"Portfolio coverage is {coverage:.2%}." if coverage is not None else "",
        ]
        risks = [
            "Elevated realized volatility may require monitoring." if annualized_vol and annualized_vol > 0.25 else "",
            "Partial data coverage affects covariance and VaR confidence." if missing else "",
        ]
        actions = ["Compare EWMA, VaR/CVaR and drawdown before validating the risk level."]

    if var_value is not None:
        drivers.append(f"Historical VaR: {var_value:.2%}.")
    if cvar_value is not None:
        drivers.append(f"Historical CVaR: {cvar_value:.2%}.")

    return {
        "summary": summary,
        "main_risks": compact_points(risks, max_points),
        "risk_drivers": compact_points(drivers, max_points),
        "breaches": [],
        "suggested_actions": compact_points(actions, max_points),
    }


def options_points(
    payload: dict[str, Any],
    language: str,
    max_points: int,
) -> dict[str, list[str] | str]:
    risk_payload = payload.get("risk_payload") if isinstance(payload.get("risk_payload"), dict) else payload
    symbol = risk_payload.get("underlying_symbol") or "underlying"
    strategy = risk_payload.get("strategy_name") or risk_payload.get("option_type") or "option"
    delta = as_float(risk_payload.get("delta"))
    gamma = as_float(risk_payload.get("gamma"))
    theta = as_float(risk_payload.get("theta"))
    vega = as_float(risk_payload.get("vega"))
    max_loss = as_float(risk_payload.get("max_loss"))
    max_profit = as_float(risk_payload.get("max_profit"))
    breakevens = risk_payload.get("breakeven_points") or []

    if language == "fr":
        summary = f"Le payload options pour {symbol} met en avant le risque de Greeks et le profil de payoff de {strategy}."
        risks = [
            "Theta negatif: la valeur temps peut se degrader." if theta is not None and theta < 0 else "",
            "Vega significatif: la strategie reste sensible a la volatilite implicite." if vega and abs(vega) > 1 else "",
            "Perte maximale non bornee ou inconnue." if max_loss is None else "",
        ]
        actions = ["Revoir Delta, Gamma, Vega et perte maximale avant toute integration portefeuille."]
    else:
        summary = f"The options payload for {symbol} highlights Greeks exposure and the payoff profile for {strategy}."
        risks = [
            "Negative Theta suggests time decay should be monitored." if theta is not None and theta < 0 else "",
            "Material Vega exposure suggests sensitivity to implied volatility." if vega and abs(vega) > 1 else "",
            "Maximum loss is unbounded or unavailable." if max_loss is None else "",
        ]
        actions = ["Review Delta, Gamma, Vega and maximum loss before adding the exposure to a portfolio."]

    drivers = [
        f"Delta: {delta:.3f}." if delta is not None else "",
        f"Gamma: {gamma:.4f}." if gamma is not None else "",
        f"Theta: {theta:.3f}." if theta is not None else "",
        f"Vega: {vega:.3f}." if vega is not None else "",
        f"Max loss: {max_loss:.2f}." if max_loss is not None else "",
        f"Max profit: {max_profit:.2f}." if max_profit is not None else "",
        f"Breakevens: {', '.join(str(point) for point in breakevens)}." if breakevens else "",
    ]
    return {
        "summary": summary,
        "main_risks": compact_points(risks, max_points),
        "risk_drivers": compact_points(drivers, max_points),
        "breaches": [],
        "suggested_actions": compact_points(actions, max_points),
    }


def rates_points(
    payload: dict[str, Any],
    language: str,
    max_points: int,
) -> dict[str, list[str] | str]:
    risk_payload = payload.get("rates_risk_payload") if isinstance(payload.get("rates_risk_payload"), dict) else payload
    duration = as_float(first_present(risk_payload, [("modified_duration",), ("macaulay_duration",)]))
    convexity = as_float(risk_payload.get("convexity"))
    dv01 = as_float(risk_payload.get("dv01"))
    ytm = as_float(risk_payload.get("ytm"))
    shock_loss = as_float(risk_payload.get("estimated_rate_shock_loss"))
    shock_bps = as_float(risk_payload.get("rate_shock_bps"))

    if language == "fr":
        summary = "Le payload Rates Lab met en evidence la sensibilite taux via duration, convexite et DV01."
        risks = [
            "Duration elevee: sensibilite taux importante." if duration and duration >= 7 else "",
            "Scenario de taux defavorable." if shock_loss and shock_loss < 0 else "",
        ]
        actions = ["Revoir DV01, duration et perte estimee avant d'augmenter l'exposition taux."]
    else:
        summary = "The Rates Lab payload highlights interest-rate sensitivity through duration, convexity and DV01."
        risks = [
            "High duration indicates material interest-rate sensitivity." if duration and duration >= 7 else "",
            "The supplied rate scenario implies an adverse loss." if shock_loss and shock_loss < 0 else "",
        ]
        actions = ["Review DV01, duration and estimated rate-shock loss before increasing rate exposure."]

    drivers = [
        f"Modified duration: {duration:.3f}." if duration is not None else "",
        f"Convexity: {convexity:.3f}." if convexity is not None else "",
        f"DV01: {dv01:.2f}." if dv01 is not None else "",
        f"YTM: {ytm:.2%}." if ytm is not None else "",
        f"Rate shock: {shock_bps:.0f} bps." if shock_bps is not None else "",
        f"Estimated rate-shock loss: {shock_loss:.2f}." if shock_loss is not None else "",
    ]
    return {
        "summary": summary,
        "main_risks": compact_points(risks, max_points),
        "risk_drivers": compact_points(drivers, max_points),
        "breaches": [],
        "suggested_actions": compact_points(actions, max_points),
    }


def trade_points(
    payload: dict[str, Any],
    language: str,
    max_points: int,
) -> dict[str, list[str] | str]:
    impact = payload.get("trade_impact_payload") if isinstance(payload.get("trade_impact_payload"), dict) else payload
    action = impact.get("action") or "trade"
    symbol = impact.get("symbol") or "symbol"
    suitability = str(impact.get("suitability_status") or nested_get(payload, "suitability_review", "status") or "review")
    constraints = impact.get("constraints") or payload.get("constraints_warnings") or []
    cash_after = as_float(nested_get(payload, "trade_ticket", "estimated_cash_after_trade"))
    before_vol = as_float(nested_get(impact, "before_risk", "portfolio_volatility"))
    after_vol = as_float(nested_get(impact, "after_risk", "portfolio_volatility"))
    costs = as_float(nested_get(impact, "transaction_costs", "total_implementation_cost"))

    if language == "fr":
        summary = f"La simulation {action} sur {symbol} donne un statut de suitability: {suitability}."
        risks = [
            "Contraintes detectees dans la simulation." if constraints else "",
            "La volatilite apres trade augmente." if before_vol is not None and after_vol is not None and after_vol > before_vol else "",
        ]
        actions = ["Revoir suitability, contraintes et couts avant toute execution reelle."]
    else:
        summary = f"The {action} simulation for {symbol} returns a suitability status of {suitability}."
        risks = [
            "The simulation detected constraint warnings." if constraints else "",
            "Post-trade volatility increases." if before_vol is not None and after_vol is not None and after_vol > before_vol else "",
        ]
        actions = ["Review suitability, constraints and costs before any real execution."]

    breaches = [
        str(item.get("message") or item.get("name"))
        for item in constraints
        if isinstance(item, dict)
    ]
    drivers = [
        f"Cash after trade: {cash_after:.2f}." if cash_after is not None else "",
        f"Before volatility: {before_vol:.2%}." if before_vol is not None else "",
        f"After volatility: {after_vol:.2%}." if after_vol is not None else "",
        f"Estimated implementation cost: {costs:.2f}." if costs is not None else "",
    ]
    return {
        "summary": summary,
        "main_risks": compact_points(risks, max_points),
        "risk_drivers": compact_points(drivers, max_points),
        "breaches": compact_points(breaches, max_points),
        "suggested_actions": compact_points(actions, max_points),
    }


def pnl_points(
    payload: dict[str, Any],
    language: str,
    max_points: int,
) -> dict[str, list[str] | str]:
    total_pnl = as_float(payload.get("total_pnl"))
    total_return = as_float(payload.get("total_pnl_percent"))
    realized = as_float(payload.get("realized_pnl"))
    unrealized = as_float(payload.get("unrealized_pnl"))
    income = as_float(payload.get("income_pnl"))
    active_return = as_float(nested_get(payload, "benchmark_comparison", "active_return"))
    winners = payload.get("top_winners") if isinstance(payload.get("top_winners"), list) else []
    losers = payload.get("top_losers") if isinstance(payload.get("top_losers"), list) else []
    top_winner = winners[0].get("symbol") if winners and isinstance(winners[0], dict) else None
    top_loser = losers[0].get("symbol") if losers and isinstance(losers[0], dict) else None
    warnings = list_strings(payload.get("warnings"))

    if language == "fr":
        direction = "positif" if (total_pnl or 0) >= 0 else "negatif"
        summary = f"Le portefeuille affiche un P&L {direction} de {total_pnl or 0:,.0f}, soit {total_return or 0:.2%} sur la periode."
        drivers = [
            f"Meilleur contributeur: {top_winner}." if top_winner else "",
            f"Pire contributeur: {top_loser}." if top_loser else "",
            f"Rendement actif vs benchmark: {active_return:.2%}." if active_return is not None else "",
            f"P&L realise: {realized:,.0f}; P&L non realise: {unrealized:,.0f}." if realized is not None and unrealized is not None else "",
            f"Revenus estimes: {income:,.0f}." if income is not None else "",
        ]
        risks = [
            "Performance concentree sur peu de lignes." if top_winner and top_loser else "",
            "Certaines donnees sources reposent sur des hypotheses demo." if warnings else "",
        ]
        actions = [
            "Verifier les hypotheses de prix, revenus, couts et benchmark avant interpretation.",
            "Comparer les contributions par position, secteur et classe d'actifs.",
        ]
    else:
        direction = "positive" if (total_pnl or 0) >= 0 else "negative"
        summary = f"The portfolio generated {direction} P&L of {total_pnl or 0:,.0f}, or {total_return or 0:.2%}, over the period."
        drivers = [
            f"Top contributor: {top_winner}." if top_winner else "",
            f"Worst contributor: {top_loser}." if top_loser else "",
            f"Active return versus benchmark: {active_return:.2%}." if active_return is not None else "",
            f"Realized P&L: {realized:,.0f}; unrealized P&L: {unrealized:,.0f}." if realized is not None and unrealized is not None else "",
            f"Estimated income: {income:,.0f}." if income is not None else "",
        ]
        risks = [
            "Performance may be concentrated in a small number of positions." if top_winner and top_loser else "",
            "Some source data relies on deterministic demo assumptions." if warnings else "",
        ]
        actions = [
            "Review price, income, cost and benchmark assumptions before interpretation.",
            "Compare position, sector and asset-class contributions.",
        ]
    return {
        "summary": summary,
        "main_risks": compact_points(risks + warnings, max_points),
        "risk_drivers": compact_points(drivers, max_points),
        "breaches": [],
        "suggested_actions": compact_points(actions, max_points),
    }


def reconciliation_points(
    payload: dict[str, Any],
    language: str,
    max_points: int,
) -> dict[str, list[str] | str]:
    status = str(payload.get("overall_status") or "unknown")
    total_breaks = as_float(payload.get("total_breaks")) or 0.0
    critical_breaks = as_float(payload.get("critical_breaks")) or 0.0
    breaks_by_type = payload.get("breaks_by_type") if isinstance(payload.get("breaks_by_type"), dict) else {}
    breaks_by_severity = payload.get("breaks_by_severity") if isinstance(payload.get("breaks_by_severity"), dict) else {}
    unresolved = list_strings(payload.get("unresolved_items"))
    warnings = list_strings(payload.get("warnings"))
    top_types = sorted(breaks_by_type.items(), key=lambda item: int(item[1]), reverse=True)
    top_severities = sorted(breaks_by_severity.items(), key=lambda item: int(item[1]), reverse=True)

    if language == "fr":
        summary = f"Le run de reconciliation affiche le statut {status} avec {total_breaks:.0f} ecart(s), dont {critical_breaks:.0f} critique(s)."
        drivers = [
            f"Type d'ecart dominant: {top_types[0][0]} ({top_types[0][1]})." if top_types else "",
            f"Severite dominante: {top_severities[0][0]} ({top_severities[0][1]})." if top_severities else "",
            "Les ecarts ouverts doivent etre revus avant de considerer le portefeuille reconcilie." if total_breaks else "",
        ]
        risks = [
            "Ecart critique a traiter immediatement." if critical_breaks else "",
            "Ecarts de position ou P&L peuvent indiquer un trade manquant ou un decalage de settlement." if unresolved else "",
            "Donnees demo custodian utilisees." if warnings else "",
        ]
        actions = [
            "Prioriser les ecarts high/critical et documenter les decisions de revue.",
            "Verifier les trades, le cash, les prix et le P&L inexplique.",
        ]
    else:
        summary = f"The reconciliation run is {status} with {total_breaks:.0f} break(s), including {critical_breaks:.0f} critical break(s)."
        drivers = [
            f"Dominant break type: {top_types[0][0]} ({top_types[0][1]})." if top_types else "",
            f"Dominant severity: {top_severities[0][0]} ({top_severities[0][1]})." if top_severities else "",
            "Open breaks should be reviewed before considering the portfolio reconciled." if total_breaks else "",
        ]
        risks = [
            "Critical break requires immediate review." if critical_breaks else "",
            "Position or P&L breaks may indicate missing trades or settlement timing." if unresolved else "",
            "Demo custodian reference data is being used." if warnings else "",
        ]
        actions = [
            "Prioritize high and critical breaks and document review decisions.",
            "Review trades, cash, prices and unexplained P&L drivers.",
        ]
    return {
        "summary": summary,
        "main_risks": compact_points(risks + unresolved + warnings, max_points),
        "risk_drivers": compact_points(drivers, max_points),
        "breaches": compact_points(unresolved, max_points),
        "suggested_actions": compact_points(actions, max_points),
    }


def generic_points(
    payload: dict[str, Any],
    module_name: str,
    language: str,
    max_points: int,
) -> dict[str, list[str] | str]:
    warnings = compact_points(list_strings(payload.get("warnings")), max_points)
    data_quality = payload.get("data_quality") if isinstance(payload.get("data_quality"), dict) else {}
    missing = list_strings(data_quality.get("missing_fields"))
    if language == "fr":
        summary = f"Athena a genere une synthese analytique pour {module_name} a partir du payload structure."
        actions = ["Verifier les hypotheses et les donnees manquantes avant interpretation."]
    else:
        summary = f"Athena generated analytical commentary for {module_name} from the structured payload."
        actions = ["Review assumptions and missing data before interpretation."]
    return {
        "summary": summary,
        "main_risks": compact_points(warnings + missing, max_points),
        "risk_drivers": compact_points(list(payload.keys())[:max_points], max_points),
        "breaches": [],
        "suggested_actions": actions,
    }


def anomaly_points(
    payload: dict[str, Any],
    language: str,
    max_points: int,
) -> dict[str, list[str] | str]:
    top = payload.get("top_anomalies") if isinstance(payload.get("top_anomalies"), list) else []
    anomalies_detected = as_float(payload.get("anomalies_detected")) or 0
    highest = payload.get("highest_severity") or "none"
    if language == "fr":
        summary = (
            f"Athena a detecte {anomalies_detected:.0f} anomalie(s) avec une severite maximale {highest}. "
            "Le scan est deterministe et sert a prioriser la revue risque et operationnelle."
        )
        fallback_action = "Prioriser les anomalies critiques et documenter les decisions de revue."
    else:
        summary = (
            f"Athena detected {anomalies_detected:.0f} anomaly/anomalies with highest severity {highest}. "
            "The scan is deterministic and supports risk and operational review prioritization."
        )
        fallback_action = "Prioritize critical anomalies and document review decisions."
    risks = []
    drivers = []
    breaches = []
    actions = []
    for item in top:
        if not isinstance(item, dict):
            continue
        title = str(item.get("title") or "Anomaly")
        severity = str(item.get("severity") or "unknown")
        source = str(item.get("source_module") or "source")
        category = str(item.get("category") or "category")
        risks.append(f"{severity}: {title} ({source})")
        drivers.append(f"{category} / {source}")
        if severity in {"high", "critical"}:
            breaches.append(f"{severity}: {title}")
        action = item.get("suggested_action")
        if action:
            actions.append(str(action))
    return {
        "summary": summary,
        "main_risks": compact_points(risks, max_points),
        "risk_drivers": compact_points(drivers, max_points),
        "breaches": compact_points(breaches, max_points),
        "suggested_actions": compact_points(actions or [fallback_action], max_points),
    }
