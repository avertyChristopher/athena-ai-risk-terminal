export type RiskModuleStatus = {
  status: string;
  module: string;
  detail: string;
  engines_available: string[];
};

export type RiskMonitorAnalyzeRequest = {
  portfolio_id: string;
  benchmark_symbol?: string;
  confidence_level?: number;
  risk_free_rate?: number;
  limits?: RiskLimitOverrides;
  stress_shocks?: StressShockOverrides;
};

export type RiskLimitOverrides = {
  max_single_position_weight?: number;
  max_sector_exposure?: number;
  max_asset_type_exposure?: number;
  minimum_cash_reserve?: number;
  max_top_3_concentration?: number;
  max_portfolio_volatility?: number;
  max_var_95?: number;
  max_cvar_95?: number;
  max_drawdown?: number;
  max_tracking_error?: number;
  max_active_exposure?: number;
};

export type StressShockOverrides = {
  equity_market_shock?: number;
  technology_sector_shock?: number;
  interest_rate_shock?: number;
  largest_holding_shock?: number;
};

export type RiskSourceMetadata = {
  metric_source: string;
  fallback_used: boolean;
  fallback_reason: string | null;
  observations: number;
  symbols_found: string[];
  symbols_missing: string[];
  quality_warnings: string[];
  badges: string[];
};

export type RiskMonitorAssumptions = {
  limits: Record<string, number>;
  stress_shocks: Record<string, number>;
};

export type RiskMetric = {
  name: string;
  value: number | null;
  unit: string;
  source: string;
  status: string;
  description: string;
};

export type ConcentrationExposure = {
  name: string;
  weight: number;
  limit: number | null;
  status: string;
};

export type ConcentrationAnalysis = {
  largest_position: ConcentrationExposure | null;
  top_3_weight: number;
  top_5_weight: number;
  sector_exposures: ConcentrationExposure[];
  asset_type_exposures: ConcentrationExposure[];
  cash_weight: number;
  concentration_score: number;
  warnings: string[];
};

export type RiskLimitBreach = {
  rule_name: string;
  category: string;
  current_value: number;
  limit_value: number;
  severity: "low" | "medium" | "high" | "critical";
  explanation: string;
  suggested_action: string;
};

export type StressScenarioResult = {
  name: string;
  estimated_impact_percent: number;
  estimated_loss: number;
  most_affected_holdings: string[];
  severity: "low" | "medium" | "high" | "critical";
  explanation: string;
};

export type RiskContributionItem = {
  name: string;
  weight: number;
  contribution: number;
  contribution_percent: number;
  source: string;
};

export type RiskContributionResponse = {
  contribution_source: string;
  method: string;
  by_asset: RiskContributionItem[];
  by_sector: RiskContributionItem[];
  largest_risk_contributor: string | null;
  diversification_warning: string | null;
};

export type BenchmarkRiskResponse = {
  benchmark_symbol: string;
  beta: number | null;
  active_exposure: number;
  tracking_error: number | null;
  information_ratio: number | null;
  active_risk_status: string;
  warnings: string[];
  badges: string[];
};

export type RiskAlert = {
  title: string;
  severity: "low" | "medium" | "high" | "critical";
  message: string;
  suggested_action: string;
};

export type AthenaRiskCommentary = {
  summary: string;
  main_drivers: string[];
  suggested_actions: string[];
};

export type RiskMonitorAnalysisResponse = {
  portfolio_id: string;
  portfolio_name: string;
  benchmark_symbol: string;
  total_value: number;
  global_risk_score: number;
  global_risk_status: string;
  main_drivers: string[];
  risk_metrics: RiskMetric[];
  concentration: ConcentrationAnalysis;
  limit_breaches: RiskLimitBreach[];
  stress_tests: StressScenarioResult[];
  risk_contribution: RiskContributionResponse;
  benchmark_risk: BenchmarkRiskResponse;
  alerts: RiskAlert[];
  athena_commentary: AthenaRiskCommentary;
  risk_source: RiskSourceMetadata;
  assumptions: RiskMonitorAssumptions;
};
