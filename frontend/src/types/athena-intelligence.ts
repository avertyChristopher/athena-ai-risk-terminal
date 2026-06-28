export type AthenaAIModuleName =
  | "market_data"
  | "equity_analysis"
  | "portfolio_builder"
  | "risk_monitor"
  | "volatility_lab"
  | "options_pricing_lab"
  | "rates_lab"
  | "trade_simulator"
  | "stress_testing"
  | "limit_center"
  | "pnl_attribution"
  | "reconciliation"
  | "ai_anomaly_center"
  | "reports_center";

export type AthenaAIAnalysisMode =
  | "status"
  | "risk"
  | "market"
  | "equity"
  | "portfolio"
  | "symbol"
  | "options"
  | "rates"
  | "trade"
  | "stress"
  | "limit"
  | "pnl"
  | "reconciliation"
  | "anomaly_monitoring"
  | "report";

export type AthenaAIProviderMode = "disabled" | "fallback" | "openai";

export type AthenaIntelligenceStatus = {
  status: string;
  module: string;
  provider_mode: AthenaAIProviderMode;
  fallback_enabled: boolean;
  model: string;
  detail: string;
  endpoints_available: string[];
  safety: {
    structured_payload_only: boolean;
    investment_advice_blocked: boolean;
    secrets_exposed_to_frontend: boolean;
  };
};

export type AthenaAICommentary = {
  summary: string;
  main_risks: string[];
  risk_drivers: string[];
  breaches: string[];
  suggested_actions: string[];
  assumptions: string[];
  limitations: string[];
  confidence_level: "low" | "medium" | "high";
  generated_by: string;
  source_modules: string[];
  disclaimer: string;
  generated_at: string;
};

export type AthenaIntelligenceRequest = {
  module_name: AthenaAIModuleName;
  analysis_mode: AthenaAIAnalysisMode;
  payload: Record<string, unknown>;
  language?: "en" | "fr";
  style?: "concise" | "professional" | "technical";
};
