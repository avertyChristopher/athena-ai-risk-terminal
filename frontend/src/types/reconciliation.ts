import type { AthenaAICommentary } from "./athena-intelligence";

export type ExternalSource =
  | "demo_custodian"
  | "uploaded_file_placeholder"
  | "manual_reference";

export type ReconciliationCheck =
  | "positions"
  | "cash"
  | "prices"
  | "trades"
  | "pnl"
  | "fx";

export type BreakType =
  | "position"
  | "cash"
  | "price"
  | "trade"
  | "pnl"
  | "fx"
  | "data_quality";

export type BreakSeverity = "low" | "medium" | "high" | "critical";

export type BreakStatus =
  | "open"
  | "under_review"
  | "explained"
  | "resolved"
  | "ignored";

export type OverallStatus =
  | "reconciled"
  | "minor_breaks"
  | "material_breaks"
  | "critical_breaks";

export type ReviewAction =
  | "mark_under_review"
  | "explain"
  | "resolve"
  | "ignore"
  | "reopen";

export type ReconciliationTolerance = {
  position_quantity_tolerance: number;
  market_value_tolerance: number;
  cash_tolerance: number;
  price_tolerance_bps: number;
  pnl_tolerance: number;
};

export type ReconciliationRequest = {
  portfolio_id: string;
  reconciliation_date: string;
  external_source: ExternalSource;
  checks: ReconciliationCheck[];
  tolerance: ReconciliationTolerance;
  language: "en" | "fr";
};

export type ReviewRequest = {
  action: ReviewAction;
  reviewer: string;
  note?: string | null;
  decision?: string | null;
};

export type ReviewEvent = ReviewRequest & {
  timestamp: string;
};

export type ReconciliationBreak = {
  break_id: string;
  run_id: string;
  portfolio_id: string;
  break_type: BreakType;
  severity: BreakSeverity;
  status: BreakStatus;
  symbol?: string | null;
  metric: string;
  internal_value?: number | string | null;
  external_value?: number | string | null;
  difference?: number | string | null;
  tolerance?: number | string | null;
  source_module: string;
  explanation: string;
  suggested_action: string;
  created_at: string;
  updated_at: string;
  reviewed_by?: string | null;
  review_note?: string | null;
  review_history: ReviewEvent[];
};

export type PositionReconciliationItem = {
  symbol: string;
  internal_quantity: number | null;
  external_quantity: number | null;
  quantity_difference: number | null;
  internal_market_value: number | null;
  external_market_value: number | null;
  market_value_difference: number | null;
  difference_percent: number | null;
  tolerance: number;
  status: string;
  severity?: BreakSeverity | null;
  explanation: string;
};

export type CashReconciliationItem = {
  internal_cash: number | null;
  external_cash: number | null;
  cash_difference: number | null;
  cash_difference_percent: number | null;
  currency: string;
  tolerance: number;
  status: string;
  severity?: BreakSeverity | null;
  explanation: string;
};

export type PriceReconciliationItem = {
  symbol: string;
  internal_price: number | null;
  external_price: number | null;
  price_difference: number | null;
  price_difference_bps: number | null;
  internal_price_timestamp: string | null;
  external_price_timestamp: string | null;
  tolerance_bps: number;
  status: string;
  severity?: BreakSeverity | null;
  explanation: string;
};

export type TradeReconciliationItem = {
  trade_id: string;
  symbol: string;
  action: string;
  quantity: number;
  internal_trade_value: number | null;
  external_trade_value: number | null;
  status: string;
  severity?: BreakSeverity | null;
  explanation: string;
};

export type PnlReconciliationItem = {
  internal_total_pnl: number | null;
  external_total_pnl: number | null;
  pnl_difference: number | null;
  pnl_difference_percent: number | null;
  tolerance: number;
  unexplained_pnl: number | null;
  status: string;
  severity?: BreakSeverity | null;
  explanation: string;
};

export type FxReconciliationItem = {
  currency: string;
  internal_fx_rate: number | null;
  external_fx_rate: number | null;
  fx_difference: number | null;
  translation_difference: number | null;
  status: string;
  severity?: BreakSeverity | null;
  explanation: string;
};

export type ReconciliationMethodology = {
  checks_performed: ReconciliationCheck[];
  tolerances: ReconciliationTolerance;
  data_sources: string[];
  assumptions: string[];
  limitations: string[];
};

export type ReconciliationRunResult = {
  run_id: string;
  portfolio_id: string;
  portfolio_name: string;
  reconciliation_date: string;
  external_source: ExternalSource;
  overall_status: OverallStatus;
  total_breaks: number;
  open_breaks: number;
  critical_breaks: number;
  breaks_by_type: Record<string, number>;
  breaks_by_severity: Record<string, number>;
  checks_performed: ReconciliationCheck[];
  position_breaks: PositionReconciliationItem[];
  cash_breaks: CashReconciliationItem[];
  price_breaks: PriceReconciliationItem[];
  trade_breaks: TradeReconciliationItem[];
  pnl_breaks: PnlReconciliationItem[];
  fx_breaks: FxReconciliationItem[];
  breaks: ReconciliationBreak[];
  unresolved_items: string[];
  warnings: string[];
  methodology: ReconciliationMethodology;
  limitations: string[];
  athena_ai_commentary: AthenaAICommentary | null;
  generated_at: string;
};

export type ReconciliationStatus = {
  status: string;
  module: string;
  detail: string;
  checks_available: ReconciliationCheck[];
  source_modules: string[];
  external_sources: ExternalSource[];
  history_enabled: boolean;
  review_workflow_enabled: boolean;
  export_formats: string[];
};

export type ReconciliationHistoryItem = {
  run_id: string;
  portfolio_id: string;
  portfolio_name: string;
  reconciliation_date: string;
  external_source: ExternalSource;
  overall_status: OverallStatus;
  total_breaks: number;
  critical_breaks: number;
  generated_at: string;
};

export type ReconciliationHistoryResponse = {
  status: string;
  module: string;
  total_runs: number;
  items: ReconciliationHistoryItem[];
};

export type BreakRegisterResponse = {
  status: string;
  module: string;
  total_breaks: number;
  items: ReconciliationBreak[];
};

export type ReconciliationCsvExportResponse = {
  run_id: string;
  content_type: string;
  csv: string;
  included_tables: string[];
};
