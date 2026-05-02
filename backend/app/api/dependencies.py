from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.market_data_repository import MarketDataRepository
from app.repositories.pnl_repository import PnlRepository
from app.repositories.portfolio_repository import PortfolioRepository
from app.repositories.report_repository import ReportRepository
from app.repositories.risk_repository import RiskRepository
from app.repositories.trade_repository import TradeRepository
from app.services.ai_service import AIService
from app.services.market_data_service import MarketDataService
from app.services.pnl_service import PnlService
from app.services.portfolio_service import PortfolioService
from app.services.pricing_service import PricingService
from app.services.rates_service import RatesService
from app.services.report_service import ReportService
from app.services.risk_service import RiskService
from app.services.riskdna_service import RiskDnaService
from app.services.trade_service import TradeService


def get_db_session() -> Generator[Session, None, None]:
    yield from get_db()


def get_market_data_service(
    db: Session = Depends(get_db_session),
) -> MarketDataService:
    return MarketDataService(MarketDataRepository(db))


def get_portfolio_service(
    db: Session = Depends(get_db_session),
) -> PortfolioService:
    return PortfolioService(PortfolioRepository(db))


def get_trade_service(db: Session = Depends(get_db_session)) -> TradeService:
    return TradeService(TradeRepository(db))


def get_risk_service(db: Session = Depends(get_db_session)) -> RiskService:
    return RiskService(RiskRepository(db))


def get_pricing_service() -> PricingService:
    return PricingService()


def get_rates_service() -> RatesService:
    return RatesService()


def get_pnl_service(db: Session = Depends(get_db_session)) -> PnlService:
    return PnlService(PnlRepository(db))


def get_riskdna_service() -> RiskDnaService:
    return RiskDnaService()


def get_ai_service(
    riskdna_service: RiskDnaService = Depends(get_riskdna_service),
) -> AIService:
    return AIService(riskdna_service)


def get_report_service(db: Session = Depends(get_db_session)) -> ReportService:
    return ReportService(ReportRepository(db))
