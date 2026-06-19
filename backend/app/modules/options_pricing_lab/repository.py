from sqlalchemy.orm import Session

from app.modules.market_data.repository import MarketDataRepository
from app.modules.volatility_lab.repository import VolatilityLabRepository
from app.modules.volatility_lab.schemas import VolatilityAssetAnalysisRequest
from app.modules.volatility_lab.service import VolatilityLabService


class OptionsPricingLabRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.market_data = MarketDataRepository(db)
        self.volatility_lab = VolatilityLabService(VolatilityLabRepository(db))

    def get_latest_price(self, symbol: str) -> float | None:
        rows = sorted(
            self.market_data.get_prices(symbol),
            key=lambda row: str(row.get("date", "")),
        )
        if not rows:
            return None
        try:
            return float(rows[-1]["close"])
        except (KeyError, TypeError, ValueError):
            return None

    def get_volatility_inputs(self, symbol: str) -> dict[str, float | str | None]:
        try:
            analysis = self.volatility_lab.analyze_asset(
                VolatilityAssetAnalysisRequest(
                    symbol=symbol.upper(),
                    benchmark_symbol="SPY",
                    rolling_window=5,
                ),
            )
        except Exception:
            return {
                "realized_volatility": None,
                "ewma_volatility": None,
                "source": "manual",
            }

        return {
            "realized_volatility": analysis.volatility_summary.annualized_volatility,
            "ewma_volatility": analysis.ewma_volatility.latest_volatility,
            "source": analysis.data_source.metric_source,
        }
