import { useEffect, useState } from "react";

export type VolatilityAnalysisMode = "asset" | "portfolio";
export type VolatilityVarMethod = "historical" | "parametric" | "monte_carlo";

export type VolatilityLabPreferences = {
  analysisMode: VolatilityAnalysisMode;
  selectedSymbol: string;
  selectedPortfolioId: string;
  benchmarkSymbol: string;
  rollingWindow: number;
  confidenceLevel: number;
  riskFreeRate: number;
  startDate: string;
  endDate: string;
  selectedVarMethod: VolatilityVarMethod;
};

const STORAGE_KEY = "athena.volatilityLab.preferences";

export const defaultVolatilityLabPreferences: VolatilityLabPreferences = {
  analysisMode: "portfolio",
  selectedSymbol: "AAPL",
  selectedPortfolioId: "",
  benchmarkSymbol: "SPY",
  rollingWindow: 20,
  confidenceLevel: 0.95,
  riskFreeRate: 0.02,
  startDate: "",
  endDate: "",
  selectedVarMethod: "historical",
};

export function useVolatilityLabPreferences() {
  const [preferences, setPreferences] = useState<VolatilityLabPreferences>(() =>
    readPreferences(),
  );

  useEffect(() => {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(preferences));
  }, [preferences]);

  function updatePreference<Key extends keyof VolatilityLabPreferences>(
    key: Key,
    value: VolatilityLabPreferences[Key],
  ) {
    setPreferences((current) => ({ ...current, [key]: value }));
  }

  function updatePreferences(nextPreferences: Partial<VolatilityLabPreferences>) {
    setPreferences((current) => ({ ...current, ...nextPreferences }));
  }

  function resetPreferences() {
    setPreferences(defaultVolatilityLabPreferences);
  }

  return {
    preferences,
    updatePreference,
    updatePreferences,
    resetPreferences,
  };
}

function readPreferences(): VolatilityLabPreferences {
  if (typeof window === "undefined") {
    return defaultVolatilityLabPreferences;
  }

  try {
    const stored = window.localStorage.getItem(STORAGE_KEY);
    if (!stored) {
      return defaultVolatilityLabPreferences;
    }
    return {
      ...defaultVolatilityLabPreferences,
      ...JSON.parse(stored),
    };
  } catch {
    return defaultVolatilityLabPreferences;
  }
}
