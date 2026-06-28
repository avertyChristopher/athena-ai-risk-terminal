from __future__ import annotations

from typing import Any

from app.modules.reports_center.schemas import ReportSection, ReportType


def build_report_sections(report_type: ReportType, payloads: dict[str, Any]) -> list[ReportSection]:
    builders = {
        "portfolio_overview": _portfolio_sections,
        "risk_monitor": _risk_sections,
        "stress_testing": _stress_sections,
        "limit_breach": _limit_sections,
        "trade_suitability": _trade_sections,
        "fixed_income_exposure": _rates_sections,
        "options_risk": _options_sections,
        "pnl_attribution": _pnl_sections,
        "reconciliation": _reconciliation_sections,
        "ai_anomaly": _ai_anomaly_sections,
        "full_portfolio_risk_pack": _full_pack_sections,
    }
    return builders[report_type](payloads)


def _portfolio_sections(payloads: dict[str, Any]) -> list[ReportSection]:
    summary = payloads.get("portfolio_summary") or {}
    portfolio = payloads.get("portfolio") or {}
    allocations = payloads.get("allocations") or {}
    return [
        _section("executive_summary", "Executive summary", _portfolio_summary(summary), ["Portfolio Builder"], summary),
        _section("portfolio_profile", "Portfolio profile", str(portfolio.get("strategy_description") or "Portfolio profile snapshot."), ["Portfolio Builder"], portfolio),
        _section("holdings", "Holdings overview", "Current portfolio holdings captured at report generation.", ["Portfolio Builder"], table=payloads.get("holdings") or []),
        _section("asset_allocation", "Asset allocation", "Invested allocation by asset type.", ["Portfolio Builder"], table=allocations.get("asset_types") or []),
        _section("sector_allocation", "Sector allocation", "Invested allocation by sector.", ["Portfolio Builder"], table=allocations.get("sectors") or []),
        _section("geographic_allocation", "Geographic allocation", "Invested allocation by country.", ["Portfolio Builder"], table=allocations.get("countries") or []),
        _section("currency_allocation", "Currency allocation", "Invested allocation by currency.", ["Portfolio Builder"], table=allocations.get("currencies") or []),
        _section("concentration", "Concentration analysis", "Issuer and top-holdings concentration snapshot.", ["Portfolio Builder"], payloads.get("concentration") or {}),
        _section("data_quality", "Data quality", "Market Data coverage for report symbols.", ["Market Data"], payloads.get("market_data_coverage") or {}),
    ]


def _risk_sections(payloads: dict[str, Any]) -> list[ReportSection]:
    risk = payloads.get("risk_monitor") or {}
    return [
        _section("risk_score", "Risk score", f"Risk status: {risk.get('global_risk_status', 'Unavailable')}.", ["Risk Monitor"], {"global_risk_score": risk.get("global_risk_score"), "global_risk_status": risk.get("global_risk_status")}),
        _section("risk_metrics", "Risk metrics", "Volatility, VaR, CVaR, drawdown and tracking metrics.", ["Risk Monitor"], table=risk.get("risk_metrics") or []),
        _section("risk_contribution", "Risk contribution", "Largest risk contributors by asset and sector.", ["Risk Monitor", "Volatility Lab"], risk.get("risk_contribution") or {}),
        _section("benchmark_risk", "Benchmark active risk", "Benchmark beta, active exposure and tracking error.", ["Risk Monitor"], risk.get("benchmark_risk") or {}),
        _section("drivers", "Main risk drivers", "Primary deterministic risk drivers and warnings.", ["Risk Monitor"], {"main_drivers": risk.get("main_drivers", []), "alerts": risk.get("alerts", [])}),
        _section("breaches", "Risk warnings and breaches", "Risk Monitor limit breaches captured in the snapshot.", ["Risk Monitor", "Limit Center"], table=risk.get("limit_breaches") or []),
    ]


def _stress_sections(payloads: dict[str, Any]) -> list[ReportSection]:
    stress = payloads.get("stress_testing") or {}
    return [
        _section("scenario", "Scenario selected", "Selected stress scenario and shock assumptions.", ["Stress Testing"], stress.get("selected_scenario") or {}),
        _section("portfolio_impact", "Portfolio impact", "Base value, stressed value and loss estimate.", ["Stress Testing"], _pick(stress, ["base_portfolio_value", "stressed_portfolio_value", "dollar_loss", "percent_loss"])),
        _section("worst_contributors", "Worst contributors", "Positions with the largest stressed losses.", ["Stress Testing"], table=stress.get("worst_contributors") or []),
        _section("sector_impact", "Sector impact", "Sector-level stress impacts.", ["Stress Testing"], table=stress.get("sector_impacts") or []),
        _section("asset_class_impact", "Asset class impact", "Asset-class stress impacts.", ["Stress Testing"], table=stress.get("asset_class_impacts") or []),
        _section("severity", "Stress severity", "Stress severity and limit breaches triggered.", ["Stress Testing", "Limit Center"], {"severity": stress.get("severity"), "limit_breaches": stress.get("limit_breaches", [])}),
    ]


def _limit_sections(payloads: dict[str, Any]) -> list[ReportSection]:
    limits = payloads.get("limit_center") or {}
    return [
        _section("overall_status", "Overall limit status", f"Overall status: {limits.get('overall_status', 'Unavailable')}.", ["Limit Center"], {"overall_status": limits.get("overall_status"), "breach_count": len(limits.get("breaches", []))}),
        _section("breach_register", "Breach register", "Limit Center breach register captured for this report.", ["Limit Center"], table=limits.get("breaches") or []),
        _section("governance_actions", "Suggested governance actions", "Deterministic governance actions and commentary.", ["Limit Center", "Athena Intelligence"], {"warnings": limits.get("warnings", []), "commentary": limits.get("athena_ai_commentary")}),
    ]


def _trade_sections(payloads: dict[str, Any]) -> list[ReportSection]:
    trade = payloads.get("trade_simulator") or {}
    return [
        _section("trade_ticket", "Trade ticket", "Simulated trade ticket captured from Trade Simulator.", ["Trade Simulator"], trade.get("trade_ticket") or {}),
        _section("cost_analysis", "Cost analysis", "Estimated transaction and implementation costs.", ["Trade Simulator"], trade.get("transaction_cost_analysis") or {}),
        _section("suitability", "Suitability review", "Trade suitability and constraints.", ["Trade Simulator"], {"suitability_review": trade.get("suitability_review"), "constraints_warnings": trade.get("constraints_warnings", [])}),
        _section("post_trade_risk", "Projected post-trade risk", "Before/after risk impact from Trade Simulator.", ["Trade Simulator", "Risk Monitor"], trade.get("risk_impact") or {}),
    ]


def _rates_sections(payloads: dict[str, Any]) -> list[ReportSection]:
    rates = payloads.get("rates") or {}
    return [
        _section("fixed_income_holdings", "Fixed income holdings", "Bond-like portfolio exposures and duration assumptions.", ["Rates Lab"], table=rates.get("fixed_income_holdings") or []),
        _section("duration", "Duration and DV01", "Weighted duration, DV01/PVBP and rate-shock loss.", ["Rates Lab"], _pick(rates, ["fixed_income_allocation", "weighted_average_duration", "estimated_portfolio_dv01", "estimated_rate_shock_loss", "shock_bps"])),
        _section("data_quality", "Rates data quality", "Demo duration, curve and metadata quality notes.", ["Rates Lab"], rates.get("data_quality") or {}),
    ]


def _options_sections(payloads: dict[str, Any]) -> list[ReportSection]:
    options = payloads.get("options") or {}
    return [
        _section("pricing", "Option pricing model", "Black-Scholes, binomial and pricing summary.", ["Options Pricing Lab"], options.get("pricing_summary") or {}),
        _section("greeks", "Greeks", "Delta, gamma, theta, vega and rho risk snapshot.", ["Options Pricing Lab"], options.get("greeks") or {}),
        _section("payoff", "Payoff profile", "Payoff, max profit/loss and breakeven analytics.", ["Options Pricing Lab"], options.get("payoff_summary") or {}),
        _section("risk_payload", "Risk payload", "Options payload prepared for Risk Monitor and Limit Center.", ["Options Pricing Lab", "Risk Monitor"], options.get("risk_payload") or {}),
    ]


def _pnl_sections(payloads: dict[str, Any]) -> list[ReportSection]:
    pnl = payloads.get("pnl_attribution") or {}
    return [
        _section("portfolio_period", "Portfolio and period", "Portfolio, reporting period and generated snapshot.", ["P&L Attribution"], _pick(pnl, ["portfolio_id", "portfolio_name", "period", "generated_at"])),
        _section("total_pnl", "Total P&L", "Starting value, ending value, total P&L and return.", ["P&L Attribution"], _pick(pnl, ["starting_value", "ending_value", "total_pnl", "total_pnl_percent", "price_pnl", "income_pnl", "fees_and_costs", "fx_pnl"])),
        _section("realized_unrealized", "Realized vs unrealized P&L", "Realized, unrealized, income and cost split.", ["P&L Attribution"], _pick(pnl, ["realized_pnl", "unrealized_pnl", "income_pnl", "fees_and_costs"])),
        _section("position_pnl", "Position-level P&L", "Position-level P&L contributions and data source notes.", ["P&L Attribution", "Portfolio Builder", "Market Data"], table=pnl.get("position_contributions") or []),
        _section("asset_class_attribution", "Asset class attribution", "P&L aggregated by asset class.", ["P&L Attribution"], table=pnl.get("asset_class_contributions") or []),
        _section("sector_attribution", "Sector attribution", "P&L aggregated by sector.", ["P&L Attribution"], table=pnl.get("sector_contributions") or []),
        _section("benchmark_comparison", "Benchmark comparison", "Portfolio return, benchmark return and active return.", ["P&L Attribution", "Market Data"], pnl.get("benchmark_comparison") or {}),
        _section("fixed_income", "Fixed income contribution", "Duration, convexity, coupon income and residual rates P&L.", ["P&L Attribution", "Rates Lab"], table=pnl.get("fixed_income_effects") or []),
        _section("options", "Options contribution", "Greeks contribution and options availability notes.", ["P&L Attribution", "Options Pricing Lab"], pnl.get("options_effects") or {}),
        _section("trade_impact", "Trade impact", "Transaction costs, turnover, slippage and trade blotter status.", ["P&L Attribution", "Trade Simulator"], pnl.get("trade_effects") or {}),
        _section("methodology", "Methodology and limitations", "P&L attribution assumptions, data sources and limitations.", ["P&L Attribution"], {"methodology": pnl.get("methodology"), "limitations": pnl.get("limitations", []), "warnings": pnl.get("warnings", [])}),
    ]


def _reconciliation_sections(payloads: dict[str, Any]) -> list[ReportSection]:
    recon = payloads.get("reconciliation") or {}
    return [
        _section("overview", "Overall status", "Reconciliation status, break counts and source reference.", ["Reconciliation Center"], _pick(recon, ["overall_status", "total_breaks", "open_breaks", "critical_breaks", "reconciliation_date", "external_source"])),
        _section("checks", "Checks performed", "Checks selected for this reconciliation run.", ["Reconciliation Center"], {"checks_performed": recon.get("checks_performed", []), "breaks_by_type": recon.get("breaks_by_type", {}), "breaks_by_severity": recon.get("breaks_by_severity", {})}),
        _section("position_breaks", "Position breaks", "Position quantity and market value reconciliation results.", ["Portfolio Builder", "Reconciliation Center"], table=recon.get("position_breaks") or []),
        _section("cash_breaks", "Cash breaks", "Cash balance reconciliation against external reference.", ["Portfolio Builder", "Reconciliation Center"], table=recon.get("cash_breaks") or []),
        _section("price_breaks", "Price breaks", "Internal Market Data prices compared with external custodian prices.", ["Market Data", "Reconciliation Center"], table=recon.get("price_breaks") or []),
        _section("trade_breaks", "Trade breaks", "Trade blotter and pending trade reconciliation.", ["Trade Simulator", "Reconciliation Center"], table=recon.get("trade_breaks") or []),
        _section("pnl_breaks", "P&L breaks", "Calculated P&L compared with external value movement.", ["P&L Attribution", "Reconciliation Center"], table=recon.get("pnl_breaks") or []),
        _section("fx_breaks", "FX breaks", "FX rate and translation reconciliation.", ["Market Data", "Reconciliation Center"], table=recon.get("fx_breaks") or []),
        _section("break_register", "Break severity summary", "Break register with severity and review status.", ["Reconciliation Center"], table=recon.get("breaks") or []),
        _section("methodology", "Methodology and limitations", "Reconciliation tolerances, data sources, warnings and limitations.", ["Reconciliation Center"], {"methodology": recon.get("methodology"), "warnings": recon.get("warnings", []), "limitations": recon.get("limitations", [])}),
    ]


def _ai_anomaly_sections(payloads: dict[str, Any]) -> list[ReportSection]:
    anomalies = payloads.get("ai_anomaly") or {}
    records = anomalies.get("anomaly_records") or []
    methodology = anomalies.get("methodology") or {}
    commentary = anomalies.get("athena_ai_commentary") or payloads.get("athena_commentary") or {}
    source_modules = ["AI Anomaly Center"]
    review_status = _count_records(records, "status")
    top_anomalies = sorted(
        records,
        key=lambda item: float(item.get("anomaly_score") or 0),
        reverse=True,
    )[:10]
    return [
        _section(
            "executive_summary",
            "Executive summary",
            "Rule-based anomaly scan summary across Athena modules.",
            source_modules,
            _pick(
                anomalies,
                [
                    "scan_id",
                    "portfolio_id",
                    "scan_scope",
                    "total_records_scanned",
                    "anomalies_detected",
                    "highest_severity",
                    "generated_at",
                ],
            ),
        ),
        _section(
            "scan_scope",
            "Scan scope",
            "Scope, lookback window and source modules included in the anomaly scan.",
            source_modules,
            {
                "scan_scope": anomalies.get("scan_scope"),
                "lookback_days": anomalies.get("lookback_days"),
                "source_modules": methodology.get("source_modules", []),
                "warnings": anomalies.get("warnings", []),
            },
        ),
        _section(
            "anomalies_by_category",
            "Anomalies by category",
            "Detected anomalies grouped by monitoring category.",
            source_modules,
            anomalies.get("anomalies_by_category") or {},
        ),
        _section(
            "anomalies_by_severity",
            "Anomalies by severity",
            "Detected anomalies grouped by severity.",
            source_modules,
            anomalies.get("anomalies_by_severity") or {},
        ),
        _section(
            "top_anomalies",
            "Top anomalies",
            "Highest-scoring anomalies requiring review priority.",
            source_modules,
            table=top_anomalies,
        ),
        _section(
            "review_workflow",
            "Review workflow status",
            "Current anomaly review workflow status distribution.",
            source_modules,
            review_status,
        ),
        _section(
            "review_priorities",
            "Suggested review priorities",
            "Deterministic actions suggested by anomaly rules.",
            source_modules,
            table=[
                {
                    "anomaly_id": item.get("anomaly_id"),
                    "severity": item.get("severity"),
                    "source_module": item.get("source_module"),
                    "title": item.get("title"),
                    "suggested_action": item.get("suggested_action"),
                }
                for item in top_anomalies
            ],
        ),
        _section(
            "athena_commentary",
            "Athena Intelligence commentary",
            "Athena commentary summarizing anomaly patterns and limitations.",
            ["AI Anomaly Center", "Athena Intelligence"],
            commentary if isinstance(commentary, dict) else {"commentary": commentary},
        ),
        _section(
            "methodology",
            "Methodology and limitations",
            "Rule-based scoring methodology, confidence levels and demo limitations.",
            source_modules,
            {
                "methodology": methodology,
                "limitations": anomalies.get("limitations", []),
            },
        ),
    ]


def _full_pack_sections(payloads: dict[str, Any]) -> list[ReportSection]:
    sections: list[ReportSection] = []
    sections.extend(_portfolio_sections(payloads)[:3])
    sections.extend(_risk_sections(payloads)[:4])
    sections.extend(_rates_sections(payloads)[:2])
    sections.extend(_stress_sections(payloads)[:4])
    sections.extend(_limit_sections(payloads)[:2])
    return sections


def unavailable_section(section_id: str, title: str, source_modules: list[str]) -> ReportSection:
    return ReportSection(
        section_id=section_id,
        title=title,
        status="unavailable",
        summary="Unavailable. Requires source data.",
        source_modules=source_modules,
        warnings=["Requires source data."],
    )


def _section(
    section_id: str,
    title: str,
    summary: str,
    source_modules: list[str],
    metrics: dict[str, Any] | None = None,
    table: list[dict[str, Any]] | None = None,
) -> ReportSection:
    metrics = metrics or {}
    table = table or []
    if not metrics and not table:
        return unavailable_section(section_id, title, source_modules)
    return ReportSection(
        section_id=section_id,
        title=title,
        summary=summary,
        source_modules=source_modules,
        metrics=metrics,
        table=table,
    )


def _portfolio_summary(summary: dict[str, Any]) -> str:
    name = summary.get("name", "Selected portfolio")
    value = summary.get("total_value")
    risk_hint = "Snapshot includes holdings, allocation, concentration and Market Data coverage."
    if value is None:
        return f"{name}: portfolio summary unavailable. {risk_hint}"
    return f"{name} total value is {value:,.2f}. {risk_hint}"


def _pick(payload: dict[str, Any], keys: list[str]) -> dict[str, Any]:
    return {key: payload.get(key) for key in keys if key in payload}


def _count_records(records: list[dict[str, Any]], field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        value = str(record.get(field) or "unknown")
        counts[value] = counts.get(value, 0) + 1
    return counts
