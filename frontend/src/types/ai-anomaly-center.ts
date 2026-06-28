import type { AthenaAICommentary } from "./athena-intelligence";

export type AnomalySeverity = "low" | "medium" | "high" | "critical";
export type AnomalyStatus = "open" | "under_review" | "explained" | "resolved" | "ignored";
export type AnomalyCategory =
  | "market_data"
  | "portfolio"
  | "trades"
  | "pnl"
  | "risk"
  | "reconciliation"
  | "limits"
  | "stress"
  | "rates_options";
export type AnomalyScanScope = "all" | AnomalyCategory;
export type AnomalyReviewAction =
  | "mark_under_review"
  | "explain"
  | "resolve"
  | "ignore"
  | "reopen";
export type AnomalyConfidence = "low" | "medium" | "high";
export type AnomalyLanguage = "en" | "fr";

export type AIAnomalyCenterStatus = {
  status: string;
  module: string;
  detail: string;
  detection_mode: string;
  persistence_enabled: boolean;
  review_workflow_enabled: boolean;
  categories: AnomalyCategory[];
  source_modules: string[];
  limitations: string[];
};

export type AnomalyReviewEvent = {
  action: AnomalyReviewAction;
  from_status: AnomalyStatus;
  to_status: AnomalyStatus;
  reviewer: string;
  note?: string | null;
  decision?: string | null;
  timestamp: string;
};

export type AnomalyRecord = {
  anomaly_id: string;
  portfolio_id?: string | null;
  module_name: string;
  anomaly_type: string;
  category: AnomalyCategory;
  severity: AnomalySeverity;
  status: AnomalyStatus;
  title: string;
  description: string;
  metric_name: string;
  observed_value: unknown;
  expected_value?: unknown;
  threshold?: unknown;
  z_score?: number | null;
  anomaly_score: number;
  confidence: AnomalyConfidence;
  source_record_id?: string | null;
  source_module: string;
  source_payload: Record<string, unknown>;
  suggested_action: string;
  explanation: string;
  review_history: AnomalyReviewEvent[];
  generated_by: string;
  detected_at: string;
  updated_at: string;
};

export type AnomalyScanRequest = {
  portfolio_id?: string | null;
  scan_scope: AnomalyScanScope;
  lookback_days: number;
  severity_threshold: AnomalySeverity;
  persist_results: boolean;
  language: AnomalyLanguage;
};

export type AnomalyMethodology = {
  detection_mode: string;
  score_mapping: Record<string, string>;
  factors: string[];
  data_sources: string[];
  limitations: string[];
};

export type AnomalyScanResponse = {
  scan_id: string;
  portfolio_id?: string | null;
  scan_scope: AnomalyScanScope;
  lookback_days: number;
  total_records_scanned: number;
  anomalies_detected: number;
  anomalies_by_category: Record<string, number>;
  anomalies_by_severity: Record<string, number>;
  highest_severity?: AnomalySeverity | null;
  anomaly_records: AnomalyRecord[];
  warnings: string[];
  methodology: AnomalyMethodology;
  limitations: string[];
  athena_ai_commentary?: AthenaAICommentary | null;
  generated_at: string;
};

export type AnomalyListResponse = {
  status: string;
  module: string;
  total_anomalies: number;
  items: AnomalyRecord[];
};

export type AnomalyHistoryResponse = {
  status: string;
  module: string;
  recent_count: number;
  items: AnomalyRecord[];
};

export type AnomalyReviewRequest = {
  action: AnomalyReviewAction;
  reviewer: string;
  note?: string | null;
  decision?: string | null;
};

export type AnomalyReviewResponse = {
  anomaly: AnomalyRecord;
  event: AnomalyReviewEvent;
};

export type AnomalyCsvExportResponse = {
  content_type: string;
  csv: string;
  included_tables: string[];
};
