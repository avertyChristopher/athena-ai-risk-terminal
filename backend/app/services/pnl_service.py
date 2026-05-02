from app.repositories.pnl_repository import PnlRepository
from app.schemas.pnl_schema import PnlModuleStatus


class PnlService:
    def __init__(self, repository: PnlRepository) -> None:
        self.repository = repository

    def get_module_status(self) -> PnlModuleStatus:
        return PnlModuleStatus(
            module="pnl",
            detail="P&L attribution routes are in place. Calculation flows and storage come later.",
            attribution_enabled=self.repository.attribution_enabled(),
        )
