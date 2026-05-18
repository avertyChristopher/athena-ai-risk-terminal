from sqlalchemy.orm import Session

from app.repositories.demo_data_store import DemoDataStore


class PortfolioRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_portfolios(self) -> list[dict[str, object]]:
        return DemoDataStore.list_portfolios()

    def get_portfolio(self, portfolio_id: str) -> dict[str, object] | None:
        return DemoDataStore.get_portfolio(portfolio_id)

    def create_portfolio(self, payload: dict[str, object]) -> dict[str, object]:
        return DemoDataStore.create_portfolio(payload)

    def update_portfolio(
        self,
        portfolio_id: str,
        payload: dict[str, object],
    ) -> dict[str, object] | None:
        return DemoDataStore.update_portfolio(portfolio_id, payload)

    def delete_portfolio(self, portfolio_id: str) -> bool:
        return DemoDataStore.delete_portfolio(portfolio_id)
