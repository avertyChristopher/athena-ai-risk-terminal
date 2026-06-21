def interpolate_curve_linear(
    curve_points: list[dict[str, float]],
    requested_maturities: list[float],
) -> list[dict[str, float]]:
    points = _sorted_unique_points(curve_points)
    if not points:
        raise ValueError("At least one curve point is required.")

    output = []
    for maturity in sorted(set(requested_maturities)):
        if maturity <= points[0]["maturity"]:
            rate = points[0]["rate"]
        elif maturity >= points[-1]["maturity"]:
            rate = points[-1]["rate"]
        else:
            left, right = next(
                (left, right)
                for left, right in zip(points, points[1:])
                if left["maturity"] <= maturity <= right["maturity"]
            )
            span = right["maturity"] - left["maturity"]
            weight = (maturity - left["maturity"]) / span
            rate = left["rate"] + weight * (right["rate"] - left["rate"])
        output.append({"maturity": maturity, "rate": rate})
    return output


def calculate_forward_rates(
    spot_curve: list[dict[str, float]],
) -> list[dict[str, float]]:
    points = _sorted_unique_points(spot_curve)
    forwards = []
    for start, end in zip(points, points[1:]):
        start_maturity = start["maturity"]
        end_maturity = end["maturity"]
        interval = end_maturity - start_maturity
        if interval <= 0 or start["rate"] <= -1 or end["rate"] <= -1:
            continue
        accumulated_end = (1 + end["rate"]) ** end_maturity
        accumulated_start = (1 + start["rate"]) ** start_maturity
        forward_rate = (accumulated_end / accumulated_start) ** (1 / interval) - 1
        forwards.append(
            {
                "start_maturity": start_maturity,
                "end_maturity": end_maturity,
                "forward_rate": forward_rate,
            }
        )
    return forwards


def curve_slope(curve_points: list[dict[str, float]]) -> float:
    points = _sorted_unique_points(curve_points)
    if len(points) < 2:
        return 0.0
    return points[-1]["rate"] - points[0]["rate"]


def classify_curve_shape(curve_points: list[dict[str, float]]) -> str:
    slope = curve_slope(curve_points)
    if slope > 0.01:
        return "steep"
    if slope > 0.001:
        return "normal"
    if slope < -0.001:
        return "inverted"
    return "flat"


def _sorted_unique_points(
    curve_points: list[dict[str, float]],
) -> list[dict[str, float]]:
    by_maturity = {
        float(point["maturity"]): float(point["rate"])
        for point in curve_points
    }
    return [
        {"maturity": maturity, "rate": rate}
        for maturity, rate in sorted(by_maturity.items())
    ]
