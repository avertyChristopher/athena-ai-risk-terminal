import { useMemo, useState } from "react";
import type { CSSProperties, ReactNode } from "react";
import { useQuery } from "@tanstack/react-query";

import { AthenaAICommentaryCard } from "../../../components/ai/AthenaAICommentaryCard";
import { MoneyValue } from "../../../components/finance/MoneyValue";
import { PercentValue } from "../../../components/finance/PercentValue";
import { PageHeader } from "../../../components/layout/PageHeader";
import { EmptyState } from "../../../components/ui/EmptyState";
import { LoadingState } from "../../../components/ui/LoadingState";
import { StatusBadge } from "../../../components/ui/StatusBadge";
import type { StatusBadgeVariant as BadgeVariant } from "../../../components/ui/StatusBadge";
import {
  StandaloneSymbolOption,
  SymbolSelectionMode,
  SymbolSelector,
} from "../../../components/workflow/SymbolSelector";
import { usePortfolioContext } from "../../../context/PortfolioContext";
import { useTranslation } from "../../../hooks/useTranslation";
import { apiClient } from "../../../lib/api-client";
import { endpoints } from "../../../lib/endpoints";
import type { MarketAsset } from "../../../types/market-data";
import type {
  DataSources,
  ImpliedVolatilityRequest,
  ImpliedVolatilityResponse,
  OptionPayoffPoint,
  OptionPricingRequest,
  OptionPricingResponse,
  OptionSensitivityPoint,
  OptionSide,
  OptionStrategyRequest,
  OptionStrategyResponse,
  OptionStrategyType,
  OptionType,
  OptionsPricingLabStatus,
  ParityMode,
  PricingModel,
  StrategyRiskValue,
} from "../../../types/options-pricing-lab";
import type { PositionRead } from "../../../types/portfolio";

type OptionsTab =
  | "overview"
  | "payoff"
  | "greeks"
  | "models"
  | "parity"
  | "impliedVolatility"
  | "strategy"
  | "sensitivity"
  | "workflow";

const tabs: OptionsTab[] = [
  "overview",
  "payoff",
  "greeks",
  "models",
  "parity",
  "impliedVolatility",
  "strategy",
  "sensitivity",
  "workflow",
];

const strategies: OptionStrategyType[] = [
  "covered_call",
  "protective_put",
  "long_straddle",
  "long_strangle",
  "bull_call_spread",
  "bear_put_spread",
  "collar",
  "cash_secured_put",
];

export function OptionsPricingLabPage() {
  const { t } = useTranslation();
  const {
    holdings,
    selectedHolding,
    selectedPortfolio,
    selectedSymbol: workflowSymbol,
    selectSymbol,
  } = usePortfolioContext();
  const [symbolSelectionMode, setSymbolSelectionMode] =
    useState<SymbolSelectionMode>("portfolio");
  const [selectedSymbol, setSelectedSymbol] = useState(
    workflowSymbol || selectedHolding?.symbol || "AAPL",
  );
  const [optionType, setOptionType] = useState<OptionType>("call");
  const [positionSide, setPositionSide] = useState<OptionSide>("long");
  const [pricingModel, setPricingModel] =
    useState<PricingModel>("black_scholes");
  const [strategyType, setStrategyType] =
    useState<OptionStrategyType>("covered_call");
  const [strikePrice, setStrikePrice] = useState(200);
  const [expirationDays, setExpirationDays] = useState(60);
  const [riskFreeRatePct, setRiskFreeRatePct] = useState(4.5);
  const [dividendYieldPct, setDividendYieldPct] = useState(0.5);
  const [volatilityPct, setVolatilityPct] = useState("");
  const [underlyingPriceInput, setUnderlyingPriceInput] = useState("");
  const [contractSize, setContractSize] = useState(100);
  const [quantity, setQuantity] = useState(1);
  const [binomialSteps, setBinomialSteps] = useState(75);
  const [parityMode, setParityMode] = useState<ParityMode>("theoretical");
  const [observedCallPrice, setObservedCallPrice] = useState("10");
  const [observedPutPrice, setObservedPutPrice] = useState("5");
  const [observedOptionPrice, setObservedOptionPrice] = useState("10");
  const [spotShockRange, setSpotShockRange] = useState(30);
  const [activeTab, setActiveTab] = useState<OptionsTab>("overview");

  const statusQuery = useQuery({
    queryKey: ["options-pricing-lab-status"],
    queryFn: () =>
      apiClient.get<OptionsPricingLabStatus>(endpoints.optionsPricingLabStatus),
  });

  const assetsQuery = useQuery({
    queryKey: ["market-data-assets"],
    queryFn: () => apiClient.get<MarketAsset[]>(endpoints.marketDataAssets),
  });

  const standaloneOptions = useMemo<StandaloneSymbolOption[]>(
    () =>
      (assetsQuery.data ?? []).map((asset) => ({
        symbol: asset.symbol,
        name: asset.name,
      })),
    [assetsQuery.data],
  );

  const selectedPortfolioHolding = useMemo(
    () =>
      holdings.find(
        (holding) =>
          holding.symbol.toUpperCase() === selectedSymbol.trim().toUpperCase(),
      ) ?? null,
    [holdings, selectedSymbol],
  );

  const pricePayload = useMemo<OptionPricingRequest>(
    () => ({
      underlying_symbol: selectedSymbol.trim().toUpperCase() || "AAPL",
      option_type: optionType,
      position_side: positionSide,
      underlying_price: optionalPositiveNumber(underlyingPriceInput),
      strike_price: clampNumber(strikePrice, 0.01, 1_000_000),
      time_to_expiration_days: clampNumber(expirationDays, 1, 3650),
      risk_free_rate: riskFreeRatePct / 100,
      dividend_yield: dividendYieldPct / 100,
      volatility: optionalPositiveNumber(volatilityPct, 100),
      pricing_model: pricingModel,
      binomial_steps: clampNumber(binomialSteps, 1, 500),
      contract_size: clampNumber(contractSize, 1, 10_000),
      quantity: clampNumber(quantity, 1, 10_000),
      parity_mode: parityMode,
      observed_call_price:
        parityMode === "observed" ? optionalNonNegativeNumber(observedCallPrice) : null,
      observed_put_price:
        parityMode === "observed" ? optionalNonNegativeNumber(observedPutPrice) : null,
      spot_shocks: scenarioShocks(spotShockRange),
    }),
    [
      binomialSteps,
      contractSize,
      dividendYieldPct,
      expirationDays,
      optionType,
      observedCallPrice,
      observedPutPrice,
      parityMode,
      positionSide,
      pricingModel,
      quantity,
      riskFreeRatePct,
      selectedSymbol,
      spotShockRange,
      strikePrice,
      underlyingPriceInput,
      volatilityPct,
    ],
  );

  const strategyPayload = useMemo<OptionStrategyRequest>(
    () => ({
      underlying_symbol: pricePayload.underlying_symbol,
      underlying_price: pricePayload.underlying_price,
      risk_free_rate: pricePayload.risk_free_rate,
      volatility: pricePayload.volatility,
      dividend_yield: pricePayload.dividend_yield,
      strategy_type: strategyType,
      contract_size: pricePayload.contract_size,
      quantity: pricePayload.quantity,
    }),
    [pricePayload, strategyType],
  );

  const priceQuery = useQuery({
    queryKey: ["options-pricing-lab-price", pricePayload],
    enabled: Boolean(pricePayload.underlying_symbol),
    queryFn: () =>
      apiClient.post<OptionPricingResponse>(
        endpoints.optionsPricingLabPrice,
        pricePayload,
      ),
  });

  const strategyQuery = useQuery({
    queryKey: ["options-pricing-lab-strategy", strategyPayload],
    enabled: Boolean(strategyPayload.underlying_symbol),
    queryFn: () =>
      apiClient.post<OptionStrategyResponse>(
        endpoints.optionsPricingLabStrategy,
        strategyPayload,
      ),
  });

  const impliedVolatilityPayload = useMemo<ImpliedVolatilityRequest>(
    () => ({
      underlying_symbol: pricePayload.underlying_symbol,
      option_type: pricePayload.option_type,
      observed_option_price: optionalPositiveNumber(observedOptionPrice) ?? 0.01,
      underlying_price: pricePayload.underlying_price,
      strike_price: pricePayload.strike_price,
      time_to_expiration_days: pricePayload.time_to_expiration_days,
      risk_free_rate: pricePayload.risk_free_rate,
      dividend_yield: pricePayload.dividend_yield,
      initial_guess: pricePayload.volatility,
    }),
    [observedOptionPrice, pricePayload],
  );

  const impliedVolatilityQuery = useQuery({
    queryKey: ["options-pricing-lab-implied-volatility", impliedVolatilityPayload],
    enabled: false,
    queryFn: () =>
      apiClient.post<ImpliedVolatilityResponse>(
        endpoints.optionsPricingLabImpliedVolatility,
        impliedVolatilityPayload,
      ),
  });

  const analysis = priceQuery.data;
  const strategy = strategyQuery.data;
  const isLoading =
    statusQuery.isLoading || assetsQuery.isLoading || priceQuery.isLoading;
  const isUsingHolding = Boolean(selectedPortfolioHolding);
  const baseCurrency = selectedPortfolioHolding?.currency ?? "USD";

  function handleSymbolChange(
    symbol: string,
    source?: StandaloneSymbolOption | PositionRead,
  ) {
    const nextSymbol = symbol.trim().toUpperCase();
    setSelectedSymbol(nextSymbol);
    selectSymbol(nextSymbol);
    setActiveTab("overview");

    if (isPositionRead(source)) {
      setUnderlyingPriceInput(String(source.current_price));
      setStrikePrice(roundToNearest(source.current_price, 5));
    }
  }

  function handleResetInputs() {
    setOptionType("call");
    setPositionSide("long");
    setPricingModel("black_scholes");
    setStrategyType("covered_call");
    setStrikePrice(200);
    setExpirationDays(60);
    setRiskFreeRatePct(4.5);
    setDividendYieldPct(0.5);
    setVolatilityPct("");
    setUnderlyingPriceInput("");
    setContractSize(100);
    setQuantity(1);
    setBinomialSteps(75);
    setParityMode("theoretical");
    setObservedCallPrice("10");
    setObservedPutPrice("5");
    setObservedOptionPrice("10");
    setSpotShockRange(30);
    setActiveTab("overview");
  }

  return (
    <div className="page options-lab-page risk-monitor-page">
      <PageHeader
        title={t("optionsPricingLab.title")}
        subtitle={t("optionsPricingLab.subtitle")}
      />

      <section className="risk-monitor-command-panel options-lab-command-panel">
        <div>
          <span>{t("optionsPricingLab.workbench.eyebrow")}</span>
          <h2>{t("optionsPricingLab.workbench.title")}</h2>
          <p>{t("optionsPricingLab.workbench.description")}</p>
        </div>
        <div className="options-lab-command-actions">
          <div className="risk-monitor-badge-cluster">
            <StatusBadge
              label={statusQuery.data?.status ?? t("common.loading")}
              variant={statusQuery.data?.status === "ready" ? "success" : "warning"}
            />
            <StatusBadge
              label={t("optionsPricingLab.badges.blackScholes")}
              variant="info"
            />
            <StatusBadge
              label={t("optionsPricingLab.badges.marketData")}
              variant={analysis?.data_sources.underlying_price_source === "market_data" ? "success" : "warning"}
            />
            <StatusBadge
              label={t("optionsPricingLab.badges.volatilityLab")}
              variant={
                analysis?.data_sources.volatility_source.includes("volatility_lab")
                  ? "success"
                  : "warning"
              }
            />
          </div>
          <div className="options-lab-symbol-strip">
            <span>{t("workflow.selectedPortfolio")}</span>
            <strong>{selectedPortfolio?.name ?? t("workflow.noPortfolio")}</strong>
            <small>
              {isUsingHolding
                ? `${selectedPortfolioHolding?.symbol} / ${selectedPortfolioHolding?.asset_name}`
                : t("optionsPricingLab.workflow.standalone")}
            </small>
          </div>
        </div>
      </section>

      <section className="risk-monitor-controls-panel options-lab-controls-panel">
        <div className="risk-monitor-controls-panel__header">
          <div>
            <span>{t("optionsPricingLab.controls.eyebrow")}</span>
            <h2>{t("optionsPricingLab.controls.title")}</h2>
            <p>{t("optionsPricingLab.controls.description")}</p>
          </div>
          <div className="options-lab-action-row">
            <button
              className="button button--ghost"
              type="button"
              onClick={handleResetInputs}
            >
              {t("optionsPricingLab.controls.reset")}
            </button>
            <button
              className="button button--primary"
              type="button"
              onClick={() => {
                void priceQuery.refetch();
                void strategyQuery.refetch();
              }}
            >
              {t("optionsPricingLab.controls.reprice")}
            </button>
          </div>
        </div>

        <div className="options-lab-control-layout">
          <SymbolSelector
            mode={symbolSelectionMode}
            selectedSymbol={selectedSymbol}
            standaloneOptions={standaloneOptions}
            title={t("optionsPricingLab.controls.underlying")}
            description={t("optionsPricingLab.controls.underlyingDescription")}
            onModeChange={setSymbolSelectionMode}
            onSymbolChange={handleSymbolChange}
          />

          <div className="risk-monitor-control-group">
            <h3>{t("optionsPricingLab.controls.contract")}</h3>
            <div className="risk-monitor-control-grid options-lab-input-grid">
              <label className="form-field">
                <span>{t("optionsPricingLab.controls.optionType")}</span>
                <select
                  value={optionType}
                  onChange={(event) => setOptionType(event.target.value as OptionType)}
                >
                  <option value="call">{t("optionsPricingLab.labels.call")}</option>
                  <option value="put">{t("optionsPricingLab.labels.put")}</option>
                </select>
              </label>
              <label className="form-field">
                <span>{t("optionsPricingLab.controls.side")}</span>
                <select
                  value={positionSide}
                  onChange={(event) =>
                    setPositionSide(event.target.value as OptionSide)
                  }
                >
                  <option value="long">{t("optionsPricingLab.labels.long")}</option>
                  <option value="short">{t("optionsPricingLab.labels.short")}</option>
                </select>
              </label>
              <label className="form-field">
                <span>{t("optionsPricingLab.controls.model")}</span>
                <select
                  value={pricingModel}
                  onChange={(event) =>
                    setPricingModel(event.target.value as PricingModel)
                  }
                >
                  <option value="black_scholes">
                    {t("optionsPricingLab.labels.blackScholes")}
                  </option>
                  <option value="binomial">
                    {t("optionsPricingLab.labels.binomial")}
                  </option>
                </select>
              </label>
              <label className="form-field">
                <span>{t("optionsPricingLab.controls.spot")}</span>
                <input
                  min={0}
                  placeholder={t("optionsPricingLab.controls.autoMarketData")}
                  type="number"
                  value={underlyingPriceInput}
                  onChange={(event) => setUnderlyingPriceInput(event.target.value)}
                />
              </label>
              <label className="form-field">
                <span>{t("optionsPricingLab.controls.strike")}</span>
                <input
                  min={0.01}
                  step={0.5}
                  type="number"
                  value={strikePrice}
                  onChange={(event) => setStrikePrice(Number(event.target.value))}
                />
              </label>
              <label className="form-field">
                <span>{t("optionsPricingLab.controls.expiration")}</span>
                <input
                  min={1}
                  step={1}
                  type="number"
                  value={expirationDays}
                  onChange={(event) =>
                    setExpirationDays(Number(event.target.value))
                  }
                />
              </label>
              <label className="form-field">
                <span>{t("optionsPricingLab.controls.volatility")}</span>
                <input
                  min={0}
                  placeholder={t("optionsPricingLab.controls.autoVolatility")}
                  step={0.1}
                  type="number"
                  value={volatilityPct}
                  onChange={(event) => setVolatilityPct(event.target.value)}
                />
              </label>
              <label className="form-field">
                <span>{t("optionsPricingLab.controls.riskFreeRate")}</span>
                <input
                  min={-5}
                  step={0.1}
                  type="number"
                  value={riskFreeRatePct}
                  onChange={(event) => setRiskFreeRatePct(Number(event.target.value))}
                />
              </label>
              <label className="form-field">
                <span>{t("optionsPricingLab.controls.dividendYield")}</span>
                <input
                  min={0}
                  step={0.1}
                  type="number"
                  value={dividendYieldPct}
                  onChange={(event) =>
                    setDividendYieldPct(Number(event.target.value))
                  }
                />
              </label>
              <label className="form-field">
                <span>{t("optionsPricingLab.controls.contractSize")}</span>
                <input
                  min={1}
                  step={1}
                  type="number"
                  value={contractSize}
                  onChange={(event) => setContractSize(Number(event.target.value))}
                />
              </label>
              <label className="form-field">
                <span>{t("optionsPricingLab.controls.quantity")}</span>
                <input
                  min={1}
                  step={1}
                  type="number"
                  value={quantity}
                  onChange={(event) => setQuantity(Number(event.target.value))}
                />
              </label>
              <label className="form-field">
                <span>{t("optionsPricingLab.controls.binomialSteps")}</span>
                <input
                  max={500}
                  min={1}
                  step={1}
                  type="number"
                  value={binomialSteps}
                  onChange={(event) => setBinomialSteps(Number(event.target.value))}
                />
              </label>
              <label className="form-field">
                <span>{t("optionsPricingLab.controls.parityMode")}</span>
                <select
                  value={parityMode}
                  onChange={(event) => setParityMode(event.target.value as ParityMode)}
                >
                  <option value="theoretical">
                    {t("optionsPricingLab.parity.theoretical")}
                  </option>
                  <option value="observed">
                    {t("optionsPricingLab.parity.observed")}
                  </option>
                </select>
              </label>
              {parityMode === "observed" ? (
                <>
                  <label className="form-field">
                    <span>{t("optionsPricingLab.controls.observedCallPrice")}</span>
                    <input
                      min={0}
                      step={0.01}
                      type="number"
                      value={observedCallPrice}
                      onChange={(event) => setObservedCallPrice(event.target.value)}
                    />
                  </label>
                  <label className="form-field">
                    <span>{t("optionsPricingLab.controls.observedPutPrice")}</span>
                    <input
                      min={0}
                      step={0.01}
                      type="number"
                      value={observedPutPrice}
                      onChange={(event) => setObservedPutPrice(event.target.value)}
                    />
                  </label>
                </>
              ) : null}
              <label className="form-field">
                <span>{t("optionsPricingLab.controls.spotShockRange")}</span>
                <input
                  max={90}
                  min={5}
                  step={5}
                  type="number"
                  value={spotShockRange}
                  onChange={(event) => setSpotShockRange(Number(event.target.value))}
                />
              </label>
            </div>
          </div>
        </div>

        <div className="risk-monitor-control-group options-lab-strategy-control">
          <h3>{t("optionsPricingLab.strategy.title")}</h3>
          <div className="options-lab-strategy-grid">
            {strategies.map((strategyName) => (
              <button
                className={strategyType === strategyName ? "is-active" : ""}
                key={strategyName}
                type="button"
                onClick={() => {
                  setStrategyType(strategyName);
                  setActiveTab("strategy");
                }}
              >
                <strong>{strategyLabel(strategyName, t)}</strong>
                <span>{strategyDescription(strategyName, t)}</span>
              </button>
            ))}
          </div>
        </div>
      </section>

      {isLoading ? <LoadingState label={t("common.loading")} /> : null}

      {priceQuery.isError ? (
        <EmptyState
          title={t("optionsPricingLab.empty.errorTitle")}
          message={t("optionsPricingLab.empty.errorMessage")}
        />
      ) : null}

      {analysis ? (
        <>
          <OptionsKpiGrid
            analysis={analysis}
            currency={baseCurrency}
            strategy={strategy}
            t={t}
          />

          <nav className="risk-monitor-tabs options-lab-tabs" aria-label="Options lab sections">
            {tabs.map((tab) => (
              <button
                className={`risk-monitor-tab ${
                  activeTab === tab ? "risk-monitor-tab--active" : ""
                }`}
                key={tab}
                type="button"
                onClick={() => setActiveTab(tab)}
              >
                <span>{t(`optionsPricingLab.tabs.${tab}`)}</span>
                <small>{t(`optionsPricingLab.tabs.${tab}Short`)}</small>
              </button>
            ))}
          </nav>

          <div className="risk-monitor-panel options-lab-panel">
            {activeTab === "overview" ? (
              <OverviewTab
                analysis={analysis}
                currency={baseCurrency}
                strategy={strategy}
                t={t}
              />
            ) : null}
            {activeTab === "payoff" ? (
              <PayoffTab analysis={analysis} currency={baseCurrency} t={t} />
            ) : null}
            {activeTab === "greeks" ? (
              <GreeksTab analysis={analysis} currency={baseCurrency} t={t} />
            ) : null}
            {activeTab === "models" ? (
              <ModelsTab analysis={analysis} t={t} />
            ) : null}
            {activeTab === "parity" ? (
              <ParityTab analysis={analysis} currency={baseCurrency} t={t} />
            ) : null}
            {activeTab === "impliedVolatility" ? (
              <ImpliedVolatilityTab
                currency={baseCurrency}
                observedOptionPrice={observedOptionPrice}
                query={impliedVolatilityQuery}
                setObservedOptionPrice={setObservedOptionPrice}
                t={t}
              />
            ) : null}
            {activeTab === "strategy" ? (
              <StrategyTab strategy={strategy} currency={baseCurrency} t={t} />
            ) : null}
            {activeTab === "sensitivity" ? (
              <SensitivityTab
                analysis={analysis}
                currency={baseCurrency}
                t={t}
              />
            ) : null}
            {activeTab === "workflow" ? (
              <WorkflowTab
                analysis={analysis}
                selectedPortfolioName={selectedPortfolio?.name}
                strategy={strategy}
                t={t}
              />
            ) : null}
          </div>
        </>
      ) : null}
    </div>
  );
}

function OptionsKpiGrid({
  analysis,
  currency,
  strategy,
  t,
}: {
  analysis: OptionPricingResponse;
  currency: string;
  strategy?: OptionStrategyResponse;
  t: (key: string) => string;
}) {
  return (
    <div className="risk-monitor-kpi-grid options-lab-kpi-grid">
      <MetricCard
        title={t("optionsPricingLab.kpis.optionPrice")}
        value={
          <MoneyValue
            currency={currency}
            value={analysis.pricing_summary.option_price}
          />
        }
        subtitle={modelLabel(analysis.model_details.selected_model, t)}
      />
      <MetricCard
        title={t("optionsPricingLab.kpis.contractPremium")}
        value={
          <MoneyValue
            currency={currency}
            value={analysis.pricing_summary.contract_premium}
          />
        }
        subtitle={t("optionsPricingLab.kpis.premiumSubtitle")}
      />
      <MetricCard
        title={t("optionsPricingLab.kpis.delta")}
        value={analysis.greeks.delta.toFixed(3)}
        subtitle={
          <MoneyValue
            currency={currency}
            value={analysis.greeks.delta_adjusted_exposure}
          />
        }
        tone={greekTone(analysis.greeks.delta)}
      />
      <MetricCard
        title={t("optionsPricingLab.kpis.breakeven")}
        value={
          <MoneyValue
            currency={currency}
            value={analysis.pricing_summary.breakeven_price}
          />
        }
        subtitle={formatMoneyness(analysis.pricing_summary.moneyness, t)}
      />
      <MetricCard
        title={t("optionsPricingLab.kpis.maxLoss")}
        value={formatNullableMoney(analysis.payoff_summary.max_loss, currency)}
        subtitle={analysis.payoff_summary.risk_note}
        tone="warning"
      />
      <MetricCard
        title={t("optionsPricingLab.kpis.strategyPremium")}
        value={formatNullableMoney(strategy?.net_premium ?? null, currency)}
        subtitle={strategy ? strategyLabel(strategy.strategy_summary.strategy_type, t) : "--"}
      />
    </div>
  );
}

function OverviewTab({
  analysis,
  currency,
  strategy,
  t,
}: {
  analysis: OptionPricingResponse;
  currency: string;
  strategy?: OptionStrategyResponse;
  t: (key: string) => string;
}) {
  return (
    <div className="risk-monitor-stack">
      <SectionCard
        title={t("optionsPricingLab.sections.pricingSummary")}
        description={analysis.athena_commentary.summary}
        badges={[
          {
            label: formatMoneyness(analysis.pricing_summary.moneyness, t),
            variant: moneynessVariant(analysis.pricing_summary.moneyness),
          },
          {
            label: sourceLabel(analysis.data_sources.underlying_price_source, t),
            variant: sourceVariant(analysis.data_sources.underlying_price_source),
          },
          {
            label: sourceLabel(analysis.data_sources.volatility_source, t),
            variant: sourceVariant(analysis.data_sources.volatility_source),
          },
        ]}
      >
        <div className="risk-monitor-overview-grid">
          <SimpleTable
            headers={[
              t("optionsPricingLab.table.metric"),
              t("optionsPricingLab.table.value"),
            ]}
            rows={[
              [
                t("optionsPricingLab.table.underlying"),
                analysis.input_summary.underlying_symbol,
              ],
              [
                t("optionsPricingLab.table.spot"),
                <MoneyValue
                  currency={currency}
                  key="spot"
                  value={analysis.input_summary.underlying_price}
                />,
              ],
              [
                t("optionsPricingLab.table.strike"),
                <MoneyValue
                  currency={currency}
                  key="strike"
                  value={analysis.input_summary.strike_price}
                />,
              ],
              [
                t("optionsPricingLab.table.expiration"),
                `${analysis.input_summary.time_to_expiration_days} ${t("optionsPricingLab.table.days")}`,
              ],
              [
                t("optionsPricingLab.table.volatility"),
                <PercentValue key="vol" value={analysis.input_summary.volatility} />,
              ],
              [
                t("optionsPricingLab.table.notional"),
                <MoneyValue
                  currency={currency}
                  key="notional"
                  value={analysis.pricing_summary.contract_notional}
                />,
              ],
            ]}
          />
          <div className="risk-monitor-driver-list">
            <h3>{t("optionsPricingLab.sections.keyPoints")}</h3>
            {analysis.athena_commentary.key_points.map((point) => (
              <p key={point}>{point}</p>
            ))}
            {strategy ? (
              <p>
                {t("optionsPricingLab.strategy.active")}:{" "}
                <strong>{strategyLabel(strategy.strategy_summary.strategy_type, t)}</strong>
              </p>
            ) : null}
          </div>
        </div>
      </SectionCard>

      <AthenaAICommentaryCard commentary={analysis.athena_ai_commentary} />

      <div className="risk-monitor-two-column">
        <SectionCard
          title={t("optionsPricingLab.sections.valueDecomposition")}
          description={t("optionsPricingLab.sections.valueDecompositionDescription")}
        >
          <div className="risk-monitor-mini-grid">
            <MetricCard
              title={t("optionsPricingLab.table.intrinsicValue")}
              value={
                <MoneyValue
                  currency={currency}
                  value={analysis.pricing_summary.intrinsic_value}
                />
              }
            />
            <MetricCard
              title={t("optionsPricingLab.table.timeValue")}
              value={
                <MoneyValue
                  currency={currency}
                  value={analysis.pricing_summary.time_value}
                />
              }
            />
            <MetricCard
              title={t("optionsPricingLab.table.moneynessRatio")}
              value={analysis.pricing_summary.moneyness_ratio.toFixed(3)}
            />
          </div>
        </SectionCard>

        <SectionCard
          title={t("optionsPricingLab.sections.cfaConcepts")}
          description={t("optionsPricingLab.sections.cfaConceptsDescription")}
        >
          <ul className="options-lab-note-list">
            {analysis.athena_commentary.cfa_notes.map((note) => (
              <li key={note}>{note}</li>
            ))}
          </ul>
        </SectionCard>
      </div>
      <SectionCard
        title={t("optionsPricingLab.sections.timeSensitivity")}
        description={t("optionsPricingLab.scenarios.timeCapped")}
        badges={[{
          label: `${analysis.sensitivity_analysis.scenario_metadata.expiration_days} ${t("optionsPricingLab.table.days")}`,
          variant: "info",
        }]}
      >
        <SimpleTable
          headers={[
            t("optionsPricingLab.table.daysRemaining"),
            t("optionsPricingLab.table.optionPrice"),
          ]}
          rows={analysis.sensitivity_analysis.time_decay.map((row) => [
            `${row.value ?? row.days ?? 0}`,
            <MoneyValue currency={currency} key="time-price" value={row.option_price ?? 0} />,
          ])}
        />
        <p className="risk-monitor-footnote">
          {t("optionsPricingLab.scenarios.spotAssumptions")}: {analysis.sensitivity_analysis.scenario_metadata.spot_shocks_percent.join("%, ")}%
        </p>
      </SectionCard>
    </div>
  );
}

function PayoffTab({
  analysis,
  currency,
  t,
}: {
  analysis: OptionPricingResponse;
  currency: string;
  t: (key: string) => string;
}) {
  return (
    <div className="risk-monitor-stack">
      <SectionCard
        title={t("optionsPricingLab.sections.payoff")}
        description={analysis.payoff_summary.risk_note}
      >
        <PayoffChart rows={analysis.payoff_summary.payoff_table} />
        <SimpleTable
          headers={[
            t("optionsPricingLab.table.underlyingPrice"),
            t("optionsPricingLab.table.payoff"),
            t("optionsPricingLab.table.profit"),
          ]}
          rows={analysis.payoff_summary.payoff_table.map((row) => [
            <MoneyValue currency={currency} key="u" value={row.underlying_price} />,
            <MoneyValue currency={currency} key="p" value={row.payoff} />,
            <span
              className={row.profit >= 0 ? "positive-value" : "negative-value"}
              key="profit"
            >
              <MoneyValue currency={currency} value={row.profit} />
            </span>,
          ])}
        />
      </SectionCard>
    </div>
  );
}

function GreeksTab({
  analysis,
  currency,
  t,
}: {
  analysis: OptionPricingResponse;
  currency: string;
  t: (key: string) => string;
}) {
  const rows = [
    ["delta", analysis.greeks.delta],
    ["gamma", analysis.greeks.gamma],
    ["thetaDaily", analysis.greeks.theta_daily],
    ["thetaAnnual", analysis.greeks.theta_annual],
    ["vega", analysis.greeks.vega],
    ["rho", analysis.greeks.rho],
  ] as const;

  return (
    <SectionCard
      title={t("optionsPricingLab.sections.greeks")}
      description={t("optionsPricingLab.sections.greeksDescription")}
    >
      <div className="risk-monitor-mini-grid options-lab-greek-grid">
        {rows.map(([key, value]) => (
          <MetricCard
            key={key}
            title={t(`optionsPricingLab.greeks.${key}`)}
            value={value.toFixed(key === "thetaAnnual" ? 2 : 4)}
            subtitle={analysis.greeks.interpretation[greekInterpretationKey(key)]}
            tone={greekTone(value)}
          />
        ))}
      </div>
      <SimpleTable
        headers={[
          t("optionsPricingLab.table.metric"),
          t("optionsPricingLab.table.value"),
        ]}
        rows={[
          [
            t("optionsPricingLab.greeks.deltaPerContract"),
            analysis.greeks.delta_per_contract.toFixed(2),
          ],
          [
            t("optionsPricingLab.greeks.deltaAdjustedExposure"),
            <MoneyValue
              currency={currency}
              key="delta-exposure"
              value={analysis.greeks.delta_adjusted_exposure}
            />,
          ],
          [t("optionsPricingLab.greeks.positionDelta"), analysis.greeks.position_delta.toFixed(2)],
          [t("optionsPricingLab.greeks.positionGamma"), analysis.greeks.position_gamma.toFixed(4)],
          [t("optionsPricingLab.greeks.positionTheta"), analysis.greeks.position_theta_daily.toFixed(2)],
          [t("optionsPricingLab.greeks.positionVega"), analysis.greeks.position_vega.toFixed(2)],
          [t("optionsPricingLab.greeks.positionRho"), analysis.greeks.position_rho.toFixed(2)],
          [t("optionsPricingLab.controls.contractSize"), analysis.input_summary.contract_size],
          [t("optionsPricingLab.controls.quantity"), analysis.input_summary.quantity],
        ]}
      />
    </SectionCard>
  );
}

function ModelsTab({
  analysis,
  t,
}: {
  analysis: OptionPricingResponse;
  t: (key: string) => string;
}) {
  return (
    <div className="risk-monitor-two-column">
      <SectionCard
        title={t("optionsPricingLab.sections.blackScholes")}
        description={t("optionsPricingLab.sections.blackScholesDescription")}
      >
        <SimpleTable
          headers={[
            t("optionsPricingLab.table.metric"),
            t("optionsPricingLab.table.value"),
          ]}
          rows={[
            [t("optionsPricingLab.table.d1"), analysis.model_details.black_scholes.d1.toFixed(4)],
            [t("optionsPricingLab.table.d2"), analysis.model_details.black_scholes.d2.toFixed(4)],
            [
              t("optionsPricingLab.table.assumptions"),
              analysis.model_details.black_scholes.assumptions.join(" | "),
            ],
          ]}
        />
      </SectionCard>

      <SectionCard
        title={t("optionsPricingLab.sections.binomial")}
        description={t("optionsPricingLab.sections.binomialDescription")}
      >
        <SimpleTable
          headers={[
            t("optionsPricingLab.table.metric"),
            t("optionsPricingLab.table.value"),
          ]}
          rows={[
            [
              t("optionsPricingLab.table.price"),
              analysis.model_details.binomial.price?.toFixed(4) ?? "--",
            ],
            [t("optionsPricingLab.table.upFactor"), analysis.model_details.binomial.up_factor.toFixed(5)],
            [t("optionsPricingLab.table.downFactor"), analysis.model_details.binomial.down_factor.toFixed(5)],
            [
              t("optionsPricingLab.table.riskNeutralProbability"),
              <PercentValue
                key="prob"
                value={analysis.model_details.binomial.risk_neutral_probability}
              />,
            ],
            [t("optionsPricingLab.table.steps"), analysis.model_details.binomial.steps.toFixed(0)],
            [
              t("optionsPricingLab.table.modelDifference"),
              analysis.model_details.model_difference?.toFixed(4) ?? "--",
            ],
          ]}
        />
        {!analysis.model_details.binomial.no_arbitrage_valid ? (
          <div className="risk-monitor-warning-list">
            <p>{t("optionsPricingLab.models.binomialWarning")}</p>
          </div>
        ) : null}
      </SectionCard>
    </div>
  );
}

function ParityTab({
  analysis,
  currency,
  t,
}: {
  analysis: OptionPricingResponse;
  currency: string;
  t: (key: string) => string;
}) {
  return (
    <SectionCard
      title={t("optionsPricingLab.sections.parity")}
      description={`${analysis.parity_check.label}. ${analysis.parity_check.note}`}
      badges={[
        {
          label: parityStatusLabel(analysis.parity_check.status, t),
          variant: parityVariant(analysis.parity_check.status),
        },
      ]}
    >
      <div className="risk-monitor-mini-grid">
        <MetricCard
          title={t("optionsPricingLab.parity.leftSide")}
          value={
            <MoneyValue
              currency={currency}
              value={analysis.parity_check.left_side}
            />
          }
        />
        <MetricCard
          title={t("optionsPricingLab.parity.rightSide")}
          value={
            <MoneyValue
              currency={currency}
              value={analysis.parity_check.right_side}
            />
          }
        />
        <MetricCard
          title={t("optionsPricingLab.parity.gap")}
          value={
            <MoneyValue
              currency={currency}
              value={analysis.parity_check.parity_gap}
            />
          }
          tone={Math.abs(analysis.parity_check.parity_gap) > 1 ? "warning" : "positive"}
        />
        <MetricCard
          title={t("optionsPricingLab.parity.percentageGap")}
          value={<PercentValue value={analysis.parity_check.percentage_gap} />}
        />
      </div>
      <SimpleTable
        headers={[
          t("optionsPricingLab.table.metric"),
          t("optionsPricingLab.table.value"),
        ]}
        rows={[
          [
            t("optionsPricingLab.parity.inputCall"),
            <MoneyValue currency={currency} key="call" value={analysis.parity_check.call_price} />,
          ],
          [
            t("optionsPricingLab.parity.inputPut"),
            <MoneyValue currency={currency} key="put" value={analysis.parity_check.put_price} />,
          ],
          [
            t("optionsPricingLab.parity.modelCall"),
            <MoneyValue currency={currency} key="model-call" value={analysis.parity_check.model_call_price ?? 0} />,
          ],
          [
            t("optionsPricingLab.parity.modelPut"),
            <MoneyValue currency={currency} key="model-put" value={analysis.parity_check.model_put_price ?? 0} />,
          ],
          [
            t("optionsPricingLab.parity.presentValueStrike"),
            <MoneyValue currency={currency} key="pv-strike" value={analysis.parity_check.present_value_strike} />,
          ],
          [
            t("optionsPricingLab.parity.discountedSpot"),
            <MoneyValue currency={currency} key="discounted-spot" value={analysis.parity_check.dividend_adjusted_spot} />,
          ],
        ]}
      />
      <p className="risk-monitor-footnote">{analysis.parity_check.caveat}</p>
    </SectionCard>
  );
}

function ImpliedVolatilityTab({
  currency,
  observedOptionPrice,
  query,
  setObservedOptionPrice,
  t,
}: {
  currency: string;
  observedOptionPrice: string;
  query: {
    data?: ImpliedVolatilityResponse;
    isError: boolean;
    isFetching: boolean;
    refetch: () => Promise<unknown>;
  };
  setObservedOptionPrice: (value: string) => void;
  t: (key: string) => string;
}) {
  const result = query.data;
  return (
    <SectionCard
      title={t("optionsPricingLab.iv.title")}
      description={t("optionsPricingLab.iv.description")}
      badges={result ? [{
        label: result.converged
          ? t("optionsPricingLab.iv.converged")
          : t("optionsPricingLab.iv.notConverged"),
        variant: result.converged ? "success" : "warning",
      }] : []}
    >
      <div className="options-lab-action-row">
        <label className="form-field">
          <span>{t("optionsPricingLab.iv.observedPrice")}</span>
          <input
            min={0.01}
            step={0.01}
            type="number"
            value={observedOptionPrice}
            onChange={(event) => setObservedOptionPrice(event.target.value)}
          />
        </label>
        <button
          className="button button--primary"
          disabled={query.isFetching}
          type="button"
          onClick={() => void query.refetch()}
        >
          {query.isFetching
            ? t("common.loading")
            : t("optionsPricingLab.iv.calculate")}
        </button>
      </div>
      {query.isError ? (
        <EmptyState
          title={t("optionsPricingLab.iv.notConverged")}
          message={t("optionsPricingLab.iv.requestError")}
        />
      ) : null}
      {result ? (
        <>
          <div className="risk-monitor-mini-grid">
            <MetricCard
              title={t("optionsPricingLab.iv.impliedVolatility")}
              value={result.implied_volatility === null
                ? "--"
                : <PercentValue value={result.implied_volatility} />}
            />
            <MetricCard
              title={t("optionsPricingLab.iv.lowerBound")}
              value={<MoneyValue currency={currency} value={result.no_arbitrage_bounds.lower_bound} />}
            />
            <MetricCard
              title={t("optionsPricingLab.iv.upperBound")}
              value={<MoneyValue currency={currency} value={result.no_arbitrage_bounds.upper_bound} />}
            />
            <MetricCard
              title={t("optionsPricingLab.iv.modelPrice")}
              value={result.model_price_at_iv === null
                ? "--"
                : <MoneyValue currency={currency} value={result.model_price_at_iv} />}
            />
          </div>
          <p className="risk-monitor-footnote">{result.methodology}</p>
          {result.warnings.map((warning) => (
            <p className="negative-value" key={warning}>{warning}</p>
          ))}
        </>
      ) : null}
    </SectionCard>
  );
}

function StrategyTab({
  strategy,
  currency,
  t,
}: {
  strategy?: OptionStrategyResponse;
  currency: string;
  t: (key: string) => string;
}) {
  if (!strategy) {
    return (
      <EmptyState
        title={t("optionsPricingLab.empty.strategyTitle")}
        message={t("optionsPricingLab.empty.strategyMessage")}
      />
    );
  }

  return (
    <div className="risk-monitor-stack">
      <AthenaAICommentaryCard commentary={strategy.athena_ai_commentary} />
      <SectionCard
        title={strategyLabel(strategy.strategy_summary.strategy_type, t)}
        description={strategy.strategy_summary.risk_profile}
        badges={[
          {
            label: strategy.stock_leg_included
              ? t(`optionsPricingLab.strategyStockNotes.${strategy.strategy_summary.strategy_type}`)
              : t("optionsPricingLab.strategy.optionsOnly"),
            variant: strategy.stock_leg_included ? "success" : "info",
          },
        ]}
      >
        <div className="risk-monitor-mini-grid">
          <MetricCard
            title={t("optionsPricingLab.strategy.netPremium")}
            value={<MoneyValue currency={currency} value={strategy.net_premium} />}
          />
          <MetricCard
            title={t("optionsPricingLab.strategy.maxProfit")}
            value={formatRiskValue(strategy.max_profit, currency, t)}
            subtitle={strategy.max_profit.explanation}
          />
          <MetricCard
            title={t("optionsPricingLab.strategy.maxLoss")}
            value={formatRiskValue(strategy.max_loss, currency, t)}
            subtitle={strategy.max_loss.explanation}
            tone="warning"
          />
          <MetricCard
            title={t("optionsPricingLab.strategy.collateral")}
            value={<MoneyValue currency={currency} value={strategy.collateral_requirement} />}
          />
          <MetricCard
            title={t("optionsPricingLab.strategy.breakevens")}
            value={strategy.breakeven_points.length
              ? strategy.breakeven_points.map((point) => formatMoney(point, currency)).join(" / ")
              : "--"}
          />
        </div>
        <div className="risk-monitor-driver-list">
          <p><strong>{t("optionsPricingLab.strategy.objective")}:</strong> {t(`optionsPricingLab.strategyObjectives.${strategy.strategy_summary.strategy_type}`)}</p>
          <p><strong>{t("optionsPricingLab.strategy.marketView")}:</strong> {t(`optionsPricingLab.strategyMarketViews.${strategy.strategy_summary.strategy_type}`)}</p>
          <p><strong>{t("optionsPricingLab.strategy.profile")}:</strong> {strategy.payoff_profile.join(" | ")}</p>
        </div>
        <div className="risk-monitor-two-column">
          <SimpleTable
            headers={[
              t("optionsPricingLab.table.leg"),
              t("optionsPricingLab.table.legType"),
              t("optionsPricingLab.table.side"),
              t("optionsPricingLab.table.strike"),
              t("optionsPricingLab.table.premium"),
              t("optionsPricingLab.controls.contractSize"),
              t("optionsPricingLab.controls.quantity"),
            ]}
            rows={strategy.legs.map((leg, index) => [
              `${index + 1}. ${leg.description}`,
              t(`optionsPricingLab.legTypes.${leg.leg_type}`),
              sideLabel(leg.side, t),
              leg.strike_price === null
                ? "--"
                : <MoneyValue currency={currency} key="strike" value={leg.strike_price} />,
              <MoneyValue
                currency={currency}
                key="premium"
                value={leg.premium ?? 0}
              />,
              leg.contract_size,
              leg.quantity,
            ])}
          />
          <div className="risk-monitor-driver-list">
            <h3>{t("optionsPricingLab.strategy.commentary")}</h3>
            {strategy.commentary.key_points.map((point) => (
              <p key={point}>{point}</p>
            ))}
            <p>{strategy.risk_summary.cfa_explanation}</p>
            {strategy.risk_notes.map((note) => <p key={note}>{note}</p>)}
          </div>
        </div>
      </SectionCard>

      <SectionCard
        title={t("optionsPricingLab.strategy.positionGreeks")}
        description={strategy.aggregate_greeks.unit_metadata.delta}
      >
        <div className="risk-monitor-mini-grid">
          <MetricCard title={t("optionsPricingLab.greeks.delta")} value={strategy.aggregate_greeks.aggregate_delta.toFixed(2)} />
          <MetricCard title={t("optionsPricingLab.greeks.gamma")} value={strategy.aggregate_greeks.aggregate_gamma.toFixed(4)} />
          <MetricCard title={t("optionsPricingLab.greeks.thetaDaily")} value={strategy.aggregate_greeks.aggregate_theta.toFixed(2)} />
          <MetricCard title={t("optionsPricingLab.greeks.deltaAdjustedExposure")} value={<MoneyValue currency={currency} value={strategy.aggregate_greeks.delta_adjusted_exposure} />} />
        </div>
        <SimpleTable
          headers={[
            t("optionsPricingLab.table.leg"),
            t("optionsPricingLab.greeks.rawGreeks"),
            t("optionsPricingLab.greeks.positionGreeks"),
            t("optionsPricingLab.controls.contractSize"),
            t("optionsPricingLab.controls.quantity"),
          ]}
          rows={strategy.aggregate_greeks.legs.map((leg, index) => [
            `${index + 1}. ${leg.description}`,
            formatGreekSet(leg.raw_greeks, 4),
            formatGreekSet(leg.position_greeks, 2),
            leg.contract_size,
            leg.quantity,
          ])}
        />
      </SectionCard>

      <SectionCard
        title={t("optionsPricingLab.strategy.payoffTable")}
        description={t("optionsPricingLab.strategy.payoffDescription")}
      >
        <PayoffChart rows={strategy.payoff_table} />
        <SimpleTable
          headers={[
            t("optionsPricingLab.table.underlyingPrice"),
            t("optionsPricingLab.table.payoff"),
            t("optionsPricingLab.table.profit"),
          ]}
          rows={strategy.payoff_table.map((row) => [
            <MoneyValue currency={currency} key="underlying" value={row.underlying_price} />,
            <MoneyValue currency={currency} key="payoff" value={row.payoff} />,
            <span
              className={row.profit >= 0 ? "positive-value" : "negative-value"}
              key="profit"
            >
              <MoneyValue currency={currency} value={row.profit} />
            </span>,
          ])}
        />
      </SectionCard>
    </div>
  );
}

function SensitivityTab({
  analysis,
  currency,
  t,
}: {
  analysis: OptionPricingResponse;
  currency: string;
  t: (key: string) => string;
}) {
  return (
    <div className="risk-monitor-stack">
      <SectionCard
        title={t("optionsPricingLab.sections.priceSensitivity")}
        description={t("optionsPricingLab.sections.priceSensitivityDescription")}
      >
        <SensitivityBars rows={analysis.sensitivity_analysis.price} />
        <SimpleTable
          headers={[
            t("optionsPricingLab.table.underlyingPrice"),
            t("optionsPricingLab.table.optionPrice"),
          ]}
          rows={analysis.sensitivity_analysis.price.map((row) => [
            <MoneyValue
              currency={currency}
              key="underlying"
              value={row.value ?? row.underlying_price ?? 0}
            />,
            <MoneyValue
              currency={currency}
              key="price"
              value={row.option_price ?? 0}
            />,
          ])}
        />
      </SectionCard>
      <div className="risk-monitor-two-column">
        <SectionCard
          title={t("optionsPricingLab.sections.volatilitySensitivity")}
          description={t("optionsPricingLab.sections.volatilitySensitivityDescription")}
        >
          <SimpleTable
            headers={[
              t("optionsPricingLab.table.volatility"),
              t("optionsPricingLab.table.optionPrice"),
            ]}
            rows={analysis.sensitivity_analysis.volatility.map((row) => [
              <PercentValue key="vol" value={row.value ?? row.volatility ?? 0} />,
              <MoneyValue
                currency={currency}
                key="price"
                value={row.option_price ?? 0}
              />,
            ])}
          />
        </SectionCard>
        <SectionCard
          title={t("optionsPricingLab.sections.greeksByPrice")}
          description={t("optionsPricingLab.sections.greeksByPriceDescription")}
        >
          <SimpleTable
            headers={[
              t("optionsPricingLab.table.underlyingPrice"),
              t("optionsPricingLab.greeks.delta"),
              t("optionsPricingLab.greeks.gamma"),
              t("optionsPricingLab.greeks.vega"),
            ]}
            rows={analysis.sensitivity_analysis.greeks_by_price.map((row) => [
              <MoneyValue
                currency={currency}
                key="underlying"
                value={row.underlying_price ?? 0}
              />,
              (row.delta ?? 0).toFixed(3),
              (row.gamma ?? 0).toFixed(4),
              (row.vega ?? 0).toFixed(4),
            ])}
          />
        </SectionCard>
      </div>
    </div>
  );
}

function WorkflowTab({
  analysis,
  selectedPortfolioName,
  strategy,
  t,
}: {
  analysis: OptionPricingResponse;
  selectedPortfolioName?: string;
  strategy?: OptionStrategyResponse;
  t: (key: string) => string;
}) {
  return (
    <div className="risk-monitor-stack">
      <SectionCard
        title={t("optionsPricingLab.workflow.title")}
        description={t("optionsPricingLab.workflow.description")}
      >
        <div className="options-lab-workflow-grid">
          <WorkflowStep
            label="01"
            title="Market Data"
            description={t("optionsPricingLab.workflow.marketData")}
            meta={sourceLabel(analysis.data_sources.underlying_price_source, t)}
          />
          <WorkflowStep
            label="02"
            title="Volatility Lab"
            description={t("optionsPricingLab.workflow.volatilityLab")}
            meta={sourceLabel(analysis.data_sources.volatility_source, t)}
          />
          <WorkflowStep
            label="03"
            title="Portfolio Builder"
            description={t("optionsPricingLab.workflow.portfolio")}
            meta={selectedPortfolioName ?? t("workflow.noPortfolio")}
          />
          <WorkflowStep
            label="04"
            title="Risk Monitor"
            description={t("optionsPricingLab.workflow.riskMonitor")}
            meta={analysis.greeks.delta.toFixed(3)}
          />
          <WorkflowStep
            label="05"
            title="Trade Simulator"
            description={t("optionsPricingLab.workflow.tradeSimulator")}
            meta={strategy ? strategyLabel(strategy.strategy_summary.strategy_type, t) : "--"}
          />
        </div>
        <DataSourcePanel source={analysis.data_sources} t={t} />
      </SectionCard>
    </div>
  );
}

function DataSourcePanel({
  source,
  t,
}: {
  source: DataSources;
  t: (key: string) => string;
}) {
  return (
    <div className="risk-monitor-data-source options-lab-data-source">
      <div>
        <span>{t("optionsPricingLab.dataSource.price")}</span>
        <strong>{sourceLabel(source.underlying_price_source, t)}</strong>
      </div>
      <div>
        <span>{t("optionsPricingLab.dataSource.volatility")}</span>
        <strong>{sourceLabel(source.volatility_source, t)}</strong>
      </div>
      <div>
        <span>{t("optionsPricingLab.dataSource.rates")}</span>
        <strong>{sourceLabel(source.risk_free_rate_source, t)}</strong>
      </div>
      <div>
        <span>{t("optionsPricingLab.dataSource.fallback")}</span>
        <strong>{source.fallback_used ? t("common.demoDataOnline") : "No"}</strong>
      </div>
      {source.warnings.length ? (
        <p>{source.warnings.join(" | ")}</p>
      ) : (
        <p>{t("optionsPricingLab.dataSource.clean")}</p>
      )}
    </div>
  );
}

function SectionCard({
  title,
  description,
  badges,
  children,
}: {
  title: string;
  description?: string;
  badges?: { label: string; variant?: BadgeVariant }[];
  children: ReactNode;
}) {
  return (
    <section className="risk-monitor-section-card">
      <div className="risk-monitor-section-card__header">
        <div>
          <h2>{title}</h2>
          {description ? <p>{description}</p> : null}
        </div>
        {badges?.length ? (
          <div className="risk-monitor-badge-cluster">
            {badges.map((badge) => (
              <StatusBadge
                key={badge.label}
                label={badge.label}
                variant={badge.variant}
              />
            ))}
          </div>
        ) : null}
      </div>
      {children}
    </section>
  );
}

function MetricCard({
  title,
  value,
  subtitle,
  tone = "neutral",
}: {
  title: string;
  value: ReactNode;
  subtitle?: ReactNode;
  tone?: "neutral" | "positive" | "warning" | "negative";
}) {
  return (
    <article className={`risk-monitor-metric-card risk-monitor-metric-card--${tone}`}>
      <span>{title}</span>
      <strong>{value}</strong>
      {subtitle ? <p>{subtitle}</p> : null}
    </article>
  );
}

function SimpleTable({
  headers,
  rows,
}: {
  headers: string[];
  rows: ReactNode[][];
}) {
  return (
    <div className="table-scroll">
      <table className="data-table risk-monitor-table options-lab-table">
        <thead>
          <tr>
            {headers.map((header) => (
              <th key={header}>{header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, rowIndex) => (
            <tr key={String(row[0] ?? rowIndex)}>
              {row.map((cell, cellIndex) => (
                <td
                  className={cellIndex === 0 ? "data-table__symbol" : "data-table__numeric"}
                  key={`${rowIndex}-${cellIndex}`}
                >
                  {cell}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function PayoffChart({ rows }: { rows: OptionPayoffPoint[] }) {
  const maxAbs = Math.max(...rows.map((row) => Math.abs(row.profit)), 1);
  return (
    <div className="options-lab-payoff-chart">
      {rows.map((row) => {
        const magnitude = Math.min(100, (Math.abs(row.profit) / maxAbs) * 100);
        return (
          <div key={row.underlying_price}>
            <span>{row.underlying_price.toFixed(0)}</span>
            <div>
              <i
                className={row.profit >= 0 ? "is-positive" : "is-negative"}
                style={{ "--bar-width": `${magnitude}%` } as CSSProperties}
              />
            </div>
            <strong className={row.profit >= 0 ? "positive-value" : "negative-value"}>
              {row.profit.toFixed(0)}
            </strong>
          </div>
        );
      })}
    </div>
  );
}

function SensitivityBars({ rows }: { rows: OptionSensitivityPoint[] }) {
  const maxPrice = Math.max(...rows.map((row) => row.option_price ?? 0), 1);
  return (
    <div className="options-lab-sensitivity-bars">
      {rows.map((row) => (
        <div key={row.value ?? row.underlying_price}>
          <span>{(row.value ?? row.underlying_price ?? 0).toFixed(0)}</span>
          <div>
            <i
              style={
                {
                  "--bar-width": `${Math.max(4, ((row.option_price ?? 0) / maxPrice) * 100)}%`,
                } as CSSProperties
              }
            />
          </div>
          <strong>{row.option_price?.toFixed(2)}</strong>
        </div>
      ))}
    </div>
  );
}

function WorkflowStep({
  label,
  title,
  description,
  meta,
}: {
  label: string;
  title: string;
  description: string;
  meta: string;
}) {
  return (
    <article className="options-lab-workflow-step">
      <span>{label}</span>
      <h3>{title}</h3>
      <p>{description}</p>
      <strong>{meta}</strong>
    </article>
  );
}

function optionalPositiveNumber(value: string, divisor = 1) {
  if (!value.trim()) {
    return null;
  }
  const parsed = Number(value);
  return Number.isFinite(parsed) && parsed > 0 ? parsed / divisor : null;
}

function optionalNonNegativeNumber(value: string) {
  if (!value.trim()) return null;
  const parsed = Number(value);
  return Number.isFinite(parsed) && parsed >= 0 ? parsed : null;
}

function scenarioShocks(range: number) {
  const boundedRange = clampNumber(range, 5, 90);
  const midpoint = boundedRange / 2;
  return [-boundedRange, -midpoint, 0, midpoint, boundedRange];
}

function clampNumber(value: number, minimum: number, maximum: number) {
  if (!Number.isFinite(value)) return minimum;
  return Math.min(maximum, Math.max(minimum, value));
}

function roundToNearest(value: number, step: number) {
  return Math.round(value / step) * step;
}

function isPositionRead(
  source?: StandaloneSymbolOption | PositionRead,
): source is PositionRead {
  return Boolean(source && "current_price" in source && "portfolio_id" in source);
}

function formatNullableMoney(value: number | null, currency: string) {
  if (value === null) return "Unlimited";
  return <MoneyValue currency={currency} value={value} />;
}

function formatRiskValue(
  risk: StrategyRiskValue,
  currency: string,
  t: (key: string) => string,
) {
  if (risk.type === "unlimited") return t("optionsPricingLab.strategy.unlimited");
  if (risk.type === "unknown") return t("optionsPricingLab.strategy.unknown");
  return <MoneyValue currency={currency} value={risk.value ?? 0} />;
}

function formatMoney(value: number, currency: string) {
  return new Intl.NumberFormat(undefined, {
    style: "currency",
    currency,
    maximumFractionDigits: 2,
  }).format(value);
}

function formatGreekSet(greeks: Record<string, number>, digits: number) {
  return `D ${greeks.delta.toFixed(digits)} | G ${greeks.gamma.toFixed(digits)} | T ${greeks.theta.toFixed(digits)} | V ${greeks.vega.toFixed(digits)} | R ${greeks.rho.toFixed(digits)}`;
}

function formatMoneyness(value: string, t: (key: string) => string) {
  return t(`optionsPricingLab.moneyness.${value}`);
}

function optionLabel(value: OptionType, t: (key: string) => string) {
  return t(`optionsPricingLab.labels.${value}`);
}

function sideLabel(value: OptionSide, t: (key: string) => string) {
  return t(`optionsPricingLab.labels.${value}`);
}

function modelLabel(value: PricingModel, t: (key: string) => string) {
  return t(`optionsPricingLab.labels.${value}`);
}

function strategyLabel(value: OptionStrategyType, t: (key: string) => string) {
  return t(`optionsPricingLab.strategyTypes.${value}`);
}

function strategyDescription(
  value: OptionStrategyType,
  t: (key: string) => string,
) {
  return t(`optionsPricingLab.strategyDescriptions.${value}`);
}

function sourceLabel(source: string, t: (key: string) => string) {
  if (source === "market_data") return t("optionsPricingLab.sources.marketData");
  if (source === "volatility_lab_ewma") return t("optionsPricingLab.sources.volatilityLabEwma");
  if (source === "volatility_lab_realized") return t("optionsPricingLab.sources.volatilityLabRealized");
  if (source === "manual_input") return t("optionsPricingLab.sources.manual");
  if (source === "deterministic_demo") return t("optionsPricingLab.sources.demo");
  if (source === "demo_risk_free_proxy") return t("optionsPricingLab.sources.demoRate");
  if (source === "demo_dividend_proxy") return t("optionsPricingLab.sources.demoDividend");
  return source;
}

function sourceVariant(source: string): BadgeVariant {
  if (source === "market_data" || source.includes("volatility_lab")) {
    return "success";
  }
  if (source === "manual_input") {
    return "info";
  }
  if (source.includes("demo")) {
    return "warning";
  }
  return "neutral";
}

function moneynessVariant(value: string): BadgeVariant {
  if (value === "in_the_money") return "success";
  if (value === "at_the_money") return "info";
  if (value === "out_of_the_money") return "warning";
  return "neutral";
}

function parityStatusLabel(status: string, t: (key: string) => string) {
  return t(`optionsPricingLab.parityStatus.${status}`);
}

function parityVariant(status: string): BadgeVariant {
  if (status === "aligned") return "success";
  if (status === "small_deviation") return "warning";
  return "danger";
}

function greekTone(
  value: number,
): "neutral" | "positive" | "warning" | "negative" {
  if (value > 0.05) return "positive";
  if (value < -0.05) return "negative";
  return "neutral";
}

function greekInterpretationKey(key: string) {
  if (key.startsWith("theta")) return "theta";
  return key;
}
