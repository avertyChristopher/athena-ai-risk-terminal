from app.modules.options_pricing_lab.domain.black_scholes import black_scholes_price
from app.modules.options_pricing_lab.domain.greeks import option_greeks
from app.modules.options_pricing_lab.domain.payoff import option_payoff, option_profit


def payoff_scenarios(
    option_type: str,
    position_side: str,
    underlying_price: float,
    strike_price: float,
    premium: float,
    contract_size: int,
    quantity: int,
    spot_shocks: list[float] | None = None,
) -> list[dict[str, float]]:
    shocks = spot_shocks or [-30.0, -20.0, -10.0, 0.0, 10.0, 20.0, 30.0]
    return [
        _payoff_row(
            underlying_price * (1.0 + shock / 100),
            option_type,
            position_side,
            strike_price,
            premium,
            contract_size,
            quantity,
        )
        for shock in shocks
    ]


def sensitivity_analysis(
    option_type: str,
    underlying_price: float,
    strike_price: float,
    time_to_expiration_years: float,
    risk_free_rate: float,
    volatility: float,
    dividend_yield: float,
    spot_shocks: list[float] | None = None,
    volatility_shocks: list[float] | None = None,
    time_points_days: list[int] | None = None,
    rate_shocks: list[float] | None = None,
) -> dict[str, object]:
    price_shocks = spot_shocks or [-30.0, -20.0, -10.0, 0.0, 10.0, 20.0, 30.0]
    volatility_points = volatility_shocks or [-10.0, -5.0, 0.0, 5.0, 10.0]
    rate_points = rate_shocks or [-1.0, 0.0, 1.0]
    expiration_days = max(1, round(time_to_expiration_years * 365))
    requested_time_points = time_points_days or [1, 7, 30, 60, 90]
    time_days = sorted(
        {
            expiration_days,
            *(day for day in requested_time_points if 1 <= day <= expiration_days),
        }
    )

    return {
        "price": [
            _price_row(
                option_type,
                underlying_price * (1 + shock / 100),
                strike_price,
                time_to_expiration_years,
                risk_free_rate,
                volatility,
                dividend_yield,
                "underlying_price",
            )
            for shock in price_shocks
        ],
        "volatility": [
            _price_row(
                option_type,
                underlying_price,
                strike_price,
                time_to_expiration_years,
                risk_free_rate,
                max(0.0001, volatility + shock / 100),
                dividend_yield,
                "volatility",
            )
            for shock in volatility_points
        ],
        "time_decay": [
            _price_row(
                option_type,
                underlying_price,
                strike_price,
                max(days / 365, 1 / 365),
                risk_free_rate,
                volatility,
                dividend_yield,
                "days",
                display_value=float(days),
            )
            for days in time_days
        ],
        "rates": [
            _price_row(
                option_type,
                underlying_price,
                strike_price,
                time_to_expiration_years,
                max(-0.99, risk_free_rate + shock / 100),
                volatility,
                dividend_yield,
                "risk_free_rate",
            )
            for shock in rate_points
        ],
        "scenario_metadata": {
            "spot_shocks_percent": price_shocks,
            "volatility_shocks_percentage_points": volatility_points,
            "rate_shocks_percentage_points": rate_points,
            "time_points_days": time_days,
            "expiration_days": expiration_days,
            "time_scenarios_capped": True,
            "note": "Time decay scenarios are capped at the option's current expiration.",
        },
    }


def greek_sensitivity(
    option_type: str,
    underlying_price: float,
    strike_price: float,
    time_to_expiration_years: float,
    risk_free_rate: float,
    volatility: float,
    dividend_yield: float,
    position_side: str,
) -> list[dict[str, float]]:
    return [
        {
            "underlying_price": underlying_price * (1.0 + shock),
            **option_greeks(
                option_type,
                underlying_price * (1.0 + shock),
                strike_price,
                time_to_expiration_years,
                risk_free_rate,
                volatility,
                dividend_yield,
                position_side,
            ),
        }
        for shock in [-0.20, -0.10, 0.0, 0.10, 0.20]
    ]


def _payoff_row(
    scenario_price: float,
    option_type: str,
    side: str,
    strike_price: float,
    premium: float,
    contract_size: int,
    quantity: int,
) -> dict[str, float]:
    payoff = option_payoff(scenario_price, strike_price, option_type, side)
    profit = option_profit(payoff, premium, side)
    multiplier = contract_size * quantity
    return {
        "underlying_price": scenario_price,
        "payoff": payoff * multiplier,
        "profit": profit * multiplier,
    }


def _price_row(
    option_type: str,
    underlying_price: float,
    strike_price: float,
    time_to_expiration_years: float,
    risk_free_rate: float,
    volatility: float,
    dividend_yield: float,
    input_name: str,
    display_value: float | None = None,
) -> dict[str, float | str]:
    price = black_scholes_price(
        option_type,
        underlying_price,
        strike_price,
        time_to_expiration_years,
        risk_free_rate,
        volatility,
        dividend_yield,
    )
    values = {
        "underlying_price": underlying_price,
        "volatility": volatility,
        "days": time_to_expiration_years * 365,
        "risk_free_rate": risk_free_rate,
    }
    return {
        "input": input_name,
        "value": display_value if display_value is not None else values[input_name],
        "option_price": price,
    }
