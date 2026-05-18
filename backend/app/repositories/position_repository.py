from sqlalchemy.orm import Session

from app.repositories.demo_data_store import DemoDataStore


class PositionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_positions(self, portfolio_id: str) -> list[dict[str, object]]:
        return DemoDataStore.list_positions(portfolio_id)

    def get_position(
        self,
        portfolio_id: str,
        position_id: str,
    ) -> dict[str, object] | None:
        return DemoDataStore.get_position(portfolio_id, position_id)

    def create_position(
        self,
        portfolio_id: str,
        payload: dict[str, object],
    ) -> dict[str, object]:
        return DemoDataStore.create_position(portfolio_id, payload)

    def update_position(
        self,
        portfolio_id: str,
        position_id: str,
        payload: dict[str, object],
    ) -> dict[str, object] | None:
        return DemoDataStore.update_position(portfolio_id, position_id, payload)

    def delete_position(self, portfolio_id: str, position_id: str) -> bool:
        return DemoDataStore.delete_position(portfolio_id, position_id)
