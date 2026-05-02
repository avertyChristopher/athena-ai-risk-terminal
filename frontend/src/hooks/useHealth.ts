import { useQuery } from "@tanstack/react-query";

import { apiClient } from "../lib/api-client";
import { endpoints } from "../lib/endpoints";

export type HealthResponse = {
  status: string;
  service: string;
};

export function useHealth() {
  return useQuery({
    queryKey: ["health"],
    queryFn: () => apiClient.get<HealthResponse>(endpoints.health),
  });
}
