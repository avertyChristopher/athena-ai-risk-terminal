import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from fastapi import HTTPException

from app.domain.equity import (
    calculate_book_value_per_share,
    calculate_current_ratio,
    calculate_debt_to_equity,
    calculate_dividend_discount_value,
    calculate_dividend_payout_ratio,
    calculate_dividend_yield,
    calculate_earnings_yield,
    calculate_enterprise_value,
    calculate_ev_ebitda,
    calculate_free_cash_flow_yield,
    calculate_gordon_growth_value,
    calculate_gross_margin,
    calculate_implied_cost_of_equity,
    calculate_implied_growth_rate,
    calculate_interest_coverage,
    calculate_margin_of_safety,
    calculate_market_cap,
    calculate_net_margin,
    calculate_operating_margin,
    calculate_pb_ratio,
    calculate_pe_ratio,
    calculate_ps_ratio,
    calculate_quick_ratio,
    calculate_retention_ratio,
    calculate_roa,
    calculate_roe,
    calculate_sustainable_growth_rate,
    classify_balance_sheet_quality,
    classify_profitability_quality,
    classify_valuation_status,
    create_equity_diagnostics_summary,
)
from app.schemas.equity_schema import (
    EquityDiagnosticsResponse,
    EquityFundamentalsResponse,
    EquityOverviewResponse,
    EquityRatiosResponse,
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
        fundamentals = record["fundamentals"]
        market_cap = calculate_market_cap(
            record["latest_price"],
            record["shares_outstanding"],
        )

        return EquityOverviewResponse(
            symbol=record["symbol"],
            company_name=record["company_name"],
            ticker=record["symbol"],
            exchange=record["exchange"],
            sector=record["sector"],
            industry=record["industry"],
            country=record["country"],
            currency=record["currency"],
            market_cap=market_cap,
            latest_price=record["latest_price"],
            benchmark_symbol=record["benchmark_symbol"],
            security_profile=record["security_profile"],
            industry_analysis=record["industry_analysis"],
            business_model=record["business_model"],
        )

    def get_fundamentals(self, symbol: str) -> EquityFundamentalsResponse:
        record = self._get_equity(symbol)
        fundamentals = record["fundamentals"]
        market_cap = calculate_market_cap(
            record["latest_price"],
            record["shares_outstanding"],
        )
        enterprise_value = calculate_enterprise_value(
            market_cap,
            fundamentals["debt"],
            fundamentals["cash"],
        )

        return EquityFundamentalsResponse(
            symbol=record["symbol"],
            revenue=fundamentals["revenue"],
            gross_profit=fundamentals["gross_profit"],
            ebit=fundamentals["ebit"],
            ebitda=fundamentals["ebitda"],
            net_income=fundamentals["net_income"],
            eps=fundamentals["eps"],
            dividends_per_share=fundamentals["dividends_per_share"],
            assets=fundamentals["assets"],
            liabilities=fundamentals["liabilities"],
            equity=fundamentals["equity"],
            debt=fundamentals["debt"],
            cash=fundamentals["cash"],
            current_assets=fundamentals["current_assets"],
            current_liabilities=fundamentals["current_liabilities"],
            receivables=fundamentals["receivables"],
            marketable_securities=fundamentals["marketable_securities"],
            interest_expense=fundamentals["interest_expense"],
            operating_cash_flow=fundamentals["operating_cash_flow"],
            free_cash_flow=fundamentals["free_cash_flow"],
            shares_outstanding=record["shares_outstanding"],
            book_value_per_share=calculate_book_value_per_share(
                fundamentals["equity"],
                record["shares_outstanding"],
            ),
            enterprise_value=enterprise_value,
        )

    def get_ratios(self, symbol: str) -> EquityRatiosResponse:
        record = self._get_equity(symbol)
        fundamentals = record["fundamentals"]
        roe = calculate_roe(fundamentals["net_income"], fundamentals["equity"])
        payout = calculate_dividend_payout_ratio(
            fundamentals["dividends_per_share"],
            fundamentals["eps"],
        )
        retention = calculate_retention_ratio(payout)

        return EquityRatiosResponse(
            symbol=record["symbol"],
            gross_margin=calculate_gross_margin(
                fundamentals["gross_profit"],
                fundamentals["revenue"],
            ),
            operating_margin=calculate_operating_margin(
                fundamentals["ebit"],
                fundamentals["revenue"],
            ),
            net_margin=calculate_net_margin(
                fundamentals["net_income"],
                fundamentals["revenue"],
            ),
            roe=roe,
            roa=calculate_roa(fundamentals["net_income"], fundamentals["assets"]),
            debt_to_equity=calculate_debt_to_equity(
                fundamentals["debt"],
                fundamentals["equity"],
            ),
            current_ratio=calculate_current_ratio(
                fundamentals["current_assets"],
                fundamentals["current_liabilities"],
            ),
            quick_ratio=calculate_quick_ratio(
                fundamentals["cash"],
                fundamentals["receivables"],
                fundamentals["marketable_securities"],
                fundamentals["current_liabilities"],
            ),
            interest_coverage=calculate_interest_coverage(
                fundamentals["ebit"],
                fundamentals["interest_expense"],
            ),
            dividend_payout_ratio=payout,
            retention_ratio=retention,
            sustainable_growth_rate=calculate_sustainable_growth_rate(roe, retention),
        )

    def get_valuation(self, symbol: str) -> EquityValuationResponse:
        record = self._get_equity(symbol)
        fundamentals = self.get_fundamentals(symbol)
        assumptions = record["valuation_assumptions"]
        dividend_next_year = fundamentals.dividends_per_share * (
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
            pe_ratio=calculate_pe_ratio(market_price, fundamentals.eps),
            pb_ratio=calculate_pb_ratio(
                market_price,
                fundamentals.book_value_per_share,
            ),
            ps_ratio=calculate_ps_ratio(
                calculate_market_cap(record["latest_price"], record["shares_outstanding"]),
                fundamentals.revenue,
            ),
            ev_ebitda=calculate_ev_ebitda(
                fundamentals.enterprise_value,
                fundamentals.ebitda,
            ),
            dividend_yield=calculate_dividend_yield(
                fundamentals.dividends_per_share,
                market_price,
            ),
            earnings_yield=calculate_earnings_yield(fundamentals.eps, market_price),
            free_cash_flow_yield=calculate_free_cash_flow_yield(
                fundamentals.free_cash_flow,
                fundamentals.enterprise_value,
            ),
            intrinsic_value=intrinsic_value,
            market_price=market_price,
            margin_of_safety=calculate_margin_of_safety(intrinsic_value, market_price),
            sector_pe_ratio=assumptions["sector_pe_ratio"],
        )

    def get_diagnostics(self, symbol: str) -> EquityDiagnosticsResponse:
        record = self._get_equity(symbol)
        ratios = self.get_ratios(symbol)
        valuation = self.get_valuation(symbol)
        valuation_status = classify_valuation_status(
            valuation.margin_of_safety,
            valuation.pe_ratio,
            valuation.sector_pe_ratio,
        )
        profitability_quality = classify_profitability_quality(
            ratios.net_margin,
            ratios.roe,
        )
        balance_sheet_quality = classify_balance_sheet_quality(
            ratios.debt_to_equity,
            ratios.current_ratio,
            ratios.interest_coverage,
        )

        return EquityDiagnosticsResponse(
            symbol=record["symbol"],
            valuation_status=valuation_status,
            profitability_quality=profitability_quality,
            balance_sheet_quality=balance_sheet_quality,
            strengths=record["strengths"],
            risks=record["risks"],
            analyst_summary=create_equity_diagnostics_summary(
                company_name=record["company_name"],
                valuation_status=valuation_status,
                profitability_quality=profitability_quality,
                balance_sheet_quality=balance_sheet_quality,
                strengths=record["strengths"],
                risks=record["risks"],
                metrics={"margin_of_safety": valuation.margin_of_safety},
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
        cells: list[SensitivityCell] = []
        for required_return in payload.required_returns:
            for growth_rate in payload.growth_rates:
                intrinsic_value: float | None
                try:
                    intrinsic_value = calculate_gordon_growth_value(
                        payload.dividend_next_year,
                        required_return,
                        growth_rate,
                    )
                except ValueError:
                    intrinsic_value = None

                cells.append(
                    SensitivityCell(
                        required_return=required_return,
                        growth_rate=growth_rate,
                        intrinsic_value=intrinsic_value,
                    ),
                )

        return SensitivityResponse(cells=cells)

    def _get_equity(self, symbol: str) -> dict[str, Any]:
        normalized_symbol = symbol.upper()
        for equity in _load_demo_equities():
            if equity["symbol"] == normalized_symbol:
                return equity

        raise HTTPException(
            status_code=404,
            detail=f"No demo equity data found for {symbol}.",
        )


@lru_cache(maxsize=1)
def _load_demo_equities() -> list[dict[str, Any]]:
    with DEMO_EQUITIES_FILE.open(encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("demo_equities.json must contain a list.")

    return data
