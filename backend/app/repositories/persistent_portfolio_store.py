import json
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.repositories.demo_data_store import DemoDataStore


PORTFOLIO_TABLE = "portfolio_builder_portfolios"
POSITION_TABLE = "portfolio_builder_positions"

PORTFOLIO_OPTIONAL_COLUMNS: dict[str, str] = {
    "strategy_type": "TEXT",
    "investment_objective": "TEXT",
    "risk_tolerance": "TEXT",
    "time_horizon": "TEXT",
    "target_allocation": "TEXT",
    "strategy_description": "TEXT",
    "ips_summary": "TEXT",
    "data_source": "TEXT",
    "risk_profile": "TEXT",
    "demo_profile": "INTEGER NOT NULL DEFAULT 0",
    "data_source_badges": "TEXT",
    "market_data_coverage": "TEXT",
    "fixed_income_assumptions": "TEXT",
    "transaction_history": "TEXT",
    "commentary_focus": "TEXT",
}

POSITION_OPTIONAL_COLUMNS: dict[str, str] = {
    "asset_class": "TEXT",
    "risk_bucket": "TEXT",
    "liquidity_profile": "TEXT",
    "beta_assumption": "REAL",
    "volatility_assumption": "REAL",
    "duration_assumption": "REAL",
    "modified_duration_assumption": "REAL",
    "dv01_assumption": "REAL",
    "dividend_yield": "REAL",
    "data_source": "TEXT",
}


class PersistentPortfolioStore:
    @classmethod
    def ensure_initialized(cls, db: Session) -> None:
        cls._create_schema(db)
        cls._seed_demo_portfolios(db)

        db.commit()

    @classmethod
    def list_portfolios(cls, db: Session) -> list[dict[str, Any]]:
        cls.ensure_initialized(db)
        rows = db.execute(
            text(
                f"""
                SELECT *
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
                SELECT *
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
                    (id, name, base_currency, benchmark, cash,
                     strategy_type, investment_objective, risk_tolerance,
                     time_horizon, target_allocation, strategy_description,
                     ips_summary, data_source, risk_profile, demo_profile,
                     data_source_badges, market_data_coverage,
                     fixed_income_assumptions, transaction_history,
                     commentary_focus)
                VALUES
                    (:id, :name, :base_currency, :benchmark, :cash,
                     :strategy_type, :investment_objective, :risk_tolerance,
                     :time_horizon, :target_allocation, :strategy_description,
                     :ips_summary, :data_source, :risk_profile, :demo_profile,
                     :data_source_badges, :market_data_coverage,
                     :fixed_income_assumptions, :transaction_history,
                     :commentary_focus)
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
                    cash = :cash,
                    strategy_type = :strategy_type,
                    investment_objective = :investment_objective,
                    risk_tolerance = :risk_tolerance,
                    time_horizon = :time_horizon,
                    target_allocation = :target_allocation,
                    strategy_description = :strategy_description,
                    ips_summary = :ips_summary,
                    data_source = :data_source,
                    risk_profile = :risk_profile,
                    demo_profile = :demo_profile,
                    data_source_badges = :data_source_badges,
                    market_data_coverage = :market_data_coverage,
                    fixed_income_assumptions = :fixed_income_assumptions,
                    transaction_history = :transaction_history,
                    commentary_focus = :commentary_focus
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
                SELECT *
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
                SELECT *
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
                     country, exchange, industry, region, asset_class, risk_bucket,
                     liquidity_profile, beta_assumption, volatility_assumption,
                     duration_assumption, modified_duration_assumption,
                     dv01_assumption, dividend_yield, data_source)
                VALUES
                    (:id, :portfolio_id, :symbol, :asset_name, :name, :asset_type,
                     :quantity, :average_price, :current_price, :currency, :sector,
                     :country, :exchange, :industry, :region, :asset_class, :risk_bucket,
                     :liquidity_profile, :beta_assumption, :volatility_assumption,
                     :duration_assumption, :modified_duration_assumption,
                     :dv01_assumption, :dividend_yield, :data_source)
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
                    region = :region,
                    asset_class = :asset_class,
                    risk_bucket = :risk_bucket,
                    liquidity_profile = :liquidity_profile,
                    beta_assumption = :beta_assumption,
                    volatility_assumption = :volatility_assumption,
                    duration_assumption = :duration_assumption,
                    modified_duration_assumption = :modified_duration_assumption,
                    dv01_assumption = :dv01_assumption,
                    dividend_yield = :dividend_yield,
                    data_source = :data_source
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
                    cash REAL NOT NULL DEFAULT 0,
                    strategy_type TEXT,
                    investment_objective TEXT,
                    risk_tolerance TEXT,
                    time_horizon TEXT,
                    target_allocation TEXT,
                    strategy_description TEXT,
                    ips_summary TEXT,
                    data_source TEXT,
                    risk_profile TEXT,
                    demo_profile INTEGER NOT NULL DEFAULT 0,
                    data_source_badges TEXT,
                    market_data_coverage TEXT,
                    fixed_income_assumptions TEXT,
                    transaction_history TEXT,
                    commentary_focus TEXT
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
                    asset_class TEXT,
                    risk_bucket TEXT,
                    liquidity_profile TEXT,
                    beta_assumption REAL,
                    volatility_assumption REAL,
                    duration_assumption REAL,
                    modified_duration_assumption REAL,
                    dv01_assumption REAL,
                    dividend_yield REAL,
                    data_source TEXT,
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
        cls._ensure_columns(db, PORTFOLIO_TABLE, PORTFOLIO_OPTIONAL_COLUMNS)
        cls._ensure_columns(db, POSITION_TABLE, POSITION_OPTIONAL_COLUMNS)

    @classmethod
    def _seed_demo_portfolios(cls, db: Session) -> None:
        for portfolio in DemoDataStore.list_portfolios():
            portfolio_id = str(portfolio["id"])
            existing = cls._raw_portfolio_row(db, portfolio_id)
            existing_name = str(existing["name"]) if existing is not None else ""
            position_count = cls._position_count(db, portfolio_id)
            should_refresh_positions = (
                existing is None
                or position_count == 0
                or (
                    portfolio_id == "pf_001"
                    and existing_name == "Athena Demo Portfolio"
                )
            )

            if existing is None:
                db.execute(
                    text(
                        f"""
                        INSERT INTO {PORTFOLIO_TABLE}
                            (id, name, base_currency, benchmark, cash,
                             strategy_type, investment_objective, risk_tolerance,
                             time_horizon, target_allocation, strategy_description,
                             ips_summary, data_source, risk_profile, demo_profile,
                             data_source_badges, market_data_coverage,
                             fixed_income_assumptions, transaction_history,
                             commentary_focus)
                        VALUES
                            (:id, :name, :base_currency, :benchmark, :cash,
                             :strategy_type, :investment_objective, :risk_tolerance,
                             :time_horizon, :target_allocation, :strategy_description,
                             :ips_summary, :data_source, :risk_profile, :demo_profile,
                             :data_source_badges, :market_data_coverage,
                             :fixed_income_assumptions, :transaction_history,
                             :commentary_focus)
                        """,
                    ),
                    cls._portfolio_params(portfolio),
                )
            elif portfolio_id == "pf_001" and existing_name == "Athena Demo Portfolio":
                db.execute(
                    text(
                        f"""
                        UPDATE {PORTFOLIO_TABLE}
                        SET name = :name,
                            base_currency = :base_currency,
                            benchmark = :benchmark,
                            cash = :cash,
                            strategy_type = :strategy_type,
                            investment_objective = :investment_objective,
                            risk_tolerance = :risk_tolerance,
                            time_horizon = :time_horizon,
                            target_allocation = :target_allocation,
                            strategy_description = :strategy_description,
                            ips_summary = :ips_summary,
                            data_source = :data_source,
                            risk_profile = :risk_profile,
                            demo_profile = :demo_profile,
                            data_source_badges = :data_source_badges,
                            market_data_coverage = :market_data_coverage,
                            fixed_income_assumptions = :fixed_income_assumptions,
                            transaction_history = :transaction_history,
                            commentary_focus = :commentary_focus
                        WHERE id = :id
                        """,
                    ),
                    cls._portfolio_params(portfolio),
                )

            if should_refresh_positions:
                db.execute(
                    text(f"DELETE FROM {POSITION_TABLE} WHERE portfolio_id = :portfolio_id"),
                    {"portfolio_id": portfolio_id},
                )

            if should_refresh_positions:
                for position in DemoDataStore.list_positions(portfolio_id):
                    db.execute(
                        text(
                            f"""
                            INSERT INTO {POSITION_TABLE}
                                (id, portfolio_id, symbol, asset_name, name, asset_type,
                                 quantity, average_price, current_price, currency, sector,
                                 country, exchange, industry, region, asset_class,
                                 risk_bucket, liquidity_profile, beta_assumption,
                                 volatility_assumption, duration_assumption,
                                 modified_duration_assumption, dv01_assumption,
                                 dividend_yield, data_source)
                            VALUES
                                (:id, :portfolio_id, :symbol, :asset_name, :name, :asset_type,
                                 :quantity, :average_price, :current_price, :currency, :sector,
                                 :country, :exchange, :industry, :region, :asset_class,
                                 :risk_bucket, :liquidity_profile, :beta_assumption,
                                 :volatility_assumption, :duration_assumption,
                                 :modified_duration_assumption, :dv01_assumption,
                                 :dividend_yield, :data_source)
                            """,
                        ),
                        cls._position_params(position),
                    )
    @classmethod
    def _ensure_columns(
        cls,
        db: Session,
        table_name: str,
        expected_columns: dict[str, str],
    ) -> None:
        existing_columns = {
            str(row["name"])
            for row in db.execute(text(f"PRAGMA table_info({table_name})")).mappings()
        }
        for column_name, column_type in expected_columns.items():
            if column_name not in existing_columns:
                db.execute(
                    text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"),
                )

    @classmethod
    def _raw_portfolio_row(cls, db: Session, portfolio_id: str) -> Any:
        return db.execute(
            text(f"SELECT * FROM {PORTFOLIO_TABLE} WHERE id = :portfolio_id"),
            {"portfolio_id": portfolio_id},
        ).mappings().first()

    @classmethod
    def _position_count(cls, db: Session, portfolio_id: str) -> int:
        return int(
            db.execute(
                text(f"SELECT COUNT(*) FROM {POSITION_TABLE} WHERE portfolio_id = :portfolio_id"),
                {"portfolio_id": portfolio_id},
            ).scalar_one()
        )

    @staticmethod
    def _portfolio_from_row(row: Any) -> dict[str, Any]:
        return {
            "id": str(row["id"]),
            "name": str(row["name"]),
            "base_currency": str(row["base_currency"]),
            "benchmark": str(row["benchmark"]),
            "cash": float(row["cash"]),
            "strategy_type": row["strategy_type"],
            "investment_objective": row["investment_objective"],
            "risk_tolerance": row["risk_tolerance"],
            "time_horizon": row["time_horizon"],
            "target_allocation": _decode_json_list(row["target_allocation"]),
            "strategy_description": row["strategy_description"],
            "ips_summary": row["ips_summary"],
            "data_source": row["data_source"],
            "risk_profile": row["risk_profile"],
            "demo_profile": bool(row["demo_profile"]),
            "data_source_badges": _decode_json_list(row["data_source_badges"]),
            "market_data_coverage": row["market_data_coverage"],
            "fixed_income_assumptions": row["fixed_income_assumptions"],
            "transaction_history": _decode_json_list(row["transaction_history"]),
            "commentary_focus": _decode_json_list(row["commentary_focus"]),
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
            "asset_class": row["asset_class"],
            "risk_bucket": row["risk_bucket"],
            "liquidity_profile": row["liquidity_profile"],
            "beta_assumption": _optional_float(row["beta_assumption"]),
            "volatility_assumption": _optional_float(row["volatility_assumption"]),
            "duration_assumption": _optional_float(row["duration_assumption"]),
            "modified_duration_assumption": _optional_float(row["modified_duration_assumption"]),
            "dv01_assumption": _optional_float(row["dv01_assumption"]),
            "dividend_yield": _optional_float(row["dividend_yield"]),
            "data_source": row["data_source"],
        }

    @staticmethod
    def _portfolio_params(portfolio: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": str(portfolio["id"]),
            "name": str(portfolio["name"]),
            "base_currency": str(portfolio.get("base_currency", "USD")),
            "benchmark": str(portfolio.get("benchmark", "SPY")),
            "cash": float(portfolio.get("cash", 0.0)),
            "strategy_type": portfolio.get("strategy_type"),
            "investment_objective": portfolio.get("investment_objective"),
            "risk_tolerance": portfolio.get("risk_tolerance"),
            "time_horizon": portfolio.get("time_horizon"),
            "target_allocation": _encode_json(portfolio.get("target_allocation")),
            "strategy_description": portfolio.get("strategy_description"),
            "ips_summary": portfolio.get("ips_summary"),
            "data_source": portfolio.get("data_source"),
            "risk_profile": portfolio.get("risk_profile"),
            "demo_profile": 1 if portfolio.get("demo_profile") else 0,
            "data_source_badges": _encode_json(portfolio.get("data_source_badges")),
            "market_data_coverage": portfolio.get("market_data_coverage"),
            "fixed_income_assumptions": portfolio.get("fixed_income_assumptions"),
            "transaction_history": _encode_json(portfolio.get("transaction_history")),
            "commentary_focus": _encode_json(portfolio.get("commentary_focus")),
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
            "asset_class": position.get("asset_class"),
            "risk_bucket": position.get("risk_bucket"),
            "liquidity_profile": position.get("liquidity_profile"),
            "beta_assumption": _optional_float(position.get("beta_assumption")),
            "volatility_assumption": _optional_float(position.get("volatility_assumption")),
            "duration_assumption": _optional_float(position.get("duration_assumption")),
            "modified_duration_assumption": _optional_float(position.get("modified_duration_assumption")),
            "dv01_assumption": _optional_float(position.get("dv01_assumption")),
            "dividend_yield": _optional_float(position.get("dividend_yield")),
            "data_source": position.get("data_source"),
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


def _encode_json(value: Any) -> str | None:
    if value is None:
        return None
    return json.dumps(value)


def _decode_json_list(value: Any) -> list[Any]:
    if value in (None, ""):
        return []
    try:
        decoded = json.loads(str(value))
    except json.JSONDecodeError:
        return []
    return decoded if isinstance(decoded, list) else []


def _optional_float(value: Any) -> float | None:
    if value is None:
        return None
    return float(value)
