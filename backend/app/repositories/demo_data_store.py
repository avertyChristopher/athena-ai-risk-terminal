import csv
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

DEMO_DATA_DIR = Path(__file__).resolve().parents[3] / "data" / "demo"


class DemoDataStore:
    _loaded = False
    _assets: list[dict[str, Any]] = []
    _prices: list[dict[str, Any]] = []
    _portfolios: dict[str, dict[str, Any]] = {}
    _positions: dict[str, dict[str, Any]] = {}

    @classmethod
    def ensure_loaded(cls) -> None:
        if cls._loaded:
            return

        cls._assets = _load_json_list("demo_assets.json")
        cls._prices = _load_price_csv("demo_prices.csv")

        portfolio = _load_json("demo_portfolio.json")
        cls._portfolios = {str(portfolio["id"]): portfolio}

        positions = _load_json_list("demo_positions.json")
        cls._positions = {str(position["id"]): position for position in positions}
        cls._loaded = True

    @classmethod
    def list_assets(cls) -> list[dict[str, Any]]:
        cls.ensure_loaded()
        return deepcopy(cls._assets)

    @classmethod
    def list_prices(cls, symbol: str | None = None) -> list[dict[str, Any]]:
        cls.ensure_loaded()
        prices = cls._prices
        if symbol is not None:
            prices = [
                price
                for price in cls._prices
                if price["symbol"].upper() == symbol.upper()
            ]

        return deepcopy(prices)

    @classmethod
    def list_portfolios(cls) -> list[dict[str, Any]]:
        cls.ensure_loaded()
        return deepcopy(list(cls._portfolios.values()))

    @classmethod
    def get_portfolio(cls, portfolio_id: str) -> dict[str, Any] | None:
        cls.ensure_loaded()
        portfolio = cls._portfolios.get(portfolio_id)
        return deepcopy(portfolio) if portfolio is not None else None

    @classmethod
    def create_portfolio(cls, payload: dict[str, Any]) -> dict[str, Any]:
        cls.ensure_loaded()
        portfolio_id = _next_id("pf", cls._portfolios)
        portfolio = {"id": portfolio_id, **payload}
        cls._portfolios[portfolio_id] = portfolio
        return deepcopy(portfolio)

    @classmethod
    def update_portfolio(
        cls,
        portfolio_id: str,
        payload: dict[str, Any],
    ) -> dict[str, Any] | None:
        cls.ensure_loaded()
        portfolio = cls._portfolios.get(portfolio_id)
        if portfolio is None:
            return None

        portfolio.update(
            {key: value for key, value in payload.items() if value is not None},
        )
        return deepcopy(portfolio)

    @classmethod
    def delete_portfolio(cls, portfolio_id: str) -> bool:
        cls.ensure_loaded()
        removed = cls._portfolios.pop(portfolio_id, None)
        if removed is None:
            return False

        cls._positions = {
            position_id: position
            for position_id, position in cls._positions.items()
            if position["portfolio_id"] != portfolio_id
        }
        return True

    @classmethod
    def list_positions(cls, portfolio_id: str) -> list[dict[str, Any]]:
        cls.ensure_loaded()
        return deepcopy(
            [
                position
                for position in cls._positions.values()
                if position["portfolio_id"] == portfolio_id
            ]
        )

    @classmethod
    def get_position(
        cls,
        portfolio_id: str,
        position_id: str,
    ) -> dict[str, Any] | None:
        cls.ensure_loaded()
        position = cls._positions.get(position_id)
        if position is None or position["portfolio_id"] != portfolio_id:
            return None

        return deepcopy(position)

    @classmethod
    def create_position(
        cls,
        portfolio_id: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        cls.ensure_loaded()
        position_id = _next_id("pos", cls._positions)
        position = {"id": position_id, "portfolio_id": portfolio_id, **payload}
        cls._positions[position_id] = position
        return deepcopy(position)

    @classmethod
    def update_position(
        cls,
        portfolio_id: str,
        position_id: str,
        payload: dict[str, Any],
    ) -> dict[str, Any] | None:
        cls.ensure_loaded()
        position = cls._positions.get(position_id)
        if position is None or position["portfolio_id"] != portfolio_id:
            return None

        position.update(
            {key: value for key, value in payload.items() if value is not None},
        )
        return deepcopy(position)

    @classmethod
    def delete_position(cls, portfolio_id: str, position_id: str) -> bool:
        cls.ensure_loaded()
        position = cls._positions.get(position_id)
        if position is None or position["portfolio_id"] != portfolio_id:
            return False

        del cls._positions[position_id]
        return True


def _load_json(file_name: str) -> Any:
    with (DEMO_DATA_DIR / file_name).open(encoding="utf-8") as file:
        return json.load(file)


def _load_json_list(file_name: str) -> list[dict[str, Any]]:
    data = _load_json(file_name)
    if not isinstance(data, list):
        raise ValueError(f"{file_name} must contain a list.")

    return data


def _load_price_csv(file_name: str) -> list[dict[str, Any]]:
    with (DEMO_DATA_DIR / file_name).open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return [_coerce_price_row(row) for row in reader]


def _coerce_price_row(row: dict[str, str]) -> dict[str, Any]:
    return {
        "date": row["date"],
        "symbol": row["symbol"],
        "open": float(row["open"]),
        "high": float(row["high"]),
        "low": float(row["low"]),
        "close": float(row["close"]),
        "volume": int(row["volume"]),
    }


def _next_id(prefix: str, records: dict[str, Any]) -> str:
    numeric_ids = []

    for record_id in records:
        try:
            numeric_ids.append(int(record_id.split("_", maxsplit=1)[1]))
        except (IndexError, ValueError):
            continue

    return f"{prefix}_{max(numeric_ids, default=0) + 1:03d}"
