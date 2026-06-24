from __future__ import annotations

from datetime import datetime

from app.modules.risk_shared.schemas import ModuleIntegrationStatus


def integration_status(
    *,
    module: str,
    status: str,
    data_source: str,
    payload_available: bool = False,
    generated_at: datetime | None = None,
    warnings: list[str] | None = None,
    required_data: list[str] | None = None,
) -> ModuleIntegrationStatus:
    return ModuleIntegrationStatus(
        module=module,
        status=status,
        data_source=data_source,
        payload_available=payload_available,
        generated_at=generated_at,
        warnings=warnings or [],
        required_data=required_data or [],
    )
