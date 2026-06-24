import { apiClient } from "../lib/api-client";
import { endpoints } from "../lib/endpoints";
import type {
  AthenaAICommentary,
  AthenaIntelligenceRequest,
  AthenaIntelligenceStatus,
} from "../types/athena-intelligence";

export const athenaIntelligenceApi = {
  status() {
    return apiClient.get<AthenaIntelligenceStatus>(
      endpoints.athenaIntelligenceStatus,
    );
  },
  commentary(payload: AthenaIntelligenceRequest) {
    return apiClient.post<AthenaAICommentary>(
      endpoints.athenaIntelligenceCommentary,
      payload,
    );
  },
  demo() {
    return apiClient.get<AthenaAICommentary>(endpoints.athenaIntelligenceDemo);
  },
};
