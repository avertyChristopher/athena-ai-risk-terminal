from app.modules.rates_lab.domain.bonds import price_coupon_bond
from app.modules.rates_lab.domain.convexity import convexity_adjusted_price_impact
from app.modules.rates_lab.domain.curves import interpolate_curve_linear
from app.modules.rates_lab.domain.duration import duration_price_impact


def parallel_shift(
    curve_points: list[dict[str, float]],
    shock_bps: float,
) -> list[dict[str, float]]:
    shift = shock_bps / 10_000
    return [
        {"maturity": point["maturity"], "rate": point["rate"] + shift}
        for point in curve_points
    ]


def steepener_shift(
    curve_points: list[dict[str, float]],
    shock_bps: float,
) -> list[dict[str, float]]:
    return _slope_shift(curve_points, shock_bps, steepener=True)


def flattener_shift(
    curve_points: list[dict[str, float]],
    shock_bps: float,
) -> list[dict[str, float]]:
    return _slope_shift(curve_points, shock_bps, steepener=False)


def short_rate_shift(
    curve_points: list[dict[str, float]],
    shock_bps: float,
) -> list[dict[str, float]]:
    return _segment_shift(curve_points, shock_bps, short_end=True)


def long_rate_shift(
    curve_points: list[dict[str, float]],
    shock_bps: float,
) -> list[dict[str, float]]:
    return _segment_shift(curve_points, shock_bps, short_end=False)


def scenario_price_impact(
    face_value: float,
    coupon_rate: float,
    coupon_frequency: str,
    years_to_maturity: float,
    yield_to_maturity: float,
    modified_duration_value: float,
    convexity_value: float,
    scenario_type: str,
    shock_bps: float,
    curve_points: list[dict[str, float]] | None = None,
    shocked_curve_points: list[dict[str, float]] | None = None,
) -> dict[str, float | str]:
    base_curve = curve_points or _fallback_curve(yield_to_maturity)
    shocked_curve = shocked_curve_points or apply_curve_scenario(
        base_curve,
        scenario_type,
        shock_bps,
    )
    base_yield_at_maturity = interpolate_shocked_yield(
        base_curve,
        years_to_maturity,
    )
    shocked_yield_at_maturity = interpolate_shocked_yield(
        shocked_curve,
        years_to_maturity,
    )
    effective_bps = calculate_effective_yield_shock(
        base_curve,
        shocked_curve,
        years_to_maturity,
    )
    rate_change = effective_bps / 10_000
    base_price, _ = price_coupon_bond(
        face_value,
        coupon_rate,
        coupon_frequency,
        years_to_maturity,
        yield_to_maturity,
    )
    stressed_yield = yield_to_maturity + rate_change
    stressed_price, _ = price_coupon_bond(
        face_value,
        coupon_rate,
        coupon_frequency,
        years_to_maturity,
        stressed_yield,
    )
    price_change = stressed_price - base_price
    return {
        "scenario_type": scenario_type,
        "requested_shock_bps": shock_bps,
        "effective_shock_bps": effective_bps,
        "base_yield": yield_to_maturity,
        "stressed_yield": stressed_yield,
        "base_yield_at_maturity": base_yield_at_maturity,
        "shocked_yield_at_maturity": shocked_yield_at_maturity,
        "base_price": base_price,
        "stressed_price": stressed_price,
        "price_change": price_change,
        "percent_change": price_change / base_price,
        "duration_estimate": duration_price_impact(
            base_price,
            modified_duration_value,
            rate_change,
        ),
        "convexity_adjusted_estimate": convexity_adjusted_price_impact(
            base_price,
            modified_duration_value,
            convexity_value,
            rate_change,
        ),
        "dv01_impact": -modified_duration_value * base_price * effective_bps / 10_000,
    }


def apply_curve_scenario(
    curve_points: list[dict[str, float]],
    scenario_type: str,
    shock_bps: float,
) -> list[dict[str, float]]:
    if scenario_type == "parallel_up":
        return parallel_shift(curve_points, abs(shock_bps))
    if scenario_type == "parallel_down":
        return parallel_shift(curve_points, -abs(shock_bps))
    if scenario_type == "steepener":
        return steepener_shift(curve_points, abs(shock_bps))
    if scenario_type == "flattener":
        return flattener_shift(curve_points, abs(shock_bps))
    if scenario_type == "short_rate_up":
        return short_rate_shift(curve_points, abs(shock_bps))
    if scenario_type == "short_rate_down":
        return short_rate_shift(curve_points, -abs(shock_bps))
    if scenario_type == "long_rate_up":
        return long_rate_shift(curve_points, abs(shock_bps))
    if scenario_type == "long_rate_down":
        return long_rate_shift(curve_points, -abs(shock_bps))
    raise ValueError(f"Unsupported scenario type: {scenario_type}.")


def shift_curve(
    curve_points: list[dict[str, float]],
    scenario_type: str,
    shock_bps: float,
) -> list[dict[str, float]]:
    return apply_curve_scenario(curve_points, scenario_type, shock_bps)


def interpolate_shocked_yield(
    curve_points: list[dict[str, float]],
    target_maturity: float,
) -> float:
    return float(
        interpolate_curve_linear(curve_points, [target_maturity])[0]["rate"]
    )


def calculate_effective_yield_shock(
    base_curve: list[dict[str, float]],
    shocked_curve: list[dict[str, float]],
    target_maturity: float,
) -> float:
    base_yield = interpolate_shocked_yield(base_curve, target_maturity)
    shocked_yield = interpolate_shocked_yield(shocked_curve, target_maturity)
    return (shocked_yield - base_yield) * 10_000


def _slope_shift(
    curve_points: list[dict[str, float]],
    shock_bps: float,
    *,
    steepener: bool,
) -> list[dict[str, float]]:
    if not curve_points:
        return []
    maturities = [float(point["maturity"]) for point in curve_points]
    low, high = min(maturities), max(maturities)
    span = max(high - low, 1e-9)
    shifted = []
    for point in curve_points:
        position = (float(point["maturity"]) - low) / span
        signed_weight = position - 0.5
        if not steepener:
            signed_weight *= -1
        shifted.append(
            {
                "maturity": float(point["maturity"]),
                "rate": float(point["rate"]) + signed_weight * shock_bps / 10_000,
            }
        )
    return shifted


def _segment_shift(
    curve_points: list[dict[str, float]],
    shock_bps: float,
    *,
    short_end: bool,
) -> list[dict[str, float]]:
    shifted = []
    for point in curve_points:
        maturity = float(point["maturity"])
        weight = max(0.0, 1 - maturity / 10) if short_end else min(1.0, maturity / 10)
        shifted.append(
            {
                "maturity": maturity,
                "rate": float(point["rate"]) + weight * shock_bps / 10_000,
            }
        )
    return shifted


def _fallback_curve(yield_to_maturity: float) -> list[dict[str, float]]:
    return [
        {"maturity": maturity, "rate": yield_to_maturity}
        for maturity in (0.25, 1.0, 2.0, 5.0, 10.0, 30.0)
    ]
