import type { AthenaAICommentary } from "./athena-intelligence";

export type TradeBlotterAction = "BUY" | "SELL" | "SHORT" | "COVER" | "OPTION" | "BOND";
export type TradeBlotterStatusValue =
  | "draft"
  | "pending_review"
  | "approved"
  | "rejected"
  | "simulated"
  | "cancelled";
export type TradeReviewAction =
  | "submit_for_review"
  | "approve"
  | "reject"
  | "simulate"
  | "cancel"
  | "reopen";

export type TradeBlotterStatus = {
  status: string;
  module: string;
  detail: string;
  persistence_enabled: boolean;
  entries_count: number;
  review_workflow_enabled: boolean;
  source_modules: string[];
};

export type TradeReviewEvent = {
  action: TradeReviewAction;
  from_status: TradeBlotterStatusValue;
  to_status: TradeBlotterStatusValue;
  reviewer: string;
  note: string | null;
  timestamp: string;
};

export type TradeBlotterEntry = {
  trade_id: string;
  portfolio_id: string;
  symbol: string;
  action: TradeBlotterAction;
  quantity: number;
  price: number;
  estimated_trade_value: number;
  currency: string;
  status: TradeBlotterStatusValue;
  trade_date: string;
  settlement_date: string | null;
  source_module: string;
  cost_estimate: number;
  slippage_estimate: number;
  suitability_status: string | null;
  constraint_status: string | null;
  risk_summary: Record<string, unknown>;
  source_payload: Record<string, unknown>;
  review_history: TradeReviewEvent[];
  athena_ai_commentary?: AthenaAICommentary | Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
  reviewed_by: string | null;
  review_note: string | null;
};

export type TradeBlotterEntryCreate = {
  portfolio_id: string;
  symbol: string;
  action: TradeBlotterAction;
  quantity: number;
  price: number;
  currency?: string;
  status?: TradeBlotterStatusValue;
  trade_date?: string;
  settlement_date?: string | null;
  source_module?: string;
  cost_estimate?: number;
  slippage_estimate?: number;
  suitability_status?: string | null;
  constraint_status?: string | null;
  risk_summary?: Record<string, unknown>;
  source_payload?: Record<string, unknown>;
};

export type TradeBlotterEntryUpdate = Partial<TradeBlotterEntryCreate>;

export type TradeBlotterReviewRequest = {
  action: TradeReviewAction;
  reviewer: string;
  note?: string | null;
};

export type TradeBlotterListResponse = {
  status: string;
  module: string;
  total_entries: number;
  entries: TradeBlotterEntry[];
};

export type TradeBlotterReviewResponse = {
  entry: TradeBlotterEntry;
  event: TradeReviewEvent;
};

export type TradeBlotterDemoResponse = {
  status: string;
  module: string;
  entries: TradeBlotterEntry[];
};
