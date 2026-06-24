from __future__ import annotations

from app.core.config import settings
from app.modules.athena_intelligence.fallback import (
    generate_fallback_commentary,
    generate_fallback_metric_explanation,
    generate_fallback_risk_synthesis,
)
from app.modules.athena_intelligence.prompt_builder import (
    build_commentary_prompt,
    build_metric_explanation_prompt,
    build_risk_synthesis_prompt,
)
from app.modules.athena_intelligence.providers import provider_from_settings
from app.modules.athena_intelligence.response_parser import (
    parse_commentary_response,
    parse_metric_explanation_response,
    parse_risk_synthesis_response,
)
from app.modules.athena_intelligence.safety import sanitize_commentary_data
from app.modules.athena_intelligence.schemas import (
    AthenaAICommentary,
    AthenaIntelligenceRequest,
    AthenaIntelligenceStatus,
    AthenaMetricExplanationRequest,
    AthenaMetricExplanationResponse,
    AthenaRiskSynthesisRequest,
    AthenaRiskSynthesisResponse,
)


class AthenaIntelligenceService:
    def __init__(self) -> None:
        self.provider = provider_from_settings(
            settings.athena_ai_provider,
            settings.openai_api_key,
            settings.athena_ai_model,
        )

    def get_status(self) -> AthenaIntelligenceStatus:
        provider_available = self.provider.is_available()
        mode = settings.athena_ai_provider.lower()
        fallback_mode = mode in {"fallback", "disabled"} or not provider_available
        return AthenaIntelligenceStatus(
            detail=(
                "Athena Intelligence Engine generates structured risk commentary "
                "from module payloads with deterministic fallback safety."
            ),
            provider_mode="fallback" if fallback_mode else mode,
            provider_available=provider_available and not fallback_mode,
            model=settings.athena_ai_model,
            fallback_enabled=True,
            safety_rules=[
                "No investment advice",
                "Use only structured payload data",
                "Mention demo, partial or fallback assumptions",
                "Structured JSON output",
            ],
        )

    def generate_commentary(
        self,
        request: AthenaIntelligenceRequest,
    ) -> AthenaAICommentary:
        prompt = build_commentary_prompt(request)
        provider_response = self.provider.generate_json(prompt)
        if provider_response.available and provider_response.content:
            parsed = parse_commentary_response(provider_response.content)
            if parsed is not None:
                parsed = sanitize_commentary_data(parsed, request.language)
                return AthenaAICommentary(
                    **parsed,
                    generated_by="ai_provider",
                    source_modules=[request.module_name],
                )

        fallback = generate_fallback_commentary(request)
        if provider_response.limitation and provider_response.limitation not in fallback.limitations:
            fallback.limitations = [provider_response.limitation, *fallback.limitations]
        sanitized = sanitize_commentary_data(fallback.model_dump(), request.language)
        return AthenaAICommentary.model_validate(sanitized)

    def generate_risk_synthesis(
        self,
        request: AthenaRiskSynthesisRequest,
    ) -> AthenaRiskSynthesisResponse:
        prompt = build_risk_synthesis_prompt(request)
        provider_response = self.provider.generate_json(prompt)
        if provider_response.available and provider_response.content:
            parsed = parse_risk_synthesis_response(provider_response.content)
            if parsed is not None:
                parsed = sanitize_commentary_data(parsed, request.language)
                return AthenaRiskSynthesisResponse(
                    **parsed,
                    generated_by="ai_provider",
                )

        fallback = generate_fallback_risk_synthesis(request)
        if provider_response.limitation and provider_response.limitation not in fallback.limitations:
            fallback.limitations = [provider_response.limitation, *fallback.limitations]
        sanitized = sanitize_commentary_data(fallback.model_dump(), request.language)
        return AthenaRiskSynthesisResponse.model_validate(sanitized)

    def explain_metric(
        self,
        request: AthenaMetricExplanationRequest,
    ) -> AthenaMetricExplanationResponse:
        prompt = build_metric_explanation_prompt(request)
        provider_response = self.provider.generate_json(prompt)
        if provider_response.available and provider_response.content:
            parsed = parse_metric_explanation_response(provider_response.content)
            if parsed is not None:
                parsed = sanitize_commentary_data(parsed, request.language)
                return AthenaMetricExplanationResponse(
                    **parsed,
                    generated_by="ai_provider",
                )

        fallback = generate_fallback_metric_explanation(request)
        if provider_response.limitation and provider_response.limitation not in fallback.limitations:
            fallback.limitations = [provider_response.limitation, *fallback.limitations]
        sanitized = sanitize_commentary_data(fallback.model_dump(), request.language)
        return AthenaMetricExplanationResponse.model_validate(sanitized)

    def demo(self) -> AthenaAICommentary:
        return self.generate_commentary(
            AthenaIntelligenceRequest(
                module_name="risk_monitor",
                analysis_mode="risk",
                payload={
                    "global_risk_score": 58,
                    "global_risk_status": "Moderate Risk",
                    "risk_metrics": [
                        {"name": "Portfolio volatility", "value": 0.186},
                        {"name": "VaR 95%", "value": 0.0235},
                        {"name": "CVaR 95%", "value": 0.038},
                        {"name": "Max drawdown", "value": -0.124},
                    ],
                    "concentration": {
                        "top_3_weight": 0.64,
                        "largest_position": {"name": "NVDA", "weight": 0.24},
                    },
                    "limit_breaches": [
                        {
                            "rule_name": "Technology concentration",
                            "explanation": "Technology exposure should be monitored.",
                        },
                    ],
                    "risk_source": {
                        "symbols_missing": [],
                        "badges": ["Demo"],
                    },
                },
                style="executive",
            ),
        )
