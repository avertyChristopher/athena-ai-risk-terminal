import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from fastapi import HTTPException

from app.domain.equity import (
    calculate_asset_turnover,
    calculate_book_value_per_share,
    calculate_buyback_yield,
    calculate_current_ratio,
    calculate_debt_to_assets,
    calculate_debt_to_equity,
    calculate_dividend_discount_value,
    calculate_dividend_payout_ratio,
    calculate_dividend_yield,
    calculate_earnings_yield,
    calculate_ebit_margin,
    calculate_ebitda_margin,
    calculate_enterprise_value,
    calculate_ev_ebitda,
    calculate_ev_sales,
    calculate_forward_pe_ratio,
    calculate_free_cash_flow,
    calculate_free_cash_flow_margin,
    calculate_free_cash_flow_yield,
    calculate_free_float_market_cap,
    calculate_gordon_growth_value,
    calculate_gross_margin,
    calculate_implied_cost_of_equity,
    calculate_implied_growth_rate,
    calculate_interest_coverage,
    calculate_inventory_turnover,
    calculate_market_cap,
    calculate_market_to_book_value,
    calculate_margin_of_safety,
    calculate_net_debt,
    calculate_net_debt_to_ebitda,
    calculate_net_margin,
    calculate_operating_income_growth,
    calculate_operating_margin,
    calculate_pb_ratio,
    calculate_pe_ratio,
    calculate_peer_medians,
    calculate_peg_ratio,
    calculate_ps_ratio,
    calculate_quick_ratio,
    calculate_receivables_turnover,
    calculate_relative_performance_vs_benchmark,
    calculate_retention_ratio,
    calculate_revenue_growth,
    calculate_roa,
    calculate_roe,
    calculate_roic,
    calculate_sustainable_growth_rate,
    calculate_total_shareholder_yield,
    calculate_valuation_sensitivity_table,
    calculate_valuation_status,
    calculate_working_capital,
    classify_balance_sheet_quality,
    classify_dividend_profile,
    classify_equity_risk_profile,
    classify_equity_security_type,
    classify_growth_profile,
    classify_multiple_level,
    classify_profitability_quality,
    classify_valuation_profile,
    classify_valuation_status,
    compare_growth_to_peers,
    compare_multiple_to_peer_median,
    compare_profitability_to_peers,
    compare_valuation_to_peers,
    create_bull_base_bear_case_summary,
    create_equity_diagnostics_summary,
    create_peer_comparison_summary,
    create_watchlist_flags,
    normalize_fundamentals_snapshot,
    summarize_corporate_actions_profile,
    summarize_dividend_profile,
    summarize_equity_security_profile,
    summarize_share_repurchases_placeholder,
    summarize_stock_split_placeholder,
)
from app.schemas.equity_schema import (
    EquityBusinessModelResponse,
    EquityCorporateActionsResponse,
    EquityDiagnosticsResponse,
    EquityFundamentalsResponse,
    EquityGrowthResponse,
    EquityIndustryResponse,
    EquityOverviewResponse,
    EquityPeerComparisonResponse,
    EquityRatiosResponse,
    EquityRelativeValuationResponse,
    EquitySecurityProfileResponse,
    EquityValuationResponse,
    GgmValuationRequest,
    GgmValuationResponse,
    SensitivityCell,
    SensitivityRequest,
    SensitivityResponse,
)

DEMO_EQUITIES_FILE = Path(__file__).resolve().parents[3] / "data" / "demo" / (
    "demo_equities.json"
)


class EquityAnalysisService:
    def get_overview(self, symbol: str) -> EquityOverviewResponse:
        record = self._get_equity(symbol)

        return EquityOverviewResponse(
            symbol=record["symbol"],
            company_name=record["company_name"],
            ticker=record["symbol"],
            exchange=record["exchange"],
            sector=record["sector"],
            industry=record["industry"],
            country=record["country"],
            currency=record["currency"],
            market_cap=self._calculate_market_cap(record),
            free_float_market_cap=calculate_free_float_market_cap(
                record["latest_price"],
                record["shares_outstanding"],
                record.get("free_float_percent"),
            ),
            shares_outstanding=record["shares_outstanding"],
            latest_price=record["latest_price"],
            beta=record.get("beta"),
            benchmark_symbol=record["benchmark_symbol"],
            business_description=record["business_description"],
            data_source="Athena deterministic demo equity dataset",
            is_demo_data=True,
            security_profile=record["security_profile"],
            industry_analysis=record["industry_analysis"],
            business_model=record["business_model"],
        )

    def get_security_profile(self, symbol: str) -> EquitySecurityProfileResponse:
        record = self._get_equity(symbol)
        fundamentals = self._fundamentals(record)
        market_structure = record["market_structure"]
        book_value_per_share = calculate_book_value_per_share(
            fundamentals.get("equity"),
            record["shares_outstanding"],
        )
        security_type = classify_equity_security_type(
            market_structure.get("security_type"),
            has_voting_rights="one share" in market_structure.get(
                "voting_rights",
                "",
            ).lower(),
            dividend_priority=market_structure.get("dividend_priority"),
        )

        summary = summarize_equity_security_profile(
            security_type=security_type,
            exchange=record["exchange"],
            currency=record["currency"],
            voting_rights=market_structure["voting_rights"],
            dividend_profile=record["security_profile"]["dividend_profile"],
            liquidity_note=market_structure["liquidity_note"],
        )

        return EquitySecurityProfileResponse(
            symbol=record["symbol"],
            security_type=security_type,
            exchange=record["exchange"],
            currency=record["currency"],
            voting_rights=market_structure["voting_rights"],
            dividend_profile=record["security_profile"]["dividend_profile"],
            liquidity_note=market_structure["liquidity_note"],
            book_value_per_share=book_value_per_share,
            market_to_book_value=calculate_market_to_book_value(
                record["latest_price"],
                book_value_per_share,
            ),
            market_cap=self._calculate_market_cap(record),
            free_float_market_cap=calculate_free_float_market_cap(
                record["latest_price"],
                record["shares_outstanding"],
                record.get("free_float_percent"),
            ),
            summary=summary,
            placeholders=[
                "Preferred equity terms are not modeled in the demo dataset.",
                "Intraday liquidity metrics are planned for a future market microstructure feed.",
            ],
        )

    def get_industry(self, symbol: str) -> EquityIndustryResponse:
        record = self._get_equity(symbol)
        industry = record["industry_analysis"]

        return EquityIndustryResponse(
            symbol=record["symbol"],
            sector=record["sector"],
            industry=record["industry"],
            classification=industry["classification"],
            industry_overview=industry["industry_overview"],
            porter_forces=industry["porter_forces"],
            pestle=industry["pestle"],
            competitive_position=industry["competitive_position"],
            barriers_to_entry=industry["barriers_to_entry"],
            pricing_power=industry["pricing_power"],
            substitution_risk=industry["substitution_risk"],
            competitive_rivalry=industry["competitive_rivalry"],
        )

    def get_business_model(self, symbol: str) -> EquityBusinessModelResponse:
        record = self._get_equity(symbol)
        model = record["business_model"]

        return EquityBusinessModelResponse(
            symbol=record["symbol"],
            summary=model["summary"],
            business_description=record["business_description"],
            revenue_drivers=model["revenue_drivers"],
            revenue_segments=record.get("revenue_segments", []),
            geographic_exposure=record.get("geographic_exposure", []),
            pricing_power=model["pricing_power"],
            cyclicality=model["cyclicality"],
            operating_leverage=model["operating_leverage"],
            capital_intensity=model["capital_intensity"],
            placeholders=[
                "Segment margins are planned once a richer fundamentals feed is available.",
                "Geographic exposure is demo-only and not a live company filing import.",
            ],
        )

    def get_fundamentals(self, symbol: str) -> EquityFundamentalsResponse:
        record = self._get_equity(symbol)
        fundamentals = self._fundamentals(record)
        market_cap = self._calculate_market_cap(record)
        enterprise_value = calculate_enterprise_value(
            market_cap,
            fundamentals.get("debt") or 0.0,
            fundamentals.get("cash") or 0.0,
        )
        free_cash_flow = fundamentals.get("free_cash_flow")
        if free_cash_flow is None:
            free_cash_flow = calculate_free_cash_flow(
                fundamentals.get("operating_cash_flow"),
                fundamentals.get("capital_expenditures"),
            )

        values = {
            "revenue": fundamentals.get("revenue"),
            "eps": fundamentals.get("eps"),
            "free_cash_flow": free_cash_flow,
            "shareholders_equity": fundamentals.get("equity"),
        }

        return EquityFundamentalsResponse(
            symbol=record["symbol"],
            revenue=fundamentals.get("revenue"),
            gross_profit=fundamentals.get("gross_profit"),
            operating_income=fundamentals.get("operating_income"),
            ebit=fundamentals.get("ebit"),
            ebitda=fundamentals.get("ebitda"),
            net_income=fundamentals.get("net_income"),
            eps=fundamentals.get("eps"),
            dividends_per_share=fundamentals.get("dividends_per_share"),
            assets=fundamentals.get("assets"),
            liabilities=fundamentals.get("liabilities"),
            equity=fundamentals.get("equity"),
            debt=fundamentals.get("debt"),
            cash=fundamentals.get("cash"),
            current_assets=fundamentals.get("current_assets"),
            current_liabilities=fundamentals.get("current_liabilities"),
            receivables=fundamentals.get("receivables"),
            marketable_securities=fundamentals.get("marketable_securities"),
            inventory=fundamentals.get("inventory"),
            interest_expense=fundamentals.get("interest_expense"),
            operating_cash_flow=fundamentals.get("operating_cash_flow"),
            capital_expenditures=fundamentals.get("capital_expenditures"),
            free_cash_flow=free_cash_flow,
            shares_outstanding=record["shares_outstanding"],
            book_value_per_share=calculate_book_value_per_share(
                fundamentals.get("equity"),
                record["shares_outstanding"],
            ),
            working_capital=calculate_working_capital(
                fundamentals.get("current_assets"),
                fundamentals.get("current_liabilities"),
            ),
            enterprise_value=enterprise_value,
            warnings=self._warnings_for_missing(values),
        )

    def get_ratios(self, symbol: str) -> EquityRatiosResponse:
        record = self._get_equity(symbol)
        fundamentals = self._fundamentals(record)
        invested_capital = (fundamentals.get("equity") or 0.0) + (
            fundamentals.get("debt") or 0.0
        ) - (fundamentals.get("cash") or 0.0)
        nopat = (
            fundamentals.get("operating_income") * 0.79
            if fundamentals.get("operating_income") is not None
            else None
        )
        roe = calculate_roe(fundamentals.get("net_income"), fundamentals.get("equity"))
        payout = calculate_dividend_payout_ratio(
            fundamentals.get("dividends_per_share"),
            fundamentals.get("eps"),
        )
        retention = calculate_retention_ratio(payout)

        metrics = {
            "gross_margin": calculate_gross_margin(
                fundamentals.get("gross_profit"),
                fundamentals.get("revenue"),
            ),
            "operating_margin": calculate_operating_margin(
                fundamentals.get("operating_income"),
                fundamentals.get("revenue"),
            ),
            "ebit_margin": calculate_ebit_margin(
                fundamentals.get("ebit"),
                fundamentals.get("revenue"),
            ),
            "ebitda_margin": calculate_ebitda_margin(
                fundamentals.get("ebitda"),
                fundamentals.get("revenue"),
            ),
            "net_margin": calculate_net_margin(
                fundamentals.get("net_income"),
                fundamentals.get("revenue"),
            ),
            "roe": roe,
            "roa": calculate_roa(
                fundamentals.get("net_income"),
                fundamentals.get("assets"),
            ),
            "roic": calculate_roic(nopat, invested_capital),
            "debt_to_equity": calculate_debt_to_equity(
                fundamentals.get("debt"),
                fundamentals.get("equity"),
            ),
            "debt_to_assets": calculate_debt_to_assets(
                fundamentals.get("debt"),
                fundamentals.get("assets"),
            ),
            "net_debt": calculate_net_debt(
                fundamentals.get("debt"),
                fundamentals.get("cash"),
            ),
            "net_debt_to_ebitda": calculate_net_debt_to_ebitda(
                fundamentals.get("debt"),
                fundamentals.get("cash"),
                fundamentals.get("ebitda"),
            ),
            "current_ratio": calculate_current_ratio(
                fundamentals.get("current_assets"),
                fundamentals.get("current_liabilities"),
            ),
            "quick_ratio": calculate_quick_ratio(
                fundamentals.get("cash"),
                fundamentals.get("receivables"),
                fundamentals.get("marketable_securities"),
                fundamentals.get("current_liabilities"),
            ),
            "interest_coverage": calculate_interest_coverage(
                fundamentals.get("ebit"),
                fundamentals.get("interest_expense"),
            ),
            "asset_turnover": calculate_asset_turnover(
                fundamentals.get("revenue"),
                fundamentals.get("average_assets"),
            ),
            "receivables_turnover": calculate_receivables_turnover(
                fundamentals.get("revenue"),
                fundamentals.get("average_receivables"),
            ),
            "inventory_turnover": calculate_inventory_turnover(
                fundamentals.get("cost_of_goods_sold"),
                fundamentals.get("average_inventory"),
            ),
            "free_cash_flow_margin": calculate_free_cash_flow_margin(
                fundamentals.get("free_cash_flow"),
                fundamentals.get("revenue"),
            ),
            "dividend_payout_ratio": payout,
            "retention_ratio": retention,
            "sustainable_growth_rate": calculate_sustainable_growth_rate(roe, retention),
        }

        return EquityRatiosResponse(
            symbol=record["symbol"],
            quality_score=self._calculate_quality_score(metrics),
            warnings=self._warnings_for_missing(metrics),
            **metrics,
        )

    def get_growth(self, symbol: str) -> EquityGrowthResponse:
        record = self._get_equity(symbol)
        fundamentals = self._fundamentals(record)
        ratios = self.get_ratios(symbol)
        revenue_growth = record.get("revenue_growth") or calculate_revenue_growth(
            fundamentals.get("revenue"),
            fundamentals.get("prior_revenue"),
        )
        eps_growth = record.get("eps_growth") or calculate_revenue_growth(
            fundamentals.get("eps"),
            fundamentals.get("prior_eps"),
        )
        operating_growth = record.get(
            "operating_income_growth",
        ) or calculate_operating_income_growth(
            fundamentals.get("operating_income"),
            fundamentals.get("prior_operating_income"),
        )

        values = {
            "revenue_growth": revenue_growth,
            "eps_growth": eps_growth,
            "operating_income_growth": operating_growth,
            "sustainable_growth_rate": ratios.sustainable_growth_rate,
        }

        warnings = self._warnings_for_missing(values)
        warnings.extend(
            self._warnings_for_extreme_sustainable_growth(
                ratios.sustainable_growth_rate,
            ),
        )

        return EquityGrowthResponse(
            symbol=record["symbol"],
            revenue_growth=revenue_growth,
            eps_growth=eps_growth,
            operating_income_growth=operating_growth,
            dividend_growth_rate=record.get("dividend_growth_rate"),
            sustainable_growth_rate=ratios.sustainable_growth_rate,
            retention_ratio=ratios.retention_ratio,
            roe=ratios.roe,
            growth_profile=classify_growth_profile(
                revenue_growth,
                eps_growth,
                ratios.sustainable_growth_rate,
            ),
            forecast_assumptions=[
                "Forecasting is deterministic demo scaffolding, not a live estimate.",
                "Revenue growth, EPS growth and ROE retention are shown as CFA-style drivers.",
                "Scenario modeling will be added after richer historical fundamentals exist.",
            ],
            warnings=warnings,
        )

    def get_valuation(self, symbol: str) -> EquityValuationResponse:
        record = self._get_equity(symbol)
        fundamentals = self.get_fundamentals(symbol)
        assumptions = record["valuation_assumptions"]
        dividend_next_year = (fundamentals.dividends_per_share or 0.0) * (
            1.0 + assumptions["growth_rate"]
        )
        ggm_value = calculate_gordon_growth_value(
            dividend_next_year,
            assumptions["required_return"],
            assumptions["growth_rate"],
        )
        terminal_value = calculate_gordon_growth_value(
            dividend_next_year * ((1.0 + assumptions["growth_rate"]) ** 3),
            assumptions["required_return"],
            assumptions["growth_rate"],
        )
        dividend_discount_value = calculate_dividend_discount_value(
            [
                dividend_next_year,
                dividend_next_year * (1.0 + assumptions["growth_rate"]),
                dividend_next_year * ((1.0 + assumptions["growth_rate"]) ** 2),
            ],
            assumptions["required_return"],
            terminal_value=terminal_value,
        )
        intrinsic_value = (ggm_value + dividend_discount_value) / 2.0
        market_price = record["latest_price"]
        market_cap = self._calculate_market_cap(record)
        margin_of_safety = calculate_margin_of_safety(intrinsic_value, market_price)
        pe_ratio = calculate_pe_ratio(market_price, fundamentals.eps)
        pb_ratio = calculate_pb_ratio(market_price, fundamentals.book_value_per_share)
        ps_ratio = calculate_ps_ratio(market_cap, fundamentals.revenue)
        ev_ebitda = calculate_ev_ebitda(fundamentals.enterprise_value, fundamentals.ebitda)
        ev_sales = calculate_ev_sales(fundamentals.enterprise_value, fundamentals.revenue)
        earnings_yield = calculate_earnings_yield(fundamentals.eps, market_price)
        fcf_yield = calculate_free_cash_flow_yield(
            fundamentals.free_cash_flow,
            fundamentals.enterprise_value,
        )
        growth = record.get("eps_growth")
        metrics = {
            "pe_ratio": pe_ratio,
            "pb_ratio": pb_ratio,
            "ps_ratio": ps_ratio,
            "ev_ebitda": ev_ebitda,
            "ev_sales": ev_sales,
            "earnings_yield": earnings_yield,
            "free_cash_flow_yield": fcf_yield,
        }

        warnings = self._warnings_for_missing(metrics)
        warnings.extend(self._warnings_for_ggm_model(margin_of_safety))

        return EquityValuationResponse(
            symbol=record["symbol"],
            required_return=assumptions["required_return"],
            growth_rate=assumptions["growth_rate"],
            dividend_next_year=dividend_next_year,
            gordon_growth_value=ggm_value,
            dividend_discount_value=dividend_discount_value,
            implied_cost_of_equity=calculate_implied_cost_of_equity(
                dividend_next_year,
                market_price,
                assumptions["growth_rate"],
            ),
            implied_growth_rate=calculate_implied_growth_rate(
                dividend_next_year,
                market_price,
                assumptions["required_return"],
            ),
            pe_ratio=pe_ratio,
            forward_pe_ratio=calculate_forward_pe_ratio(
                market_price,
                assumptions.get("forward_eps"),
            ),
            pb_ratio=pb_ratio,
            ps_ratio=ps_ratio,
            enterprise_value=fundamentals.enterprise_value,
            ev_ebitda=ev_ebitda,
            ev_sales=ev_sales,
            peg_ratio=calculate_peg_ratio(pe_ratio, growth),
            dividend_yield=calculate_dividend_yield(
                fundamentals.dividends_per_share or 0.0,
                market_price,
            ),
            earnings_yield=earnings_yield,
            free_cash_flow_yield=fcf_yield,
            intrinsic_value=intrinsic_value,
            market_price=market_price,
            margin_of_safety=margin_of_safety,
            valuation_status=calculate_valuation_status(margin_of_safety),
            sector_pe_ratio=assumptions["sector_pe_ratio"],
            sensitivity_table=calculate_valuation_sensitivity_table(
                dividend_next_year,
                [
                    assumptions["required_return"] - 0.01,
                    assumptions["required_return"],
                    assumptions["required_return"] + 0.01,
                ],
                [
                    assumptions["growth_rate"] - 0.01,
                    assumptions["growth_rate"],
                    assumptions["growth_rate"] + 0.01,
                ],
            ),
            warnings=warnings,
        )

    def get_relative_valuation(self, symbol: str) -> EquityRelativeValuationResponse:
        valuation = self.get_valuation(symbol)
        peer_rows = self._get_peer_metric_rows(symbol)
        peer_medians = calculate_peer_medians(peer_rows)
        multiples = {
            "pe_ratio": valuation.pe_ratio,
            "pb_ratio": valuation.pb_ratio,
            "ps_ratio": valuation.ps_ratio,
            "ev_ebitda": valuation.ev_ebitda,
        }
        status = {
            key: classify_multiple_level(value, peer_medians.get(key))
            for key, value in multiples.items()
        }
        premium_discount = {
            key: compare_multiple_to_peer_median(value, peer_medians.get(key))
            for key, value in multiples.items()
        }

        return EquityRelativeValuationResponse(
            symbol=valuation.symbol,
            multiples=multiples,
            peer_medians=peer_medians,
            multiple_status=status,
            premium_discount_to_peers=premium_discount,
            warnings=self._warnings_for_missing({**multiples, **peer_medians}),
        )

    def get_peer_comparison(self, symbol: str) -> EquityPeerComparisonResponse:
        record = self._get_equity(symbol)
        company_ratios = self.get_ratios(symbol)
        company_growth = self.get_growth(symbol)
        company_valuation = self.get_valuation(symbol)
        peer_rows = self._get_peer_metric_rows(symbol)
        peer_symbols = [row["symbol"] for row in peer_rows]
        profitability_signal = compare_profitability_to_peers(
            company_ratios.roe,
            [row["roe"] for row in peer_rows if row.get("roe") is not None],
        )
        growth_signal = compare_growth_to_peers(
            company_growth.revenue_growth,
            [
                row["revenue_growth"]
                for row in peer_rows
                if row.get("revenue_growth") is not None
            ],
        )
        valuation_signal = compare_valuation_to_peers(
            company_valuation.pe_ratio,
            [row["pe_ratio"] for row in peer_rows if row.get("pe_ratio") is not None],
        )

        return EquityPeerComparisonResponse(
            symbol=record["symbol"],
            benchmark_symbol=record["benchmark_symbol"],
            peer_symbols=peer_symbols,
            peer_rows=peer_rows,
            profitability_vs_peers=profitability_signal,
            growth_vs_peers=growth_signal,
            valuation_vs_peers=valuation_signal,
            relative_performance_vs_benchmark=calculate_relative_performance_vs_benchmark(
                0.126,
                0.084,
            ),
            sector_relative_summary=create_peer_comparison_summary(
                company_symbol=record["symbol"],
                peer_symbols=peer_symbols,
                profitability_signal=profitability_signal,
                growth_signal=growth_signal,
                valuation_signal=valuation_signal,
            ),
        )

    def get_corporate_actions(self, symbol: str) -> EquityCorporateActionsResponse:
        record = self._get_equity(symbol)
        fundamentals = self.get_fundamentals(symbol)
        ratios = self.get_ratios(symbol)
        valuation = self.get_valuation(symbol)
        actions = record.get("corporate_actions", {})
        buyback_yield = calculate_buyback_yield(
            actions.get("net_share_repurchases"),
            self._calculate_market_cap(record),
        )
        total_yield = calculate_total_shareholder_yield(
            valuation.dividend_yield,
            buyback_yield,
        )
        dividend_summary = summarize_dividend_profile(
            fundamentals.dividends_per_share,
            valuation.dividend_yield,
            ratios.dividend_payout_ratio,
        )
        split_summary = summarize_stock_split_placeholder(actions.get("split_history"))
        repurchase_summary = summarize_share_repurchases_placeholder(buyback_yield)
        profile = summarize_corporate_actions_profile(
            dividend_profile=dividend_summary,
            stock_split_summary=split_summary,
            repurchase_summary=repurchase_summary,
            total_shareholder_yield=total_yield,
        )

        return EquityCorporateActionsResponse(
            symbol=record["symbol"],
            dividend_profile=profile["dividend_profile"],
            dividend_yield=valuation.dividend_yield,
            payout_ratio=ratios.dividend_payout_ratio,
            retention_ratio=ratios.retention_ratio,
            stock_split_summary=profile["stock_split_summary"],
            share_repurchases_summary=profile["repurchase_summary"],
            buyback_yield=buyback_yield,
            total_shareholder_yield=total_yield,
            timeline=[
                {"label": "Dividend", "detail": profile["dividend_profile"]},
                {"label": "Split", "detail": profile["stock_split_summary"]},
                {"label": "Repurchases", "detail": profile["repurchase_summary"]},
            ],
            placeholders=[
                "Event-level corporate action feed is planned.",
                actions.get("repurchase_note", "Repurchase data is demo-only."),
            ],
        )

    def get_diagnostics(self, symbol: str) -> EquityDiagnosticsResponse:
        record = self._get_equity(symbol)
        ratios = self.get_ratios(symbol)
        growth = self.get_growth(symbol)
        valuation = self.get_valuation(symbol)
        relative = self.get_relative_valuation(symbol)
        corporate_actions = self.get_corporate_actions(symbol)
        valuation_status = classify_valuation_status(
            valuation.margin_of_safety,
            valuation.pe_ratio or 0.0,
            valuation.sector_pe_ratio,
        )
        profitability_quality = classify_profitability_quality(
            ratios.net_margin or 0.0,
            ratios.roe or 0.0,
        )
        balance_sheet_quality = classify_balance_sheet_quality(
            ratios.debt_to_equity or 0.0,
            ratios.current_ratio or 0.0,
            ratios.interest_coverage or 0.0,
        )
        valuation_profile = classify_valuation_profile(
            valuation.margin_of_safety,
            relative.multiple_status.get("pe_ratio", "Insufficient data"),
        )
        dividend_profile = classify_dividend_profile(
            valuation.dividend_yield,
            ratios.dividend_payout_ratio,
        )
        risk_profile = classify_equity_risk_profile(
            record.get("beta"),
            ratios.debt_to_equity,
            valuation_profile,
        )
        bull_base_bear = create_bull_base_bear_case_summary(
            strengths=record["strengths"],
            risks=record["key_risks"],
            growth_profile=growth.growth_profile,
            valuation_profile=valuation_profile,
        )
        watchlist_flags = create_watchlist_flags(
            valuation_profile=valuation_profile,
            balance_sheet_quality=balance_sheet_quality,
            growth_profile=growth.growth_profile,
            risk_profile=risk_profile,
        )

        return EquityDiagnosticsResponse(
            symbol=record["symbol"],
            valuation_status=valuation_status,
            valuation_profile=valuation_profile,
            profitability_quality=profitability_quality,
            balance_sheet_quality=balance_sheet_quality,
            growth_profile=growth.growth_profile,
            dividend_profile=dividend_profile,
            risk_profile=risk_profile,
            strengths=record["strengths"],
            weaknesses=record["weaknesses"],
            risks=record["key_risks"],
            watchlist_flags=watchlist_flags,
            bull_base_bear=bull_base_bear,
            governance=record["governance"],
            esg_considerations=record["esg_considerations"],
            risk_factors={
                "company": record["key_risks"],
                "industry": record["industry_risks"],
                "financial": record["financial_risks"],
                "valuation": record["valuation_risks"],
                "liquidity": record["liquidity_risks"],
                "regulatory": record["regulatory_risks"],
            },
            analyst_summary=create_equity_diagnostics_summary(
                company_name=record["company_name"],
                valuation_status=valuation_status,
                profitability_quality=profitability_quality,
                balance_sheet_quality=balance_sheet_quality,
                strengths=record["strengths"],
                risks=record["key_risks"],
                metrics={
                    "margin_of_safety": valuation.margin_of_safety,
                    "total_shareholder_yield": corporate_actions.total_shareholder_yield,
                },
            ),
            educational_note=(
                "Educational equity analysis only. This is not investment advice, "
                "a recommendation, or a buy/sell/hold rating."
            ),
        )

    def calculate_ggm(self, payload: GgmValuationRequest) -> GgmValuationResponse:
        try:
            intrinsic_value = calculate_gordon_growth_value(
                payload.dividend_next_year,
                payload.required_return,
                payload.growth_rate,
            )
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

        return GgmValuationResponse(
            intrinsic_value=intrinsic_value,
            spread=payload.required_return - payload.growth_rate,
        )

    def calculate_sensitivity(
        self,
        payload: SensitivityRequest,
    ) -> SensitivityResponse:
        cells = [
            SensitivityCell.model_validate(cell)
            for cell in calculate_valuation_sensitivity_table(
                payload.dividend_next_year,
                payload.required_returns,
                payload.growth_rates,
            )
        ]
        return SensitivityResponse(cells=cells)

    def _get_peer_metric_rows(self, symbol: str) -> list[dict[str, Any]]:
        normalized_symbol = symbol.upper()
        rows = []

        for peer in _load_demo_equities():
            if peer["symbol"] == normalized_symbol or peer.get("is_benchmark_only"):
                continue

            valuation = self.get_valuation(peer["symbol"])
            ratios = self.get_ratios(peer["symbol"])
            growth = self.get_growth(peer["symbol"])
            rows.append(
                {
                    "symbol": peer["symbol"],
                    "company_name": peer["company_name"],
                    "sector": peer["sector"],
                    "pe_ratio": valuation.pe_ratio,
                    "pb_ratio": valuation.pb_ratio,
                    "ps_ratio": valuation.ps_ratio,
                    "ev_ebitda": valuation.ev_ebitda,
                    "roe": ratios.roe,
                    "net_margin": ratios.net_margin,
                    "revenue_growth": growth.revenue_growth,
                    "valuation_status": valuation.valuation_status,
                },
            )

        return rows

    def _get_equity(self, symbol: str) -> dict[str, Any]:
        normalized_symbol = symbol.upper()
        for equity in _load_demo_equities():
            if equity["symbol"] == normalized_symbol:
                return equity

        raise HTTPException(
            status_code=404,
            detail=f"No demo equity data found for {symbol}.",
        )

    def _fundamentals(self, record: dict[str, Any]) -> dict[str, Any]:
        return normalize_fundamentals_snapshot(record["fundamentals"])

    def _calculate_market_cap(self, record: dict[str, Any]) -> float:
        return calculate_market_cap(record["latest_price"], record["shares_outstanding"])

    def _calculate_quality_score(self, metrics: dict[str, float | None]) -> float:
        components = [
            self._score_threshold(metrics.get("roe"), 0.12, 0.25),
            self._score_threshold(metrics.get("net_margin"), 0.10, 0.25),
            self._score_inverse(metrics.get("debt_to_equity"), 2.0, 0.5),
            self._score_threshold(metrics.get("current_ratio"), 0.8, 1.5),
            self._score_threshold(metrics.get("free_cash_flow_margin"), 0.05, 0.20),
        ]
        available_components = [value for value in components if value is not None]
        if not available_components:
            return 0.0
        return sum(available_components) / len(available_components)

    def _score_threshold(
        self,
        value: float | None,
        weak: float,
        strong: float,
    ) -> float | None:
        if value is None:
            return None
        if value <= weak:
            return 0.25
        if value >= strong:
            return 1.0
        return 0.25 + ((value - weak) / (strong - weak)) * 0.75

    def _score_inverse(
        self,
        value: float | None,
        weak: float,
        strong: float,
    ) -> float | None:
        if value is None:
            return None
        if value >= weak:
            return 0.25
        if value <= strong:
            return 1.0
        return 1.0 - ((value - strong) / (weak - strong)) * 0.75

    def _warnings_for_missing(self, values: dict[str, Any]) -> list[str]:
        warnings = [
            f"{key} could not be calculated because required demo inputs are missing or zero."
            for key, value in values.items()
            if value is None
        ]
        return warnings

    def _warnings_for_ggm_model(
        self,
        margin_of_safety: float | None,
    ) -> list[str]:
        warnings = [
            (
                "GGM is a dividend-focused model that assumes constant perpetual "
                "growth; treat it as one model signal, not a complete fair-value estimate."
            ),
            (
                "For low-yield or buyback-heavy companies, dividend models can "
                "understate shareholder returns and should be read alongside multiples."
            ),
        ]
        if margin_of_safety is not None and abs(margin_of_safety) > 1.0:
            warnings.append(
                "The model price gap is extreme because dividend-model value is far "
                "from the market price; interpret the output as sensitivity, not a recommendation.",
            )
        return warnings

    def _warnings_for_extreme_sustainable_growth(
        self,
        sustainable_growth_rate: float | None,
    ) -> list[str]:
        if sustainable_growth_rate is None:
            return []
        if sustainable_growth_rate > 0.25:
            return [
                (
                    "Sustainable growth rate is unusually high because ROE and "
                    "retention are high in the demo fundamentals; treat it as an "
                    "accounting-driver signal, not a forecast."
                ),
            ]
        if sustainable_growth_rate < -0.05:
            return [
                (
                    "Sustainable growth rate is negative in the demo fundamentals; "
                    "review ROE, payout and retained earnings drivers before using it."
                ),
            ]
        return []


@lru_cache(maxsize=1)
def _load_demo_equities() -> list[dict[str, Any]]:
    with DEMO_EQUITIES_FILE.open(encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("demo_equities.json must contain a list.")

    return data
