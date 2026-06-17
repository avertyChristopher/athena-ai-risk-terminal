from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.repositories.demo_data_store import DemoDataStore


PORTFOLIO_TABLE = "portfolio_builder_portfolios"
POSITION_TABLE = "portfolio_builder_positions"


class PersistentPortfolioStore:
    @classmethod
    def ensure_initialized(cls, db: Session) -> None:
        cls._create_schema(db)
        portfolio_count = db.execute(
            text(f"SELECT COUNT(*) FROM {PORTFOLIO_TABLE}"),
        ).scalar_one()

        if int(portfolio_count) == 0:
            cls._seed_demo_portfolio(db)

        db.commit()

    @classmethod
    def list_portfolios(cls, db: Session) -> list[dict[str, Any]]:
        cls.ensure_initialized(db)
        rows = db.execute(
            text(
                f"""
                SELECT id, name, base_currency, benchmark, cash
                FROM {PORTFOLIO_TABLE}
                ORDER BY id
                """,
            ),
        ).mappings()
        return [cls._portfolio_from_row(row) for row in rows]

    @classmethod
    def get_portfolio(cls, db: Session, portfolio_id: str) -> dict[str, Any] | None:
        cls.ensure_initialized(db)
        row = db.execute(
            text(
                f"""
                SELECT id, name, base_currency, benchmark, cash
                FROM {PORTFOLIO_TABLE}
                WHERE id = :portfolio_id
                """,
            ),
            {"portfolio_id": portfolio_id},
        ).mappings().first()
        return cls._portfolio_from_row(row) if row is not None else None

    @classmethod
    def create_portfolio(
        cls,
        db: Session,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        cls.ensure_initialized(db)
        portfolio_id = cls._next_id(db, PORTFOLIO_TABLE, "pf")
        portfolio = {"id": portfolio_id, **payload}
        db.execute(
            text(
                f"""
                INSERT INTO {PORTFOLIO_TABLE}
                    (id, name, base_currency, benchmark, cash)
                VALUES
                    (:id, :name, :base_currency, :benchmark, :cash)
                """,
            ),
            cls._portfolio_params(portfolio),
        )
        db.commit()
        return cls.get_portfolio(db, portfolio_id) or portfolio

    @classmethod
    def update_portfolio(
        cls,
        db: Session,
        portfolio_id: str,
        payload: dict[str, Any],
    ) -> dict[str, Any] | None:
        cls.ensure_initialized(db)
        existing = cls.get_portfolio(db, portfolio_id)
        if existing is None:
            return None

        updated = {**existing, **{key: value for key, value in payload.items() if value is not None}}
        db.execute(
            text(
                f"""
                UPDATE {PORTFOLIO_TABLE}
                SET name = :name,
                    base_currency = :base_currency,
                    benchmark = :benchmark,
                    cash = :cash
                WHERE id = :id
                """,
            ),
            cls._portfolio_params(updated),
        )
        db.commit()
        return cls.get_portfolio(db, portfolio_id)

    @classmethod
    def delete_portfolio(cls, db: Session, portfolio_id: str) -> bool:
        cls.ensure_initialized(db)
        result = db.execute(
            text(f"DELETE FROM {PORTFOLIO_TABLE} WHERE id = :portfolio_id"),
            {"portfolio_id": portfolio_id},
        )
        db.commit()
        return result.rowcount > 0

    @classmethod
    def list_positions(cls, db: Session, portfolio_id: str) -> list[dict[str, Any]]:
        cls.ensure_initialized(db)
        rows = db.execute(
            text(
                f"""
                SELECT id, portfolio_id, symbol, asset_name, name, asset_type,
                       quantity, average_price, current_price, currency, sector,
                       country, exchange, industry, region
                FROM {POSITION_TABLE}
                WHERE portfolio_id = :portfolio_id
                ORDER BY id
                """,
            ),
            {"portfolio_id": portfolio_id},
        ).mappings()
        return [cls._position_from_row(row) for row in rows]

    @classmethod
    def get_position(
        cls,
        db: Session,
        portfolio_id: str,
        position_id: str,
    ) -> dict[str, Any] | None:
        cls.ensure_initialized(db)
        row = db.execute(
            text(
                f"""
                SELECT id, portfolio_id, symbol, asset_name, name, asset_type,
                       quantity, average_price, current_price, currency, sector,
                       country, exchange, industry, region
                FROM {POSITION_TABLE}
                WHERE portfolio_id = :portfolio_id
                  AND id = :position_id
                """,
            ),
            {"portfolio_id": portfolio_id, "position_id": position_id},
        ).mappings().first()
        return cls._position_from_row(row) if row is not None else None

    @classmethod
    def create_position(
        cls,
        db: Session,
        portfolio_id: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        cls.ensure_initialized(db)
        position_id = cls._next_id(db, POSITION_TABLE, "pos")
        position = {"id": position_id, "portfolio_id": portfolio_id, **payload}
        db.execute(
            text(
                f"""
                INSERT INTO {POSITION_TABLE}
                    (id, portfolio_id, symbol, asset_name, name, asset_type,
                     quantity, average_price, current_price, currency, sector,
                     country, exchange, industry, region)
                VALUES
                    (:id, :portfolio_id, :symbol, :asset_name, :name, :asset_type,
                     :quantity, :average_price, :current_price, :currency, :sector,
                     :country, :exchange, :industry, :region)
                """,
            ),
            cls._position_params(position),
        )
        db.commit()
        return cls.get_position(db, portfolio_id, position_id) or position

    @classmethod
    def update_position(
        cls,
        db: Session,
        portfolio_id: str,
        position_id: str,
        payload: dict[str, Any],
    ) -> dict[str, Any] | None:
        cls.ensure_initialized(db)
        existing = cls.get_position(db, portfolio_id, position_id)
        if existing is None:
            return None

        updated = {**existing, **{key: value for key, value in payload.items() if value is not None}}
        db.execute(
            text(
                f"""
                UPDATE {POSITION_TABLE}
                SET symbol = :symbol,
                    asset_name = :asset_name,
                    name = :name,
                    asset_type = :asset_type,
                    quantity = :quantity,
                    average_price = :average_price,
                    current_price = :current_price,
                    currency = :currency,
                    sector = :sector,
                    country = :country,
                    exchange = :exchange,
                    industry = :industry,
                    region = :region
                WHERE portfolio_id = :portfolio_id
                  AND id = :id
                """,
            ),
            cls._position_params(updated),
        )
        db.commit()
        return cls.get_position(db, portfolio_id, position_id)

    @classmethod
    def delete_position(cls, db: Session, portfolio_id: str, position_id: str) -> bool:
        cls.ensure_initialized(db)
        result = db.execute(
            text(
                f"""
                DELETE FROM {POSITION_TABLE}
                WHERE portfolio_id = :portfolio_id
                  AND id = :position_id
                """,
            ),
            {"portfolio_id": portfolio_id, "position_id": position_id},
        )
        db.commit()
        return result.rowcount > 0

    @classmethod
    def _create_schema(cls, db: Session) -> None:
        db.execute(
            text(
                f"""
                CREATE TABLE IF NOT EXISTS {PORTFOLIO_TABLE} (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    base_currency TEXT NOT NULL DEFAULT 'USD',
                    benchmark TEXT NOT NULL DEFAULT 'SPY',
                    cash REAL NOT NULL DEFAULT 0
                )
                """,
            ),
        )
        db.execute(
            text(
                f"""
                CREATE TABLE IF NOT EXISTS {POSITION_TABLE} (
                    id TEXT PRIMARY KEY,
                    portfolio_id TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    asset_name TEXT NOT NULL,
                    name TEXT,
                    asset_type TEXT NOT NULL,
                    quantity REAL NOT NULL,
                    average_price REAL NOT NULL,
                    current_price REAL NOT NULL,
                    currency TEXT NOT NULL,
                    sector TEXT NOT NULL,
                    country TEXT NOT NULL,
                    exchange TEXT,
                    industry TEXT,
                    region TEXT,
                    FOREIGN KEY(portfolio_id) REFERENCES {PORTFOLIO_TABLE}(id)
                        ON DELETE CASCADE
                )
                """,
            ),
        )
        db.execute(
            text(
                f"""
                CREATE INDEX IF NOT EXISTS idx_{POSITION_TABLE}_portfolio_id
                ON {POSITION_TABLE} (portfolio_id)
                """,
            ),
        )

    @classmethod
    def _seed_demo_portfolio(cls, db: Session) -> None:
        portfolio = DemoDataStore.get_portfolio("pf_001")
        if portfolio is not None:
            db.execute(
                text(
                    f"""
                    INSERT INTO {PORTFOLIO_TABLE}
                        (id, name, base_currency, benchmark, cash)
                    VALUES
                        (:id, :name, :base_currency, :benchmark, :cash)
                    """,
                ),
                cls._portfolio_params(portfolio),
            )

        for position in DemoDataStore.list_positions("pf_001"):
            db.execute(
                text(
                    f"""
                    INSERT INTO {POSITION_TABLE}
                        (id, portfolio_id, symbol, asset_name, name, asset_type,
                         quantity, average_price, current_price, currency, sector,
                         country, exchange, industry, region)
                    VALUES
                        (:id, :portfolio_id, :symbol, :asset_name, :name, :asset_type,
                         :quantity, :average_price, :current_price, :currency, :sector,
                         :country, :exchange, :industry, :region)
                    """,
                ),
                cls._position_params(position),
            )

    @staticmethod
    def _portfolio_from_row(row: Any) -> dict[str, Any]:
        return {
            "id": str(row["id"]),
            "name": str(row["name"]),
            "base_currency": str(row["base_currency"]),
            "benchmark": str(row["benchmark"]),
            "cash": float(row["cash"]),
        }

    @staticmethod
    def _position_from_row(row: Any) -> dict[str, Any]:
        return {
            "id": str(row["id"]),
            "portfolio_id": str(row["portfolio_id"]),
            "symbol": str(row["symbol"]),
            "asset_name": str(row["asset_name"]),
            "name": row["name"],
            "asset_type": str(row["asset_type"]),
            "quantity": float(row["quantity"]),
            "average_price": float(row["average_price"]),
            "current_price": float(row["current_price"]),
            "currency": str(row["currency"]),
            "sector": str(row["sector"]),
            "country": str(row["country"]),
            "exchange": row["exchange"],
            "industry": row["industry"],
            "region": row["region"],
        }

    @staticmethod
    def _portfolio_params(portfolio: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": str(portfolio["id"]),
            "name": str(portfolio["name"]),
            "base_currency": str(portfolio.get("base_currency", "USD")),
            "benchmark": str(portfolio.get("benchmark", "SPY")),
            "cash": float(portfolio.get("cash", 0.0)),
        }

    @staticmethod
    def _position_params(position: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": str(position["id"]),
            "portfolio_id": str(position["portfolio_id"]),
            "symbol": str(position["symbol"]).upper(),
            "asset_name": str(position["asset_name"]),
            "name": position.get("name"),
            "asset_type": str(position["asset_type"]),
            "quantity": float(position["quantity"]),
            "average_price": float(position["average_price"]),
            "current_price": float(position["current_price"]),
            "currency": str(position["currency"]).upper(),
            "sector": str(position["sector"]),
            "country": str(position["country"]),
            "exchange": position.get("exchange"),
            "industry": position.get("industry"),
            "region": position.get("region"),
        }

    @staticmethod
    def _next_id(db: Session, table_name: str, prefix: str) -> str:
        rows = db.execute(text(f"SELECT id FROM {table_name}")).scalars().all()
        numeric_ids = []

        for record_id in rows:
            try:
                numeric_ids.append(int(str(record_id).split("_", maxsplit=1)[1]))
            except (IndexError, ValueError):
                continue

        return f"{prefix}_{max(numeric_ids, default=0) + 1:03d}"
