from __future__ import annotations

from app.modules.athena_intelligence.schemas import AthenaAICommentary
from app.modules.athena_intelligence.schemas import AthenaIntelligenceRequest
from app.modules.athena_intelligence.service import AthenaIntelligenceService
from app.modules.ai_anomaly_center.schemas import AnomalyRecord


def build_anomaly_commentary(
    *,
    records: list[AnomalyRecord],
    language: str,
    service: AthenaIntelligenceService,
) -> AthenaAICommentary:
    top = sorted(records, key=lambda item: item.anomaly_score, reverse=True)[:5]
    payload = {
        "anomalies_detected": len(records),
        "highest_severity": top[0].severity if top else None,
        "top_anomalies": [
            {
                "title": item.title,
                "category": item.category,
                "severity": item.severity,
                "score": item.anomaly_score,
                "source_module": item.source_module,
                "suggested_action": item.suggested_action,
            }
            for item in top
        ],
        "limitations": [
            "Rule-based monitoring only.",
            "Not production fraud detection.",
            "Outputs support operational review and are not investment advice.",
        ],
    }
    return service.generate_commentary(
        AthenaIntelligenceRequest(
            module_name="ai_anomaly_center",
            analysis_mode="anomaly_monitoring",
            language=language,
            style="professional",
            payload=payload,
        ),
    )
