from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.modules.limit_center.domain.limit_rules import default_limit_rule_payloads
from app.modules.limit_center.schemas import (
    BreachReviewEvent,
    BreachStatus,
    LimitBreach,
    LimitRule,
    LimitRuleCreate,
    LimitRuleUpdate,
)
from app.persistence.repositories import LimitBreachPersistenceRepository


_RULES: dict[str, LimitRule] = {}
_BREACHES: dict[str, LimitBreach] = {}


class LimitCenterRepository:
    def __init__(self, db: Session | None = None) -> None:
        self.db = db
        self.persistence = LimitBreachPersistenceRepository(db)
        self._ensure_defaults()

    def list_rules(self) -> list[LimitRule]:
        return [rule.model_copy(deep=True) for rule in _RULES.values()]

    def get_rule(self, rule_id: str) -> LimitRule | None:
        rule = _RULES.get(rule_id)
        return rule.model_copy(deep=True) if rule else None

    def create_rule(self, payload: LimitRuleCreate) -> LimitRule:
        now = datetime.now(UTC)
        rule_id = payload.rule_id or self._new_rule_id(payload.name)
        if rule_id in _RULES:
            raise ValueError(f"Limit rule '{rule_id}' already exists.")
        rule = LimitRule(
            **payload.model_dump(exclude={"rule_id"}),
            rule_id=rule_id,
            created_at=now,
            updated_at=now,
        )
        _RULES[rule.rule_id] = rule
        return rule.model_copy(deep=True)

    def update_rule(self, rule_id: str, payload: LimitRuleUpdate) -> LimitRule | None:
        existing = _RULES.get(rule_id)
        if existing is None:
            return None
        updated_data = existing.model_dump()
        updated_data.update(payload.model_dump(exclude_none=True))
        updated_data["updated_at"] = datetime.now(UTC)
        rule = LimitRule(**updated_data)
        _RULES[rule_id] = rule
        return rule.model_copy(deep=True)

    def delete_rule(self, rule_id: str) -> bool:
        return _RULES.pop(rule_id, None) is not None

    def save_breaches(self, breaches: list[LimitBreach]) -> list[LimitBreach]:
        for breach in breaches:
            _BREACHES[breach.breach_id] = breach
        self.persistence.save_many(breaches)
        return [breach.model_copy(deep=True) for breach in breaches]

    def list_breaches(self) -> list[LimitBreach]:
        persisted = self.persistence.list()
        if persisted:
            return persisted
        return [breach.model_copy(deep=True) for breach in _BREACHES.values()]

    def get_breach(self, breach_id: str) -> LimitBreach | None:
        persisted = self.persistence.get(breach_id)
        if persisted:
            return persisted
        breach = _BREACHES.get(breach_id)
        return breach.model_copy(deep=True) if breach else None

    def update_breach_status(
        self,
        breach_id: str,
        status: BreachStatus,
        event: BreachReviewEvent,
    ) -> LimitBreach | None:
        breach = _BREACHES.get(breach_id)
        if breach is None:
            return None
        updated = breach.model_copy(deep=True)
        updated.status = status
        updated.updated_at = event.timestamp
        updated.reviewed_by = event.reviewer
        updated.review_note = event.note
        updated.review_history.append(event)
        _BREACHES[breach_id] = updated
        self.persistence.save(updated)
        return updated.model_copy(deep=True)

    def reset_demo_state(self) -> None:
        _RULES.clear()
        _BREACHES.clear()
        self.persistence.clear()
        self._ensure_defaults()

    def _ensure_defaults(self) -> None:
        if _RULES:
            return
        for payload in default_limit_rule_payloads():
            rule = LimitRule(**payload)
            _RULES[rule.rule_id] = rule

    def _new_rule_id(self, name: str) -> str:
        base = "".join(ch.lower() if ch.isalnum() else "_" for ch in name).strip("_")
        base = "_".join(part for part in base.split("_") if part) or "custom_rule"
        candidate = base
        index = 2
        while candidate in _RULES:
            candidate = f"{base}_{index}"
            index += 1
        return candidate
