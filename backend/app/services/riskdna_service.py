class RiskDnaService:
    def get_structured_context(self) -> dict[str, object]:
        return {
            "riskdna_score": "NotCalculated",
            "drivers": [],
            "recommendation": "RiskDNA scoring will be implemented in a later milestone.",
        }
