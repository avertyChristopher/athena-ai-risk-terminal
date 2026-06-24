from __future__ import annotations

from typing import Any


def extract_limit_metrics(
    source_module: str,
    payload: dict[str, Any],
) -> tuple[dict[str, float | bool], list[str]]:
    metrics: dict[str, float | bool] = {}
    warnings: list[str] = []
    _extract_generic(metrics, payload)
    if source_module == "portfolio_builder":
        _extract_portfolio_builder(metrics, payload)
    elif source_module == "risk_monitor":
        _extract_risk_monitor(metrics, payload)
    elif source_module == "volatility_lab":
        _extract_volatility_lab(metrics, payload)
    elif source_module == "options_pricing_lab":
        _extract_options_pricing_lab(metrics, payload)
    elif source_module == "rates_lab":
        _extract_rates_lab(metrics, payload)
    elif source_module == "stress_testing":
        _extract_stress_testing(metrics, payload)
    elif source_module == "trade_simulator":
        _extract_trade_simulator(metrics, payload)

    if not metrics:
        warnings.append(f"No recognizable limit metrics found for source module '{source_module}'.")
    return metrics, warnings


def source_module_cards() -> list[dict[str, object]]:
    return [
        _card(
            "portfolio_builder",
            "Portfolio Builder",
            [
                "single_position_weight",
                "top_3_concentration",
                "sector_exposure",
                "asset_class_exposure",
                "cash_weight",
            ],
        ),
        _card(
            "risk_monitor",
            "Risk Monitor",
            [
                "var_95",
                "cvar_95",
                "portfolio_volatility",
                "max_drawdown",
                "tracking_error",
                "risk_score",
            ],
        ),
        _card(
            "volatility_lab",
            "Volatility Lab",
            ["realized_volatility", "ewma_volatility", "var_95", "cvar_95", "beta"],
        ),
        _card(
            "options_pricing_lab",
            "Options Pricing Lab",
            [
                "delta_adjusted_exposure",
                "vega_exposure",
                "option_max_loss",
                "unlimited_loss",
            ],
        ),
        _card(
            "rates_lab",
            "Rates Lab",
            ["duration", "modified_duration", "dv01", "rate_shock_loss_100bps"],
        ),
        _card(
            "stress_testing",
            "Stress Testing",
            ["single_scenario_loss", "stress_loss_severe", "stressed_var", "stressed_cvar"],
        ),
        _card(
            "trade_simulator",
            "Trade Simulator",
            [
                "trade_turnover",
                "cash_after_trade",
                "post_trade_single_position_weight",
                "post_trade_sector_exposure",
            ],
        ),
    ]


def _extract_generic(metrics: dict[str, float | bool], payload: dict[str, Any]) -> None:
    aliases = {
        "single_position_weight": ["single_position_weight", "largest_position_weight"],
        "top_3_concentration": ["top_3_concentration", "top_3_weight"],
        "sector_exposure": ["sector_exposure", "largest_sector_weight"],
        "asset_class_exposure": ["asset_class_exposure", "asset_type_exposure"],
        "cash_weight": ["cash_weight", "cash_allocation"],
        "portfolio_volatility": ["portfolio_volatility", "annualized_volatility"],
        "max_drawdown": ["max_drawdown"],
        "var_95": ["var_95", "historical_var", "parametric_var"],
        "cvar_95": ["cvar_95", "historical_cvar", "parametric_cvar"],
        "tracking_error": ["tracking_error"],
        "beta": ["beta"],
        "risk_score": ["risk_score", "global_risk_score"],
        "duration": ["duration", "macaulay_duration", "weighted_average_duration"],
        "modified_duration": ["modified_duration"],
        "dv01": ["dv01", "estimated_portfolio_dv01"],
        "delta_adjusted_exposure": ["delta_adjusted_exposure"],
        "vega_exposure": ["vega_exposure", "vega", "aggregate_vega"],
        "option_max_loss": ["option_max_loss", "max_loss"],
        "short_option_exposure": ["short_option_exposure"],
        "trade_turnover": ["trade_turnover", "turnover"],
        "cash_after_trade": ["cash_after_trade", "estimated_cash_after_trade_weight"],
        "post_trade_single_position_weight": ["post_trade_single_position_weight"],
        "post_trade_sector_exposure": ["post_trade_sector_exposure"],
        "single_scenario_loss": ["single_scenario_loss", "percent_loss"],
        "stress_loss_moderate": ["stress_loss_moderate"],
        "stress_loss_severe": ["stress_loss_severe"],
        "rate_shock_loss_100bps": ["rate_shock_loss_100bps"],
    }
    flattened = _flatten(payload)
    for metric_key, paths in aliases.items():
        for path in paths:
            value = _as_metric(flattened.get(path))
            if value is not None:
                metrics[metric_key] = _normalize_loss(metric_key, value)
                break
    unlimited = _detect_unlimited_loss(payload)
    if unlimited is not None:
        metrics["unlimited_loss"] = unlimited


def _extract_portfolio_builder(metrics: dict[str, float | bool], payload: dict[str, Any]) -> None:
    concentration = _dict(payload.get("concentration"))
    largest = _dict(concentration.get("largest_position") or payload.get("largest_position"))
    _set_number(metrics, "single_position_weight", largest.get("weight"))
    _set_number(metrics, "top_3_concentration", concentration.get("top_3_weight"))
    sector_values = _weights_from_exposures(
        concentration.get("sector_exposures")
        or payload.get("sector_exposures")
        or payload.get("sector_allocation")
    )
    if sector_values:
        metrics["sector_exposure"] = max(sector_values)
    asset_values = _weights_from_exposures(
        concentration.get("asset_type_exposures")
        or payload.get("asset_class_exposures")
        or payload.get("asset_allocation")
    )
    if asset_values:
        metrics["asset_class_exposure"] = max(asset_values)
    _set_number(metrics, "cash_weight", concentration.get("cash_weight") or payload.get("cash_weight"))


def _extract_risk_monitor(metrics: dict[str, float | bool], payload: dict[str, Any]) -> None:
    _set_number(metrics, "risk_score", payload.get("global_risk_score"))
    concentration = _dict(payload.get("concentration"))
    if concentration:
        _extract_portfolio_builder(metrics, {"concentration": concentration})
    benchmark = _dict(payload.get("benchmark_risk"))
    _set_number(metrics, "tracking_error", benchmark.get("tracking_error"))
    _set_number(metrics, "beta", benchmark.get("beta"))
    for item in payload.get("risk_metrics", []) if isinstance(payload.get("risk_metrics"), list) else []:
        metric = _dict(item)
        name = str(metric.get("name", "")).lower()
        value = _as_metric(metric.get("value"))
        if value is None:
            continue
        if "cvar" in name:
            metrics["cvar_95"] = abs(float(value))
        elif "var" in name:
            metrics["var_95"] = abs(float(value))
        elif "volatility" in name:
            metrics["portfolio_volatility"] = abs(float(value))
        elif "drawdown" in name:
            metrics["max_drawdown"] = abs(float(value))
        elif "tracking" in name:
            metrics["tracking_error"] = abs(float(value))


def _extract_volatility_lab(metrics: dict[str, float | bool], payload: dict[str, Any]) -> None:
    volatility = _dict(payload.get("volatility_summary"))
    _set_number(metrics, "portfolio_volatility", volatility.get("annualized_volatility"))
    _set_number(metrics, "realized_volatility", volatility.get("realized_volatility"))
    ewma = _dict(payload.get("ewma_volatility"))
    _set_number(metrics, "portfolio_volatility", ewma.get("latest_volatility"))
    var_models = _dict(payload.get("var_models"))
    _set_number(metrics, "var_95", var_models.get("historical_var") or var_models.get("parametric_var"))
    _set_number(metrics, "cvar_95", var_models.get("historical_cvar") or var_models.get("parametric_cvar"))
    downside = _dict(payload.get("downside_risk"))
    _set_number(metrics, "max_drawdown", downside.get("max_drawdown"))
    benchmark = _dict(payload.get("benchmark_risk"))
    _set_number(metrics, "beta", benchmark.get("beta"))
    coverage = _dict(payload.get("portfolio_coverage"))
    _set_number(metrics, "coverage_ratio", coverage.get("coverage_ratio"))


def _extract_options_pricing_lab(metrics: dict[str, float | bool], payload: dict[str, Any]) -> None:
    risk_payload = _dict(payload.get("risk_payload")) or payload
    greeks = _dict(payload.get("greeks"))
    aggregate = _dict(payload.get("aggregate_greeks"))
    _set_number(
        metrics,
        "delta_adjusted_exposure",
        risk_payload.get("delta_adjusted_exposure")
        or greeks.get("delta_adjusted_exposure")
        or aggregate.get("delta_adjusted_exposure"),
    )
    _set_number(metrics, "vega_exposure", risk_payload.get("vega") or greeks.get("position_vega") or aggregate.get("aggregate_vega"))
    payoff = _dict(payload.get("payoff_summary"))
    max_loss = risk_payload.get("max_loss") or payoff.get("max_loss")
    if isinstance(payload.get("max_loss"), dict):
        max_loss = _dict(payload["max_loss"]).get("value")
    _set_number(metrics, "option_max_loss", max_loss)
    if _detect_unlimited_loss(payload):
        metrics["unlimited_loss"] = True
    if str(payload.get("position_side", "")).lower() == "short":
        _set_number(metrics, "short_option_exposure", risk_payload.get("delta_adjusted_exposure"))


def _extract_rates_lab(metrics: dict[str, float | bool], payload: dict[str, Any]) -> None:
    rates_payload = _dict(payload.get("rates_risk_payload")) or payload
    _set_number(metrics, "duration", payload.get("macaulay_duration") or payload.get("weighted_average_duration") or rates_payload.get("macaulay_duration"))
    _set_number(metrics, "modified_duration", payload.get("modified_duration") or rates_payload.get("modified_duration"))
    _set_number(metrics, "dv01", payload.get("dv01") or payload.get("estimated_portfolio_dv01") or rates_payload.get("dv01"))
    loss = (
        payload.get("estimated_rate_shock_loss")
        or rates_payload.get("rate_shock_loss")
        or rates_payload.get("curve_scenario_impact")
    )
    if loss is not None:
        base = payload.get("fixed_income_market_value") or payload.get("base_price") or rates_payload.get("clean_price")
        loss_value = _as_metric(loss)
        base_value = _as_metric(base)
        if loss_value is not None:
            metrics["rate_shock_loss_100bps"] = abs(loss_value / base_value) if base_value else abs(loss_value)


def _extract_stress_testing(metrics: dict[str, float | bool], payload: dict[str, Any]) -> None:
    loss = _as_metric(payload.get("percent_loss"))
    if loss is not None:
        metrics["single_scenario_loss"] = abs(loss)
        severity = str(_dict(payload.get("severity")).get("severity") or payload.get("severity", "")).lower()
        if severity in {"critical", "severe", "high"}:
            metrics["stress_loss_severe"] = abs(loss)
        else:
            metrics["stress_loss_moderate"] = abs(loss)
    for metric in payload.get("risk_metrics", []) if isinstance(payload.get("risk_metrics"), list) else []:
        item = _dict(metric)
        name = str(item.get("metric", "")).lower()
        after = _as_metric(item.get("after"))
        if after is None:
            continue
        if "cvar" in name:
            metrics["stressed_cvar"] = abs(after)
        elif "var" in name:
            metrics["stressed_var"] = abs(after)
        elif "volatility" in name:
            metrics["portfolio_volatility"] = abs(after)


def _extract_trade_simulator(metrics: dict[str, float | bool], payload: dict[str, Any]) -> None:
    ticket = _dict(payload.get("trade_ticket"))
    trade_value = _as_metric(ticket.get("gross_trade_value"))
    portfolio_value = _as_metric(payload.get("portfolio_value") or payload.get("total_value"))
    if trade_value is not None and portfolio_value:
        metrics["trade_turnover"] = abs(trade_value / portfolio_value)
    _set_number(metrics, "cash_after_trade", ticket.get("estimated_cash_after_trade_weight"))
    impact = _dict(payload.get("trade_impact_payload"))
    after_weights = _dict(impact.get("after_weights"))
    if after_weights:
        values = [_as_metric(value) for value in after_weights.values()]
        numeric = [abs(float(value)) for value in values if value is not None]
        if numeric:
            metrics["post_trade_single_position_weight"] = max(numeric)
    for warning in payload.get("constraints_warnings", []) if isinstance(payload.get("constraints_warnings"), list) else []:
        item = _dict(warning)
        name = str(item.get("name", "")).lower()
        actual = _as_metric(item.get("actual"))
        if actual is None:
            continue
        if "sector" in name:
            metrics["post_trade_sector_exposure"] = actual
        if "single" in name or "position" in name:
            metrics["post_trade_single_position_weight"] = actual


def _flatten(data: dict[str, Any]) -> dict[str, Any]:
    values: dict[str, Any] = {}

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            for key, nested in value.items():
                if key not in values:
                    values[key] = nested
                visit(nested)
        elif isinstance(value, list):
            for item in value:
                visit(item)

    visit(data)
    return values


def _weights_from_exposures(raw: Any) -> list[float]:
    if isinstance(raw, dict):
        return [float(value) for value in raw.values() if _as_metric(value) is not None]
    if isinstance(raw, list):
        weights: list[float] = []
        for item in raw:
            row = _dict(item)
            weight = _as_metric(row.get("weight") or row.get("value"))
            if weight is not None:
                weights.append(abs(weight))
        return weights
    return []


def _detect_unlimited_loss(payload: dict[str, Any]) -> bool | None:
    if isinstance(payload.get("unlimited_loss"), bool):
        return payload["unlimited_loss"]
    max_loss = payload.get("max_loss")
    if isinstance(max_loss, dict):
        loss_type = str(max_loss.get("type", "")).lower()
        if loss_type == "unlimited":
            return True
    payoff = _dict(payload.get("payoff_summary"))
    label = str(payoff.get("max_loss_label", "") or payoff.get("risk_note", "")).lower()
    if "unlimited" in label:
        return True
    return None


def _set_number(metrics: dict[str, float | bool], key: str, value: Any) -> None:
    number = _as_metric(value)
    if number is not None:
        metrics[key] = _normalize_loss(key, number)


def _normalize_loss(key: str, value: float | bool) -> float | bool:
    if isinstance(value, bool):
        return value
    if key in {
        "max_drawdown",
        "var_95",
        "cvar_95",
        "option_max_loss",
        "rate_shock_loss_100bps",
        "single_scenario_loss",
        "stress_loss_moderate",
        "stress_loss_severe",
    }:
        return abs(value)
    return value


def _as_metric(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, dict) and "value" in value:
        return _as_metric(value["value"])
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _card(module: str, display_name: str, metrics: list[str]) -> dict[str, object]:
    return {
        "module": module,
        "display_name": display_name,
        "connected": True,
        "payload_available": True,
        "metrics_provided": metrics,
        "warnings": [],
    }
