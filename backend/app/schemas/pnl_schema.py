from app.schemas.common_schema import ModuleStatus


class PnlModuleStatus(ModuleStatus):
    attribution_enabled: bool = True
