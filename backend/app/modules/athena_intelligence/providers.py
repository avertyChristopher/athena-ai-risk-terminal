from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderResponse:
    available: bool
    generated_by: str
    content: str | None = None
    limitation: str | None = None


class AthenaAIProvider:
    name = "base"

    def is_available(self) -> bool:
        return False

    def generate_json(self, prompt: str) -> ProviderResponse:
        _ = prompt
        return ProviderResponse(
            available=False,
            generated_by="deterministic_fallback",
            limitation="AI provider unavailable.",
        )


class DisabledProvider(AthenaAIProvider):
    name = "disabled"

    def generate_json(self, prompt: str) -> ProviderResponse:
        _ = prompt
        return ProviderResponse(
            available=False,
            generated_by="deterministic_fallback",
            limitation="AI provider disabled.",
        )


class FallbackProvider(AthenaAIProvider):
    name = "fallback"

    def generate_json(self, prompt: str) -> ProviderResponse:
        _ = prompt
        return ProviderResponse(
            available=False,
            generated_by="deterministic_fallback",
            limitation="Deterministic fallback mode configured.",
        )


class OpenAIProvider(AthenaAIProvider):
    name = "openai"

    def __init__(self, api_key: str | None, model: str | None) -> None:
        self.api_key = api_key
        self.model = model or "gpt-4.1-mini"

    def is_available(self) -> bool:
        return bool(self.api_key)

    def generate_json(self, prompt: str) -> ProviderResponse:
        _ = prompt
        if not self.is_available():
            return ProviderResponse(
                available=False,
                generated_by="deterministic_fallback",
                limitation="OpenAI provider selected but OPENAI_API_KEY is unavailable.",
            )
        return ProviderResponse(
            available=False,
            generated_by="deterministic_fallback",
            limitation=(
                "OpenAI provider abstraction is configured, but live generation is "
                "disabled in this deterministic build."
            ),
        )


def provider_from_settings(
    provider_mode: str,
    api_key: str | None,
    model: str | None,
) -> AthenaAIProvider:
    normalized = provider_mode.lower()
    if normalized == "disabled":
        return DisabledProvider()
    if normalized == "openai":
        return OpenAIProvider(api_key, model)
    return FallbackProvider()
