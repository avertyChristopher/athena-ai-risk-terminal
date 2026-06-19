from app.modules.risk_monitor.schemas import RiskSourceMetadata
from app.modules.risk_shared.schemas import SharedRiskPayload


def shared_payload_to_risk_source(payload: SharedRiskPayload) -> RiskSourceMetadata:
    badges = list(payload.data_source.badges)
    if "Volatility Lab" not in badges:
        badges.append("Volatility Lab")

    return RiskSourceMetadata(
        metric_source=payload.metric_source,
        fallback_used=payload.fallback_used,
        fallback_reason=payload.data_source.fallback_reason,
        observations=payload.data_source.observations,
        symbols_found=payload.data_source.symbols_found,
        symbols_missing=payload.missing_symbols,
        quality_warnings=payload.warnings,
        badges=badges,
    )
