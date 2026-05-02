from app.schemas.rates_schema import RatesModuleStatus


class RatesService:
    def get_module_status(self) -> RatesModuleStatus:
        return RatesModuleStatus(
            module="rates",
            detail="Rates and bond analytics will be implemented as pure domain calculations in a later phase.",
            analytics_available=[],
        )
