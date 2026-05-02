from app.schemas.common_schema import ModuleStatus


class MarketDataModuleStatus(ModuleStatus):
    assets_tracked: int = 0
