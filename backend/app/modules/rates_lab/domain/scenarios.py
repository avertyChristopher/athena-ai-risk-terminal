from app.modules.rates_lab.domain.bonds import price_coupon_bond
from app.modules.rates_lab.domain.convexity import convexity_adjusted_price_impact
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
) -> dict[str, float | str]:
    effective_bps = _effective_bond_shock(
        scenario_type,
        shock_bps,
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


def shift_curve(
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


def _effective_bond_shock(
    scenario_type: str,
    shock_bps: float,
    maturity: float,
) -> float:
    magnitude = abs(shock_bps)
    if scenario_type == "parallel_up":
        return magnitude
    if scenario_type == "parallel_down":
        return -magnitude
    long_weight = min(1.0, max(0.0, maturity / 10))
    short_weight = 1 - long_weight
    if scenario_type == "steepener":
        return magnitude * (long_weight - short_weight) / 2
    if scenario_type == "flattener":
        return magnitude * (short_weight - long_weight) / 2
    if scenario_type == "short_rate_up":
        return magnitude * short_weight
    if scenario_type == "short_rate_down":
        return -magnitude * short_weight
    if scenario_type == "long_rate_up":
        return magnitude * long_weight
    if scenario_type == "long_rate_down":
        return -magnitude * long_weight
    raise ValueError(f"Unsupported scenario type: {scenario_type}.")


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
