from app.repositories.risk_repository import RiskRepository
from app.schemas.risk_schema import RiskModuleStatus


class RiskService:
    def __init__(self, repository: RiskRepository) -> None:
        self.repository = repository

    def get_module_status(self) -> RiskModuleStatus:
        return RiskModuleStatus(
            module="risk",
            detail="Risk routes are connected to the service layer. Quant engines will be added in domain modules next.",
            engines_available=self.repository.list_available_metrics(),
        )
