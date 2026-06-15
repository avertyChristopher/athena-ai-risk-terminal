import { useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { PageHeader } from "../../../components/layout/PageHeader";
import { EmptyState } from "../../../components/ui/EmptyState";
import { LoadingState } from "../../../components/ui/LoadingState";
import { MoneyValue } from "../../../components/finance/MoneyValue";
import { PercentValue } from "../../../components/finance/PercentValue";
import { apiClient } from "../../../lib/api-client";
import { endpoints } from "../../../lib/endpoints";
import { useTranslation } from "../../../hooks/useTranslation";
import {
  AllocationResponse,
  BenchmarkResponse,
  CfaConceptsResponse,
  ConcentrationResponse,
  ConstraintsResponse,
  PerformanceMeasurementResponse,
  PortfolioCreate,
  PortfolioDiagnosticsResponse,
  PortfolioListResponse,
  PortfolioMarketDataIntegrationResponse,
  PortfolioRead,
  PortfolioSummary,
  PolicyResponse,
  PositionCreate,
  PositionListResponse,
  RebalancingPreviewResponse,
  RiskReturnResponse,
  TargetAllocationResponse,
} from "../../../types/portfolio";
import { AddPositionModal } from "../components/AddPositionModal";
import { AllocationChart } from "../components/AllocationChart";
import { PortfolioDetailsPanel } from "../components/PortfolioDetailsPanel";
import { PortfolioDiagnosticsPanel } from "../components/PortfolioDiagnosticsPanel";
import { PortfolioForm } from "../components/PortfolioForm";
import { PortfolioMetricCard } from "../components/PortfolioMetricCard";
import { PortfolioSectionCard } from "../components/PortfolioSectionCard";
import { PortfolioSelector } from "../components/PortfolioSelector";
import { PortfolioStatusBadge } from "../components/PortfolioStatusBadge";
import { PortfolioSummaryCards } from "../components/PortfolioSummaryCards";
import { PortfolioTabNavigation } from "../components/PortfolioTabNavigation";
import type { PortfolioTab } from "../components/PortfolioTabNavigation";
import { PortfolioWarningCard } from "../components/PortfolioWarningCard";
import { PositionTable } from "../components/PositionTable";
import { RebalancingPreviewTable } from "../components/RebalancingPreviewTable";

type PortfolioTabId =
  | "overview"
  | "positions"
  | "allocation"
  | "risk"
  | "policy"
  | "rebalancing"
  | "performance"
  | "diagnostics";

type SimpleRow = {
  label: string;
  value: ReactNode;
};

export function PortfolioPage() {
  const { t } = useTranslation();
  const queryClient = useQueryClient();
  const [selectedPortfolioId, setSelectedPortfolioId] = useState("");
  const [activeTab, setActiveTab] = useState<PortfolioTabId>("overview");
  const [isAddPositionOpen, setIsAddPositionOpen] = useState(false);

  const portfoliosQuery = useQuery({
    queryKey: ["portfolios"],
    queryFn: () => apiClient.get<PortfolioListResponse>(endpoints.portfolios),
  });

  const portfolios = portfoliosQuery.data?.items ?? [];

  useEffect(() => {
    if (!selectedPortfolioId && portfolios.length > 0) {
      setSelectedPortfolioId(portfolios[0].id);
    }
  }, [portfolios, selectedPortfolioId]);

  const selectedPortfolio = useMemo(
    () =>
      portfolios.find((portfolio) => portfolio.id === selectedPortfolioId) ??
      portfolios[0],
    [portfolios, selectedPortfolioId],
  );

  const summaryQuery = useQuery({
    queryKey: ["portfolio-summary", selectedPortfolio?.id],
    enabled: Boolean(selectedPortfolio?.id),
    queryFn: () =>
      apiClient.get<PortfolioSummary>(
        endpoints.portfolioSummary(selectedPortfolio?.id ?? ""),
      ),
  });

  const positionsQuery = useQuery({
    queryKey: ["portfolio-positions", selectedPortfolio?.id],
    enabled: Boolean(selectedPortfolio?.id),
    queryFn: () =>
      apiClient.get<PositionListResponse>(
        endpoints.portfolioPositions(selectedPortfolio?.id ?? ""),
      ),
  });

  const assetAllocationQuery = useQuery({
    queryKey: ["portfolio-asset-allocation", selectedPortfolio?.id],
    enabled: Boolean(selectedPortfolio?.id),
    queryFn: () =>
      apiClient.get<AllocationResponse>(
        endpoints.portfolioAssetAllocation(selectedPortfolio?.id ?? ""),
      ),
  });

  const sectorAllocationQuery = useQuery({
    queryKey: ["portfolio-sector-allocation", selectedPortfolio?.id],
    enabled: Boolean(selectedPortfolio?.id),
    queryFn: () =>
      apiClient.get<AllocationResponse>(
        endpoints.portfolioSectorAllocation(selectedPortfolio?.id ?? ""),
      ),
  });

  const currencyAllocationQuery = useQuery({
    queryKey: ["portfolio-currency-allocation", selectedPortfolio?.id],
    enabled: Boolean(selectedPortfolio?.id),
    queryFn: () =>
      apiClient.get<AllocationResponse>(
        endpoints.portfolioCurrencyAllocation(selectedPortfolio?.id ?? ""),
      ),
  });

  const assetTypeAllocationQuery = useQuery({
    queryKey: ["portfolio-asset-type-allocation", selectedPortfolio?.id],
    enabled: Boolean(selectedPortfolio?.id),
    queryFn: () =>
      apiClient.get<AllocationResponse>(
        endpoints.portfolioAssetTypeAllocation(selectedPortfolio?.id ?? ""),
      ),
  });

  const concentrationQuery = useQuery({
    queryKey: ["portfolio-concentration", selectedPortfolio?.id],
    enabled: Boolean(selectedPortfolio?.id),
    queryFn: () =>
      apiClient.get<ConcentrationResponse>(
        endpoints.portfolioConcentration(selectedPortfolio?.id ?? ""),
      ),
  });

  const riskReturnQuery = useQuery({
    queryKey: ["portfolio-risk-return", selectedPortfolio?.id],
    enabled: Boolean(selectedPortfolio?.id),
    queryFn: () =>
      apiClient.get<RiskReturnResponse>(
        endpoints.portfolioRiskReturn(selectedPortfolio?.id ?? ""),
      ),
  });

  const benchmarkQuery = useQuery({
    queryKey: ["portfolio-benchmark", selectedPortfolio?.id],
    enabled: Boolean(selectedPortfolio?.id),
    queryFn: () =>
      apiClient.get<BenchmarkResponse>(
        endpoints.portfolioBenchmark(selectedPortfolio?.id ?? ""),
      ),
  });

  const policyQuery = useQuery({
    queryKey: ["portfolio-policy", selectedPortfolio?.id],
    enabled: Boolean(selectedPortfolio?.id),
    queryFn: () =>
      apiClient.get<PolicyResponse>(
        endpoints.portfolioPolicy(selectedPortfolio?.id ?? ""),
      ),
  });

  const targetAllocationQuery = useQuery({
    queryKey: ["portfolio-target-allocation", selectedPortfolio?.id],
    enabled: Boolean(selectedPortfolio?.id),
    queryFn: () =>
      apiClient.get<TargetAllocationResponse>(
        endpoints.portfolioTargetAllocation(selectedPortfolio?.id ?? ""),
      ),
  });

  const rebalancingQuery = useQuery({
    queryKey: ["portfolio-rebalancing", selectedPortfolio?.id],
    enabled: Boolean(selectedPortfolio?.id),
    queryFn: () =>
      apiClient.get<RebalancingPreviewResponse>(
        endpoints.portfolioRebalancingPreview(selectedPortfolio?.id ?? ""),
      ),
  });

  const performanceQuery = useQuery({
    queryKey: ["portfolio-performance", selectedPortfolio?.id],
    enabled: Boolean(selectedPortfolio?.id),
    queryFn: () =>
      apiClient.get<PerformanceMeasurementResponse>(
        endpoints.portfolioPerformanceMeasurement(selectedPortfolio?.id ?? ""),
      ),
  });

  const constraintsQuery = useQuery({
    queryKey: ["portfolio-constraints", selectedPortfolio?.id],
    enabled: Boolean(selectedPortfolio?.id),
    queryFn: () =>
      apiClient.get<ConstraintsResponse>(
        endpoints.portfolioConstraints(selectedPortfolio?.id ?? ""),
      ),
  });

  const diagnosticsQuery = useQuery({
    queryKey: ["portfolio-diagnostics", selectedPortfolio?.id],
    enabled: Boolean(selectedPortfolio?.id),
    queryFn: () =>
      apiClient.get<PortfolioDiagnosticsResponse>(
        endpoints.portfolioDiagnostics(selectedPortfolio?.id ?? ""),
      ),
  });

  const marketDataIntegrationQuery = useQuery({
    queryKey: ["portfolio-market-data-integration", selectedPortfolio?.id],
    enabled: Boolean(selectedPortfolio?.id),
    queryFn: () =>
      apiClient.get<PortfolioMarketDataIntegrationResponse>(
        endpoints.portfolioMarketDataIntegration(selectedPortfolio?.id ?? ""),
      ),
  });

  const cfaConceptsQuery = useQuery({
    queryKey: ["portfolio-cfa-concepts", selectedPortfolio?.id],
    enabled: Boolean(selectedPortfolio?.id),
    queryFn: () =>
      apiClient.get<CfaConceptsResponse>(
        endpoints.portfolioCfaConcepts(selectedPortfolio?.id ?? ""),
      ),
  });

  const createPortfolioMutation = useMutation({
    mutationFn: (payload: PortfolioCreate) =>
      apiClient.post<PortfolioRead>(endpoints.portfolios, payload),
    onSuccess: (portfolio) => {
      queryClient.invalidateQueries({ queryKey: ["portfolios"] });
      setSelectedPortfolioId(portfolio.id);
      setActiveTab("overview");
    },
  });

  const createPositionMutation = useMutation({
    mutationFn: (payload: PositionCreate) =>
      apiClient.post(
        endpoints.portfolioPositions(selectedPortfolio?.id ?? ""),
        payload,
      ),
    onSuccess: () => {
      setIsAddPositionOpen(false);
      invalidatePortfolioQueries();
    },
  });

  const deletePositionMutation = useMutation({
    mutationFn: (positionId: string) =>
      apiClient.delete(
        endpoints.portfolioPosition(selectedPortfolio?.id ?? "", positionId),
      ),
    onSuccess: () => invalidatePortfolioQueries(),
  });

  function invalidatePortfolioQueries() {
    [
      "portfolio-summary",
      "portfolio-positions",
      "portfolio-asset-allocation",
      "portfolio-sector-allocation",
      "portfolio-currency-allocation",
      "portfolio-asset-type-allocation",
      "portfolio-concentration",
      "portfolio-risk-return",
      "portfolio-benchmark",
      "portfolio-policy",
      "portfolio-target-allocation",
      "portfolio-rebalancing",
      "portfolio-performance",
      "portfolio-constraints",
      "portfolio-diagnostics",
      "portfolio-market-data-integration",
      "portfolio-cfa-concepts",
    ].forEach((queryKey) => {
      queryClient.invalidateQueries({ queryKey: [queryKey] });
    });
  }

  const tabs: PortfolioTab[] = [
    {
      id: "overview",
      label: t("portfolio.tabs.overview"),
      description: t("portfolio.tabs.overviewShort"),
    },
    {
      id: "positions",
      label: t("portfolio.tabs.positions"),
      description: t("portfolio.tabs.positionsShort"),
    },
    {
      id: "allocation",
      label: t("portfolio.tabs.allocation"),
      description: t("portfolio.tabs.allocationShort"),
    },
    {
      id: "risk",
      label: t("portfolio.tabs.risk"),
      description: t("portfolio.tabs.riskShort"),
    },
    {
      id: "policy",
      label: t("portfolio.tabs.policy"),
      description: t("portfolio.tabs.policyShort"),
    },
    {
      id: "rebalancing",
      label: t("portfolio.tabs.rebalancing"),
      description: t("portfolio.tabs.rebalancingShort"),
    },
    {
      id: "performance",
      label: t("portfolio.tabs.performance"),
      description: t("portfolio.tabs.performanceShort"),
    },
    {
      id: "diagnostics",
      label: t("portfolio.tabs.diagnostics"),
      description: t("portfolio.tabs.diagnosticsShort"),
    },
  ];

  const isLoading = portfoliosQuery.isLoading || summaryQuery.isLoading;
  const summary = summaryQuery.data;
  const positions = positionsQuery.data?.items ?? [];
  const baseCurrency = summary?.base_currency ?? selectedPortfolio?.base_currency ?? "USD";

  return (
    <div className="page portfolio-page">
      <PageHeader
        title={t("portfolio.title")}
        subtitle={t("portfolio.subtitle")}
      />

      <section className="portfolio-command-panel">
        <div className="portfolio-command-panel__copy">
          <span>{t("portfolio.workbench.eyebrow")}</span>
          <h2>{t("portfolio.workbench.title")}</h2>
          <p>{t("portfolio.workbench.description")}</p>
        </div>
        <div className="portfolio-command-panel__controls">
          {selectedPortfolio ? (
            <PortfolioSelector
              portfolios={portfolios}
              selectedPortfolioId={selectedPortfolio.id}
              onSelect={(portfolioId) => {
                setSelectedPortfolioId(portfolioId);
                setActiveTab("overview");
              }}
              label={t("portfolio.selector")}
            />
          ) : null}
          <div className="portfolio-badge-cluster">
            <PortfolioStatusBadge label={t("portfolio.badges.demo")} variant="info" />
            <PortfolioStatusBadge
              label={t("portfolio.badges.inMemoryStore")}
              variant="warning"
            />
            <PortfolioStatusBadge
              label={t("portfolio.badges.marketDataBridge")}
              variant="success"
            />
          </div>
        </div>
      </section>

      <div className="portfolio-setup-grid">
        <PortfolioForm
          labels={{
            title: t("portfolio.form.title"),
            name: t("portfolio.form.name"),
            currency: t("portfolio.form.currency"),
            benchmark: t("portfolio.form.benchmark"),
            cash: t("portfolio.form.cash"),
            create: t("portfolio.form.create"),
          }}
          onCreate={(payload) => createPortfolioMutation.mutate(payload)}
        />

        {selectedPortfolio ? (
          <PortfolioDetailsPanel
            portfolio={selectedPortfolio}
            labels={{
              title: t("portfolio.details.title"),
              name: t("portfolio.form.name"),
              currency: t("portfolio.form.currency"),
              benchmark: t("portfolio.form.benchmark"),
            }}
          />
        ) : null}
      </div>

      {isLoading ? <LoadingState label={t("common.loading")} /> : null}

      {!selectedPortfolio && !isLoading ? (
        <EmptyState
          title={t("portfolio.empty.title")}
          message={t("portfolio.empty.message")}
        />
      ) : null}

      {selectedPortfolio ? (
        <>
          <PortfolioTabNavigation
            tabs={tabs}
            activeTab={activeTab}
            onTabChange={(tabId) => setActiveTab(tabId as PortfolioTabId)}
          />

          <div className="portfolio-tab-panel">
            {activeTab === "overview" ? (
              <OverviewTab
                baseCurrency={baseCurrency}
                concentration={concentrationQuery.data}
                marketDataIntegration={marketDataIntegrationQuery.data}
                riskReturn={riskReturnQuery.data}
                summary={summary}
                t={t}
              />
            ) : null}

            {activeTab === "positions" ? (
              <PositionTable
                positions={positions}
                onAddClick={() => setIsAddPositionOpen(true)}
                onDelete={(positionId) =>
                  deletePositionMutation.mutate(positionId)
                }
                labels={{
                  title: t("portfolio.positions.title"),
                  add: t("portfolio.positions.add"),
                  symbol: t("portfolio.positions.symbol"),
                  name: t("portfolio.positions.name"),
                  type: t("portfolio.positions.type"),
                  quantity: t("portfolio.positions.quantity"),
                  averagePrice: t("portfolio.positions.averagePrice"),
                  currentPrice: t("portfolio.positions.currentPrice"),
                  marketValue: t("portfolio.positions.marketValue"),
                  weight: t("portfolio.positions.weight"),
                  portfolioWeight: t("portfolio.positions.portfolioWeight"),
                  investedWeight: t("portfolio.positions.investedWeight"),
                  costBasis: t("portfolio.positions.costBasis"),
                  unrealizedPnl: t("portfolio.positions.unrealizedPnl"),
                  currency: t("portfolio.positions.currency"),
                  sector: t("portfolio.positions.sector"),
                  country: t("portfolio.positions.country"),
                  actions: t("portfolio.positions.actions"),
                  delete: t("portfolio.positions.delete"),
                  emptyTitle: t("portfolio.positions.emptyTitle"),
                  emptyMessage: t("portfolio.positions.emptyMessage"),
                }}
              />
            ) : null}

            {activeTab === "allocation" ? (
              <AllocationTab
                assetAllocation={assetAllocationQuery.data}
                assetTypeAllocation={assetTypeAllocationQuery.data}
                baseCurrency={baseCurrency}
                currencyAllocation={currencyAllocationQuery.data}
                sectorAllocation={sectorAllocationQuery.data}
                t={t}
              />
            ) : null}

            {activeTab === "risk" ? (
              <RiskTab
                baseCurrency={baseCurrency}
                concentration={concentrationQuery.data}
                constraints={constraintsQuery.data}
                marketDataIntegration={marketDataIntegrationQuery.data}
                riskReturn={riskReturnQuery.data}
                t={t}
              />
            ) : null}

            {activeTab === "policy" ? (
              <PolicyTab
                cfaConcepts={cfaConceptsQuery.data}
                constraints={constraintsQuery.data}
                policy={policyQuery.data}
                t={t}
              />
            ) : null}

            {activeTab === "rebalancing" ? (
              <RebalancingTab
                baseCurrency={baseCurrency}
                rebalancing={rebalancingQuery.data}
                targetAllocation={targetAllocationQuery.data}
                t={t}
              />
            ) : null}

            {activeTab === "performance" ? (
              <PerformanceTab
                baseCurrency={baseCurrency}
                cfaConcepts={cfaConceptsQuery.data}
                performance={performanceQuery.data}
                t={t}
              />
            ) : null}

            {activeTab === "diagnostics" ? (
              <DiagnosticsTab
                benchmark={benchmarkQuery.data}
                cfaConcepts={cfaConceptsQuery.data}
                diagnostics={diagnosticsQuery.data}
                marketDataIntegration={marketDataIntegrationQuery.data}
                t={t}
              />
            ) : null}
          </div>
        </>
      ) : null}

      <AddPositionModal
        isOpen={isAddPositionOpen}
        onClose={() => setIsAddPositionOpen(false)}
        onCreate={(payload) => createPositionMutation.mutate(payload)}
        labels={{
          title: t("portfolio.addPosition.title"),
          symbol: t("portfolio.positions.symbol"),
          name: t("portfolio.positions.name"),
          type: t("portfolio.positions.type"),
          quantity: t("portfolio.positions.quantity"),
          averagePrice: t("portfolio.positions.averagePrice"),
          currentPrice: t("portfolio.positions.currentPrice"),
          currency: t("portfolio.positions.currency"),
          sector: t("portfolio.positions.sector"),
          country: t("portfolio.positions.country"),
          cancel: t("portfolio.addPosition.cancel"),
          add: t("portfolio.addPosition.add"),
        }}
      />
    </div>
  );
}

function OverviewTab({
  baseCurrency,
  concentration,
  marketDataIntegration,
  riskReturn,
  summary,
  t,
}: {
  baseCurrency: string;
  concentration?: ConcentrationResponse;
  marketDataIntegration?: PortfolioMarketDataIntegrationResponse;
  riskReturn?: RiskReturnResponse;
  summary?: PortfolioSummary;
  t: (key: string) => string;
}) {
  if (!summary) {
    return <LoadingState label={t("common.loading")} />;
  }

  return (
    <div className="portfolio-tab-stack">
      <PortfolioSummaryCards
        summary={summary}
        labels={{
          totalValue: t("portfolio.summary.totalValue"),
          positions: t("portfolio.summary.positions"),
          cash: t("portfolio.summary.cash"),
          largestPosition: t("portfolio.summary.largestPosition"),
          benchmark: t("portfolio.summary.benchmark"),
          baseCurrency: t("portfolio.summary.baseCurrency"),
          cashWeight: t("portfolio.summary.cashWeight"),
          concentration: t("portfolio.summary.concentration"),
        }}
      />

      <div className="portfolio-metric-grid">
        <PortfolioMetricCard
          title={t("portfolio.metrics.largestHolding")}
          value={summary.largest_position ?? t("common.unavailable")}
          subtitle={<PercentValue value={summary.largest_position_weight} />}
          badge={t("portfolio.badges.investedWeights")}
        />
        <PortfolioMetricCard
          title={t("portfolio.metrics.diversificationScore")}
          value={<PercentValue value={summary.diversification_score} />}
          subtitle={concentration?.concentration_level ?? t("common.unavailable")}
          tone={
            summary.diversification_score >= 0.7
              ? "positive"
              : summary.diversification_score >= 0.45
                ? "warning"
                : "negative"
          }
        />
        <PortfolioMetricCard
          title={t("portfolio.metrics.expectedReturn")}
          value={
            riskReturn ? (
              <PercentValue value={riskReturn.expected_return} />
            ) : (
              t("common.unavailable")
            )
          }
          subtitle={riskReturn?.risk_return_profile ?? t("common.unavailable")}
          badge={t("portfolio.badges.demo")}
        />
        <PortfolioMetricCard
          title={t("portfolio.metrics.volatility")}
          value={
            riskReturn?.standard_deviation === null || !riskReturn ? (
              t("common.unavailable")
            ) : (
              <PercentValue value={riskReturn.standard_deviation} />
            )
          }
          subtitle={riskReturn?.covariance_matrix_status ?? t("common.unavailable")}
          badge={t("portfolio.badges.placeholder")}
        />
      </div>

      <PortfolioSectionCard
        title={t("portfolio.marketDataIntegration.title")}
        description={t("portfolio.marketDataIntegration.description")}
        badges={[
          { label: t("portfolio.badges.requiresMarketData"), variant: "warning" },
          { label: t("portfolio.badges.notProductionReady"), variant: "warning" },
        ]}
      >
        <p className="portfolio-callout">
          {t("portfolio.marketDataIntegration.message")}
        </p>
        <div className="portfolio-endpoint-grid">
          <EndpointTile
            label={t("portfolio.marketDataIntegration.returnSeries")}
            value={
              marketDataIntegration?.return_series_endpoint ??
              t("common.unavailable")
            }
          />
          <EndpointTile
            label={t("portfolio.marketDataIntegration.alignedReturns")}
            value={
              marketDataIntegration?.aligned_returns_endpoint ??
              endpoints.marketDataAlignedReturns(
                marketDataIntegration?.symbols.join(",") ?? "",
              )
            }
          />
          <EndpointTile
            label={t("portfolio.marketDataIntegration.dataQuality")}
            value={
              marketDataIntegration?.data_quality_endpoint ??
              endpoints.marketDataQualityBatch("", baseCurrency)
            }
          />
        </div>
      </PortfolioSectionCard>
    </div>
  );
}

function AllocationTab({
  assetAllocation,
  assetTypeAllocation,
  baseCurrency,
  currencyAllocation,
  sectorAllocation,
  t,
}: {
  assetAllocation?: AllocationResponse;
  assetTypeAllocation?: AllocationResponse;
  baseCurrency: string;
  currencyAllocation?: AllocationResponse;
  sectorAllocation?: AllocationResponse;
  t: (key: string) => string;
}) {
  return (
    <div className="portfolio-tab-stack">
      <PortfolioSectionCard
        title={t("portfolio.sections.allocationTitle")}
        description={t("portfolio.sections.allocationDescription")}
        badges={[{ label: t("portfolio.badges.investedWeights"), variant: "info" }]}
      >
        <div className="portfolio-allocation-grid">
          {assetAllocation ? (
            <AllocationChart
              title={t("portfolio.allocation.assets")}
              items={assetAllocation.items}
              currency={baseCurrency}
            />
          ) : null}
          {sectorAllocation ? (
            <AllocationChart
              title={t("portfolio.allocation.sectors")}
              items={sectorAllocation.items}
              currency={baseCurrency}
            />
          ) : null}
          {currencyAllocation ? (
            <AllocationChart
              title={t("portfolio.allocation.currencies")}
              items={currencyAllocation.items}
              currency={baseCurrency}
            />
          ) : null}
          {assetTypeAllocation ? (
            <AllocationChart
              title={t("portfolio.allocation.assetTypes")}
              items={assetTypeAllocation.items}
              currency={baseCurrency}
            />
          ) : null}
        </div>
      </PortfolioSectionCard>
    </div>
  );
}

function RiskTab({
  concentration,
  constraints,
  marketDataIntegration,
  riskReturn,
  t,
}: {
  baseCurrency: string;
  concentration?: ConcentrationResponse;
  constraints?: ConstraintsResponse;
  marketDataIntegration?: PortfolioMarketDataIntegrationResponse;
  riskReturn?: RiskReturnResponse;
  t: (key: string) => string;
}) {
  return (
    <div className="portfolio-tab-stack">
      <div className="portfolio-metric-grid">
        <PortfolioMetricCard
          title={t("portfolio.metrics.hhi")}
          value={concentration?.hhi_concentration.toFixed(3) ?? t("common.unavailable")}
          subtitle={concentration?.concentration_level ?? t("common.unavailable")}
          tone={
            (concentration?.hhi_concentration ?? 0) > 0.25 ? "warning" : "positive"
          }
        />
        <PortfolioMetricCard
          title={t("portfolio.metrics.effectiveHoldings")}
          value={
            concentration?.effective_number_of_holdings.toFixed(2) ??
            t("common.unavailable")
          }
          subtitle={t("portfolio.metrics.effectiveHoldingsHelp")}
        />
        <PortfolioMetricCard
          title={t("portfolio.metrics.topThree")}
          value={
            concentration ? (
              <PercentValue value={concentration.top_3_holdings_weight} />
            ) : (
              t("common.unavailable")
            )
          }
          subtitle={t("portfolio.badges.investedWeights")}
        />
        <PortfolioMetricCard
          title={t("portfolio.metrics.diversificationBenefit")}
          value={
            riskReturn?.diversification_benefit === null || !riskReturn ? (
              t("common.unavailable")
            ) : (
              <PercentValue value={riskReturn.diversification_benefit} />
            )
          }
          subtitle={riskReturn?.correlation_matrix_status ?? t("common.unavailable")}
          badge={t("portfolio.badges.placeholder")}
        />
      </div>

      <PortfolioSectionCard
        title={t("portfolio.sections.riskTitle")}
        description={t("portfolio.sections.riskDescription")}
        badges={[
          { label: t("portfolio.badges.demoCovariance"), variant: "warning" },
          { label: t("portfolio.badges.placeholderCorrelation"), variant: "warning" },
        ]}
      >
        <div className="portfolio-metric-grid portfolio-metric-grid--compact">
          <PortfolioMetricCard
            title={t("portfolio.metrics.expectedReturn")}
            value={
              riskReturn ? (
                <PercentValue value={riskReturn.expected_return} />
              ) : (
                t("common.unavailable")
              )
            }
            subtitle={riskReturn?.risk_return_profile ?? t("common.unavailable")}
          />
          <PortfolioMetricCard
            title={t("portfolio.metrics.volatility")}
            value={
              riskReturn?.standard_deviation === null || !riskReturn ? (
                t("common.unavailable")
              ) : (
                <PercentValue value={riskReturn.standard_deviation} />
              )
            }
            subtitle={riskReturn?.covariance_matrix_status ?? t("common.unavailable")}
          />
        </div>

        <div className="portfolio-warning-grid">
          {(concentration?.warnings ?? []).map((warning) => (
            <PortfolioWarningCard
              key={warning}
              title={t("portfolio.diagnostics.warning")}
              message={warning}
              badge={t("portfolio.badges.concentration")}
            />
          ))}
          {(constraints?.breaches ?? []).map((breach) => (
            <PortfolioWarningCard
              key={`${breach.constraint}-${breach.name}`}
              title={breach.constraint}
              message={`${breach.name}: ${(breach.actual * 100).toFixed(1)}% / ${(breach.limit * 100).toFixed(1)}%`}
              badge={breach.severity}
              severity={breach.severity === "high" ? "danger" : "warning"}
            />
          ))}
          {marketDataIntegration ? (
            <PortfolioWarningCard
              title={t("portfolio.marketDataIntegration.title")}
              message={t("portfolio.marketDataIntegration.message")}
              badge={t("portfolio.badges.requiresMarketData")}
              severity="info"
            />
          ) : null}
        </div>
      </PortfolioSectionCard>
    </div>
  );
}

function PolicyTab({
  cfaConcepts,
  constraints,
  policy,
  t,
}: {
  cfaConcepts?: CfaConceptsResponse;
  constraints?: ConstraintsResponse;
  policy?: PolicyResponse;
  t: (key: string) => string;
}) {
  return (
    <div className="portfolio-tab-stack">
      {cfaConcepts ? (
        <PortfolioSectionCard
          title={t("portfolio.sections.processTitle")}
          description={t("portfolio.sections.processDescription")}
        >
          <div className="portfolio-process">
            {cfaConcepts.portfolio_management_process.map((step) => (
              <article className="portfolio-process-step" key={step.phase}>
                <span>{step.phase}</span>
                <p>{step.description}</p>
              </article>
            ))}
          </div>
        </PortfolioSectionCard>
      ) : null}

      <div className="portfolio-two-column">
        {policy ? (
          <KeyValuePanel
            title={t("portfolio.sections.policyTitle")}
            description={t("portfolio.sections.policyDescription")}
            rows={[
              {
                label: t("portfolio.policy.objective"),
                value: policy.policy.investment_objective,
              },
              {
                label: t("portfolio.policy.returnObjective"),
                value: policy.policy.return_objective,
              },
              {
                label: t("portfolio.policy.riskTolerance"),
                value: policy.policy.risk_tolerance,
              },
              {
                label: t("portfolio.policy.timeHorizon"),
                value: policy.policy.time_horizon,
              },
              {
                label: t("portfolio.policy.liquidity"),
                value: policy.policy.liquidity_needs,
              },
            ]}
            notes={policy.breaches.length ? policy.breaches : policy.warnings}
          />
        ) : null}

        {cfaConcepts ? (
          <KeyValuePanel
            title={t("portfolio.sections.investorTitle")}
            description={t("portfolio.sections.investorDescription")}
            rows={[
              {
                label: t("portfolio.policy.investorType"),
                value: cfaConcepts.investor_profile.investor_type,
              },
              {
                label: t("portfolio.policy.riskObjective"),
                value: cfaConcepts.investor_profile.risk_objective,
              },
              {
                label: t("portfolio.policy.liabilityProfile"),
                value: cfaConcepts.investor_profile.liability_profile,
              },
              {
                label: t("portfolio.policy.riskAbility"),
                value: cfaConcepts.risk_tolerance.ability_to_take_risk,
              },
              {
                label: t("portfolio.policy.riskWillingness"),
                value: cfaConcepts.risk_tolerance.willingness_to_take_risk,
              },
              {
                label: t("portfolio.policy.overallRisk"),
                value: cfaConcepts.risk_tolerance.overall_risk_tolerance,
              },
            ]}
            notes={[cfaConcepts.risk_tolerance.summary]}
          />
        ) : null}
      </div>

      {constraints ? (
        <PortfolioSectionCard
          title={t("portfolio.sections.constraintsTitle")}
          description={t("portfolio.sections.constraintsDescription")}
        >
          {constraints.breaches.length ? (
            <div className="portfolio-warning-grid">
              {constraints.breaches.map((breach) => (
                <PortfolioWarningCard
                  key={`${breach.constraint}-${breach.name}`}
                  title={breach.constraint}
                  message={`${breach.name}: ${(breach.actual * 100).toFixed(1)}% / ${(breach.limit * 100).toFixed(1)}%`}
                  badge={breach.severity}
                  severity={breach.severity === "high" ? "danger" : "warning"}
                />
              ))}
            </div>
          ) : (
            <EmptyState
              title={t("portfolio.diagnostics.noConstraintBreaches")}
              message={t("portfolio.diagnostics.noConstraintBreachesMessage")}
            />
          )}
        </PortfolioSectionCard>
      ) : null}
    </div>
  );
}

function RebalancingTab({
  baseCurrency,
  rebalancing,
  targetAllocation,
  t,
}: {
  baseCurrency: string;
  rebalancing?: RebalancingPreviewResponse;
  targetAllocation?: TargetAllocationResponse;
  t: (key: string) => string;
}) {
  return (
    <div className="portfolio-tab-stack">
      {targetAllocation ? (
        <PortfolioSectionCard
          title={t("portfolio.sections.targetAllocationTitle")}
          description={t("portfolio.sections.targetAllocationDescription")}
          badges={[
            {
              label: targetAllocation.rebalance_needed
                ? t("portfolio.badges.reviewRequired")
                : t("portfolio.badges.withinBands"),
              variant: targetAllocation.rebalance_needed ? "warning" : "success",
            },
          ]}
        >
          <div className="table-scroll">
            <table className="data-table portfolio-target-table">
              <thead>
                <tr>
                  <th>{t("portfolio.rebalancing.name")}</th>
                  <th>{t("portfolio.rebalancing.currentWeight")}</th>
                  <th>{t("portfolio.rebalancing.targetWeight")}</th>
                  <th>{t("portfolio.rebalancing.drift")}</th>
                  <th>{t("portfolio.rebalancing.status")}</th>
                </tr>
              </thead>
              <tbody>
                {targetAllocation.items.map((item) => (
                  <tr key={item.name}>
                    <td className="data-table__symbol">{item.name}</td>
                    <td className="data-table__numeric">
                      <PercentValue value={item.current_weight} />
                    </td>
                    <td className="data-table__numeric">
                      <PercentValue value={item.target_weight} />
                    </td>
                    <td
                      className={`data-table__numeric ${
                        Math.abs(item.drift) > item.tolerance_band
                          ? "negative-value"
                          : "positive-value"
                      }`}
                    >
                      <PercentValue value={item.drift} />
                    </td>
                    <td>{item.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </PortfolioSectionCard>
      ) : null}

      {rebalancing ? (
        <PortfolioSectionCard
          title={t("portfolio.sections.rebalancingTitle")}
          description={t("portfolio.sections.rebalancingDescription")}
          badges={[{ label: t("portfolio.badges.previewOnly"), variant: "warning" }]}
        >
          <RebalancingPreviewTable
            preview={rebalancing}
            currency={baseCurrency}
            labels={{
              name: t("portfolio.rebalancing.name"),
              action: t("portfolio.rebalancing.action"),
              currentValue: t("portfolio.rebalancing.currentValue"),
              targetValue: t("portfolio.rebalancing.targetValue"),
              valueDifference: t("portfolio.rebalancing.valueDifference"),
              quantity: t("portfolio.rebalancing.quantity"),
              turnover: t("portfolio.rebalancing.turnover"),
              notes: t("portfolio.rebalancing.notes"),
            }}
          />
        </PortfolioSectionCard>
      ) : null}
    </div>
  );
}

function PerformanceTab({
  baseCurrency,
  cfaConcepts,
  performance,
  t,
}: {
  baseCurrency: string;
  cfaConcepts?: CfaConceptsResponse;
  performance?: PerformanceMeasurementResponse;
  t: (key: string) => string;
}) {
  return (
    <div className="portfolio-tab-stack">
      {performance ? (
        <PortfolioSectionCard
          title={t("portfolio.sections.performanceTitle")}
          description={t("portfolio.sections.performanceDescription")}
          badges={[{ label: t("portfolio.badges.mwrPlaceholder"), variant: "warning" }]}
        >
          <div className="portfolio-metric-grid">
            <PortfolioMetricCard
              title={t("portfolio.performance.beginningValue")}
              value={
                <MoneyValue
                  value={performance.beginning_value}
                  currency={baseCurrency}
                />
              }
              subtitle={t("portfolio.performance.costBasisDemo")}
            />
            <PortfolioMetricCard
              title={t("portfolio.performance.endingValue")}
              value={
                <MoneyValue value={performance.ending_value} currency={baseCurrency} />
              }
              subtitle={t("portfolio.performance.currentMarketValue")}
            />
            <PortfolioMetricCard
              title={t("portfolio.performance.hpr")}
              value={<PercentValue value={performance.holding_period_return} />}
              subtitle={t("portfolio.performance.hprDescription")}
            />
            <PortfolioMetricCard
              title={t("portfolio.performance.twr")}
              value={<PercentValue value={performance.time_weighted_return} />}
              subtitle={t("portfolio.performance.twrDescription")}
            />
            <PortfolioMetricCard
              title={t("portfolio.performance.mwr")}
              value={
                performance.money_weighted_return === null ? (
                  t("common.unavailable")
                ) : (
                  <PercentValue value={performance.money_weighted_return} />
                )
              }
              subtitle={t("portfolio.badges.placeholder")}
            />
          </div>
        </PortfolioSectionCard>
      ) : null}

      {cfaConcepts ? (
        <div className="portfolio-two-column">
          <KeyValuePanel
            title={t("portfolio.sections.riskAdjustedTitle")}
            description={t("portfolio.sections.riskAdjustedDescription")}
            badges={[{ label: t("portfolio.badges.benchmarkHistory"), variant: "warning" }]}
            rows={[
              {
                label: t("portfolio.performance.sharpe"),
                value: formatNullableNumber(
                  cfaConcepts.risk_adjusted_performance.sharpe_ratio,
                ),
              },
              {
                label: t("portfolio.performance.treynor"),
                value: formatNullableNumber(
                  cfaConcepts.risk_adjusted_performance.treynor_ratio,
                ),
              },
              {
                label: t("portfolio.performance.jensenAlpha"),
                value: (
                  <PercentValue
                    value={cfaConcepts.risk_adjusted_performance.jensen_alpha}
                  />
                ),
              },
              {
                label: t("portfolio.performance.informationRatio"),
                value: formatNullableNumber(
                  cfaConcepts.risk_adjusted_performance.information_ratio,
                ),
              },
              {
                label: t("portfolio.performance.trackingError"),
                value:
                  cfaConcepts.risk_adjusted_performance.tracking_error === null ? (
                    t("common.unavailable")
                  ) : (
                    <PercentValue
                      value={
                        cfaConcepts.risk_adjusted_performance.tracking_error
                      }
                    />
                  ),
              },
            ]}
            notes={cfaConcepts.risk_adjusted_performance.notes}
          />

          <KeyValuePanel
            title={t("portfolio.sections.capmTitle")}
            description={t("portfolio.sections.capmDescription")}
            rows={[
              {
                label: t("portfolio.performance.portfolioBeta"),
                value: cfaConcepts.capm.portfolio_beta.toFixed(2),
              },
              {
                label: t("portfolio.performance.requiredReturn"),
                value: <PercentValue value={cfaConcepts.capm.capm_required_return} />,
              },
              {
                label: t("portfolio.performance.expectedReturnGap"),
                value: <PercentValue value={cfaConcepts.capm.expected_return_gap} />,
              },
              {
                label: t("portfolio.performance.utilityScore"),
                value: cfaConcepts.utility.utility_score.toFixed(4),
              },
            ]}
            notes={[cfaConcepts.capm.interpretation]}
          />
        </div>
      ) : null}
    </div>
  );
}

function DiagnosticsTab({
  benchmark,
  cfaConcepts,
  diagnostics,
  marketDataIntegration,
  t,
}: {
  benchmark?: BenchmarkResponse;
  cfaConcepts?: CfaConceptsResponse;
  diagnostics?: PortfolioDiagnosticsResponse;
  marketDataIntegration?: PortfolioMarketDataIntegrationResponse;
  t: (key: string) => string;
}) {
  return (
    <div className="portfolio-tab-stack">
      {diagnostics ? (
        <PortfolioDiagnosticsPanel
          diagnostics={diagnostics}
          marketDataIntegration={marketDataIntegration}
          labels={{
            title: t("portfolio.sections.diagnosticsTitle"),
            description: t("portfolio.sections.diagnosticsDescription"),
            allocation: t("portfolio.diagnostics.allocation"),
            diversification: t("portfolio.diagnostics.diversification"),
            concentration: t("portfolio.diagnostics.concentration"),
            cash: t("portfolio.diagnostics.cash"),
            benchmark: t("portfolio.diagnostics.benchmark"),
            policy: t("portfolio.diagnostics.policy"),
            rebalancing: t("portfolio.diagnostics.rebalancing"),
            limitations: t("portfolio.diagnostics.limitations"),
            nextSteps: t("portfolio.diagnostics.nextSteps"),
            assumptions: t("portfolio.diagnostics.assumptions"),
            plannedAnalytics: t("portfolio.diagnostics.plannedAnalytics"),
            readiness: t("portfolio.diagnostics.readiness"),
          }}
        />
      ) : null}

      {marketDataIntegration ? (
        <PortfolioSectionCard
          title={t("portfolio.marketDataIntegration.title")}
          description={marketDataIntegration.current_status}
          badges={marketDataIntegration.readiness_badges.slice(0, 5).map((label) => ({
            label,
            variant: label.includes("No") ? "warning" : "info",
          }))}
        >
          <p className="portfolio-callout">
            {t("portfolio.marketDataIntegration.message")}
          </p>
          <div className="portfolio-warning-grid">
            {marketDataIntegration.limitations.map((limitation) => (
              <PortfolioWarningCard
                key={limitation}
                title={t("portfolio.diagnostics.limitations")}
                message={limitation}
                badge={t("portfolio.badges.notProductionReady")}
              />
            ))}
          </div>
        </PortfolioSectionCard>
      ) : null}

      <div className="portfolio-two-column">
        {benchmark ? (
          <KeyValuePanel
            title={t("portfolio.sections.benchmarkTitle")}
            description={t("portfolio.sections.benchmarkDescription")}
            badges={[
              { label: t("portfolio.badges.benchmarkPlaceholder"), variant: "warning" },
            ]}
            rows={[
              {
                label: t("portfolio.benchmark.symbol"),
                value: benchmark.benchmark_symbol,
              },
              {
                label: t("portfolio.benchmark.totalActiveWeight"),
                value: <PercentValue value={benchmark.total_active_weight} />,
              },
              ...benchmark.holdings.map((holding) => ({
                label: holding.name,
                value: <PercentValue value={holding.active_weight} />,
              })),
            ]}
            notes={benchmark.notes}
          />
        ) : null}

        {cfaConcepts ? (
          <KeyValuePanel
            title={t("portfolio.sections.behavioralTitle")}
            description={t("portfolio.sections.behavioralDescription")}
            rows={[
              {
                label: t("portfolio.performance.etfExposure"),
                value: (
                  <PercentValue
                    value={cfaConcepts.pooled_vehicle_exposure.etf_exposure}
                  />
                ),
              },
              {
                label: t("portfolio.performance.singleStockExposure"),
                value: (
                  <PercentValue
                    value={cfaConcepts.pooled_vehicle_exposure.single_stock_exposure}
                  />
                ),
              },
              {
                label: t("portfolio.performance.pooledVehicleUsage"),
                value: cfaConcepts.pooled_vehicle_exposure.usage_classification,
              },
              ...cfaConcepts.efficient_frontier.points.map((point) => ({
                label: point.label,
                value: `${(point.expected_return * 100).toFixed(1)}% / ${(point.risk * 100).toFixed(1)}%`,
              })),
            ]}
            notes={[
              cfaConcepts.behavioral_biases.summary,
              cfaConcepts.efficient_frontier.status,
            ]}
          />
        ) : null}
      </div>
    </div>
  );
}

function KeyValuePanel({
  title,
  description,
  rows,
  notes,
  badges,
}: {
  title: string;
  description?: string;
  rows: SimpleRow[];
  notes?: string[];
  badges?: { label: string; variant?: "neutral" | "info" | "success" | "warning" | "danger" }[];
}) {
  return (
    <PortfolioSectionCard title={title} description={description} badges={badges}>
      <div className="table-scroll portfolio-key-value-scroll">
        <table className="data-table portfolio-key-value-table">
          <tbody>
            {rows.map((row) => (
              <tr key={row.label}>
                <td>{row.label}</td>
                <td>{row.value}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {notes?.length ? (
        <div className="portfolio-note-list">
          <ul>
            {notes.map((note) => (
              <li key={note}>{note}</li>
            ))}
          </ul>
        </div>
      ) : null}
    </PortfolioSectionCard>
  );
}

function EndpointTile({ label, value }: { label: string; value: string }) {
  return (
    <div className="portfolio-endpoint-tile">
      <span>{label}</span>
      <code>{value}</code>
    </div>
  );
}

function formatNullableNumber(value: number | null) {
  return value === null ? "Unavailable" : value.toFixed(3);
}
