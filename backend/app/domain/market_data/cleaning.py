from collections.abc import Mapping
from typing import Any

OHLCV_COLUMN_ALIASES = {
    "date": "date",
    "as_of": "date",
    "timestamp": "date",
    "symbol": "symbol",
    "ticker": "symbol",
    "open": "open",
    "open_price": "open",
    "high": "high",
    "high_price": "high",
    "low": "low",
    "low_price": "low",
    "close": "close",
    "adj_close": "close",
    "adjusted_close": "close",
    "price": "close",
    "volume": "volume",
    "shares_traded": "volume",
}


def normalize_ohlcv_columns(row: Mapping[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}

    for key, value in row.items():
        normalized_key = key.strip().lower()
        canonical_key = OHLCV_COLUMN_ALIASES.get(normalized_key, normalized_key)
        normalized[canonical_key] = value

    return normalized
