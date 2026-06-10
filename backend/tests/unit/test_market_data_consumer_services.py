import pytest

from app.modules.market_data.domain.adjustments import (
    calculate_price_return,
    calculate_total_return,
    validate_adjusted_close,
)
from app.modules.market_data.domain.consumer_quality import (
    create_data_quality_score,
    detect_currency_mismatches,
    detect_missing_symbols,
    detect_stale_prices,
)
from app.modules.market_data.domain.panels import (
    build_price_panel,
    build_returns_panel,
)
from app.modules.market_data.domain.reference_data import (
    convert_market_value,
    get_demo_fx_rate,
    get_risk_free_rate_proxy,
)


def test_build_price_panel_aligns_symbols_by_common_dates() -> None:
    panel = build_price_panel(
        {
            "AAPL": [
                {"date": "2026-01-01", "close": 100},
                {"date": "2026-01-02", "close": 101},
            ],
            "MSFT": [
                {"date": "2026-01-02", "close": 200},
                {"date": "2026-01-03", "close": 203},
            ],
        },
    )

    assert panel == [{"date": "2026-01-02", "AAPL": 101.0, "MSFT": 200.0}]


def test_build_returns_panel_aligns_return_dates() -> None:
    panel = build_returns_panel(
        {
            "AAPL": [
                {"date": "2026-01-01", "close": 100},
                {"date": "2026-01-02", "close": 110},
                {"date": "2026-01-03", "close": 121},
            ],
            "MSFT": [
                {"date": "2026-01-01", "close": 200},
                {"date": "2026-01-02", "close": 210},
                {"date": "2026-01-03", "close": 231},
            ],
        },
    )

    assert panel[0]["date"] == "2026-01-02"
    assert panel[0]["AAPL"] == pytest.approx(0.10)
    assert panel[1]["MSFT"] == pytest.approx(0.10)


def test_missing_stale_and_currency_quality_helpers() -> None:
    assert detect_missing_symbols(["AAPL", "XXX"], ["AAPL"]) == ["XXX"]
    assert detect_currency_mismatches(
        [{"symbol": "BNS", "currency": "CAD"}],
        "USD",
    ) == ["BNS"]
    assert detect_stale_prices(
        [{"symbol": "AAPL", "date": "2026-06-01"}],
        as_of_date=__import__("datetime").date(2026, 6, 10),
    ) == ["AAPL"]


def test_data_quality_score_penalizes_warnings() -> None:
    score = create_data_quality_score(
        [
            {
                "is_valid": True,
                "stale_latest_price": True,
                "currency_mismatch": False,
                "missing_price_dates": [],
            },
        ],
    )

    assert score == pytest.approx(0.75)


def test_adjusted_price_and_reference_data_helpers() -> None:
    assert calculate_price_return(100, 105) == pytest.approx(0.05)
    assert calculate_total_return(100, 106) == pytest.approx(0.06)
    assert validate_adjusted_close([{"close": 100, "adjusted_close": 99}]) is True
    assert get_demo_fx_rate("USD", "CAD") == pytest.approx(1.37)
    assert convert_market_value(100, 1.37) == pytest.approx(137)
    assert get_risk_free_rate_proxy("USD", "3M") == pytest.approx(0.04)
