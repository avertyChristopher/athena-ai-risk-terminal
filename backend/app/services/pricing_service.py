from app.schemas.pricing_schema import PricingModuleStatus


class PricingService:
    def get_module_status(self) -> PricingModuleStatus:
        return PricingModuleStatus(
            module="pricing",
            detail="Option pricing endpoints are scaffolded. Black-Scholes and Greeks stay in the pricing domain later.",
            supported_models=[],
        )
