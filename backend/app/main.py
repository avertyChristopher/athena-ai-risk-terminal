from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api.routes.ai_routes import router as ai_router
from app.api.routes.health_routes import router as health_router
from app.api.routes.pnl_routes import router as pnl_router
from app.api.routes.pricing_routes import router as pricing_router
from app.api.routes.rates_routes import router as rates_router
from app.api.routes.report_routes import router as report_router
from app.api.routes.risk_routes import router as risk_router
from app.api.routes.trade_routes import router as trade_router
from app.core.config import settings
from app.core.exceptions import AthenaError, athena_exception_handler
from app.core.logging import configure_logging
from app.modules.equity_analysis.routes import router as equity_router
from app.modules.market_data.routes import router as market_data_router
from app.modules.options_pricing_lab.routes import router as options_pricing_lab_router
from app.modules.portfolio_builder.routes import router as portfolio_router
from app.modules.rates_lab.routes import router as rates_lab_router
from app.modules.risk_monitor.routes import router as risk_monitor_router
from app.modules.stress_testing.routes import router as stress_testing_router
from app.modules.trade_simulator.routes import router as trade_simulator_router
from app.modules.volatility_lab.routes import router as volatility_lab_router


def create_app() -> FastAPI:
    configure_logging(settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    app.add_exception_handler(AthenaError, athena_exception_handler)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router, prefix=settings.api_prefix)
    app.include_router(market_data_router, prefix=settings.api_prefix)
    app.include_router(equity_router, prefix=settings.api_prefix)
    app.include_router(portfolio_router, prefix=settings.api_prefix)
    app.include_router(trade_simulator_router, prefix=settings.api_prefix)
    app.include_router(risk_monitor_router, prefix=settings.api_prefix)
    app.include_router(volatility_lab_router, prefix=settings.api_prefix)
    app.include_router(options_pricing_lab_router, prefix=settings.api_prefix)
    app.include_router(rates_lab_router, prefix=settings.api_prefix)
    app.include_router(stress_testing_router, prefix=settings.api_prefix)
    app.include_router(trade_router, prefix=settings.api_prefix)
    app.include_router(risk_router, prefix=settings.api_prefix)
    app.include_router(pricing_router, prefix=settings.api_prefix)
    app.include_router(rates_router, prefix=settings.api_prefix)
    app.include_router(pnl_router, prefix=settings.api_prefix)
    app.include_router(ai_router, prefix=settings.api_prefix)
    app.include_router(report_router, prefix=settings.api_prefix)

    return app


app = create_app()
