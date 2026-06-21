def bond_commentary(
    price_status: str,
    coupon_rate: float,
    yield_to_maturity: float,
    modified_duration: float | None = None,
    shock_bps: float | None = None,
) -> dict[str, object]:
    relation = {
        "discount": "The bond trades below par because its yield exceeds its coupon rate.",
        "premium": "The bond trades above par because its coupon rate exceeds its yield.",
        "par": "The bond trades near par because its coupon rate and yield are aligned.",
    }[price_status]
    key_points = [relation, "Bond prices and yields move inversely."]
    if modified_duration is not None and shock_bps is not None:
        approximate_change = -modified_duration * shock_bps / 10_000
        key_points.append(
            f"Modified duration implies an approximate {approximate_change:.2%} price change for the selected shock before convexity."
        )
    return {
        "summary": relation,
        "key_points": key_points,
        "cfa_notes": [
            "Longer maturities generally increase interest-rate sensitivity.",
            "Lower coupons generally increase duration, all else equal.",
            "Convexity improves estimates for larger yield changes.",
        ],
        "not_investment_advice": True,
        "input_relationship": {
            "coupon_rate": coupon_rate,
            "yield_to_maturity": yield_to_maturity,
        },
    }


def curve_commentary(curve_shape: str, slope: float) -> dict[str, object]:
    descriptions = {
        "normal": "Long-term rates exceed short-term rates in a normally upward-sloping curve.",
        "steep": "The curve is steep, with a pronounced long-term rate premium.",
        "inverted": "Short-term rates exceed long-term rates, producing an inverted curve.",
        "flat": "Short- and long-term rates are closely aligned.",
    }
    return {
        "summary": descriptions[curve_shape],
        "key_points": [
            f"Curve slope is {slope * 10_000:.1f} basis points.",
            "Forward rates are implied by spot rates and are not forecasts.",
        ],
        "cfa_notes": [
            "The term structure reflects expectations, risk premiums and market conditions.",
        ],
        "not_investment_advice": True,
    }
