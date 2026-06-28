from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session

from app.modules.ai_anomaly_center.schemas import AnomalyRecord
from app.modules.limit_center.repository import LimitCenterRepository
from app.modules.market_data.repository import MarketDataRepository
from app.modules.pnl_attribution.repository import PnlAttributionRepository
from app.modules.portfolio_builder.repository import PortfolioRepository, PositionRepository
from app.modules.reconciliation.repository import ReconciliationRepository
from app.modules.stress_testing.repository import StressTestingRepository
from app.persistence.repositories import AnomalyRecordPersistenceRepository, TradeBlotterPersistenceRepository


class AIAnomalyCenterRepository:
    _records: dict[str, AnomalyRecord] = {}

    def __init__(self, db: Session | None = None) -> None:
        self.db = db
        self.persistence = AnomalyRecordPersistenceRepository(db)
        self.market_data = MarketDataRepository(db)
        self.portfolios = PortfolioRepository(db) if db is not None else None
        self.positions = PositionRepository(db) if db is not None else None
        self.trade_blotter = TradeBlotterPersistenceRepository(db)
        self.pnl = PnlAttributionRepository(db)
        self.reconciliation = ReconciliationRepository(db)
        self.limits = LimitCenterRepository(db)
        self.stress = StressTestingRepository(db) if db is not None else None

    def save(self, anomaly: AnomalyRecord) -> AnomalyRecord:
        self._records[anomaly.anomaly_id] = anomaly
        self.persistence.save(anomaly.model_dump(mode="json"))
        return anomaly

    def save_many(self, anomalies: list[AnomalyRecord]) -> list[AnomalyRecord]:
        for anomaly in anomalies:
            self.save(anomaly)
        return anomalies

    def list_anomalies(
        self,
        *,
        portfolio_id: str | None = None,
        severity: str | None = None,
        module_name: str | None = None,
        status: str | None = None,
    ) -> list[AnomalyRecord]:
        persisted = [
            AnomalyRecord.model_validate(row)
            for row in self.persistence.list(
                portfolio_id=portfolio_id,
                severity=severity,
                module_name=module_name,
                status=status,
            )
        ]
        if persisted:
            return persisted
        rows = list(self._records.values())
        if portfolio_id:
            rows = [row for row in rows if row.portfolio_id == portfolio_id]
        if severity:
            rows = [row for row in rows if row.severity == severity]
        if module_name:
            rows = [row for row in rows if row.module_name == module_name]
        if status:
            rows = [row for row in rows if row.status == status]
        return sorted(rows, key=lambda row: row.detected_at, reverse=True)

    def get(self, anomaly_id: str) -> AnomalyRecord | None:
        row = self.persistence.get(anomaly_id)
        if row:
            return AnomalyRecord.model_validate(row)
        return self._records.get(anomaly_id)

    def delete(self, anomaly_id: str) -> bool:
        deleted_memory = self._records.pop(anomaly_id, None) is not None
        return self.persistence.delete(anomaly_id) or deleted_memory

    def recent(self, limit: int = 50) -> list[AnomalyRecord]:
        persisted = [AnomalyRecord.model_validate(row) for row in self.persistence.recent(limit)]
        if persisted:
            return persisted
        return sorted(self._records.values(), key=lambda row: row.detected_at, reverse=True)[:limit]

    def clear(self) -> None:
        self._records.clear()
        self.persistence.clear()

    def load_scan_context(self, portfolio_id: str | None, lookback_days: int) -> tuple[dict[str, Any], list[str]]:
        warnings: list[str] = []
        since = datetime.now(UTC) - timedelta(days=lookback_days)
        portfolio = self.get_portfolio(portfolio_id) if portfolio_id else None
        positions = self.list_positions(portfolio_id) if portfolio_id else []
        symbols = [str(position.get("symbol", "")).upper() for position in positions if position.get("symbol")]
        assets = self.market_data.list_assets()
        prices = {symbol: self.market_data.get_prices(symbol) for symbol in symbols}
        if portfolio_id and portfolio is None:
            warnings.append(f"Portfolio '{portfolio_id}' was not found; scan continues with available persisted records.")
        return {
            "portfolio": portfolio,
            "positions": positions,
            "assets": assets,
            "prices": prices,
            "trade_blotter": self._recent_trade_rows(portfolio_id, since),
            "pnl_history": self._recent_model_rows(self.pnl.list_history(), "generated_at", since),
            "reconciliation_runs": self._recent_model_rows(self.reconciliation.list_runs(), "generated_at", since),
            "reconciliation_breaks": self._recent_model_rows(self.reconciliation.list_breaks(), "created_at", since),
            "limit_breaches": self._recent_model_rows(self.limits.list_breaches(), "created_at", since),
            "stress_runs": self._recent_stress_rows(since),
        }, warnings

    def get_portfolio(self, portfolio_id: str | None) -> dict[str, Any] | None:
        if not portfolio_id or self.portfolios is None:
            return None
        return self.portfolios.get_portfolio(portfolio_id)

    def list_positions(self, portfolio_id: str | None) -> list[dict[str, Any]]:
        if not portfolio_id or self.positions is None:
            return []
        return self.positions.list_positions(portfolio_id)

    def _recent_trade_rows(self, portfolio_id: str | None, since: datetime) -> list[dict[str, Any]]:
        rows = self.trade_blotter.list()
        selected: list[dict[str, Any]] = []
        for row in rows:
            if portfolio_id and row.get("portfolio_id") != portfolio_id:
                continue
            created = _parse_datetime(row.get("created_at") or row.get("trade_date"))
            if created is None or created >= since:
                selected.append(row)
        return selected

    def _recent_model_rows(self, rows: list[Any], field: str, since: datetime) -> list[dict[str, Any]]:
        selected: list[dict[str, Any]] = []
        for row in rows:
            payload = row.model_dump(mode="json") if hasattr(row, "model_dump") else dict(row)
            timestamp = _parse_datetime(payload.get(field))
            if timestamp is None or timestamp >= since:
                selected.append(payload)
        return selected

    def _recent_stress_rows(self, since: datetime) -> list[dict[str, Any]]:
        if self.stress is None:
            return []
        rows = self.stress.list_runs()
        selected = []
        for row in rows:
            timestamp = _parse_datetime(row.get("generated_at"))
            if timestamp is None or timestamp >= since:
                detail = self.stress.get_run(str(row["run_id"]))
                selected.append(detail.model_dump(mode="json") if detail else row)
        return selected


def _parse_datetime(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=UTC)
    try:
        text = str(value).replace("Z", "+00:00")
        parsed = datetime.fromisoformat(text)
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)
    except ValueError:
        return None
