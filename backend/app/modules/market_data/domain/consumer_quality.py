from collections.abc import Mapping, Sequence
from datetime import date, datetime
from typing import Any


def detect_missing_symbols(
    requested_symbols: Sequence[str],
    available_symbols: Sequence[str],
) -> list[str]:
    available = {symbol.upper() for symbol in available_symbols}
    return [
        symbol.upper()
        for symbol in requested_symbols
        if symbol.upper() not in available
    ]


def validate_symbol_universe(
    requested_symbols: Sequence[str],
    available_symbols: Sequence[str],
) -> bool:
    return not detect_missing_symbols(requested_symbols, available_symbols)


def detect_stale_prices(
    latest_prices: Sequence[Mapping[str, Any]],
    as_of_date: date,
    stale_after_days: int = 3,
) -> list[str]:
    stale_symbols = []
    for latest_price in latest_prices:
        price_date = datetime.strptime(str(latest_price["date"]), "%Y-%m-%d").date()
        if (as_of_date - price_date).days > stale_after_days:
            stale_symbols.append(str(latest_price["symbol"]).upper())
    return stale_symbols


def detect_currency_mismatches(
    assets: Sequence[Mapping[str, Any]],
    expected_currency: str,
) -> list[str]:
    expected = expected_currency.upper()
    return [
        str(asset["symbol"]).upper()
        for asset in assets
        if str(asset.get("currency", "")).upper() != expected
    ]


def summarize_data_quality_for_symbols(
    symbol_reports: Sequence[Mapping[str, Any]],
) -> list[str]:
    warnings = []
    for report in symbol_reports:
        symbol = str(report["symbol"]).upper()
        if not report.get("is_valid", False):
            warnings.append(f"{symbol}: invalid price series.")
        if report.get("stale_latest_price", False):
            warnings.append(f"{symbol}: stale latest price.")
        if report.get("currency_mismatch", False):
            warnings.append(f"{symbol}: currency mismatch warning.")
        if report.get("missing_price_dates"):
            warnings.append(f"{symbol}: missing price dates.")
    return warnings


def create_data_quality_score(symbol_reports: Sequence[Mapping[str, Any]]) -> float:
    if not symbol_reports:
        return 0.0

    penalties = 0
    for report in symbol_reports:
        penalties += int(not report.get("is_valid", False))
        penalties += int(report.get("stale_latest_price", False))
        penalties += int(report.get("currency_mismatch", False))
        penalties += int(bool(report.get("missing_price_dates")))

    possible_penalties = len(symbol_reports) * 4
    return max(0.0, 1.0 - penalties / possible_penalties)


def validate_portfolio_market_data(
    symbol_reports: Sequence[Mapping[str, Any]],
) -> bool:
    return create_data_quality_score(symbol_reports) >= 0.75
