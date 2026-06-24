from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from app.modules.athena_intelligence.schemas import AthenaAICommentary
from app.modules.athena_intelligence.schemas import AthenaIntelligenceRequest
from app.modules.athena_intelligence.service import AthenaIntelligenceService


def attach_athena_ai_commentary(
    response: BaseModel,
    *,
    module_name: str,
    analysis_mode: str,
    payload: dict[str, Any] | None = None,
    language: str = "en",
    style: str = "professional",
) -> BaseModel:
    commentary = build_athena_ai_commentary(
        module_name=module_name,
        analysis_mode=analysis_mode,
        payload=payload or _response_payload(response),
        language=language,
        style=style,
    )
    setattr(response, "athena_ai_commentary", commentary)
    return response


def build_athena_ai_commentary(
    *,
    module_name: str,
    analysis_mode: str,
    payload: dict[str, Any],
    language: str = "en",
    style: str = "professional",
) -> AthenaAICommentary:
    return AthenaIntelligenceService().generate_commentary(
        AthenaIntelligenceRequest(
            module_name=module_name,
            analysis_mode=analysis_mode,
            language=language,
            payload=payload,
            style=style,
        ),
    )


def _response_payload(response: BaseModel) -> dict[str, Any]:
    return response.model_dump(mode="json", exclude={"athena_ai_commentary"})
