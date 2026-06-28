from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from app.modules.demo_workflow.schemas import DemoPersistenceItem


ACTIVE_MODULE_COUNT = 16
DEMO_LIMITATIONS = [
    "Demo workflow uses local SQLite persistence and deterministic fallback analytics where needed.",
    "No real broker execution, custodian integration or live market data vendor is active by default.",
    "Athena Intelligence may use deterministic fallback commentary when no AI provider is configured.",
    "Outputs are educational and analytical and are not investment advice.",
]


def persistence_map() -> list[DemoPersistenceItem]:
    return [
        DemoPersistenceItem(
            object_name="Trade blotter entries",
            module="Trade Blotter",
            status="persistent_history",
            storage="SQLite via SQLAlchemy",
            notes="Simulated and manual trades are persisted with review history.",
        ),
        DemoPersistenceItem(
            object_name="P&L analyses",
            module="P&L Attribution",
            status="persistent_history",
            storage="SQLite via SQLAlchemy",
            notes="Generated P&L snapshots are stored and exportable.",
        ),
        DemoPersistenceItem(
            object_name="Reconciliation runs and breaks",
            module="Reconciliation Center",
            status="persistent_history",
            storage="SQLite via SQLAlchemy",
            notes="Runs, breaks and review actions are persisted.",
        ),
        DemoPersistenceItem(
            object_name="Limit breaches",
            module="Limit Center",
            status="persistent_history",
            storage="SQLite via SQLAlchemy with memory fallback",
            notes="Rule evaluations create breach records and review workflow state.",
        ),
        DemoPersistenceItem(
            object_name="Stress runs",
            module="Stress Testing",
            status="persistent_history",
            storage="SQLite via SQLAlchemy",
            notes="Stress scenario runs are available to downstream monitoring.",
        ),
        DemoPersistenceItem(
            object_name="AI anomaly records",
            module="AI Anomaly Center",
            status="persistent_history",
            storage="SQLite via SQLAlchemy with memory fallback",
            notes="Anomaly scan records and review state are persisted.",
        ),
        DemoPersistenceItem(
            object_name="Reports",
            module="Reports Center",
            status="sqlite_demo",
            storage="Repository snapshot store",
            notes="Reports are snapshot-based demo artifacts with JSON/Markdown/CSV export.",
        ),
        DemoPersistenceItem(
            object_name="Athena AI commentary snapshots",
            module="Athena Intelligence",
            status="sqlite_demo",
            storage="Structured payload fallback and local snapshots where called",
            notes="Commentary is generated from structured payloads and never from hidden frontend secrets.",
        ),
    ]


def dump_payload(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if isinstance(value, list):
        return [dump_payload(item) for item in value]
    if isinstance(value, dict):
        return {key: dump_payload(item) for key, item in value.items()}
    return value


def records_count(value: Any, *keys: str) -> int:
    payload = dump_payload(value)
    if not isinstance(payload, dict):
        return 0
    for key in keys:
        item = payload.get(key)
        if isinstance(item, list):
            return len(item)
        if isinstance(item, int):
            return item
    return 1 if payload else 0
