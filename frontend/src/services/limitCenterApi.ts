import { apiClient } from "../lib/api-client";
import { endpoints } from "../lib/endpoints";
import type {
  BreachListResponse,
  BreachReviewRequest,
  BreachReviewResponse,
  LimitBreach,
  LimitCenterStatus,
  LimitEvaluationRequest,
  LimitEvaluationResponse,
  LimitRule,
  LimitRuleCreate,
  LimitRuleListResponse,
  LimitRuleUpdate,
  SourceModuleCard,
} from "../types/limit-center";

export const limitCenterApi = {
  status() {
    return apiClient.get<LimitCenterStatus>(endpoints.limitCenterStatus);
  },
  rules() {
    return apiClient.get<LimitRuleListResponse>(endpoints.limitCenterRules);
  },
  createRule(payload: LimitRuleCreate) {
    return apiClient.post<LimitRule>(endpoints.limitCenterRules, payload);
  },
  updateRule(ruleId: string, payload: LimitRuleUpdate) {
    return apiClient.put<LimitRule>(endpoints.limitCenterRule(ruleId), payload);
  },
  deleteRule(ruleId: string) {
    return apiClient.delete<{ deleted: boolean }>(endpoints.limitCenterRule(ruleId));
  },
  evaluate(payload: LimitEvaluationRequest) {
    return apiClient.post<LimitEvaluationResponse>(
      endpoints.limitCenterEvaluate,
      payload,
    );
  },
  breaches() {
    return apiClient.get<BreachListResponse>(endpoints.limitCenterBreaches);
  },
  breach(breachId: string) {
    return apiClient.get<LimitBreach>(endpoints.limitCenterBreach(breachId));
  },
  reviewBreach(breachId: string, payload: BreachReviewRequest) {
    return apiClient.post<BreachReviewResponse>(
      endpoints.limitCenterBreachReview(breachId),
      payload,
    );
  },
  sourceModules() {
    return apiClient.get<SourceModuleCard[]>(endpoints.limitCenterSourceModules);
  },
  demo() {
    return apiClient.get<LimitEvaluationResponse>(endpoints.limitCenterDemo);
  },
};
