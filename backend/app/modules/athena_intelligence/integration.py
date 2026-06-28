from __future__ import annotations

from typing import Any
from uuid import uuid4

from pydantic import BaseModel

from app.modules.athena_intelligence.schemas import AthenaAICommentary
from app.modules.athena_intelligence.schemas import AthenaIntelligenceRequest
from app.modules.athena_intelligence.service import AthenaIntelligenceService
from app.persistence.repositories import AthenaCommentaryPersistenceRepository


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
    commentary = AthenaIntelligenceService().generate_commentary(
        AthenaIntelligenceRequest(
            module_name=module_name,
            analysis_mode=analysis_mode,
            language=language,
            payload=payload,
            style=style,
        ),
    )
    _persist_commentary(module_name, payload, language, commentary)
    return commentary


def _response_payload(response: BaseModel) -> dict[str, Any]:
    return response.model_dump(mode="json", exclude={"athena_ai_commentary"})


def _persist_commentary(
    module_name: str,
    payload: dict[str, Any],
    language: str,
    commentary: AthenaAICommentary,
) -> None:
    try:
        AthenaCommentaryPersistenceRepository().save(
            commentary_id=f"athena_{uuid4().hex[:12]}",
            module_name=module_name,
            portfolio_id=_first_text(payload, "portfolio_id"),
            symbol=_first_text(payload, "symbol"),
            language=language,
            payload=payload,
            summary=commentary.summary,
            generated_by=commentary.generated_by,
        )
    except Exception:
        return


def _first_text(payload: dict[str, Any], key: str) -> str | None:
    value = payload.get(key)
    if value is not None:
        return str(value)
    for nested in payload.values():
        if isinstance(nested, dict) and nested.get(key) is not None:
            return str(nested[key])
    return None
