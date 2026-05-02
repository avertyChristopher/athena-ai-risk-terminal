from app.schemas.common_schema import ModuleStatus


class RiskModuleStatus(ModuleStatus):
    engines_available: list[str] = []
