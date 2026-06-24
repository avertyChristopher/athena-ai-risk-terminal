export type StressTestingStatus = {
  status: string;
  module: string;
  detail: string;
  engines_available: string[];
};

export type ShockAssumptions = {
  asset_class_shocks: Record<string, number>;
  sector_shocks: Record<string, number>;
  symbol_shocks: Record<string, number>;
  rate_shock_bps: number;
  volatility_shock: number;
  fx_shock: number;
  credit_spread_shock_bps: number;
  liquidity_multiplier: number;
};

export type StressScenarioDefinition = {
  id: string;
  name: string;
  description: string;
  shocks: ShockAssumptions;
};

export type ScenarioLibraryResponse = {
  status: string;
  module: string;
  scenarios: StressScenarioDefinition[];
};

export type CustomStressScenario = {
  name: string;
  description?: string;
  equity_shock: number;
  asset_class_shocks: Record<string, number>;
  sector_shocks: Record<string, number>;
  symbol_shocks: Record<string, number>;
  rate_shock_bps: number;
  volatility_shock: number;
  fx_shock: number;
  credit_spread_shock_bps: number;
  liquidity_multiplier: number;
};

export type StressTestingRunRequest = {
  portfolio_id: string;
  scenario_id?: string | null;
  custom_scenario?: CustomStressScenario | null;
  benchmark_symbol: string;
  confidence_level: number;
  include_position_impacts: boolean;
  include_risk_metrics: boolean;
  include_module_links: boolean;
};

export type SelectedPortfolio = {
  portfolio_id: string;
  name: string;
  base_currency: string;
  benchmark_symbol: string;
  positions: number;
  cash: number;
};

export type PositionStressImpact = {
  position_id: string;
  symbol: string;
  name: string;
  asset_class: string;
  sector: string;
  currency: string;
  base_value: number;
  shock_applied: number;
  shock_source: string;
  stressed_value: number;
  dollar_impact: number;
  percent_impact: number;
  contribution_to_loss: number;
  duration: number | null;
  dv01: number | null;
  rate_impact: number;
  credit_impact: number;
  fx_impact: number;
  liquidity_impact: number;
  data_source: string;
  warnings: string[];
};

export type GroupStressImpact = {
  name: string;
  base_value: number;
  stressed_value: number;
  dollar_impact: number;
  percent_impact: number;
  loss_contribution: number;
};

export type WorstContributor = {
  name: string;
  label: string;
  dollar_loss: number;
  percent_impact: number;
  contribution_to_loss: number;
};

export type RiskMetricComparison = {
  metric: string;
  before: number | null;
  after: number | null;
  unit: string;
  source: string;
};

export type FixedIncomeStressSummary = {
  fixed_income_exposure: number;
  fixed_income_weight: number;
  weighted_average_duration: number | null;
  estimated_dv01: number | null;
  rate_shock_bps: number;
  credit_spread_shock_bps: number;
  rate_risk_impact: number;
  data_source: string;
  warnings: string[];
};

export type OptionsRiskIntegration = {
  status: string;
  options_pricing_lab_ready: boolean;
  option_positions_detected: boolean;
  delta_adjusted_exposure: number | null;
  gamma_effect: number | null;
  vega_effect: number | null;
  theta_decay: number | null;
  warnings: string[];
};

export type IntegrationStatus = {
  module: string;
  status: string;
  data_source: string;
  warnings: string[];
};

export type StressLimitBreach = {
  rule_name: string;
  category: string;
  current_value: number;
  limit_value: number;
  severity: string;
  explanation: string;
  suggested_action: string;
};

export type StressSeverityAssessment = {
  severity: string;
  score: number;
  main_drivers: string[];
};

export type StressMethodology = {
  method: string;
  assumptions: string[];
  limitations: string[];
  data_sources: string[];
  generated_at: string;
};

export type AthenaStressCommentary = {
  summary: string;
  key_points: string[];
  suggested_actions: string[];
  not_investment_advice: boolean;
};

export type RiskMonitorStressPayload = {
  portfolio_id: string;
  scenario_id: string;
  stressed_value: number;
  percent_loss: number;
  worst_contributors: WorstContributor[];
  stressed_var: number | null;
  stressed_cvar: number | null;
  stressed_volatility: number | null;
  breached_limits: StressLimitBreach[];
  severity: string;
  generated_at: string;
};

export type StressTestingResponse = {
  selected_portfolio: SelectedPortfolio;
  selected_scenario: StressScenarioDefinition;
  base_portfolio_value: number;
  stressed_portfolio_value: number;
  dollar_loss: number;
  percent_loss: number;
  severity: StressSeverityAssessment;
  position_impacts: PositionStressImpact[];
  asset_class_impacts: GroupStressImpact[];
  sector_impacts: GroupStressImpact[];
  currency_impacts: GroupStressImpact[];
  worst_contributors: WorstContributor[];
  risk_metrics: RiskMetricComparison[];
  fixed_income_stress: FixedIncomeStressSummary;
  options_risk: OptionsRiskIntegration;
  integrations: IntegrationStatus[];
  limit_breaches: StressLimitBreach[];
  warnings: string[];
  methodology: StressMethodology;
  risk_monitor_payload: RiskMonitorStressPayload;
  athena_commentary: AthenaStressCommentary;
  module_links: Record<string, string>;
};
