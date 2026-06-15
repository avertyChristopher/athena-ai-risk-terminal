import { FormEvent, useEffect, useMemo, useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";

import { MoneyValue } from "../../../components/finance/MoneyValue";
import { PercentValue } from "../../../components/finance/PercentValue";
import { PageHeader } from "../../../components/layout/PageHeader";
import { EmptyState } from "../../../components/ui/EmptyState";
import { LoadingState } from "../../../components/ui/LoadingState";
import { apiClient } from "../../../lib/api-client";
import { endpoints } from "../../../lib/endpoints";
import { useTranslation } from "../../../hooks/useTranslation";
import { PortfolioListResponse } from "../../../types/portfolio";
import {
  ImpactMetric,
  OrderType,
  TimeInForce,
  TradeAction,
  TradeRationale,
  TradeSimulationRequest,
  TradeSimulationResponse,
} from "../../../types/trade";
import { BeforeAfterTable } from "../components/BeforeAfterTable";
import { TradeMetricCard } from "../components/TradeMetricCard";
import { TradeSectionCard } from "../components/TradeSectionCard";
import { TradeStatusBadge } from "../components/TradeStatusBadge";

type AnalysisTab =
  | "impact"
  | "risk"
  | "suitability"
  | "costs"
  | "benchmark"
  | "commentary";

const orderTypes: OrderType[] = ["Market", "Limit", "Stop"];
const timeInForceOptions: TimeInForce[] = ["Day", "GTC"];
const rationaleOptions: TradeRationale[] = [
  "Rebalancing",
  "Risk reduction",
  "Growth opportunity",
  "Income objective",
  "Hedging",
  "Liquidity need",
  "Valuation view",
  "Momentum view",
];
const assetTypes = ["equity", "etf", "fixed_income", "bond"];

export function TradeSimulatorPage() {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState<AnalysisTab>("impact");
  const [formState, setFormState] = useState<TradeSimulationRequest>({
    portfolio_id: "",
    action: "BUY",
    symbol: "NVDA",
    asset_name: "NVIDIA Corporation",
    asset_type: "equity",
    quantity: 5,
    estimated_price: 125,
    order_type: "Market",
    limit_price: null,
    time_in_force: "Day",
    trade_rationale: "Growth opportunity",
  });

  const portfoliosQuery = useQuery({
    queryKey: ["portfolios"],
    queryFn: () => apiClient.get<PortfolioListResponse>(endpoints.portfolios),
  });

  const portfolios = portfoliosQuery.data?.items ?? [];

  useEffect(() => {
    if (!formState.portfolio_id && portfolios.length > 0) {
      setFormState((current) => ({
        ...current,
        portfolio_id: portfolios[0].id,
      }));
    }
  }, [formState.portfolio_id, portfolios]);

  const selectedPortfolio = useMemo(
    () =>
      portfolios.find((portfolio) => portfolio.id === formState.portfolio_id) ??
      portfolios[0],
    [formState.portfolio_id, portfolios],
  );

  const simulateMutation = useMutation({
    mutationFn: (payload: TradeSimulationRequest) =>
      apiClient.post<TradeSimulationResponse>(
        endpoints.tradeSimulatorSimulate,
        payload,
      ),
    onSuccess: () => setActiveTab("impact"),
  });

  const simulation = simulateMutation.data;
  const liveTradeValue = formState.quantity * formState.estimated_price;
  const liveCommission = Math.max(1, liveTradeValue * 0.0005);
  const liveSpread = liveTradeValue * 0.0004;
  const liveSlippage =
    liveTradeValue *
    (formState.order_type === "Limit"
      ? 0.0003
      : formState.order_type === "Stop"
        ? 0.001
        : 0.0008);
  const liveEstimatedCost = liveCommission + liveSpread + liveSlippage;

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    simulateMutation.mutate({
      ...formState,
      symbol: formState.symbol.toUpperCase(),
      asset_name: formState.asset_name || null,
      limit_price:
        formState.order_type === "Limit" ? formState.limit_price : null,
    });
  }

  function updateForm<Value extends keyof TradeSimulationRequest>(
    key: Value,
    value: TradeSimulationRequest[Value],
  ) {
    setFormState((current) => ({ ...current, [key]: value }));
  }

  return (
    <div className="page trade-simulator-page">
      <PageHeader
        title={t("tradeSimulator.title")}
        subtitle={t("tradeSimulator.subtitle")}
      />

      <section className="trade-command-panel">
        <div>
          <span>{t("tradeSimulator.workbench.eyebrow")}</span>
          <h2>{t("tradeSimulator.workbench.title")}</h2>
          <p>{t("tradeSimulator.workbench.description")}</p>
        </div>
        <div className="trade-badge-cluster">
          <TradeStatusBadge
            label={t("tradeSimulator.badges.simulationOnly")}
            variant="warning"
          />
          <TradeStatusBadge
            label={t("tradeSimulator.badges.demoAssumptions")}
            variant="info"
          />
          <TradeStatusBadge
            label={t("tradeSimulator.badges.requiresMarketData")}
            variant="warning"
          />
        </div>
      </section>

      <div className="trade-workbench-grid">
        <TradeSectionCard
          title={t("tradeSimulator.ticket.title")}
          description={t("tradeSimulator.ticket.description")}
          badges={[{ label: t("tradeSimulator.badges.noExecution"), variant: "warning" }]}
        >
          <form className="trade-ticket-form" onSubmit={handleSubmit}>
            <label className="form-field">
              <span>{t("tradeSimulator.ticket.portfolio")}</span>
              <select
                value={formState.portfolio_id}
                onChange={(event) => updateForm("portfolio_id", event.target.value)}
              >
                {portfolios.map((portfolio) => (
                  <option key={portfolio.id} value={portfolio.id}>
                    {portfolio.name}
                  </option>
                ))}
              </select>
            </label>

            <div className="trade-action-toggle">
              {(["BUY", "SELL"] as TradeAction[]).map((action) => (
                <button
                  key={action}
                  className={`trade-action-toggle__button ${
                    formState.action === action
                      ? "trade-action-toggle__button--active"
                      : ""
                  }`}
                  type="button"
                  onClick={() => updateForm("action", action)}
                >
                  {action}
                </button>
              ))}
            </div>

            <div className="form-grid">
              <label className="form-field">
                <span>{t("tradeSimulator.ticket.symbol")}</span>
                <input
                  required
                  value={formState.symbol}
                  onChange={(event) => updateForm("symbol", event.target.value)}
                />
              </label>
              <label className="form-field">
                <span>{t("tradeSimulator.ticket.assetName")}</span>
                <input
                  value={formState.asset_name ?? ""}
                  onChange={(event) => updateForm("asset_name", event.target.value)}
                />
              </label>
              <label className="form-field">
                <span>{t("tradeSimulator.ticket.assetType")}</span>
                <select
                  value={formState.asset_type}
                  onChange={(event) => updateForm("asset_type", event.target.value)}
                >
                  {assetTypes.map((assetType) => (
                    <option key={assetType} value={assetType}>
                      {assetType}
                    </option>
                  ))}
                </select>
              </label>
              <label className="form-field">
                <span>{t("tradeSimulator.ticket.quantity")}</span>
                <input
                  min="0.01"
                  required
                  step="0.01"
                  type="number"
                  value={formState.quantity}
                  onChange={(event) =>
                    updateForm("quantity", Number(event.target.value))
                  }
                />
              </label>
              <label className="form-field">
                <span>{t("tradeSimulator.ticket.estimatedPrice")}</span>
                <input
                  min="0.01"
                  required
                  step="0.01"
                  type="number"
                  value={formState.estimated_price}
                  onChange={(event) =>
                    updateForm("estimated_price", Number(event.target.value))
                  }
                />
              </label>
              <label className="form-field">
                <span>{t("tradeSimulator.ticket.orderType")}</span>
                <select
                  value={formState.order_type}
                  onChange={(event) =>
                    updateForm("order_type", event.target.value as OrderType)
                  }
                >
                  {orderTypes.map((orderType) => (
                    <option key={orderType} value={orderType}>
                      {orderType}
                    </option>
                  ))}
                </select>
              </label>
              <label className="form-field">
                <span>{t("tradeSimulator.ticket.limitPrice")}</span>
                <input
                  disabled={formState.order_type !== "Limit"}
                  min="0.01"
                  step="0.01"
                  type="number"
                  value={formState.limit_price ?? ""}
                  onChange={(event) =>
                    updateForm(
                      "limit_price",
                      event.target.value ? Number(event.target.value) : null,
                    )
                  }
                />
              </label>
              <label className="form-field">
                <span>{t("tradeSimulator.ticket.timeInForce")}</span>
                <select
                  value={formState.time_in_force}
                  onChange={(event) =>
                    updateForm("time_in_force", event.target.value as TimeInForce)
                  }
                >
                  {timeInForceOptions.map((option) => (
                    <option key={option} value={option}>
                      {option}
                    </option>
                  ))}
                </select>
              </label>
              <label className="form-field">
                <span>{t("tradeSimulator.ticket.rationale")}</span>
                <select
                  value={formState.trade_rationale}
                  onChange={(event) =>
                    updateForm(
                      "trade_rationale",
                      event.target.value as TradeRationale,
                    )
                  }
                >
                  {rationaleOptions.map((rationale) => (
                    <option key={rationale} value={rationale}>
                      {rationale}
                    </option>
                  ))}
                </select>
              </label>
            </div>

            <div className="trade-ticket-cost-strip">
              <TradeMetricCard
                title={t("tradeSimulator.ticket.tradeValue")}
                value={
                  <MoneyValue
                    value={liveTradeValue}
                    currency={selectedPortfolio?.base_currency ?? "USD"}
                  />
                }
                subtitle={t("tradeSimulator.badges.demoPrice")}
              />
              <TradeMetricCard
                title={t("tradeSimulator.ticket.estimatedCosts")}
                value={
                  <MoneyValue
                    value={liveEstimatedCost}
                    currency={selectedPortfolio?.base_currency ?? "USD"}
                  />
                }
                subtitle={`${t("tradeSimulator.ticket.commission")} + ${t("tradeSimulator.ticket.spread")} + ${t("tradeSimulator.ticket.slippage")}`}
              />
              <TradeMetricCard
                title={t("tradeSimulator.ticket.cashDirection")}
                value={
                  formState.action === "BUY"
                    ? t("tradeSimulator.ticket.cashOutflow")
                    : t("tradeSimulator.ticket.cashInflow")
                }
                subtitle={t("tradeSimulator.ticket.preExecution")}
              />
            </div>

            <button
              className="button button--primary"
              disabled={!formState.portfolio_id || simulateMutation.isPending}
              type="submit"
            >
              {t("tradeSimulator.ticket.simulate")}
            </button>
          </form>
        </TradeSectionCard>

        <TradeSectionCard
          title={t("tradeSimulator.summary.title")}
          description={t("tradeSimulator.summary.description")}
          badges={[
            {
              label:
                simulation?.simulation_result.trade_status ??
                t("tradeSimulator.summary.pending"),
              variant: statusVariant(simulation?.simulation_result.trade_status),
            },
          ]}
        >
          {simulateMutation.isPending ? (
            <LoadingState label={t("common.loading")} />
          ) : simulation ? (
            <SimulationSummary
              simulation={simulation}
              currency={selectedPortfolio?.base_currency ?? "USD"}
              t={t}
            />
          ) : (
            <EmptyState
              title={t("tradeSimulator.summary.emptyTitle")}
              message={t("tradeSimulator.summary.emptyMessage")}
            />
          )}
        </TradeSectionCard>
      </div>

      {simulation ? (
        <>
          <nav className="trade-analysis-tabs" aria-label="Trade analysis sections">
            {analysisTabs(t).map((tab) => (
              <button
                key={tab.id}
                className={`trade-analysis-tab ${
                  activeTab === tab.id ? "trade-analysis-tab--active" : ""
                }`}
                type="button"
                onClick={() => setActiveTab(tab.id)}
              >
                <span>{tab.label}</span>
                <small>{tab.description}</small>
              </button>
            ))}
          </nav>

          <div className="trade-analysis-panel">
            {activeTab === "impact" ? (
              <TradeSectionCard
                title={t("tradeSimulator.impact.title")}
                description={simulation.pre_trade_impact.interpretation}
              >
                <BeforeAfterTable
                  metrics={simulation.pre_trade_impact.metrics}
                  labels={tableLabels(t)}
                  formatValue={(metric, value) =>
                    formatImpactValue(metric, value, selectedPortfolio?.base_currency ?? "USD")
                  }
                />
              </TradeSectionCard>
            ) : null}

            {activeTab === "risk" ? (
              <TradeSectionCard
                title={t("tradeSimulator.risk.title")}
                description={simulation.risk_impact.message}
                badges={simulation.risk_impact.badges.map((badge) => ({
                  label: badge,
                  variant: "warning",
                }))}
              >
                <BeforeAfterTable
                  metrics={simulation.risk_impact.metrics}
                  labels={tableLabels(t)}
                  formatValue={(metric, value) =>
                    formatImpactValue(metric, value, selectedPortfolio?.base_currency ?? "USD")
                  }
                />
              </TradeSectionCard>
            ) : null}

            {activeTab === "suitability" ? (
              <SuitabilityAndCompliance
                simulation={simulation}
                t={t}
              />
            ) : null}

            {activeTab === "costs" ? (
              <CostsAndExecution
                simulation={simulation}
                currency={selectedPortfolio?.base_currency ?? "USD"}
                t={t}
              />
            ) : null}

            {activeTab === "benchmark" ? (
              <BenchmarkPanel
                simulation={simulation}
                t={t}
              />
            ) : null}

            {activeTab === "commentary" ? (
              <CommentaryPanel
                simulation={simulation}
                currency={selectedPortfolio?.base_currency ?? "USD"}
                t={t}
              />
            ) : null}
          </div>
        </>
      ) : null}
    </div>
  );
}

function SimulationSummary({
  simulation,
  currency,
  t,
}: {
  simulation: TradeSimulationResponse;
  currency: string;
  t: (key: string) => string;
}) {
  return (
    <div className="trade-summary-stack">
      <div className="trade-result-banner">
        <TradeStatusBadge
          label={simulation.simulation_result.trade_status}
          variant={statusVariant(simulation.simulation_result.trade_status)}
        />
        <strong>{simulation.simulation_result.main_reason}</strong>
        <p>{simulation.simulation_result.notice}</p>
      </div>
      <div className="trade-summary-grid">
        <TradeMetricCard
          title={t("tradeSimulator.summary.estimatedCost")}
          value={
            <MoneyValue
              value={simulation.simulation_result.estimated_cost}
              currency={currency}
            />
          }
          subtitle={simulation.trade_ticket.trade_rationale}
        />
        <TradeMetricCard
          title={t("tradeSimulator.summary.riskImpact")}
          value={simulation.simulation_result.risk_impact}
          subtitle={simulation.simulation_result.suitability_result}
          tone={
            simulation.simulation_result.trade_status === "Approved"
              ? "positive"
              : "warning"
          }
        />
        <TradeMetricCard
          title={t("tradeSimulator.summary.cashAfter")}
          value={
            <MoneyValue
              value={simulation.trade_ticket.estimated_cash_after_trade}
              currency={currency}
            />
          }
          subtitle={t("tradeSimulator.ticket.estimatedCashAfter")}
        />
      </div>
      {simulation.simulation_result.key_warnings.length ? (
        <div className="trade-warning-list">
          {simulation.simulation_result.key_warnings.map((warning) => (
            <p key={warning}>{warning}</p>
          ))}
        </div>
      ) : null}
    </div>
  );
}

function SuitabilityAndCompliance({
  simulation,
  t,
}: {
  simulation: TradeSimulationResponse;
  t: (key: string) => string;
}) {
  return (
    <div className="trade-two-column">
      <TradeSectionCard
        title={t("tradeSimulator.suitability.title")}
        description={simulation.suitability_review.commentary}
        badges={[
          {
            label: simulation.suitability_review.status,
            variant: statusVariant(simulation.suitability_review.status),
          },
        ]}
      >
        <div className="trade-policy-grid">
          <TradeMetricCard
            title={t("tradeSimulator.suitability.investorType")}
            value={simulation.suitability_review.investor_type}
          />
          <TradeMetricCard
            title={t("tradeSimulator.suitability.riskTolerance")}
            value={simulation.suitability_review.risk_tolerance}
          />
          <TradeMetricCard
            title={t("tradeSimulator.suitability.timeHorizon")}
            value={simulation.suitability_review.time_horizon}
          />
          <TradeMetricCard
            title={t("tradeSimulator.suitability.liquidityNeeds")}
            value={simulation.suitability_review.liquidity_needs}
          />
        </div>
        <div className="trade-badge-cluster">
          {simulation.suitability_review.factors.map((factor) => (
            <TradeStatusBadge key={factor} label={factor} variant="info" />
          ))}
        </div>
      </TradeSectionCard>

      <TradeSectionCard
        title={t("tradeSimulator.compliance.title")}
        description={t("tradeSimulator.compliance.description")}
      >
        {simulation.constraints_warnings.length ? (
          <div className="trade-warning-card-grid">
            {simulation.constraints_warnings.map((warning) => (
              <article
                className={`trade-warning-card trade-warning-card--${warning.severity}`}
                key={`${warning.name}-${warning.message}`}
              >
                <div>
                  <strong>{warning.name}</strong>
                  <TradeStatusBadge
                    label={warning.severity}
                    variant={warning.severity === "high" ? "danger" : "warning"}
                  />
                </div>
                <p>{warning.message}</p>
              </article>
            ))}
          </div>
        ) : (
          <EmptyState
            title={t("tradeSimulator.compliance.noWarnings")}
            message={t("tradeSimulator.compliance.noWarningsMessage")}
          />
        )}
      </TradeSectionCard>
    </div>
  );
}

function CostsAndExecution({
  simulation,
  currency,
  t,
}: {
  simulation: TradeSimulationResponse;
  currency: string;
  t: (key: string) => string;
}) {
  const costs = simulation.transaction_cost_analysis;
  const execution = simulation.execution_quality;

  return (
    <div className="trade-two-column">
      <TradeSectionCard
        title={t("tradeSimulator.costs.title")}
        description={costs.note}
        badges={costs.badges.map((badge) => ({ label: badge, variant: "warning" }))}
      >
        <div className="trade-cost-grid">
          <TradeMetricCard
            title={t("tradeSimulator.costs.gross")}
            value={<MoneyValue value={costs.gross_trade_value} currency={currency} />}
          />
          <TradeMetricCard
            title={t("tradeSimulator.costs.total")}
            value={<MoneyValue value={costs.total_estimated_cost} currency={currency} />}
          />
          <TradeMetricCard
            title={t("tradeSimulator.costs.percent")}
            value={<PercentValue value={costs.cost_as_percent_of_trade_value} />}
          />
          <TradeMetricCard
            title={t("tradeSimulator.costs.net")}
            value={<MoneyValue value={costs.estimated_net_trade_value} currency={currency} />}
          />
        </div>
        <CostList
          title={t("tradeSimulator.costs.explicit")}
          items={costs.explicit_costs}
          currency={currency}
        />
        <CostList
          title={t("tradeSimulator.costs.implicit")}
          items={costs.implicit_costs}
          currency={currency}
        />
      </TradeSectionCard>

      <TradeSectionCard
        title={t("tradeSimulator.execution.title")}
        description={execution.order_type_impact}
        badges={[{ label: execution.badge, variant: "warning" }]}
      >
        <div className="trade-cost-grid">
          <TradeMetricCard
            title={t("tradeSimulator.execution.expectedPrice")}
            value={<MoneyValue value={execution.expected_execution_price} currency={currency} />}
          />
          <TradeMetricCard
            title={t("tradeSimulator.execution.simulatedPrice")}
            value={<MoneyValue value={execution.simulated_execution_price} currency={currency} />}
          />
          <TradeMetricCard
            title={t("tradeSimulator.execution.shortfall")}
            value={
              <MoneyValue
                value={execution.implementation_shortfall}
                currency={currency}
              />
            }
            tone={execution.implementation_shortfall > 0 ? "warning" : "positive"}
          />
          <TradeMetricCard
            title={t("tradeSimulator.execution.priceImpact")}
            value={
              <MoneyValue
                value={execution.price_improvement_or_shortfall}
                currency={currency}
              />
            }
          />
        </div>
        {execution.liquidity_warning ? (
          <div className="trade-warning-list">
            <p>{execution.liquidity_warning}</p>
          </div>
        ) : null}
      </TradeSectionCard>
    </div>
  );
}

function BenchmarkPanel({
  simulation,
  t,
}: {
  simulation: TradeSimulationResponse;
  t: (key: string) => string;
}) {
  const benchmark = simulation.benchmark_active_risk;
  return (
    <TradeSectionCard
      title={t("tradeSimulator.benchmark.title")}
      description={benchmark.active_management_warning}
      badges={[{ label: benchmark.badge, variant: "warning" }]}
    >
      <div className="trade-cost-grid">
        <TradeMetricCard
          title={t("tradeSimulator.benchmark.name")}
          value={benchmark.benchmark_name}
        />
        <TradeMetricCard
          title={t("tradeSimulator.benchmark.activeBefore")}
          value={<PercentValue value={benchmark.active_weight_before} />}
        />
        <TradeMetricCard
          title={t("tradeSimulator.benchmark.activeAfter")}
          value={<PercentValue value={benchmark.active_weight_after} />}
        />
        <TradeMetricCard
          title={t("tradeSimulator.benchmark.activeExposure")}
          value={<PercentValue value={benchmark.active_exposure_after_trade} />}
        />
        <TradeMetricCard
          title={t("tradeSimulator.benchmark.trackingError")}
          value={<PercentValue value={benchmark.tracking_error_impact} />}
        />
        <TradeMetricCard
          title={t("tradeSimulator.benchmark.informationRatio")}
          value={
            benchmark.information_ratio_impact === null
              ? "-"
              : benchmark.information_ratio_impact.toFixed(3)
          }
        />
      </div>
    </TradeSectionCard>
  );
}

function CommentaryPanel({
  simulation,
  currency,
  t,
}: {
  simulation: TradeSimulationResponse;
  currency: string;
  t: (key: string) => string;
}) {
  return (
    <TradeSectionCard
      title={t("tradeSimulator.commentary.title")}
      description={simulation.athena_commentary.summary}
      badges={[
        { label: t("tradeSimulator.badges.deterministicCommentary"), variant: "info" },
      ]}
    >
      <div className="trade-commentary-grid">
        <div className="trade-commentary-note">
          <strong>{simulation.athena_commentary.summary}</strong>
          <ul>
            {simulation.athena_commentary.bullets.map((bullet) => (
              <li key={bullet}>{bullet}</li>
            ))}
          </ul>
        </div>
        <div className="trade-summary-stack">
          <TradeMetricCard
            title={t("tradeSimulator.summary.status")}
            value={simulation.simulation_result.trade_status}
          />
          <TradeMetricCard
            title={t("tradeSimulator.summary.estimatedCost")}
            value={
              <MoneyValue
                value={simulation.simulation_result.estimated_cost}
                currency={currency}
              />
            }
          />
          <TradeMetricCard
            title={t("tradeSimulator.summary.notice")}
            value={simulation.simulation_result.notice}
          />
        </div>
      </div>
    </TradeSectionCard>
  );
}

function CostList({
  title,
  items,
  currency,
}: {
  title: string;
  items: Record<string, number>;
  currency: string;
}) {
  return (
    <div className="trade-cost-list">
      <h3>{title}</h3>
      {Object.entries(items).map(([key, value]) => (
        <div key={key}>
          <span>{key.replace(/_/g, " ")}</span>
          <strong>
            <MoneyValue value={value} currency={currency} />
          </strong>
        </div>
      ))}
    </div>
  );
}

function analysisTabs(t: (key: string) => string) {
  return [
    {
      id: "impact" as const,
      label: t("tradeSimulator.tabs.impact"),
      description: t("tradeSimulator.tabs.impactShort"),
    },
    {
      id: "risk" as const,
      label: t("tradeSimulator.tabs.risk"),
      description: t("tradeSimulator.tabs.riskShort"),
    },
    {
      id: "suitability" as const,
      label: t("tradeSimulator.tabs.suitability"),
      description: t("tradeSimulator.tabs.suitabilityShort"),
    },
    {
      id: "costs" as const,
      label: t("tradeSimulator.tabs.costs"),
      description: t("tradeSimulator.tabs.costsShort"),
    },
    {
      id: "benchmark" as const,
      label: t("tradeSimulator.tabs.benchmark"),
      description: t("tradeSimulator.tabs.benchmarkShort"),
    },
    {
      id: "commentary" as const,
      label: t("tradeSimulator.tabs.commentary"),
      description: t("tradeSimulator.tabs.commentaryShort"),
    },
  ];
}

function tableLabels(t: (key: string) => string) {
  return {
    metric: t("tradeSimulator.table.metric"),
    before: t("tradeSimulator.table.before"),
    after: t("tradeSimulator.table.after"),
    change: t("tradeSimulator.table.change"),
    limit: t("tradeSimulator.table.limit"),
    status: t("tradeSimulator.table.status"),
  };
}

function formatImpactValue(
  metric: ImpactMetric,
  value: number | string | null,
  currency: string,
) {
  if (value === null) {
    return "-";
  }
  if (typeof value === "string") {
    return value;
  }
  if (["Portfolio value", "Cash", "VaR 95%", "CVaR 95%"].includes(metric.name)) {
    return new Intl.NumberFormat(undefined, {
      style: "currency",
      currency,
      maximumFractionDigits: 0,
    }).format(value);
  }
  if (
    metric.name.includes("weight") ||
    metric.name.includes("exposure") ||
    metric.name.includes("allocation") ||
    metric.name.includes("concentration") ||
    metric.name.includes("score") ||
    metric.name.includes("return") ||
    metric.name.includes("Volatility") ||
    metric.name.includes("drawdown") ||
    metric.name.includes("error")
  ) {
    return `${(value * 100).toFixed(2)}%`;
  }
  return value.toFixed(3);
}

function statusVariant(status?: string) {
  if (status === "Approved" || status === "Suitable") {
    return "success";
  }
  if (status === "Rejected" || status === "Not Suitable") {
    return "danger";
  }
  if (status === "Requires Review") {
    return "warning";
  }
  return "neutral";
}
