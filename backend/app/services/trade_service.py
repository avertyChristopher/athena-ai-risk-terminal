from app.repositories.trade_repository import TradeRepository
from app.schemas.trade_schema import TradeModuleStatus


class TradeService:
    def __init__(self, repository: TradeRepository) -> None:
        self.repository = repository

    def get_module_status(self) -> TradeModuleStatus:
        return TradeModuleStatus(
            module="trades",
            detail="Trade simulation orchestration will sit here once portfolio and risk flows are connected.",
            simulation_ready=self.repository.simulation_available(),
        )
