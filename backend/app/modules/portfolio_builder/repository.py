from sqlalchemy.orm import Session

from app.repositories.persistent_portfolio_store import PersistentPortfolioStore

_POLICIES: dict[str, dict[str, object]] = {}
_CONSTRAINTS: dict[str, dict[str, object]] = {}


class PortfolioRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_portfolios(self) -> list[dict[str, object]]:
        return PersistentPortfolioStore.list_portfolios(self.db)

    def get_portfolio(self, portfolio_id: str) -> dict[str, object] | None:
        return PersistentPortfolioStore.get_portfolio(self.db, portfolio_id)

    def create_portfolio(self, payload: dict[str, object]) -> dict[str, object]:
        return PersistentPortfolioStore.create_portfolio(self.db, payload)

    def update_portfolio(
        self,
        portfolio_id: str,
        payload: dict[str, object],
    ) -> dict[str, object] | None:
        return PersistentPortfolioStore.update_portfolio(
            self.db,
            portfolio_id,
            payload,
        )

    def delete_portfolio(self, portfolio_id: str) -> bool:
        _POLICIES.pop(portfolio_id, None)
        _CONSTRAINTS.pop(portfolio_id, None)
        return PersistentPortfolioStore.delete_portfolio(self.db, portfolio_id)

    def get_policy(self, portfolio_id: str) -> dict[str, object] | None:
        policy = _POLICIES.get(portfolio_id)
        return dict(policy) if policy is not None else None

    def update_policy(
        self,
        portfolio_id: str,
        payload: dict[str, object],
    ) -> dict[str, object]:
        _POLICIES[portfolio_id] = payload
        return dict(payload)

    def get_constraints(self, portfolio_id: str) -> dict[str, object] | None:
        constraints = _CONSTRAINTS.get(portfolio_id)
        return dict(constraints) if constraints is not None else None

    def update_constraints(
        self,
        portfolio_id: str,
        payload: dict[str, object],
    ) -> dict[str, object]:
        _CONSTRAINTS[portfolio_id] = payload
        return dict(payload)


class PositionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_positions(self, portfolio_id: str) -> list[dict[str, object]]:
        return PersistentPortfolioStore.list_positions(self.db, portfolio_id)

    def get_position(
        self,
        portfolio_id: str,
        position_id: str,
    ) -> dict[str, object] | None:
        return PersistentPortfolioStore.get_position(
            self.db,
            portfolio_id,
            position_id,
        )

    def create_position(
        self,
        portfolio_id: str,
        payload: dict[str, object],
    ) -> dict[str, object]:
        return PersistentPortfolioStore.create_position(
            self.db,
            portfolio_id,
            payload,
        )

    def update_position(
        self,
        portfolio_id: str,
        position_id: str,
        payload: dict[str, object],
    ) -> dict[str, object] | None:
        return PersistentPortfolioStore.update_position(
            self.db,
            portfolio_id,
            position_id,
            payload,
        )

    def delete_position(self, portfolio_id: str, position_id: str) -> bool:
        return PersistentPortfolioStore.delete_position(
            self.db,
            portfolio_id,
            position_id,
        )
