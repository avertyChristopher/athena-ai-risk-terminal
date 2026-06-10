import { useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { PageHeader } from "../../../components/layout/PageHeader";
import { LoadingState } from "../../../components/ui/LoadingState";
import { MetricCard } from "../../../components/finance/MetricCard";
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
import { PortfolioForm } from "../components/PortfolioForm";
import { PortfolioSelector } from "../components/PortfolioSelector";
import { PortfolioSummaryCards } from "../components/PortfolioSummaryCards";
import { PositionTable } from "../components/PositionTable";

export function PortfolioPage() {
  const { t } = useTranslation();
  const queryClient = useQueryClient();
  const [selectedPortfolioId, setSelectedPortfolioId] = useState("");
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

  const sectorAllocationQuery = useQuery({
    queryKey: ["portfolio-sector-allocation", selectedPortfolio?.id],
    enabled: Boolean(selectedPortfolio?.id),
    queryFn: () =>
      apiClient.get<AllocationResponse>(
        endpoints.portfolioSectorAllocation(selectedPortfolio?.id ?? ""),
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
    },
  });

  const createPositionMutation = useMutation({
    mutationFn: (payload: PositionCreate) =>
      apiClient.post(
        endpoints.portfolioPositions(selectedPortfolio?.id ?? ""),
        payload,
      ),
    onSuccess: () => invalidatePortfolioQueries(),
  });

  const deletePositionMutation = useMutation({
    mutationFn: (positionId: string) =>
      apiClient.delete(
        endpoints.portfolioPosition(selectedPortfolio?.id ?? "", positionId),
      ),
    onSuccess: () => invalidatePortfolioQueries(),
  });

  function invalidatePortfolioQueries() {
    queryClient.invalidateQueries({ queryKey: ["portfolio-summary"] });
    queryClient.invalidateQueries({ queryKey: ["portfolio-positions"] });
    queryClient.invalidateQueries({ queryKey: ["portfolio-sector-allocation"] });
    queryClient.invalidateQueries({ queryKey: ["portfolio-cfa-concepts"] });
  }

  const isLoading =
    portfoliosQuery.isLoading ||
    summaryQuery.isLoading ||
    positionsQuery.isLoading ||
    sectorAllocationQuery.isLoading;

  return (
    <div className="page portfolio-page">
      <PageHeader
        title={t("portfolio.title")}
        subtitle={t("portfolio.subtitle")}
      />

      <section className="portfolio-toolbar">
        {selectedPortfolio ? (
          <PortfolioSelector
            portfolios={portfolios}
            selectedPortfolioId={selectedPortfolio.id}
            onSelect={setSelectedPortfolioId}
            label={t("portfolio.selector")}
          />
        ) : null}
      </section>

      <div className="portfolio-layout">
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

      {summaryQuery.data ? (
        <PortfolioSummaryCards
          summary={summaryQuery.data}
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
      ) : null}

      {selectedPortfolio ? (
        <PositionTable
          positions={positionsQuery.data?.items ?? []}
          onAddClick={() => setIsAddPositionOpen(true)}
          onDelete={(positionId) => deletePositionMutation.mutate(positionId)}
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
            portfolioWeight: "Portfolio weight",
            investedWeight: "Invested weight",
            costBasis: "Cost basis",
            unrealizedPnl: "Unrealized P&L",
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

      {summaryQuery.data && sectorAllocationQuery.data ? (
        <section className="grid">
          {assetAllocationQuery.data ? (
            <AllocationChart
              title="Asset allocation - invested weights"
              items={assetAllocationQuery.data.items}
              currency={summaryQuery.data.base_currency}
            />
          ) : null}
          <AllocationChart
            title={t("portfolio.allocation.sectors") + " - invested weights"}
            items={sectorAllocationQuery.data.items}
            currency={summaryQuery.data.base_currency}
          />
          {currencyAllocationQuery.data ? (
            <AllocationChart
              title="Currency allocation - invested weights"
              items={currencyAllocationQuery.data.items}
              currency={summaryQuery.data.base_currency}
            />
          ) : null}
          {assetTypeAllocationQuery.data ? (
            <AllocationChart
              title="Asset type allocation - invested weights"
              items={assetTypeAllocationQuery.data.items}
              currency={summaryQuery.data.base_currency}
            />
          ) : null}
        </section>
      ) : null}

      {concentrationQuery.data ? (
        <section className="grid">
          <MetricCard
            title="HHI concentration"
            value={concentrationQuery.data.hhi_concentration.toFixed(3)}
            subtitle={concentrationQuery.data.concentration_level}
          />
          <MetricCard
            title="Effective holdings"
            value={concentrationQuery.data.effective_number_of_holdings.toFixed(2)}
            subtitle="Holdings-only diversification measure"
          />
          <MetricCard
            title="Top 3 holdings"
            value={<PercentValue value={concentrationQuery.data.top_3_holdings_weight} />}
            subtitle="Invested weight basis"
          />
          <MetricCard
            title="Diversification score"
            value={<PercentValue value={concentrationQuery.data.diversification_score} />}
            subtitle="1 minus HHI"
          />
        </section>
      ) : null}

      {riskReturnQuery.data ? (
        <section className="grid">
          <MetricCard
            title="Expected return"
            value={<PercentValue value={riskReturnQuery.data.expected_return} />}
            subtitle={riskReturnQuery.data.risk_return_profile}
          />
          <MetricCard
            title="Portfolio volatility"
            value={
              riskReturnQuery.data.standard_deviation === null ? (
                t("common.unavailable")
              ) : (
                <PercentValue value={riskReturnQuery.data.standard_deviation} />
              )
            }
            subtitle="Demo covariance scaffold"
          />
          <MetricCard
            title="Diversification benefit"
            value={
              riskReturnQuery.data.diversification_benefit === null ? (
                t("common.unavailable")
              ) : (
                <PercentValue value={riskReturnQuery.data.diversification_benefit} />
              )
            }
            subtitle={riskReturnQuery.data.correlation_matrix_status}
          />
        </section>
      ) : null}

      <div className="portfolio-layout">
        {benchmarkQuery.data ? (
          <SimplePanel
            title="Benchmark & active weights"
            rows={benchmarkQuery.data.holdings.map((holding) => ({
              label: holding.name,
              value: `${(holding.active_weight * 100).toFixed(2)}% active weight`,
            }))}
            notes={benchmarkQuery.data.notes}
          />
        ) : null}

        {policyQuery.data ? (
          <SimplePanel
            title="Investment Policy Statement"
            rows={[
              {
                label: "Objective",
                value: policyQuery.data.policy.investment_objective,
              },
              {
                label: "Risk tolerance",
                value: policyQuery.data.policy.risk_tolerance,
              },
              {
                label: "Time horizon",
                value: policyQuery.data.policy.time_horizon,
              },
              {
                label: "Liquidity",
                value: policyQuery.data.policy.liquidity_needs,
              },
            ]}
            notes={policyQuery.data.breaches.length ? policyQuery.data.breaches : policyQuery.data.warnings}
          />
        ) : null}
      </div>

      <div className="portfolio-layout">
        {targetAllocationQuery.data ? (
          <SimplePanel
            title="Target allocation & drift"
            rows={targetAllocationQuery.data.items.map((item) => ({
              label: item.name,
              value: `${(item.current_weight * 100).toFixed(1)}% current / ${(item.target_weight * 100).toFixed(1)}% target - ${item.status}`,
            }))}
            notes={[targetAllocationQuery.data.rebalance_needed ? "Rebalance review needed" : "Within target bands"]}
          />
        ) : null}

        {rebalancingQuery.data ? (
          <SimplePanel
            title="Rebalancing preview"
            rows={rebalancingQuery.data.items.map((item) => ({
              label: item.name,
              value: `${item.action.toUpperCase()} ${item.estimated_quantity_difference.toFixed(2)} units`,
            }))}
            notes={[
              `Estimated turnover: ${(rebalancingQuery.data.turnover_estimate * 100).toFixed(2)}%`,
              ...rebalancingQuery.data.notes,
            ]}
          />
        ) : null}
      </div>

      <div className="portfolio-layout">
        {performanceQuery.data && summaryQuery.data ? (
          <SimplePanel
            title="Performance measurement foundation"
            rows={[
              {
                label: "Beginning value",
                value: <MoneyValue value={performanceQuery.data.beginning_value} currency={summaryQuery.data.base_currency} />,
              },
              {
                label: "Ending value",
                value: <MoneyValue value={performanceQuery.data.ending_value} currency={summaryQuery.data.base_currency} />,
              },
              {
                label: "Holding-period return",
                value: <PercentValue value={performanceQuery.data.holding_period_return} />,
              },
              {
                label: "TWR",
                value: <PercentValue value={performanceQuery.data.time_weighted_return} />,
              },
            ]}
            notes={performanceQuery.data.notes}
          />
        ) : null}

        {constraintsQuery.data ? (
          <SimplePanel
            title="Constraints & warnings"
            rows={constraintsQuery.data.breaches.map((breach) => ({
              label: breach.constraint,
              value: `${breach.name}: ${(breach.actual * 100).toFixed(1)}% / limit ${(breach.limit * 100).toFixed(1)}%`,
            }))}
            notes={constraintsQuery.data.breaches.length ? [] : ["No constraint breaches flagged in demo mode."]}
          />
        ) : null}
      </div>

      {diagnosticsQuery.data ? (
        <SimplePanel
          title="Portfolio diagnostics"
          rows={[
            { label: "Allocation", value: diagnosticsQuery.data.allocation_quality },
            { label: "Diversification", value: diagnosticsQuery.data.diversification_quality },
            { label: "Concentration", value: diagnosticsQuery.data.concentration_risk },
            { label: "Cash level", value: diagnosticsQuery.data.cash_level },
            { label: "Benchmark", value: diagnosticsQuery.data.benchmark_alignment },
            { label: "Policy", value: diagnosticsQuery.data.policy_alignment },
          ]}
          notes={[
            diagnosticsQuery.data.summary,
            ...diagnosticsQuery.data.data_quality_limitations,
            ...diagnosticsQuery.data.next_analytical_steps,
          ]}
        />
      ) : null}

      {cfaConceptsQuery.data ? (
        <div className="portfolio-layout">
          <SimplePanel
            title="CFA portfolio management process"
            rows={cfaConceptsQuery.data.portfolio_management_process.map((step) => ({
              label: step.phase,
              value: step.description,
            }))}
          />

          <SimplePanel
            title="Investor profile & IPS"
            rows={[
              {
                label: "Investor type",
                value: cfaConceptsQuery.data.investor_profile.investor_type,
              },
              {
                label: "Return objective",
                value: cfaConceptsQuery.data.investor_profile.return_objective,
              },
              {
                label: "Risk objective",
                value: cfaConceptsQuery.data.investor_profile.risk_objective,
              },
              {
                label: "Liquidity needs",
                value: cfaConceptsQuery.data.investor_profile.liquidity_needs,
              },
              {
                label: "Liability profile",
                value: cfaConceptsQuery.data.investor_profile.liability_profile,
              },
            ]}
            notes={[
              cfaConceptsQuery.data.investor_profile.tax_considerations,
              cfaConceptsQuery.data.investor_profile.legal_regulatory_constraints,
              cfaConceptsQuery.data.investor_profile.unique_circumstances,
            ]}
          />
        </div>
      ) : null}

      {cfaConceptsQuery.data ? (
        <div className="portfolio-layout">
          <SimplePanel
            title="Risk tolerance"
            rows={[
              {
                label: "Ability",
                value: cfaConceptsQuery.data.risk_tolerance.ability_to_take_risk,
              },
              {
                label: "Willingness",
                value: cfaConceptsQuery.data.risk_tolerance.willingness_to_take_risk,
              },
              {
                label: "Overall",
                value: cfaConceptsQuery.data.risk_tolerance.overall_risk_tolerance,
              },
              {
                label: "Conflict",
                value: cfaConceptsQuery.data.risk_tolerance.conflict_detected
                  ? "Review required"
                  : "No conflict flagged",
              },
            ]}
            notes={[cfaConceptsQuery.data.risk_tolerance.summary]}
          />

          <SimplePanel
            title="Utility & CAPM"
            rows={[
              {
                label: "Risk aversion",
                value: `${cfaConceptsQuery.data.utility.risk_aversion_coefficient.toFixed(1)} - ${cfaConceptsQuery.data.utility.risk_aversion_classification}`,
              },
              {
                label: "Utility score",
                value: cfaConceptsQuery.data.utility.utility_score.toFixed(4),
              },
              {
                label: "Portfolio beta",
                value: cfaConceptsQuery.data.capm.portfolio_beta.toFixed(2),
              },
              {
                label: "CAPM required return",
                value: <PercentValue value={cfaConceptsQuery.data.capm.capm_required_return} />,
              },
              {
                label: "Expected return gap",
                value: <PercentValue value={cfaConceptsQuery.data.capm.expected_return_gap} />,
              },
            ]}
            notes={[cfaConceptsQuery.data.capm.interpretation]}
          />
        </div>
      ) : null}

      {cfaConceptsQuery.data ? (
        <div className="portfolio-layout">
          <SimplePanel
            title="Risk-adjusted performance"
            rows={[
              {
                label: "Sharpe ratio",
                value: formatNullableNumber(cfaConceptsQuery.data.risk_adjusted_performance.sharpe_ratio),
              },
              {
                label: "Treynor ratio",
                value: formatNullableNumber(cfaConceptsQuery.data.risk_adjusted_performance.treynor_ratio),
              },
              {
                label: "Jensen alpha",
                value: <PercentValue value={cfaConceptsQuery.data.risk_adjusted_performance.jensen_alpha} />,
              },
              {
                label: "Information ratio",
                value: formatNullableNumber(cfaConceptsQuery.data.risk_adjusted_performance.information_ratio),
              },
              {
                label: "Tracking error",
                value:
                  cfaConceptsQuery.data.risk_adjusted_performance.tracking_error === null ? (
                    t("common.unavailable")
                  ) : (
                    <PercentValue value={cfaConceptsQuery.data.risk_adjusted_performance.tracking_error} />
                  ),
              },
            ]}
            notes={cfaConceptsQuery.data.risk_adjusted_performance.notes}
          />

          <SimplePanel
            title="Behavioral and pooled exposure"
            rows={[
              {
                label: "ETF exposure",
                value: <PercentValue value={cfaConceptsQuery.data.pooled_vehicle_exposure.etf_exposure} />,
              },
              {
                label: "Single-stock exposure",
                value: <PercentValue value={cfaConceptsQuery.data.pooled_vehicle_exposure.single_stock_exposure} />,
              },
              {
                label: "Pooled-vehicle usage",
                value: cfaConceptsQuery.data.pooled_vehicle_exposure.usage_classification,
              },
              ...cfaConceptsQuery.data.efficient_frontier.points.map((point) => ({
                label: point.label,
                value: `${(point.expected_return * 100).toFixed(1)}% return / ${(point.risk * 100).toFixed(1)}% risk`,
              })),
            ]}
            notes={[
              cfaConceptsQuery.data.behavioral_biases.summary,
              cfaConceptsQuery.data.efficient_frontier.status,
            ]}
          />
        </div>
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

function formatNullableNumber(value: number | null) {
  return value === null ? "Unavailable" : value.toFixed(3);
}

function SimplePanel({
  title,
  rows,
  notes,
}: {
  title: string;
  rows: { label: string; value: ReactNode }[];
  notes?: string[];
}) {
  return (
    <section className="card table-section">
      <div className="section-heading">
        <h2>{title}</h2>
      </div>
      <div className="table-scroll">
        <table className="data-table">
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
        <ul>
          {notes.map((note) => (
            <li key={note}>{note}</li>
          ))}
        </ul>
      ) : null}
    </section>
  );
}
