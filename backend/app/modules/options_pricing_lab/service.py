from fastapi import HTTPException

from app.modules.options_pricing_lab.domain.binomial import binomial_option_price
from app.modules.options_pricing_lab.domain.black_scholes import (
    black_scholes_price,
    d1,
    d2,
)
from app.modules.options_pricing_lab.domain.commentary import (
    option_commentary,
    strategy_commentary,
)
from app.modules.options_pricing_lab.domain.greeks import option_greeks
from app.modules.options_pricing_lab.domain.implied_volatility import (
    implied_volatility_placeholder,
)
from app.modules.options_pricing_lab.domain.moneyness import (
    classify_moneyness,
    moneyness_ratio,
)
from app.modules.options_pricing_lab.domain.payoff import (
    breakeven_call,
    breakeven_put,
    intrinsic_value,
    option_payoff,
    option_profit,
    time_value,
)
from app.modules.options_pricing_lab.domain.put_call_parity import (
    put_call_parity_check,
)
from app.modules.options_pricing_lab.domain.risk_summary import (
    single_option_risk_summary,
)
from app.modules.options_pricing_lab.domain.scenarios import (
    greek_sensitivity,
    payoff_scenarios,
    sensitivity_analysis,
)
from app.modules.options_pricing_lab.domain.strategies import strategy_summary
from app.modules.options_pricing_lab.repository import OptionsPricingLabRepository
from app.modules.options_pricing_lab.schemas import (
    DataSources,
    GreeksResponse,
    OptionPricingRequest,
    OptionPricingResponse,
    OptionsPricingLabStatus,
    OptionStrategyRequest,
    OptionStrategyResponse,
)


class OptionsPricingLabService:
    def __init__(self, repository: OptionsPricingLabRepository) -> None:
        self.repository = repository

    def get_status(self) -> OptionsPricingLabStatus:
        return OptionsPricingLabStatus(
            detail=(
                "Options Pricing Lab is ready for payoff analytics, "
                "Black-Scholes pricing, binomial pricing, Greeks, put-call "
                "parity and deterministic strategy scenarios."
            ),
            engines_available=[
                "payoff_logic",
                "black_scholes",
                "binomial_crr",
                "greeks",
                "put_call_parity",
                "strategy_payoff",
                "volatility_lab_inputs",
            ],
        )

    def price_option(self, payload: OptionPricingRequest) -> OptionPricingResponse:
        try:
            inputs = self._resolve_inputs(
                payload.underlying_symbol,
                payload.underlying_price,
                payload.volatility,
                payload.risk_free_rate,
                payload.dividend_yield,
            )
            underlying_price = float(inputs["underlying_price"])
            volatility = float(inputs["volatility"])
            years = payload.time_to_expiration_days / 365
            bs_price = black_scholes_price(
                payload.option_type,
                underlying_price,
                payload.strike_price,
                years,
                payload.risk_free_rate,
                volatility,
                payload.dividend_yield,
            )
            binomial = binomial_option_price(
                payload.option_type,
                underlying_price,
                payload.strike_price,
                years,
                payload.risk_free_rate,
                volatility,
                payload.dividend_yield,
                payload.binomial_steps,
            )
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

        option_price = (
            bs_price
            if payload.pricing_model == "black_scholes"
            else float(binomial["price"])
        )
        intrinsic = intrinsic_value(
            underlying_price,
            payload.strike_price,
            payload.option_type,
        )
        moneyness = classify_moneyness(
            underlying_price,
            payload.strike_price,
            payload.option_type,
        )
        breakeven = (
            breakeven_call(payload.strike_price, option_price)
            if payload.option_type == "call"
            else breakeven_put(payload.strike_price, option_price)
        )
        payoff = option_payoff(
            underlying_price,
            payload.strike_price,
            payload.option_type,
            payload.position_side,
        )
        profit = option_profit(payoff, option_price, payload.position_side)
        risk_summary = single_option_risk_summary(
            payload.option_type,
            payload.position_side,
            payload.strike_price,
            option_price,
            payload.contract_size,
            payload.quantity,
        )
        greeks = option_greeks(
            payload.option_type,
            underlying_price,
            payload.strike_price,
            years,
            payload.risk_free_rate,
            volatility,
            payload.dividend_yield,
            payload.position_side,
        )
        call_price = black_scholes_price(
            "call",
            underlying_price,
            payload.strike_price,
            years,
            payload.risk_free_rate,
            volatility,
            payload.dividend_yield,
        )
        put_price = black_scholes_price(
            "put",
            underlying_price,
            payload.strike_price,
            years,
            payload.risk_free_rate,
            volatility,
            payload.dividend_yield,
        )
        commentary = option_commentary(
            payload.option_type,
            payload.position_side,
            moneyness,
            greeks["delta"],
            greeks["theta_daily"],
            greeks["vega"],
            str(risk_summary["risk_note"]),
        )

        return OptionPricingResponse(
            input_summary={
                "underlying_symbol": payload.underlying_symbol.upper(),
                "underlying_price": underlying_price,
                "option_type": payload.option_type,
                "position_side": payload.position_side,
                "strike_price": payload.strike_price,
                "time_to_expiration_days": payload.time_to_expiration_days,
                "volatility": volatility,
                "risk_free_rate": payload.risk_free_rate,
                "dividend_yield": payload.dividend_yield,
                "contract_size": payload.contract_size,
                "quantity": payload.quantity,
            },
            pricing_summary={
                "option_price": option_price,
                "black_scholes_price": bs_price,
                "binomial_price": binomial["price"],
                "intrinsic_value": intrinsic,
                "time_value": time_value(option_price, intrinsic),
                "moneyness": moneyness,
                "moneyness_ratio": moneyness_ratio(
                    underlying_price,
                    payload.strike_price,
                ),
                "breakeven_price": breakeven,
                "contract_premium": option_price
                * payload.contract_size
                * payload.quantity,
                "contract_notional": underlying_price
                * payload.contract_size
                * payload.quantity,
            },
            payoff_summary={
                "payoff_at_spot": payoff
                * payload.contract_size
                * payload.quantity,
                "profit_at_spot": profit
                * payload.contract_size
                * payload.quantity,
                "max_profit": risk_summary["max_profit"],
                "max_profit_label": risk_summary["max_profit_label"],
                "max_loss": risk_summary["max_loss"],
                "risk_note": risk_summary["risk_note"],
                "payoff_table": payoff_scenarios(
                    payload.option_type,
                    payload.position_side,
                    underlying_price,
                    payload.strike_price,
                    option_price,
                    payload.contract_size,
                    payload.quantity,
                ),
            },
            greeks=self._greeks_response(
                greeks,
                underlying_price,
                payload.contract_size,
                payload.quantity,
            ),
            model_details={
                "selected_model": payload.pricing_model,
                "black_scholes": {
                    "d1": d1(
                        underlying_price,
                        payload.strike_price,
                        years,
                        payload.risk_free_rate,
                        volatility,
                        payload.dividend_yield,
                    ),
                    "d2": d2(
                        underlying_price,
                        payload.strike_price,
                        years,
                        payload.risk_free_rate,
                        volatility,
                        payload.dividend_yield,
                    ),
                    "assumptions": self._black_scholes_assumptions(),
                },
                "binomial": binomial,
                "model_difference": bs_price - float(binomial["price"]),
            },
            parity_check=put_call_parity_check(
                call_price,
                put_price,
                underlying_price,
                payload.strike_price,
                years,
                payload.risk_free_rate,
                payload.dividend_yield,
            ),
            sensitivity_analysis={
                **sensitivity_analysis(
                    payload.option_type,
                    underlying_price,
                    payload.strike_price,
                    years,
                    payload.risk_free_rate,
                    volatility,
                    payload.dividend_yield,
                ),
                "greeks_by_price": greek_sensitivity(
                    payload.option_type,
                    underlying_price,
                    payload.strike_price,
                    years,
                    payload.risk_free_rate,
                    volatility,
                    payload.dividend_yield,
                    payload.position_side,
                ),
            },
            methodology=self._methodology(payload.pricing_model),
            assumptions={
                "implied_volatility": implied_volatility_placeholder(),
                "american_option_note": (
                    "American early exercise is a roadmap item; current pricing is European style."
                ),
                "not_investment_advice": True,
            },
            data_sources=inputs["data_sources"],
            athena_commentary=commentary,
        )

    def analyze_strategy(
        self,
        payload: OptionStrategyRequest,
    ) -> OptionStrategyResponse:
        inputs = self._resolve_inputs(
            payload.underlying_symbol,
            payload.underlying_price,
            payload.volatility,
            payload.risk_free_rate,
            payload.dividend_yield,
        )
        underlying_price = float(inputs["underlying_price"])
        volatility = float(inputs["volatility"])
        legs = payload.legs or self._default_strategy_legs(
            payload.strategy_type,
            underlying_price,
            volatility,
            payload.risk_free_rate,
            payload.dividend_yield,
        )
        priced_legs = [
            self._price_leg(
                leg.model_dump() if hasattr(leg, "model_dump") else leg,
                underlying_price,
                payload.risk_free_rate,
                volatility,
                payload.dividend_yield,
            )
            for leg in legs
        ]
        summary = strategy_summary(
            payload.strategy_type,
            underlying_price,
            priced_legs,
            payload.contract_size,
        )
        aggregate_greeks = self._aggregate_strategy_greeks(
            priced_legs,
            underlying_price,
            payload.risk_free_rate,
            volatility,
            payload.dividend_yield,
        )
        commentary = strategy_commentary(
            payload.strategy_type,
            str(summary["risk_profile"]),
        )

        return OptionStrategyResponse(
            strategy_summary={
                "strategy_type": payload.strategy_type,
                "underlying_symbol": payload.underlying_symbol.upper(),
                "underlying_price": underlying_price,
                "risk_profile": summary["risk_profile"],
            },
            legs=priced_legs,
            net_premium=float(summary["net_premium"]),
            payoff_table=list(summary["payoff_table"]),
            max_profit=summary["max_profit"],
            max_loss=summary["max_loss"],
            breakeven_points=list(summary["breakeven_points"]),
            aggregate_greeks=aggregate_greeks,
            risk_summary={
                "cfa_explanation": self._strategy_cfa_note(payload.strategy_type),
                "trade_simulator_note": (
                    "Strategy notional, premium and Greeks can feed future Trade Simulator tickets."
                ),
                "risk_monitor_note": (
                    "Delta-adjusted exposure and Greeks can feed future Risk Monitor option exposure."
                ),
            },
            commentary=commentary,
            data_sources=inputs["data_sources"],
        )

    def demo(self) -> OptionPricingResponse:
        return self.price_option(OptionPricingRequest())

    def _resolve_inputs(
        self,
        symbol: str,
        manual_price: float | None,
        manual_volatility: float | None,
        risk_free_rate: float,
        dividend_yield: float,
    ) -> dict[str, float | DataSources]:
        warnings = []
        badges = []
        fallback_used = False
        latest_price = self.repository.get_latest_price(symbol)
        if manual_price is not None:
            underlying_price = manual_price
            price_source = "manual_input"
            badges.append("Manual Input")
        elif latest_price is not None:
            underlying_price = latest_price
            price_source = "market_data"
            badges.append("Market Data")
        else:
            underlying_price = 191.0
            price_source = "deterministic_demo"
            fallback_used = True
            badges.append("Demo")
            warnings.append(f"{symbol.upper()}: Market Data price unavailable; demo price used.")

        volatility_inputs = self.repository.get_volatility_inputs(symbol)
        if manual_volatility is not None:
            volatility = manual_volatility
            volatility_source = "manual_input"
            badges.append("Manual Volatility")
        elif volatility_inputs["ewma_volatility"] is not None:
            volatility = float(volatility_inputs["ewma_volatility"])
            volatility_source = "volatility_lab_ewma"
            badges.append("Volatility Lab")
        elif volatility_inputs["realized_volatility"] is not None:
            volatility = float(volatility_inputs["realized_volatility"])
            volatility_source = "volatility_lab_realized"
            badges.append("Volatility Lab")
        else:
            volatility = 0.25
            volatility_source = "deterministic_demo"
            fallback_used = True
            badges.append("Demo")
            warnings.append(f"{symbol.upper()}: volatility unavailable; demo 25% volatility used.")

        return {
            "underlying_price": underlying_price,
            "volatility": volatility,
            "data_sources": DataSources(
                underlying_price_source=price_source,
                volatility_source=volatility_source,
                risk_free_rate_source="manual_input"
                if risk_free_rate != 0.045
                else "demo_risk_free_proxy",
                dividend_yield_source="manual_input"
                if dividend_yield != 0.005
                else "demo_dividend_proxy",
                fallback_used=fallback_used,
                badges=badges,
                warnings=warnings,
            ),
        }

    def _greeks_response(
        self,
        greeks: dict[str, float],
        underlying_price: float,
        contract_size: int,
        quantity: int,
    ) -> GreeksResponse:
        delta_per_contract = greeks["delta"] * contract_size
        return GreeksResponse(
            **greeks,
            delta_per_contract=delta_per_contract,
            delta_adjusted_exposure=delta_per_contract * underlying_price * quantity,
            interpretation={
                "delta": "Delta estimates option price change for a $1 move in the underlying.",
                "gamma": "Gamma measures how quickly Delta changes.",
                "theta": "Theta measures time decay. Long options usually have negative Theta.",
                "vega": "Vega measures price change for a 1 percentage point volatility change.",
                "rho": "Rho measures price change for a 1 percentage point rate change.",
            },
        )

    def _methodology(self, pricing_model: str) -> dict[str, object]:
        return {
            "selected_model": pricing_model,
            "black_scholes": {
                "method": "European Black-Scholes with continuous dividend yield.",
                "limitations": [
                    "European exercise",
                    "constant volatility",
                    "constant risk-free rate",
                    "frictionless markets",
                    "lognormal underlying returns",
                ],
            },
            "binomial": {
                "method": "Cox-Ross-Rubinstein risk-neutral tree.",
                "limitation": "American exercise is planned but not implemented.",
            },
            "cfa_scope": [
                "Payoff versus profit",
                "Intrinsic and time value",
                "Moneyness",
                "Put-call parity",
                "Greeks and non-linear risk",
            ],
        }

    def _black_scholes_assumptions(self) -> list[str]:
        return [
            "European option",
            "Lognormal underlying returns",
            "Constant volatility",
            "Constant risk-free rate",
            "Frictionless markets",
            "No arbitrage",
        ]

    def _default_strategy_legs(
        self,
        strategy_type: str,
        underlying_price: float,
        volatility: float,
        risk_free_rate: float,
        dividend_yield: float,
    ) -> list[dict[str, float | int | str]]:
        strike = round(underlying_price / 5) * 5
        if strategy_type == "protective_put":
            raw_legs = [{"option_type": "put", "side": "long", "strike": strike, "expiration_days": 60, "quantity": 1}]
        elif strategy_type == "long_straddle":
            raw_legs = [
                {"option_type": "call", "side": "long", "strike": strike, "expiration_days": 60, "quantity": 1},
                {"option_type": "put", "side": "long", "strike": strike, "expiration_days": 60, "quantity": 1},
            ]
        elif strategy_type == "long_strangle":
            raw_legs = [
                {"option_type": "call", "side": "long", "strike": strike * 1.05, "expiration_days": 60, "quantity": 1},
                {"option_type": "put", "side": "long", "strike": strike * 0.95, "expiration_days": 60, "quantity": 1},
            ]
        elif strategy_type == "bull_call_spread":
            raw_legs = [
                {"option_type": "call", "side": "long", "strike": strike, "expiration_days": 60, "quantity": 1},
                {"option_type": "call", "side": "short", "strike": strike * 1.1, "expiration_days": 60, "quantity": 1},
            ]
        elif strategy_type == "bear_put_spread":
            raw_legs = [
                {"option_type": "put", "side": "long", "strike": strike, "expiration_days": 60, "quantity": 1},
                {"option_type": "put", "side": "short", "strike": strike * 0.9, "expiration_days": 60, "quantity": 1},
            ]
        elif strategy_type == "collar":
            raw_legs = [
                {"option_type": "put", "side": "long", "strike": strike * 0.95, "expiration_days": 60, "quantity": 1},
                {"option_type": "call", "side": "short", "strike": strike * 1.05, "expiration_days": 60, "quantity": 1},
            ]
        elif strategy_type == "cash_secured_put":
            raw_legs = [{"option_type": "put", "side": "short", "strike": strike, "expiration_days": 60, "quantity": 1}]
        else:
            raw_legs = [{"option_type": "call", "side": "short", "strike": strike, "expiration_days": 60, "quantity": 1}]

        return [
            self._price_leg(
                leg,
                underlying_price,
                risk_free_rate,
                volatility,
                dividend_yield,
            )
            for leg in raw_legs
        ]

    def _price_leg(
        self,
        leg: dict[str, object],
        underlying_price: float,
        risk_free_rate: float,
        volatility: float,
        dividend_yield: float,
    ) -> dict[str, float | int | str]:
        expiration_days = int(leg.get("expiration_days", 60))
        premium = leg.get("premium")
        if premium is None:
            premium = black_scholes_price(
                str(leg["option_type"]),
                underlying_price,
                float(leg["strike"]),
                expiration_days / 365,
                risk_free_rate,
                volatility,
                dividend_yield,
            )
        return {
            "option_type": str(leg["option_type"]),
            "side": str(leg["side"]),
            "strike": float(leg["strike"]),
            "expiration_days": expiration_days,
            "quantity": int(leg.get("quantity", 1)),
            "premium": float(premium),
        }

    def _aggregate_strategy_greeks(
        self,
        legs: list[dict[str, float | int | str]],
        underlying_price: float,
        risk_free_rate: float,
        volatility: float,
        dividend_yield: float,
    ) -> dict[str, float]:
        totals = {"delta": 0.0, "gamma": 0.0, "theta_daily": 0.0, "vega": 0.0, "rho": 0.0}
        for leg in legs:
            greeks = option_greeks(
                str(leg["option_type"]),
                underlying_price,
                float(leg["strike"]),
                int(leg["expiration_days"]) / 365,
                risk_free_rate,
                volatility,
                dividend_yield,
                str(leg["side"]),
            )
            quantity = int(leg["quantity"])
            for key in totals:
                totals[key] += greeks[key] * quantity
        return totals

    def _strategy_cfa_note(self, strategy_type: str) -> str:
        return {
            "covered_call": "Covered calls combine long stock with a short call.",
            "protective_put": "Protective puts combine long stock with a long put floor.",
            "long_straddle": "A straddle buys call and put exposure at the same strike.",
            "long_strangle": "A strangle buys OTM call and put exposure.",
            "bull_call_spread": "Bull call spreads use two calls to define bullish risk/reward.",
            "bear_put_spread": "Bear put spreads use two puts to define bearish risk/reward.",
            "collar": "A collar buys downside protection and sells upside.",
            "cash_secured_put": "A cash-secured put earns premium with purchase obligation.",
        }[strategy_type]
