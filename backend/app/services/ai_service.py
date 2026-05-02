from app.schemas.common_schema import ModuleStatus
from app.services.riskdna_service import RiskDnaService


class AIService:
    def __init__(self, riskdna_service: RiskDnaService) -> None:
        self.riskdna_service = riskdna_service

    def get_module_status(self) -> ModuleStatus:
        _ = self.riskdna_service.get_structured_context()
        return ModuleStatus(
            module="ai",
            detail="AI explanation routes are scaffolded and reserved for explanation workflows, not source-of-truth calculations.",
        )
