import { createBrowserRouter } from "react-router-dom";
import { Suspense, lazy } from "react";
import type { ReactNode } from "react";

import { AppShell } from "../components/layout/AppShell";
import { LoadingState } from "../components/ui/LoadingState";

const DashboardPage = lazy(() =>
  import("../features/dashboard/pages/DashboardPage").then((module) => ({
    default: module.DashboardPage,
  })),
);
const ArchitecturePage = lazy(() =>
  import("../features/architecture/pages/ArchitecturePage").then((module) => ({
    default: module.ArchitecturePage,
  })),
);
const MarketDataPage = lazy(() =>
  import("../features/market-data/pages/MarketDataPage").then((module) => ({
    default: module.MarketDataPage,
  })),
);
const EquityAnalysisPage = lazy(() =>
  import("../features/equity-analysis/pages/EquityAnalysisPage").then((module) => ({
    default: module.EquityAnalysisPage,
  })),
);
const PortfolioPage = lazy(() =>
  import("../features/portfolio/pages/PortfolioPage").then((module) => ({
    default: module.PortfolioPage,
  })),
);
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
const TradeBlotterPage = lazy(() =>
  import("../features/trade-blotter/pages/TradeBlotterPage").then((module) => ({
    default: module.TradeBlotterPage,
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
const ReportsCenterPage = lazy(() =>
  import("../features/reports-center/pages/ReportsCenterPage").then((module) => ({
    default: module.ReportsCenterPage,
  })),
);
const PnlAttributionPage = lazy(() =>
  import("../features/pnl-attribution/pages/PnlAttributionPage").then((module) => ({
    default: module.PnlAttributionPage,
  })),
);
const ReconciliationPage = lazy(() =>
  import("../features/reconciliation/pages/ReconciliationPage").then((module) => ({
    default: module.ReconciliationPage,
  })),
);
const AIAnomalyCenterPage = lazy(() =>
  import("../features/ai-anomaly-center/pages/AIAnomalyCenterPage").then((module) => ({
    default: module.AIAnomalyCenterPage,
  })),
);
const SettingsPage = lazy(() =>
  import("../features/settings/pages/SettingsPage").then((module) => ({
    default: module.SettingsPage,
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
      { index: true, element: lazyRoute(<DashboardPage />) },
      { path: "dashboard", element: lazyRoute(<DashboardPage />) },
      { path: "architecture", element: lazyRoute(<ArchitecturePage />) },
      { path: "market-data", element: lazyRoute(<MarketDataPage />) },
      { path: "equity-analysis", element: lazyRoute(<EquityAnalysisPage />) },
      { path: "portfolio-builder", element: lazyRoute(<PortfolioPage />) },
      { path: "trade-simulator", element: lazyRoute(<TradeSimulatorPage />) },
      { path: "trade-blotter", element: lazyRoute(<TradeBlotterPage />) },
      { path: "risk-monitor", element: lazyRoute(<RiskMonitorPage />) },
      { path: "volatility-lab", element: lazyRoute(<VolatilityLabPage />) },
      { path: "options-pricing-lab", element: lazyRoute(<OptionsPricingPage />) },
      { path: "rates-lab", element: lazyRoute(<RatesLabPage />) },
      { path: "stress-testing", element: lazyRoute(<StressTestingPage />) },
      { path: "limit-center", element: lazyRoute(<LimitCenterPage />) },
      { path: "pnl-attribution", element: lazyRoute(<PnlAttributionPage />) },
      { path: "reconciliation", element: lazyRoute(<ReconciliationPage />) },
      { path: "ai-anomaly-center", element: lazyRoute(<AIAnomalyCenterPage />) },
      { path: "reports-center", element: lazyRoute(<ReportsCenterPage />) },
      { path: "settings", element: lazyRoute(<SettingsPage />) },
    ],
  },
]);
