from sqlalchemy.orm import Session

from app.repositories.demo_data_store import DemoDataStore


class RiskMonitorRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_portfolios(self) -> list[dict[str, object]]:
        return DemoDataStore.list_portfolios()

    def get_portfolio(self, portfolio_id: str) -> dict[str, object] | None:
        return DemoDataStore.get_portfolio(portfolio_id)

    def list_positions(self, portfolio_id: str) -> list[dict[str, object]]:
        return DemoDataStore.list_positions(portfolio_id)
