from sqlalchemy.orm import Session

from app.models.portfolio_model import PortfolioModel


class PortfolioRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_portfolios(self) -> list[PortfolioModel]:
        return []
