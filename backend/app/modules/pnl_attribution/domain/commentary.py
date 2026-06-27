from __future__ import annotations

from typing import Any

from app.modules.athena_intelligence.schemas import AthenaIntelligenceRequest
from app.modules.athena_intelligence.service import AthenaIntelligenceService


def build_pnl_commentary(
    *,
    payload: dict[str, Any],
    language: str,
    service: AthenaIntelligenceService,
) -> dict[str, Any]:
    commentary = service.generate_commentary(
        AthenaIntelligenceRequest(
            module_name="pnl_attribution",
            analysis_mode="pnl",
            language=language,
            style="executive",
            payload=payload,
        ),
    )
    return commentary.model_dump(mode="json")
