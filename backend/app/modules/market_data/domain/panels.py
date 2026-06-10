from collections.abc import Mapping, Sequence
from typing import Any

from app.modules.market_data.domain.price_series import sort_price_series
from app.modules.market_data.domain.returns import calculate_simple_returns


def align_price_series(
    series_by_symbol: Mapping[str, Sequence[Mapping[str, Any]]],
) -> list[dict[str, float | str]]:
    dates = _common_dates(series_by_symbol)
    close_by_symbol = {
        symbol: {
            str(row["date"]): float(row["close"])
            for row in sort_price_series(rows)
            if row.get("close") not in (None, "")
        }
        for symbol, rows in series_by_symbol.items()
    }
    return [
        {
            "date": date,
            **{symbol: close_by_symbol[symbol][date] for symbol in close_by_symbol},
        }
        for date in dates
    ]


def build_price_panel(
    series_by_symbol: Mapping[str, Sequence[Mapping[str, Any]]],
) -> list[dict[str, float | str]]:
    return align_price_series(series_by_symbol)


def align_return_series(
    series_by_symbol: Mapping[str, Sequence[Mapping[str, Any]]],
    return_type: str = "price_return",
) -> list[dict[str, float | str]]:
    returns_by_symbol: dict[str, dict[str, float]] = {}
    for symbol, rows in series_by_symbol.items():
        sorted_rows = sort_price_series(rows)
        prices = [
            _price_for_return(row, return_type)
            for row in sorted_rows
            if row.get("close") not in (None, "")
        ]
        dates = [str(row["date"]) for row in sorted_rows if row.get("close") not in (None, "")]
        returns = calculate_simple_returns(prices)
        returns_by_symbol[symbol] = {
            date: period_return
            for date, period_return in zip(dates[1:], returns)
        }

    common_dates = sorted(
        set.intersection(
            *(set(symbol_returns) for symbol_returns in returns_by_symbol.values()),
        )
        if returns_by_symbol
        else set(),
    )
    return [
        {
            "date": date,
            **{
                symbol: symbol_returns[date]
                for symbol, symbol_returns in returns_by_symbol.items()
            },
        }
        for date in common_dates
    ]


def build_returns_panel(
    series_by_symbol: Mapping[str, Sequence[Mapping[str, Any]]],
    return_type: str = "price_return",
) -> list[dict[str, float | str]]:
    return align_return_series(series_by_symbol, return_type)


def detect_non_overlapping_dates(
    series_by_symbol: Mapping[str, Sequence[Mapping[str, Any]]],
) -> list[str]:
    if not series_by_symbol:
        return []

    common_dates = set(_common_dates(series_by_symbol))
    warnings = []
    for symbol, rows in series_by_symbol.items():
        symbol_dates = {str(row["date"]) for row in rows}
        missing_from_common = sorted(symbol_dates - common_dates)
        if missing_from_common:
            warnings.append(
                f"{symbol} has {len(missing_from_common)} dates outside the aligned panel.",
            )
    return warnings


def _common_dates(
    series_by_symbol: Mapping[str, Sequence[Mapping[str, Any]]],
) -> list[str]:
    if not series_by_symbol:
        return []

    date_sets = [
        {str(row["date"]) for row in rows if row.get("close") not in (None, "")}
        for rows in series_by_symbol.values()
    ]
    return sorted(set.intersection(*date_sets) if date_sets else set())


def _price_for_return(row: Mapping[str, Any], return_type: str) -> float:
    if return_type == "total_return":
        return float(row.get("adjusted_close", row["close"]))
    return float(row["close"])
