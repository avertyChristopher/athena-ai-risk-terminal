from math import exp, sqrt

from app.modules.options_pricing_lab.domain.black_scholes import (
    d1,
    d2,
    normal_cdf,
    normal_pdf,
)


def option_greeks(
    option_type: str,
    underlying_price: float,
    strike_price: float,
    time_to_expiration_years: float,
    risk_free_rate: float,
    volatility: float,
    dividend_yield: float = 0.0,
    position_side: str = "long",
) -> dict[str, float]:
    first = d1(
        underlying_price,
        strike_price,
        time_to_expiration_years,
        risk_free_rate,
        volatility,
        dividend_yield,
    )
    second = d2(
        underlying_price,
        strike_price,
        time_to_expiration_years,
        risk_free_rate,
        volatility,
        dividend_yield,
    )
    discount_dividend = exp(-dividend_yield * time_to_expiration_years)
    discount_rate = exp(-risk_free_rate * time_to_expiration_years)
    pdf = normal_pdf(first)

    if option_type == "call":
        delta = discount_dividend * normal_cdf(first)
        theta = (
            -underlying_price
            * discount_dividend
            * pdf
            * volatility
            / (2 * sqrt(time_to_expiration_years))
            - risk_free_rate
            * strike_price
            * discount_rate
            * normal_cdf(second)
            + dividend_yield
            * underlying_price
            * discount_dividend
            * normal_cdf(first)
        )
        rho = strike_price * time_to_expiration_years * discount_rate * normal_cdf(second)
    else:
        delta = discount_dividend * (normal_cdf(first) - 1)
        theta = (
            -underlying_price
            * discount_dividend
            * pdf
            * volatility
            / (2 * sqrt(time_to_expiration_years))
            + risk_free_rate
            * strike_price
            * discount_rate
            * normal_cdf(-second)
            - dividend_yield
            * underlying_price
            * discount_dividend
            * normal_cdf(-first)
        )
        rho = -strike_price * time_to_expiration_years * discount_rate * normal_cdf(-second)

    gamma = (
        discount_dividend
        * pdf
        / (underlying_price * volatility * sqrt(time_to_expiration_years))
    )
    vega = underlying_price * discount_dividend * pdf * sqrt(time_to_expiration_years)
    sign = 1.0 if position_side == "long" else -1.0

    return {
        "delta": delta * sign,
        "gamma": gamma * sign,
        "theta_annual": theta * sign,
        "theta_daily": theta / 365 * sign,
        "vega": vega / 100 * sign,
        "rho": rho / 100 * sign,
    }


def aggregate_strategy_greeks(
    legs: list[dict[str, object]],
    underlying_price: float,
    risk_free_rate: float,
    volatility: float,
    dividend_yield: float,
) -> dict[str, object]:
    aggregate = {
        "aggregate_delta": 0.0,
        "aggregate_gamma": 0.0,
        "aggregate_theta": 0.0,
        "aggregate_vega": 0.0,
        "aggregate_rho": 0.0,
    }
    leg_results = []

    for leg in legs:
        leg_type = str(leg.get("leg_type", "option"))
        side = str(leg.get("side", "long"))
        side_multiplier = 1.0 if side == "long" else -1.0
        quantity = int(leg.get("quantity", 1) or 1)
        contract_size = int(leg.get("contract_size", 100) or 100)

        if leg_type == "stock":
            raw = {
                "delta": side_multiplier,
                "gamma": 0.0,
                "theta": 0.0,
                "vega": 0.0,
                "rho": 0.0,
            }
        elif leg_type == "option":
            option_values = option_greeks(
                str(leg["option_type"]),
                underlying_price,
                float(leg["strike_price"]),
                int(leg["expiration_days"]) / 365,
                risk_free_rate,
                volatility,
                dividend_yield,
                side,
            )
            raw = {
                "delta": option_values["delta"],
                "gamma": option_values["gamma"],
                "theta": option_values["theta_daily"],
                "vega": option_values["vega"],
                "rho": option_values["rho"],
            }
        else:
            raw = {"delta": 0.0, "gamma": 0.0, "theta": 0.0, "vega": 0.0, "rho": 0.0}

        contract = {key: value * contract_size for key, value in raw.items()}
        position = {key: value * quantity for key, value in contract.items()}
        aggregate["aggregate_delta"] += position["delta"]
        aggregate["aggregate_gamma"] += position["gamma"]
        aggregate["aggregate_theta"] += position["theta"]
        aggregate["aggregate_vega"] += position["vega"]
        aggregate["aggregate_rho"] += position["rho"]
        leg_results.append(
            {
                "leg_type": leg_type,
                "description": str(leg.get("description", "")),
                "contract_size": contract_size,
                "quantity": quantity,
                "raw_greeks": raw,
                "contract_greeks": contract,
                "position_greeks": position,
            }
        )

    aggregate["delta_adjusted_exposure"] = (
        aggregate["aggregate_delta"] * underlying_price
    )
    return {
        **aggregate,
        "delta": aggregate["aggregate_delta"],
        "gamma": aggregate["aggregate_gamma"],
        "theta": aggregate["aggregate_theta"],
        "vega": aggregate["aggregate_vega"],
        "rho": aggregate["aggregate_rho"],
        "legs": leg_results,
        "unit_metadata": {
            "delta": "Position value change for a $1 move in the underlying.",
            "gamma": "Position Delta change for a $1 move in the underlying.",
            "theta": "Estimated daily position time decay.",
            "vega": "Position value change for a 1 percentage point volatility move.",
            "rho": "Position value change for a 1 percentage point rate move.",
            "delta_adjusted_exposure": "Aggregate Delta multiplied by underlying price.",
        },
    }
