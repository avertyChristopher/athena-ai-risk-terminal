from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


ASSET_TABLE = "market_data_custom_assets"
PRICE_TABLE = "market_data_custom_prices"


class PersistentMarketDataStore:
    @classmethod
    def ensure_initialized(cls, db: Session) -> None:
        cls._create_schema(db)
        db.commit()

    @classmethod
    def list_assets(cls, db: Session) -> list[dict[str, Any]]:
        cls.ensure_initialized(db)
        rows = db.execute(
            text(
                f"""
                SELECT symbol, name, asset_type, currency, sector, country,
                       exchange, industry
                FROM {ASSET_TABLE}
                ORDER BY symbol
                """,
            ),
        ).mappings()
        return [cls._asset_from_row(row) for row in rows]

    @classmethod
    def get_prices(cls, db: Session, symbol: str) -> list[dict[str, Any]]:
        cls.ensure_initialized(db)
        rows = db.execute(
            text(
                f"""
                SELECT date, symbol, open, high, low, close, volume
                FROM {PRICE_TABLE}
                WHERE symbol = :symbol
                ORDER BY date
                """,
            ),
            {"symbol": symbol.upper()},
        ).mappings()
        return [cls._price_from_row(row) for row in rows]

    @classmethod
    def import_prices(
        cls,
        db: Session,
        rows: list[dict[str, Any]],
    ) -> tuple[int, list[str]]:
        cls.ensure_initialized(db)
        imported_symbols = sorted(
            {str(row["symbol"]).strip().upper() for row in rows if str(row.get("symbol", "")).strip()},
        )

        for symbol in imported_symbols:
            first_row = next(row for row in rows if str(row["symbol"]).strip().upper() == symbol)
            db.execute(
                text(
                    f"""
                    INSERT INTO {ASSET_TABLE}
                        (symbol, name, asset_type, currency, sector, country, exchange, industry)
                    VALUES
                        (:symbol, :name, :asset_type, :currency, :sector, :country, :exchange, :industry)
                    ON CONFLICT(symbol) DO UPDATE SET
                        name = excluded.name,
                        asset_type = excluded.asset_type,
                        currency = excluded.currency,
                        sector = excluded.sector,
                        country = excluded.country,
                        exchange = excluded.exchange,
                        industry = excluded.industry
                    """,
                ),
                cls._asset_params(symbol, first_row),
            )

        for row in rows:
            db.execute(
                text(
                    f"""
                    INSERT INTO {PRICE_TABLE}
                        (symbol, date, open, high, low, close, volume)
                    VALUES
                        (:symbol, :date, :open, :high, :low, :close, :volume)
                    ON CONFLICT(symbol, date) DO UPDATE SET
                        open = excluded.open,
                        high = excluded.high,
                        low = excluded.low,
                        close = excluded.close,
                        volume = excluded.volume
                    """,
                ),
                cls._price_params(row),
            )

        db.commit()
        return len(rows), imported_symbols

    @classmethod
    def _create_schema(cls, db: Session) -> None:
        db.execute(
            text(
                f"""
                CREATE TABLE IF NOT EXISTS {ASSET_TABLE} (
                    symbol TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    asset_type TEXT NOT NULL DEFAULT 'equity',
                    currency TEXT NOT NULL DEFAULT 'USD',
                    sector TEXT NOT NULL DEFAULT 'Imported',
                    country TEXT NOT NULL DEFAULT 'United States',
                    exchange TEXT,
                    industry TEXT
                )
                """,
            ),
        )
        db.execute(
            text(
                f"""
                CREATE TABLE IF NOT EXISTS {PRICE_TABLE} (
                    symbol TEXT NOT NULL,
                    date TEXT NOT NULL,
                    open REAL NOT NULL,
                    high REAL NOT NULL,
                    low REAL NOT NULL,
                    close REAL NOT NULL,
                    volume INTEGER NOT NULL,
                    PRIMARY KEY(symbol, date)
                )
                """,
            ),
        )
        db.execute(
            text(
                f"""
                CREATE INDEX IF NOT EXISTS idx_{PRICE_TABLE}_symbol_date
                ON {PRICE_TABLE} (symbol, date)
                """,
            ),
        )

    @staticmethod
    def _asset_from_row(row: Any) -> dict[str, Any]:
        return {
            "symbol": str(row["symbol"]).upper(),
            "name": str(row["name"]),
            "asset_type": str(row["asset_type"]),
            "currency": str(row["currency"]).upper(),
            "sector": str(row["sector"]),
            "country": str(row["country"]),
            "exchange": row["exchange"],
            "industry": row["industry"],
            "data_source": "imported",
        }

    @staticmethod
    def _price_from_row(row: Any) -> dict[str, Any]:
        return {
            "date": str(row["date"]),
            "symbol": str(row["symbol"]).upper(),
            "open": float(row["open"]),
            "high": float(row["high"]),
            "low": float(row["low"]),
            "close": float(row["close"]),
            "volume": int(row["volume"]),
            "data_source": "imported",
        }

    @staticmethod
    def _asset_params(symbol: str, row: dict[str, Any]) -> dict[str, Any]:
        return {
            "symbol": symbol,
            "name": str(row.get("name") or symbol),
            "asset_type": str(row.get("asset_type") or "equity").lower(),
            "currency": str(row.get("currency") or "USD").upper(),
            "sector": str(row.get("sector") or "Imported"),
            "country": str(row.get("country") or "United States"),
            "exchange": row.get("exchange"),
            "industry": row.get("industry"),
        }

    @staticmethod
    def _price_params(row: dict[str, Any]) -> dict[str, Any]:
        return {
            "symbol": str(row["symbol"]).strip().upper(),
            "date": str(row["date"]),
            "open": float(row["open"]),
            "high": float(row["high"]),
            "low": float(row["low"]),
            "close": float(row["close"]),
            "volume": int(row["volume"]),
        }
