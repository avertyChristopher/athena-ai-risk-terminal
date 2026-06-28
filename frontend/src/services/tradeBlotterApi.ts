import { apiClient } from "../lib/api-client";
import { endpoints } from "../lib/endpoints";
import type {
  TradeBlotterDemoResponse,
  TradeBlotterEntry,
  TradeBlotterEntryCreate,
  TradeBlotterEntryUpdate,
  TradeBlotterListResponse,
  TradeBlotterReviewRequest,
  TradeBlotterReviewResponse,
  TradeBlotterStatus,
} from "../types/trade-blotter";

export const tradeBlotterApi = {
  status() {
    return apiClient.get<TradeBlotterStatus>(endpoints.tradeBlotterStatus);
  },
  list(params?: { portfolio_id?: string; symbol?: string; status?: string }) {
    const query = new URLSearchParams();
    if (params?.portfolio_id) query.set("portfolio_id", params.portfolio_id);
    if (params?.symbol) query.set("symbol", params.symbol);
    if (params?.status) query.set("status", params.status);
    const suffix = query.toString() ? `?${query.toString()}` : "";
    return apiClient.get<TradeBlotterListResponse>(`${endpoints.tradeBlotterTrades}${suffix}`);
  },
  create(payload: TradeBlotterEntryCreate) {
    return apiClient.post<TradeBlotterEntry>(endpoints.tradeBlotterTrades, payload);
  },
  update(tradeId: string, payload: TradeBlotterEntryUpdate) {
    return apiClient.put<TradeBlotterEntry>(endpoints.tradeBlotterTrade(tradeId), payload);
  },
  review(tradeId: string, payload: TradeBlotterReviewRequest) {
    return apiClient.post<TradeBlotterReviewResponse>(endpoints.tradeBlotterReview(tradeId), payload);
  },
  delete(tradeId: string) {
    return apiClient.delete<{ deleted: boolean; trade_id: string }>(endpoints.tradeBlotterTrade(tradeId));
  },
  demo() {
    return apiClient.get<TradeBlotterDemoResponse>(endpoints.tradeBlotterDemo);
  },
};
