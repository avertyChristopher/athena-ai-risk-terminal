from sqlalchemy.orm import Session

from app.modules.portfolio_builder.repository import (
    PortfolioRepository,
    PositionRepository,
)


DEMO_TREASURY_CURVE = [
    {"maturity": 0.25, "rate": 0.0430},
    {"maturity": 0.5, "rate": 0.0425},
    {"maturity": 1.0, "rate": 0.0410},
    {"maturity": 2.0, "rate": 0.0390},
    {"maturity": 5.0, "rate": 0.0400},
    {"maturity": 10.0, "rate": 0.0420},
    {"maturity": 30.0, "rate": 0.0440},
]


DEMO_DURATION_METADATA = {
    "BND": 6.0,
    "AGG": 6.1,
    "IEF": 7.3,
    "TLT": 16.5,
    "LQD": 8.2,
    "HYG": 3.5,
}


class RatesLabRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.portfolios = PortfolioRepository(db)
        self.positions = PositionRepository(db)

    def get_demo_curve(self) -> list[dict[str, float]]:
        return [dict(point) for point in DEMO_TREASURY_CURVE]

    def get_portfolio(self, portfolio_id: str) -> dict[str, object] | None:
        return self.portfolios.get_portfolio(portfolio_id)

    def list_positions(self, portfolio_id: str) -> list[dict[str, object]]:
        return self.positions.list_positions(portfolio_id)

    def get_duration_metadata(self, symbol: str) -> float | None:
        return DEMO_DURATION_METADATA.get(symbol.upper())
