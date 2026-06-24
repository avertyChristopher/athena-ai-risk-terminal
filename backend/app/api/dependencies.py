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
from app.modules.options_pricing_lab.repository import OptionsPricingLabRepository
from app.modules.options_pricing_lab.service import OptionsPricingLabService
from app.modules.portfolio_builder.repository import (
    PortfolioRepository,
    PositionRepository,
)
from app.modules.portfolio_builder.service import PortfolioService, PositionService
from app.modules.rates_lab.repository import RatesLabRepository
from app.modules.rates_lab.service import RatesLabService
from app.modules.risk_monitor.repository import RiskMonitorRepository
from app.modules.risk_monitor.service import RiskMonitorService
from app.modules.stress_testing.repository import StressTestingRepository
from app.modules.stress_testing.service import StressTestingService
from app.modules.trade_simulator.repository import TradeSimulatorRepository
from app.modules.trade_simulator.service import TradeSimulatorService
from app.modules.volatility_lab.repository import VolatilityLabRepository
from app.modules.volatility_lab.service import VolatilityLabService


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


def get_risk_monitor_service(
    db: Session = Depends(get_db_session),
) -> RiskMonitorService:
    return RiskMonitorService(RiskMonitorRepository(db))


def get_volatility_lab_service(
    db: Session = Depends(get_db_session),
) -> VolatilityLabService:
    return VolatilityLabService(VolatilityLabRepository(db))


def get_options_pricing_lab_service(
    db: Session = Depends(get_db_session),
) -> OptionsPricingLabService:
    return OptionsPricingLabService(OptionsPricingLabRepository(db))


def get_rates_lab_service(
    db: Session = Depends(get_db_session),
) -> RatesLabService:
    return RatesLabService(RatesLabRepository(db))


def get_stress_testing_service(
    db: Session = Depends(get_db_session),
) -> StressTestingService:
    return StressTestingService(StressTestingRepository(db))


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
