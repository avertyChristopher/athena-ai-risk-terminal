import type { AthenaAICommentary } from "./athena-intelligence";

export type LimitSourceModule =
  | "portfolio_builder"
  | "risk_monitor"
  | "volatility_lab"
  | "options_pricing_lab"
  | "rates_lab"
  | "stress_testing"
  | "trade_simulator"
  | "limit_center";

export type ComparisonOperator =
  | "greater_than"
  | "greater_than_or_equal"
  | "less_than"
  | "less_than_or_equal"
  | "equal"
  | "not_equal";

export type LimitSeverity = "low" | "medium" | "high" | "critical";
export type LimitCategory =
  | "portfolio"
  | "risk"
  | "stress"
  | "fixed_income"
  | "options"
  | "trade";
export type BreachStatus =
  | "open"
  | "under_review"
  | "approved_exception"
  | "rejected"
  | "resolved";
export type ReviewAction =
  | "mark_under_review"
  | "approve_exception"
  | "reject"
  | "resolve"
  | "reopen";
export type OverallLimitStatus =
  | "within_limits"
  | "watchlist"
  | "breached"
  | "severe_breach"
  | "critical_breach";

export type LimitCenterStatus = {
  status: string;
  module: string;
  detail: string;
  engines_available: string[];
  active_rules: number;
  supported_source_modules: LimitSourceModule[];
};

export type LimitRule = {
  rule_id: string;
  name: string;
  category: LimitCategory;
  metric_key: string;
  limit_value: number | boolean;
  comparison_operator: ComparisonOperator;
  severity_if_breached: LimitSeverity;
  enabled: boolean;
  description: string;
  source_modules: LimitSourceModule[];
  methodology: string;
  created_at: string;
  updated_at: string;
};

export type LimitRuleCreate = Omit<
  LimitRule,
  "rule_id" | "created_at" | "updated_at"
> & {
  rule_id?: string | null;
};

export type LimitRuleUpdate = Partial<
  Omit<LimitRule, "rule_id" | "created_at" | "updated_at">
>;

export type LimitRuleListResponse = {
  total_rules: number;
  active_rules: number;
  rules: LimitRule[];
};

export type EvaluatedLimitRule = {
  rule_id: string;
  rule_name: string;
  category: LimitCategory;
  source_module: LimitSourceModule;
  metric_key: string;
  current_value: number | boolean | null;
  limit_value: number | boolean;
  comparison_operator: ComparisonOperator;
  breached: boolean;
  severity: LimitSeverity | null;
  enabled: boolean;
  warning: string | null;
};

export type BreachReviewEvent = {
  action: ReviewAction;
  from_status: BreachStatus;
  to_status: BreachStatus;
  reviewer: string;
  note: string | null;
  decision: string;
  timestamp: string;
};

export type LimitBreach = {
  breach_id: string;
  rule_id: string;
  rule_name: string;
  portfolio_id: string;
  source_module: LimitSourceModule;
  metric_key: string;
  current_value: number | boolean;
  limit_value: number | boolean;
  comparison_operator: ComparisonOperator;
  severity: LimitSeverity;
  status: BreachStatus;
  explanation: string;
  suggested_action: string;
  created_at: string;
  updated_at: string;
  reviewed_by: string | null;
  review_note: string | null;
  review_history: BreachReviewEvent[];
};

export type LimitEvaluationSummary = {
  portfolio_id: string;
  source_module: LimitSourceModule;
  evaluated_rule_count: number;
  breach_count: number;
  open_breach_count: number;
  critical_breach_count: number;
  highest_severity: LimitSeverity | null;
  overall_status: OverallLimitStatus;
  source_modules: LimitSourceModule[];
};

export type LimitEvaluationRequest = {
  portfolio_id: string;
  source_module: LimitSourceModule;
  payload: Record<string, unknown>;
  language?: "en" | "fr";
};

export type LimitEvaluationResponse = {
  portfolio_id: string;
  source_module: LimitSourceModule;
  evaluated_rules: EvaluatedLimitRule[];
  breaches: LimitBreach[];
  warnings: string[];
  summary: LimitEvaluationSummary;
  highest_severity: LimitSeverity | null;
  overall_status: OverallLimitStatus;
  athena_ai_commentary: AthenaAICommentary;
  generated_at: string;
};

export type BreachListResponse = {
  total_breaches: number;
  open_breaches: number;
  critical_breaches: number;
  approved_exceptions: number;
  resolved_breaches: number;
  breaches: LimitBreach[];
};

export type BreachReviewRequest = {
  action: ReviewAction;
  reviewer: string;
  note?: string | null;
};

export type BreachReviewResponse = {
  breach: LimitBreach;
  event: BreachReviewEvent;
};

export type SourceModuleCard = {
  module: LimitSourceModule;
  display_name: string;
  connected: boolean;
  payload_available: boolean;
  metrics_provided: string[];
  last_evaluated: string | null;
  warnings: string[];
};
