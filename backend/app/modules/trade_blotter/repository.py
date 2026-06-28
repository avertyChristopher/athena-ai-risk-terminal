from __future__ import annotations

from sqlalchemy.orm import Session

from app.modules.trade_blotter.schemas import TradeBlotterEntry
from app.persistence.repositories import TradeBlotterPersistenceRepository


class TradeBlotterRepository:
    _entries: dict[str, TradeBlotterEntry] = {}

    def __init__(self, db: Session | None = None) -> None:
        self.db = db
        self.persistence = TradeBlotterPersistenceRepository(db)

    def save(self, entry: TradeBlotterEntry) -> TradeBlotterEntry:
        self._entries[entry.trade_id] = entry
        self.persistence.save(entry.model_dump(mode="json"))
        return entry

    def list(self) -> list[TradeBlotterEntry]:
        persisted = [
            TradeBlotterEntry.model_validate(row)
            for row in self.persistence.list()
        ]
        if persisted:
            return persisted
        return sorted(self._entries.values(), key=lambda item: item.created_at, reverse=True)

    def get(self, trade_id: str) -> TradeBlotterEntry | None:
        row = self.persistence.get(trade_id)
        if row:
            return TradeBlotterEntry.model_validate(row)
        return self._entries.get(trade_id)

    def delete(self, trade_id: str) -> bool:
        deleted_from_memory = self._entries.pop(trade_id, None) is not None
        return self.persistence.delete(trade_id) or deleted_from_memory

    def clear(self) -> None:
        self._entries.clear()
        self.persistence.clear()
