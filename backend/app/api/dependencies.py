from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.pnl_repository import PnlRepository
from app.repositories.report_repository import ReportRepository
from app.repositories.risk_repository import RiskRepository
from app.services.ai_service import AIService
from app.services.pnl_service import PnlService
from app.services.pricing_service import PricingService
from app.services.rates_service import RatesService
from app.services.report_service import ReportService
from app.services.risk_service import RiskService
from app.services.riskdna_service import RiskDnaService
from app.modules.equity_analysis.service import EquityAnalysisService
from app.modules.market_data.repository import MarketDataRepository
from app.modules.market_data.service import MarketDataService
from app.modules.portfolio_builder.repository import (
    PortfolioRepository,
    PositionRepository,
)
from app.modules.portfolio_builder.service import PortfolioService, PositionService
from app.modules.trade_simulator.repository import TradeSimulatorRepository
from app.modules.trade_simulator.service import TradeSimulatorService


def get_db_session() -> Generator[Session, None, None]:
    yield from get_db()


def get_market_data_service(
    db: Session = Depends(get_db_session),
) -> MarketDataService:
    return MarketDataService(MarketDataRepository(db))


def get_equity_analysis_service() -> EquityAnalysisService:
    return EquityAnalysisService()


def get_portfolio_service(
    db: Session = Depends(get_db_session),
) -> PortfolioService:
    return PortfolioService(PortfolioRepository(db), PositionRepository(db))


def get_position_service(
    db: Session = Depends(get_db_session),
) -> PositionService:
    return PositionService(PositionRepository(db), PortfolioRepository(db))


def get_trade_simulator_service(
    db: Session = Depends(get_db_session),
) -> TradeSimulatorService:
    return TradeSimulatorService(TradeSimulatorRepository(db))


def get_trade_service(
    db: Session = Depends(get_db_session),
) -> TradeSimulatorService:
    return get_trade_simulator_service(db)


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
