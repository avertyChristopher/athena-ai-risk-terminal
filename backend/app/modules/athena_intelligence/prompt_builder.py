from __future__ import annotations

import json
from typing import Any

from app.modules.athena_intelligence.schemas import (
    AthenaIntelligenceRequest,
    AthenaMetricExplanationRequest,
    AthenaRiskSynthesisRequest,
)


def _payload_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True, default=str)


def build_commentary_prompt(request: AthenaIntelligenceRequest) -> str:
    return "\n".join(
        [
            "You are Athena Intelligence Engine, an institutional financial risk commentary engine.",
            "Use only the structured payload provided below.",
            "Do not invent facts, prices, holdings, ratings, forecasts or recommendations.",
            "Do not provide investment advice. Do not recommend buy, sell or hold.",
            "Mention missing data, demo data, fallback assumptions and limitations when present.",
            "Use cautious wording such as may indicate, suggests, should be reviewed, could increase risk, or may require monitoring.",
            "Output structured JSON only with keys: summary, main_risks, risk_drivers, breaches, suggested_actions, assumptions, limitations, confidence_level.",
            f"Module name: {request.module_name}",
            f"Analysis mode: {request.analysis_mode}",
            f"Language: {request.language}",
            f"Style: {request.style}",
            f"Maximum bullet points per list: {request.max_points}",
            "Structured payload:",
            _payload_json(request.payload),
        ],
    )


def build_risk_synthesis_prompt(request: AthenaRiskSynthesisRequest) -> str:
    return "\n".join(
        [
            "You are Athena Intelligence Engine, a cross-module portfolio risk synthesis engine.",
            "Use only the structured payloads provided below.",
            "Do not invent unavailable analytics. Do not provide investment advice.",
            "Return structured JSON only with keys: executive_summary, overall_risk_level, top_risk_drivers, cross_module_findings, breached_limits, portfolio_vulnerabilities, suggested_next_actions, module_specific_notes, assumptions, limitations.",
            f"Portfolio id: {request.portfolio_id}",
            f"Language: {request.language}",
            f"Style: {request.style}",
            f"Maximum bullet points per list: {request.max_points}",
            "Structured payloads:",
            _payload_json(request.payloads.model_dump(exclude_none=True)),
        ],
    )


def build_metric_explanation_prompt(request: AthenaMetricExplanationRequest) -> str:
    return "\n".join(
        [
            "You are Athena Intelligence Engine, a financial education and risk interpretation engine.",
            "Use only the provided metric and context.",
            "Do not provide investment advice or recommendations.",
            "Return structured JSON only with keys: explanation, interpretation, risk_meaning, limitations, cfa_note.",
            f"Metric name: {request.metric_name}",
            f"Metric value: {request.metric_value}",
            f"Module name: {request.module_name}",
            f"Language: {request.language}",
            "Structured context:",
            _payload_json(request.context),
        ],
    )
