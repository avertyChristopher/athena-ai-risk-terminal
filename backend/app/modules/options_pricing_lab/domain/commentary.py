def option_commentary(
    option_type: str,
    position_side: str,
    moneyness: str,
    delta: float,
    theta_daily: float,
    vega: float,
    risk_note: str,
) -> dict[str, list[str] | str]:
    direction = "benefits from upside moves" if delta > 0 else "benefits from downside moves"
    return {
        "summary": (
            f"This {position_side} {option_type} is {moneyness.replace('_', ' ')} and "
            f"{direction}. Theta of {theta_daily:.4f} highlights time decay, while "
            f"Vega of {vega:.4f} shows volatility sensitivity."
        ),
        "key_points": [
            risk_note,
            "Higher volatility generally increases option value.",
            "Greeks change as price, volatility and time to expiration change.",
            "This is educational and not investment advice.",
        ],
        "cfa_notes": [
            "A derivative derives value from an underlying asset.",
            "A call option gives the right to buy; a put option gives the right to sell.",
            "Intrinsic value is immediate exercise value; time value is premium above intrinsic value.",
            "Put-call parity links European calls, puts, the underlying and a risk-free bond.",
            "Black-Scholes assumes European exercise, lognormal returns and constant volatility.",
            "The binomial model prices options by backward induction from future payoffs.",
            "Delta measures directional exposure, Gamma convexity, Theta time decay, Vega volatility sensitivity and Rho rate sensitivity.",
        ],
    }


def strategy_commentary(strategy_type: str, risk_profile: str) -> dict[str, list[str] | str]:
    return {
        "summary": f"{strategy_type.replace('_', ' ').title()} profile: {risk_profile}",
        "key_points": [
            "Strategy payoffs are deterministic educational scenarios.",
            "Premiums, strikes and quantities drive max gain, max loss and breakevens.",
            "Options strategies can hedge, amplify or reshape portfolio exposure.",
        ],
        "cfa_notes": [
            "Covered calls exchange upside for premium income.",
            "Protective puts reduce downside risk at the cost of premium.",
            "Spreads combine long and short options to define risk and reward.",
            "Straddles and strangles express volatility views.",
        ],
    }
