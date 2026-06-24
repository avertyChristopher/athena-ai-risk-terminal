import { createBrowserRouter } from "react-router-dom";
import { Suspense, lazy } from "react";
import type { ReactNode } from "react";

import { AppShell } from "../components/layout/AppShell";
import { LoadingState } from "../components/ui/LoadingState";
import { AiAnomaliesPage } from "../features/ai-anomalies/pages/AiAnomaliesPage";
import { DashboardPage } from "../features/dashboard/pages/DashboardPage";
import { EquityAnalysisPage } from "../features/equity-analysis/pages/EquityAnalysisPage";
import { MarketDataPage } from "../features/market-data/pages/MarketDataPage";
import { PnlPage } from "../features/pnl/pages/PnlPage";
import { PortfolioPage } from "../features/portfolio/pages/PortfolioPage";
import { ReconciliationPage } from "../features/reconciliation/pages/ReconciliationPage";
import { ReportsPage } from "../features/reports/pages/ReportsPage";
import { SettingsPage } from "../features/settings/pages/SettingsPage";

const RiskMonitorPage = lazy(() =>
  import("../features/risk-monitor/pages/RiskMonitorPage").then((module) => ({
    default: module.RiskMonitorPage,
  })),
);
const TradeSimulatorPage = lazy(() =>
  import("../features/trade-simulator/pages/TradeSimulatorPage").then((module) => ({
    default: module.TradeSimulatorPage,
  })),
);
const VolatilityLabPage = lazy(() =>
  import("../features/volatility-lab/pages/VolatilityLabPage").then((module) => ({
    default: module.VolatilityLabPage,
  })),
);
const OptionsPricingPage = lazy(() =>
  import("../features/options-pricing/pages/OptionsPricingPage").then((module) => ({
    default: module.OptionsPricingPage,
  })),
);
const RatesLabPage = lazy(() =>
  import("../features/rates-lab/pages/RatesLabPage").then((module) => ({
    default: module.RatesLabPage,
  })),
);
const StressTestingPage = lazy(() =>
  import("../features/stress-testing/pages/StressTestingPage").then((module) => ({
    default: module.StressTestingPage,
  })),
);
const LimitCenterPage = lazy(() =>
  import("../features/limit-center/pages/LimitCenterPage").then((module) => ({
    default: module.LimitCenterPage,
  })),
);

function lazyRoute(element: ReactNode) {
  return (
    <Suspense fallback={<LoadingState label="Loading" />}>
      {element}
    </Suspense>
  );
}

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
      { path: "trade-simulator", element: lazyRoute(<TradeSimulatorPage />) },
      { path: "risk-monitor", element: lazyRoute(<RiskMonitorPage />) },
      { path: "volatility-lab", element: lazyRoute(<VolatilityLabPage />) },
      { path: "options-pricing-lab", element: lazyRoute(<OptionsPricingPage />) },
      { path: "rates-lab", element: lazyRoute(<RatesLabPage />) },
      { path: "stress-testing", element: lazyRoute(<StressTestingPage />) },
      { path: "limit-center", element: lazyRoute(<LimitCenterPage />) },
      { path: "pnl-attribution", element: <PnlPage /> },
      { path: "reconciliation", element: <ReconciliationPage /> },
      { path: "ai-anomaly-center", element: <AiAnomaliesPage /> },
      { path: "reports-center", element: <ReportsPage /> },
      { path: "settings", element: <SettingsPage /> },
    ],
  },
]);
