export type NavigationItem = {
  path: string;
  labelKey: string;
};

export const navigationItems: NavigationItem[] = [
  { path: "/", labelKey: "nav.dashboard" },
  { path: "/market-data", labelKey: "nav.marketData" },
  { path: "/equity-analysis", labelKey: "nav.equityAnalysis" },
  { path: "/portfolio-builder", labelKey: "nav.portfolioBuilder" },
  { path: "/trade-simulator", labelKey: "nav.tradeSimulator" },
  { path: "/trade-blotter", labelKey: "nav.tradeBlotter" },
  { path: "/risk-monitor", labelKey: "nav.riskMonitor" },
  { path: "/volatility-lab", labelKey: "nav.volatilityLab" },
  { path: "/options-pricing-lab", labelKey: "nav.optionsPricingLab" },
  { path: "/rates-lab", labelKey: "nav.ratesLab" },
  { path: "/stress-testing", labelKey: "nav.stressTesting" },
  { path: "/limit-center", labelKey: "nav.limitCenter" },
  { path: "/pnl-attribution", labelKey: "nav.pnlAttribution" },
  { path: "/reconciliation", labelKey: "nav.reconciliation" },
  { path: "/ai-anomaly-center", labelKey: "nav.aiAnomalyCenter" },
  { path: "/reports-center", labelKey: "nav.reportsCenter" },
  { path: "/settings", labelKey: "nav.settings" }
];
