export type DemoLanguage = "en" | "fr";
export type DemoPersistenceStatus =
  | "persistent_history"
  | "sqlite_demo"
  | "in_memory_fallback"
  | "not_persisted";

export type DemoRunRequest = {
  portfolio_id: string;
  language: DemoLanguage;
  include_report: boolean;
};

export type DemoModuleRun = {
  module: string;
  status: "completed" | "warning" | "failed";
  detail: string;
  records_created: number;
  output_id?: string | null;
};

export type DemoPersistenceItem = {
  object_name: string;
  module: string;
  status: DemoPersistenceStatus;
  storage: string;
  notes: string;
};

export type DemoWorkflowStatus = {
  status: string;
  module: string;
  detail: string;
  demo_portfolio_id: string;
  active_modules: number;
  database_connected: boolean;
  persistence: DemoPersistenceItem[];
  endpoints: string[];
  limitations: string[];
};

export type DemoRunSummary = {
  demo_run_id: string;
  portfolio_id: string;
  portfolio_name?: string | null;
  modules_run: string[];
  module_results: DemoModuleRun[];
  records_created: Record<string, number>;
  warnings: string[];
  generated_report_id?: string | null;
  highest_risk_status?: string | null;
  open_breaks?: number | null;
  limit_breaches?: number | null;
  anomalies_detected?: number | null;
  total_pnl?: number | null;
  risk_score?: number | null;
  quick_links: Record<string, string>;
  persistence: DemoPersistenceItem[];
  generated_at: string;
};

export type DemoRunHistoryResponse = {
  status: string;
  module: string;
  total_runs: number;
  items: DemoRunSummary[];
};
