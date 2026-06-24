from app.modules.athena_intelligence.fallback import generate_fallback_commentary
from app.modules.athena_intelligence.prompt_builder import build_commentary_prompt
from app.modules.athena_intelligence.providers import ProviderResponse
from app.modules.athena_intelligence.response_parser import parse_commentary_response
from app.modules.athena_intelligence.safety import sanitize_text
from app.modules.athena_intelligence.schemas import AthenaIntelligenceRequest
from app.modules.athena_intelligence.service import AthenaIntelligenceService


def test_prompt_builder_includes_module_payload_and_safety_instructions() -> None:
    request = AthenaIntelligenceRequest(
        module_name="risk_monitor",
        analysis_mode="risk",
        payload={"global_risk_score": 72, "custom_metric": "included"},
    )

    prompt = build_commentary_prompt(request)

    assert "Module name: risk_monitor" in prompt
    assert "custom_metric" in prompt
    assert "Do not provide investment advice" in prompt
    assert "Output structured JSON only" in prompt


def test_fallback_detects_risk_concentration_and_var_warnings() -> None:
    commentary = generate_fallback_commentary(
        AthenaIntelligenceRequest(
            module_name="risk_monitor",
            analysis_mode="risk",
            payload={
                "global_risk_score": 78,
                "global_risk_status": "High Risk",
                "risk_metrics": [
                    {"name": "VaR 95%", "value": 0.04},
                    {"name": "CVaR 95%", "value": 0.06},
                ],
                "concentration": {"top_3_weight": 0.75},
            },
        ),
    )

    assert commentary.generated_by == "deterministic_fallback"
    assert any("concentration" in item.lower() for item in commentary.main_risks)
    assert any("cvar" in item.lower() for item in commentary.risk_drivers)


def test_options_fallback_detects_theta_and_vega_exposure() -> None:
    commentary = generate_fallback_commentary(
        AthenaIntelligenceRequest(
            module_name="options_pricing_lab",
            analysis_mode="options",
            payload={
                "underlying_symbol": "AAPL",
                "theta": -12.5,
                "vega": 42.0,
                "delta": 75.0,
            },
        ),
    )

    assert any("theta" in item.lower() for item in commentary.main_risks)
    assert any("vega" in item.lower() for item in commentary.main_risks)


def test_rates_fallback_detects_duration_and_dv01_risk() -> None:
    commentary = generate_fallback_commentary(
        AthenaIntelligenceRequest(
            module_name="rates_lab",
            analysis_mode="rates",
            payload={
                "modified_duration": 8.2,
                "dv01": 51.0,
                "estimated_rate_shock_loss": -5100,
                "rate_shock_bps": 100,
            },
        ),
    )

    assert any("duration" in item.lower() for item in commentary.main_risks)
    assert any("dv01" in item.lower() for item in commentary.risk_drivers)


def test_trade_fallback_detects_suitability_and_constraints() -> None:
    commentary = generate_fallback_commentary(
        AthenaIntelligenceRequest(
            module_name="trade_simulator",
            analysis_mode="trade",
            payload={
                "action": "BUY",
                "symbol": "NVDA",
                "suitability_status": "Requires Review",
                "constraints": [{"message": "Position weight exceeds policy limit."}],
            },
        ),
    )

    assert "Requires Review" in commentary.summary
    assert commentary.breaches


def test_safety_sanitizes_unsafe_recommendation_wording() -> None:
    assert "strong buy" not in sanitize_text("This is a strong buy.").lower()
    assert "you should sell" not in sanitize_text("You should sell this.").lower()


def test_response_parser_rejects_invalid_json() -> None:
    assert parse_commentary_response("not json") is None


def test_service_falls_back_when_provider_response_is_invalid() -> None:
    class InvalidProvider:
        def is_available(self) -> bool:
            return True

        def generate_json(self, prompt: str) -> ProviderResponse:
            _ = prompt
            return ProviderResponse(
                available=True,
                generated_by="ai_provider",
                content="not json",
            )

    service = AthenaIntelligenceService()
    service.provider = InvalidProvider()
    response = service.generate_commentary(
        AthenaIntelligenceRequest(
            module_name="risk_monitor",
            analysis_mode="risk",
            payload={"global_risk_score": 50},
        ),
    )

    assert response.generated_by == "deterministic_fallback"
    assert response.disclaimer
