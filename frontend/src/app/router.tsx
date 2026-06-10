import { createBrowserRouter } from "react-router-dom";

import { AppShell } from "../components/layout/AppShell";
import { AiAnomaliesPage } from "../features/ai-anomalies/pages/AiAnomaliesPage";
import { DashboardPage } from "../features/dashboard/pages/DashboardPage";
import { EquityAnalysisPage } from "../features/equity-analysis/pages/EquityAnalysisPage";
import { LimitsPage } from "../features/limits/pages/LimitsPage";
import { MarketDataPage } from "../features/market-data/pages/MarketDataPage";
import { OptionsPricingPage } from "../features/options-pricing/pages/OptionsPricingPage";
import { PnlPage } from "../features/pnl/pages/PnlPage";
import { PortfolioPage } from "../features/portfolio/pages/PortfolioPage";
import { RatesLabPage } from "../features/rates-lab/pages/RatesLabPage";
import { ReconciliationPage } from "../features/reconciliation/pages/ReconciliationPage";
import { ReportsPage } from "../features/reports/pages/ReportsPage";
import { RiskMonitorPage } from "../features/risk-monitor/pages/RiskMonitorPage";
import { SettingsPage } from "../features/settings/pages/SettingsPage";
import { StressTestingPage } from "../features/stress-testing/pages/StressTestingPage";
import { TradeSimulatorPage } from "../features/trade-simulator/pages/TradeSimulatorPage";
import { VolatilityLabPage } from "../features/volatility-lab/pages/VolatilityLabPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <AppShell />,
    children: [
      { index: true, element: <DashboardPage /> },
      { path: "dashboard", element: <DashboardPage /> },
      { path: "market-data", element: <MarketDataPage /> },
      { path: "equity-analysis", element: <EquityAnalysisPage /> },
      { path: "portfolio-builder", element: <PortfolioPage /> },
      { path: "trade-simulator", element: <TradeSimulatorPage /> },
      { path: "risk-monitor", element: <RiskMonitorPage /> },
      { path: "volatility-lab", element: <VolatilityLabPage /> },
      { path: "options-pricing-lab", element: <OptionsPricingPage /> },
      { path: "rates-lab", element: <RatesLabPage /> },
      { path: "stress-testing", element: <StressTestingPage /> },
      { path: "limit-center", element: <LimitsPage /> },
      { path: "pnl-attribution", element: <PnlPage /> },
      { path: "reconciliation", element: <ReconciliationPage /> },
      { path: "ai-anomaly-center", element: <AiAnomaliesPage /> },
      { path: "reports-center", element: <ReportsPage /> },
      { path: "settings", element: <SettingsPage /> },
    ],
  },
]);
