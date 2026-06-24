import { Link } from "react-router-dom";
import { useEffect, useMemo, useState } from "react";
import type { CSSProperties, ReactNode } from "react";
import { useQuery } from "@tanstack/react-query";

import { AthenaAICommentaryCard } from "../../../components/ai/AthenaAICommentaryCard";
import { MoneyValue } from "../../../components/finance/MoneyValue";
import { PercentValue } from "../../../components/finance/PercentValue";
import { PageHeader } from "../../../components/layout/PageHeader";
import { EmptyState } from "../../../components/ui/EmptyState";
import { LoadingState } from "../../../components/ui/LoadingState";
import { StatusBadge as VolatilityStatusBadge } from "../../../components/ui/StatusBadge";
import type { StatusBadgeVariant as BadgeVariant } from "../../../components/ui/StatusBadge";
import { PortfolioSelector } from "../../../components/workflow/PortfolioSelector";
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
import type { PositionRead } from "../../../types/portfolio";
import type {
  AthenaVolatilityCommentary,
  BenchmarkRiskSummary,
  DrawdownPoint,
  DistributionSummary,
  DownsideRiskSummary,
  DateFilterMetadata,
  MatrixSummary,
  MethodologyMetadata,
  PortfolioCoverageMetadata,
  ReturnSummary,
  ReturnQualityMetadata,
  RiskAdjustedSummary,
  RiskContributionItem,
  RollingVolatilityPoint,
  StressScenarioSummary,
  VarBacktestSummary,
  VolatilityAnalysis,
  VolatilityAssetAnalysisResponse,
  VolatilityDataSource,
  VolatilityLabStatus,
  VolatilityPortfolioAnalysisResponse,
  VolatilityRegimeSummary,
  VolatilitySummary,
} from "../../../types/volatility";
import type { RiskMonitorAnalysisResponse } from "../../../types/risk";
import { exportCsv, type CsvRow } from "../../../utils/exportCsv";
import {
  useVolatilityLabPreferences,
  type VolatilityVarMethod,
} from "../hooks/useVolatilityLabPreferences";

type AnalysisMode = "asset" | "portfolio";
type VolatilityTab =
  | "overview"
  | "rolling"
  | "distribution"
  | "downside"
  | "benchmark"
  | "portfolio"
  | "riskAdjusted"
  | "dataQuality"
  | "methodology"
  | "advanced"
  | "commentary";

const volatilityTabs: VolatilityTab[] = [
  "overview",
  "rolling",
  "distribution",
  "downside",
  "benchmark",
  "portfolio",
  "riskAdjusted",
  "dataQuality",
  "methodology",
  "advanced",
  "commentary",
];

export function VolatilityLabPage() {
  const { t } = useTranslation();
  const {
    preferences,
    resetPreferences,
    updatePreferences,
  } = useVolatilityLabPreferences();
  const {
    holdings,
    selectedHolding,
    selectedPortfolio,
    selectedPortfolioId,
    selectedSymbol: workflowSymbol,
    selectPortfolio,
    selectSymbol,
  } = usePortfolioContext();
  const [analysisMode, setAnalysisMode] = useState<AnalysisMode>(
    preferences.analysisMode,
  );
  const [symbolSelectionMode, setSymbolSelectionMode] =
    useState<SymbolSelectionMode>("portfolio");
  const [selectedSymbol, setSelectedSymbol] = useState(
    workflowSymbol || preferences.selectedSymbol,
  );
  const [benchmarkSymbol, setBenchmarkSymbol] = useState(
    selectedPortfolio?.benchmark || preferences.benchmarkSymbol,
  );
  const [rollingWindow, setRollingWindow] = useState(preferences.rollingWindow);
  const [confidenceLevel, setConfidenceLevel] = useState(
    preferences.confidenceLevel,
  );
  const [riskFreeRate, setRiskFreeRate] = useState(preferences.riskFreeRate);
  const [startDate, setStartDate] = useState(preferences.startDate);
  const [endDate, setEndDate] = useState(preferences.endDate);
  const [horizonDays, setHorizonDays] = useState(preferences.horizonDays);
  const [selectedVarMethod, setSelectedVarMethod] =
    useState<VolatilityVarMethod>(preferences.selectedVarMethod);
  const [activeTab, setActiveTab] = useState<VolatilityTab>("overview");
  const [preferenceMessage, setPreferenceMessage] = useState("");
  const [riskMonitorMessage, setRiskMonitorMessage] = useState("");

  const statusQuery = useQuery({
    queryKey: ["volatility-lab-status"],
    queryFn: () =>
      apiClient.get<VolatilityLabStatus>(endpoints.volatilityLabStatus),
  });

  const assetsQuery = useQuery({
    queryKey: ["market-data-assets"],
    queryFn: () => apiClient.get<MarketAsset[]>(endpoints.marketDataAssets),
  });

  const assets = assetsQuery.data ?? [];
  const standaloneOptions = useMemo<StandaloneSymbolOption[]>(
    () =>
      assets.map((asset) => ({
        symbol: asset.symbol,
        name: asset.name,
      })),
    [assets],
  );
  const holdingsSignature = useMemo(
    () =>
      holdings
        .map(
          (holding) =>
            [
              holding.id,
              holding.symbol,
              holding.quantity,
              holding.current_price,
              holding.portfolio_weight,
            ].join(":"),
        )
        .join("|"),
    [holdings],
  );
  const dateRangeInvalid = Boolean(startDate && endDate && startDate > endDate);
  const dateRangeTooShort = useMemo(() => {
    if (!startDate || !endDate || dateRangeInvalid) {
      return false;
    }
    const start = new Date(startDate);
    const end = new Date(endDate);
    const days = Math.ceil((end.getTime() - start.getTime()) / 86400000);
    return days < Math.max(rollingWindow + 1, 5);
  }, [dateRangeInvalid, endDate, rollingWindow, startDate]);

  useEffect(() => {
    if (workflowSymbol && workflowSymbol !== selectedSymbol) {
      setSelectedSymbol(workflowSymbol);
    }
  }, [selectedSymbol, workflowSymbol]);

  useEffect(() => {
    if (selectedPortfolio?.benchmark) {
      setBenchmarkSymbol(selectedPortfolio.benchmark);
    }
  }, [selectedPortfolio?.benchmark]);

  useEffect(() => {
    if (preferences.selectedPortfolioId && !selectedPortfolioId) {
      selectPortfolio(preferences.selectedPortfolioId);
    }
  }, [preferences.selectedPortfolioId, selectPortfolio, selectedPortfolioId]);

  useEffect(() => {
    updatePreferences({
      analysisMode,
      selectedSymbol,
      selectedPortfolioId: selectedPortfolio?.id ?? selectedPortfolioId,
      benchmarkSymbol,
      rollingWindow,
      confidenceLevel,
      riskFreeRate,
      startDate,
      endDate,
      horizonDays,
      selectedVarMethod,
    });
    setPreferenceMessage(t("volatilityLab.preferences.saved"));
  }, [
    analysisMode,
    benchmarkSymbol,
    confidenceLevel,
    endDate,
    horizonDays,
    riskFreeRate,
    rollingWindow,
    selectedPortfolio?.id,
    selectedPortfolioId,
    selectedSymbol,
    selectedVarMethod,
    startDate,
  ]);

  useEffect(() => {
    if (!selectedPortfolioId && holdings.length === 0) {
      setAnalysisMode("asset");
    }
  }, [holdings.length, selectedPortfolioId]);

  const analysisQuery = useQuery<VolatilityAnalysis>({
    queryKey: [
      "volatility-lab-analysis",
      analysisMode,
      selectedSymbol,
      selectedPortfolio?.id,
      benchmarkSymbol,
      rollingWindow,
      confidenceLevel,
      riskFreeRate,
      startDate,
      endDate,
      horizonDays,
      holdingsSignature,
    ],
    enabled:
      !dateRangeInvalid &&
      (analysisMode === "asset"
        ? Boolean(selectedSymbol.trim())
        : Boolean(selectedPortfolio?.id)),
    queryFn: () => {
      const sharedPayload = {
        benchmark_symbol: benchmarkSymbol.trim().toUpperCase() || "SPY",
        rolling_window: rollingWindow,
        confidence_level: confidenceLevel,
        risk_free_rate: riskFreeRate,
        start_date: startDate || null,
        end_date: endDate || null,
        horizon_days: horizonDays,
      };

      if (analysisMode === "asset") {
        return apiClient.post<VolatilityAssetAnalysisResponse>(
          endpoints.volatilityLabAnalyzeAsset,
          {
            ...sharedPayload,
            symbol: selectedSymbol.trim().toUpperCase(),
          },
        );
      }

      if (!selectedPortfolio?.id) {
        throw new Error("Portfolio is required for portfolio volatility analysis.");
      }

      return apiClient.post<VolatilityPortfolioAnalysisResponse>(
        endpoints.volatilityLabAnalyzePortfolio,
        {
          ...sharedPayload,
          portfolio_id: selectedPortfolio.id,
        },
      );
    },
  });

  const analysis = analysisQuery.data;
  const isLoading =
    statusQuery.isLoading || assetsQuery.isLoading || analysisQuery.isLoading;
  const baseCurrency = selectedPortfolio?.base_currency ?? "USD";
  const analysisTitle = analysis
    ? isPortfolioAnalysis(analysis)
      ? analysis.portfolio_name
      : analysis.symbol
    : analysisMode === "portfolio"
      ? selectedPortfolio?.name ?? t("workflow.noPortfolio")
      : selectedSymbol.toUpperCase();
  const insufficientObservations = Boolean(
    analysis && analysis.return_summary.observations < rollingWindow,
  );
  const dateRangeLabel =
    startDate || endDate
      ? `${startDate || t("volatilityLab.controls.openStart")} / ${
          endDate || t("volatilityLab.controls.openEnd")
        }`
      : t("volatilityLab.controls.defaultRange");

  function handleSymbolChange(
    symbol: string,
    source?: StandaloneSymbolOption | PositionRead,
  ) {
    const nextSymbol = symbol.trim().toUpperCase();
    setSelectedSymbol(nextSymbol);
    selectSymbol(nextSymbol);

    if (isPositionRead(source)) {
      setBenchmarkSymbol(selectedPortfolio?.benchmark ?? benchmarkSymbol);
    }
  }

  function handleResetFilters() {
    setStartDate("");
    setEndDate("");
    setRollingWindow(20);
    setConfidenceLevel(0.95);
    setRiskFreeRate(0.02);
    setHorizonDays(1);
    setSelectedVarMethod("historical");
    setPreferenceMessage(t("volatilityLab.preferences.reset"));
  }

  function handleResetPreferences() {
    resetPreferences();
    setAnalysisMode("portfolio");
    setSelectedSymbol("AAPL");
    setBenchmarkSymbol(selectedPortfolio?.benchmark || "SPY");
    handleResetFilters();
  }

  function handleExportCsv() {
    if (!analysis) {
      return;
    }
    exportCsv(buildCsvFilename(analysis), buildVolatilityCsvRows(analysis));
  }

  function handlePrintReport() {
    window.print();
  }

  async function handleSendToRiskMonitor() {
    if (!analysis) {
      return;
    }
    setRiskMonitorMessage(t("common.loading"));
    try {
      await apiClient.post<RiskMonitorAnalysisResponse>(
        endpoints.riskMonitorAnalyzeFromVolatility,
        analysis.risk_monitor_payload,
      );
      window.sessionStorage.setItem(
        "athena.volatilityLab.riskPayload",
        JSON.stringify(analysis.risk_monitor_payload),
      );
      setRiskMonitorMessage(t("volatilityLab.sections.riskMonitorSent"));
    } catch {
      setRiskMonitorMessage(t("volatilityLab.sections.riskMonitorPrepared"));
    }
  }

  return (
    <div className="page volatility-lab-page risk-monitor-page">
      <PageHeader
        title={t("volatilityLab.title")}
        subtitle={t("volatilityLab.subtitle")}
      />

      <section className="risk-monitor-command-panel volatility-lab-command-panel">
        <div>
          <span>{t("volatilityLab.workbench.eyebrow")}</span>
          <h2>{t("volatilityLab.workbench.title")}</h2>
          <p>{t("volatilityLab.workbench.description")}</p>
        </div>
        <div className="volatility-lab-command-actions">
          <div className="risk-monitor-badge-cluster">
            <VolatilityStatusBadge
              label={statusQuery.data?.status ?? t("common.loading")}
              variant={statusQuery.data?.status === "ready" ? "success" : "warning"}
            />
            <VolatilityStatusBadge
              label={`${t("volatilityLab.dataSource.observations")}: ${
                analysis?.return_summary.observations ?? "--"
              }`}
              variant={insufficientObservations ? "warning" : "info"}
            />
            {(analysis?.data_source.badges ?? [
              t("volatilityLab.badges.awaitingAnalysis"),
            ]).map((badge) => (
              <VolatilityStatusBadge
                key={badge}
                label={translateSourceBadge(badge, t)}
                variant={sourceBadgeVariant(badge)}
              />
            ))}
          </div>
          <div className="volatility-lab-export-actions">
            <button
              className="button button--ghost"
              disabled={!analysis}
              type="button"
              onClick={handleExportCsv}
            >
              {t("volatilityLab.exports.csv")}
            </button>
            <button
              className="button button--primary"
              disabled={!analysis}
              type="button"
              onClick={handlePrintReport}
            >
              {t("volatilityLab.exports.report")}
            </button>
          </div>
        </div>
      </section>

      <section className="risk-monitor-controls-panel volatility-lab-controls-panel">
        <div className="risk-monitor-controls-panel__header">
          <div>
            <span>{t("volatilityLab.controls.eyebrow")}</span>
            <h2>{t("volatilityLab.controls.title")}</h2>
            <p>{t("volatilityLab.controls.description")}</p>
          </div>
          <div className="workflow-segmented-control volatility-lab-mode-toggle">
            <button
              className={analysisMode === "portfolio" ? "is-active" : ""}
              type="button"
              onClick={() => {
                setAnalysisMode("portfolio");
                setActiveTab("overview");
              }}
            >
              {t("volatilityLab.controls.portfolioMode")}
            </button>
            <button
              className={analysisMode === "asset" ? "is-active" : ""}
              type="button"
              onClick={() => {
                setAnalysisMode("asset");
                setActiveTab("overview");
              }}
            >
              {t("volatilityLab.controls.assetMode")}
            </button>
          </div>
        </div>

        <div className="volatility-lab-control-layout">
          {analysisMode === "portfolio" ? (
            <PortfolioSelector
              compact
              showDetails
              onPortfolioChange={(portfolioId) => {
                selectPortfolio(portfolioId);
                setActiveTab("overview");
              }}
            />
          ) : (
            <SymbolSelector
              mode={symbolSelectionMode}
              selectedSymbol={selectedSymbol}
              standaloneOptions={standaloneOptions}
              title={t("volatilityLab.controls.asset")}
              description={t("volatilityLab.controls.assetDescription")}
              onModeChange={setSymbolSelectionMode}
              onSymbolChange={handleSymbolChange}
            />
          )}

          <div className="risk-monitor-control-group volatility-lab-parameter-panel">
            <h3>{t("volatilityLab.controls.parameters")}</h3>
            <div className="risk-monitor-control-grid">
              <label className="form-field">
                <span>{t("volatilityLab.controls.benchmark")}</span>
                <input
                  value={benchmarkSymbol}
                  onChange={(event) =>
                    setBenchmarkSymbol(event.target.value.toUpperCase())
                  }
                />
              </label>
              <label className="form-field">
                <span>{t("volatilityLab.controls.rollingWindow")}</span>
                <input
                  max={252}
                  min={2}
                  step={1}
                  type="number"
                  value={rollingWindow}
                  onChange={(event) =>
                    setRollingWindow(clampNumber(Number(event.target.value), 2, 252))
                  }
                />
              </label>
              <label className="form-field">
                <span>{t("volatilityLab.controls.startDate")}</span>
                <input
                  type="date"
                  value={startDate}
                  onChange={(event) => setStartDate(event.target.value)}
                />
              </label>
              <label className="form-field">
                <span>{t("volatilityLab.controls.endDate")}</span>
                <input
                  type="date"
                  value={endDate}
                  onChange={(event) => setEndDate(event.target.value)}
                />
              </label>
              <label className="form-field">
                <span>{t("volatilityLab.controls.confidence")}</span>
                <input
                  max={99}
                  min={80}
                  step={1}
                  type="number"
                  value={Math.round(confidenceLevel * 100)}
                  onChange={(event) =>
                    setConfidenceLevel(
                      clampNumber(Number(event.target.value), 80, 99) / 100,
                    )
                  }
                />
              </label>
              <label className="form-field">
                <span>{t("volatilityLab.controls.riskFreeRate")}</span>
                <input
                  max={20}
                  min={0}
                  step={0.25}
                  type="number"
                  value={Number((riskFreeRate * 100).toFixed(2))}
                  onChange={(event) =>
                    setRiskFreeRate(
                      clampNumber(Number(event.target.value), 0, 20) / 100,
                    )
                  }
                />
              </label>
              <label className="form-field">
                <span>{t("volatilityLab.controls.varMethod")}</span>
                <select
                  value={selectedVarMethod}
                  onChange={(event) =>
                    setSelectedVarMethod(event.target.value as VolatilityVarMethod)
                  }
                >
                  <option value="historical">
                    {t("volatilityLab.varMethods.historical")}
                  </option>
                  <option value="parametric">
                    {t("volatilityLab.varMethods.parametric")}
                  </option>
                  <option value="monte_carlo">
                    {t("volatilityLab.varMethods.monteCarlo")}
                  </option>
                </select>
              </label>
              <label className="form-field">
                <span>{t("volatilityLab.controls.varHorizon")}</span>
                <select
                  value={horizonDays}
                  onChange={(event) => setHorizonDays(Number(event.target.value))}
                >
                  <option value={1}>{t("volatilityLab.controls.oneDayVar")}</option>
                  <option value={5}>{t("volatilityLab.controls.fiveDayVar")}</option>
                  <option value={10}>{t("volatilityLab.controls.tenDayVar")}</option>
                </select>
              </label>
            </div>
            <div className="volatility-lab-window-buttons" role="group">
              {[20, 60, 120].map((windowValue) => (
                <button
                  className={rollingWindow === windowValue ? "is-active" : ""}
                  key={windowValue}
                  type="button"
                  onClick={() => setRollingWindow(windowValue)}
                >
                  {windowValue}
                </button>
              ))}
            </div>
            <div className="volatility-lab-filter-actions">
              <button
                className="button button--primary"
                disabled={dateRangeInvalid}
                type="button"
                onClick={() => void analysisQuery.refetch()}
              >
                {t("volatilityLab.controls.applyFilters")}
              </button>
              <button
                className="button button--ghost"
                type="button"
                onClick={handleResetFilters}
              >
                {t("volatilityLab.controls.resetFilters")}
              </button>
              <button
                className="button button--ghost"
                type="button"
                onClick={handleResetPreferences}
              >
                {t("volatilityLab.preferences.reset")}
              </button>
            </div>
            <div className="volatility-lab-filter-messages">
              <p>{preferenceMessage}</p>
              <p>
                {t("volatilityLab.controls.dateRange")}: {dateRangeLabel}
              </p>
              {dateRangeInvalid ? (
                <p className="status-message status-message--error">
                  {t("volatilityLab.validation.invalidDateRange")}
                </p>
              ) : null}
              {dateRangeTooShort ? (
                <p className="status-message status-message--warning">
                  {t("volatilityLab.validation.shortDateRange")}
                </p>
              ) : null}
              {insufficientObservations ? (
                <p className="status-message status-message--warning">
                  {t("volatilityLab.validation.insufficientObservations")}
                </p>
              ) : null}
            </div>
          </div>
        </div>
      </section>

      {isLoading ? <LoadingState label={t("common.loading")} /> : null}

      {analysisMode === "portfolio" && !selectedPortfolio && !isLoading ? (
        <EmptyState
          title={t("volatilityLab.empty.noPortfolioTitle")}
          message={t("volatilityLab.empty.noPortfolioMessage")}
        />
      ) : null}

      {analysisQuery.isError ? (
        <EmptyState
          title={t("volatilityLab.empty.errorTitle")}
          message={t("volatilityLab.empty.errorMessage")}
        />
      ) : null}

      {analysis ? (
        <>
          <div className="workflow-notice volatility-lab-notice">
            <strong>
              {t("volatilityLab.workflow.analyzing").replace(
                "{{name}}",
                analysisTitle,
              )}
            </strong>
            <span>{analysis.athena_commentary.trade_simulator_reuse_note}</span>
          </div>
          <p className="volatility-lab-disclaimer">
            {t("volatilityLab.exports.disclaimer")}
          </p>

          <VolatilityKpis
            analysis={analysis}
            currency={baseCurrency}
            t={t}
          />

          <nav className="risk-monitor-tabs" aria-label="Volatility lab sections">
            {volatilityTabs.map((tab) => (
              <button
                key={tab}
                className={`risk-monitor-tab ${
                  activeTab === tab ? "risk-monitor-tab--active" : ""
                }`}
                type="button"
                onClick={() => setActiveTab(tab)}
              >
                <span>{t(`volatilityLab.tabs.${tab}`)}</span>
                <small>{t(`volatilityLab.tabs.${tab}Short`)}</small>
              </button>
            ))}
          </nav>

          <div className="risk-monitor-panel">
            {activeTab === "overview" ? (
              <OverviewTab
                analysis={analysis}
                riskMonitorMessage={riskMonitorMessage}
                t={t}
                onSendToRiskMonitor={handleSendToRiskMonitor}
              />
            ) : null}
            {activeTab === "rolling" ? (
              <RollingTab
                drawdown={analysis.drawdown_series}
                rolling={analysis.rolling_volatility}
                summary={analysis.volatility_summary}
                t={t}
              />
            ) : null}
            {activeTab === "distribution" ? (
              <DistributionTab distribution={analysis.distribution} t={t} />
            ) : null}
            {activeTab === "downside" ? (
              <DownsideTab
                analysis={analysis}
                selectedVarMethod={selectedVarMethod}
                t={t}
              />
            ) : null}
            {activeTab === "benchmark" ? (
              <BenchmarkTab analysis={analysis} t={t} />
            ) : null}
            {activeTab === "portfolio" ? (
              <PortfolioTab analysis={analysis} t={t} />
            ) : null}
            {activeTab === "riskAdjusted" ? (
              <RiskAdjustedTab
                riskAdjusted={analysis.risk_adjusted}
                returns={analysis.return_summary}
                t={t}
              />
            ) : null}
            {activeTab === "dataQuality" ? (
              <DataQualityTab analysis={analysis} t={t} />
            ) : null}
            {activeTab === "methodology" ? (
              <MethodologyTab analysis={analysis} t={t} />
            ) : null}
            {activeTab === "advanced" ? (
              <AdvancedModelsTab analysis={analysis} t={t} />
            ) : null}
            {activeTab === "commentary" ? (
              <CommentaryTab
                aiCommentary={analysis.athena_ai_commentary}
                commentary={analysis.athena_commentary}
                t={t}
              />
            ) : null}
          </div>
          <PrintReport
            analysis={analysis}
            dateRangeLabel={dateRangeLabel}
            mode={analysisMode}
            t={t}
          />
        </>
      ) : null}
    </div>
  );
}

function VolatilityKpis({
  analysis,
  currency,
  t,
}: {
  analysis: VolatilityAnalysis;
  currency: string;
  t: (key: string) => string;
}) {
  const benchmarkBeta = isPortfolioAnalysis(analysis)
    ? analysis.portfolio_risk.beta
    : analysis.benchmark_risk.beta;
  const trackingError = isPortfolioAnalysis(analysis)
    ? analysis.portfolio_risk.tracking_error
    : analysis.risk_adjusted.tracking_error;

  return (
    <div className="risk-monitor-kpi-grid volatility-lab-kpi-grid">
      <VolatilityMetricCard
        title={t("volatilityLab.kpis.annualizedVol")}
        value={<PercentValue value={analysis.volatility_summary.annualized_volatility} />}
        subtitle={analysis.volatility_regime.regime}
        tone={volatilityTone(analysis.volatility_summary.annualized_volatility)}
      />
      <VolatilityMetricCard
        title={t("volatilityLab.kpis.ewmaVol")}
        value={formatNullablePercent(analysis.ewma_volatility.latest_volatility)}
        subtitle={translateSourceBadge(analysis.ewma_volatility.badge, t)}
        tone={volatilityTone(analysis.ewma_volatility.latest_volatility ?? 0)}
      />
      <VolatilityMetricCard
        title={t("volatilityLab.kpis.rollingVol")}
        value={formatNullablePercent(analysis.volatility_summary.rolling_latest)}
        subtitle={t("volatilityLab.kpis.latestWindow")}
      />
      <VolatilityMetricCard
        title={t("volatilityLab.kpis.beta")}
        value={benchmarkBeta.toFixed(2)}
        subtitle={analysis.benchmark_symbol}
        tone={benchmarkBeta > 1.1 ? "warning" : "neutral"}
      />
      <VolatilityMetricCard
        title={t("volatilityLab.kpis.var")}
        value={<PercentValue value={analysis.downside_risk.historical_var} />}
        subtitle={t("volatilityLab.kpis.historicalLoss")}
      />
      <VolatilityMetricCard
        title={t("volatilityLab.kpis.cvar")}
        value={<PercentValue value={analysis.downside_risk.historical_cvar} />}
        subtitle={t("volatilityLab.kpis.tailAverage")}
        tone="warning"
      />
      <VolatilityMetricCard
        title={t("volatilityLab.kpis.maxDrawdown")}
        value={<PercentValue value={analysis.downside_risk.max_drawdown} />}
        subtitle={t("volatilityLab.kpis.peakToTrough")}
        tone="negative"
      />
      <VolatilityMetricCard
        title={t("volatilityLab.kpis.sharpe")}
        value={formatRatio(analysis.risk_adjusted.sharpe_ratio)}
        subtitle={t("volatilityLab.kpis.totalRisk")}
      />
      <VolatilityMetricCard
        title={
          isPortfolioAnalysis(analysis)
            ? t("volatilityLab.kpis.trackingError")
            : t("volatilityLab.kpis.latestPrice")
        }
        value={
          isPortfolioAnalysis(analysis) ? (
            formatNullablePercent(trackingError)
          ) : analysis.latest_price === null ? (
            "--"
          ) : (
            <MoneyValue value={analysis.latest_price} currency={currency} />
          )
        }
        subtitle={
          isPortfolioAnalysis(analysis)
            ? t("volatilityLab.kpis.activeRisk")
            : analysis.symbol
        }
      />
    </div>
  );
}

function OverviewTab({
  analysis,
  riskMonitorMessage,
  t,
  onSendToRiskMonitor,
}: {
  analysis: VolatilityAnalysis;
  riskMonitorMessage: string;
  t: (key: string) => string;
  onSendToRiskMonitor: () => void;
}) {
  return (
    <div className="risk-monitor-stack">
      <VolatilitySectionCard
        title={t("volatilityLab.sections.overview")}
        description={analysis.athena_commentary.summary}
        badges={[
          {
            label: analysis.volatility_regime.regime,
            variant: regimeVariant(analysis.volatility_regime.regime),
          },
        ]}
      >
        <div className="risk-monitor-overview-grid">
          <DataSourcePanel source={analysis.data_source} t={t} />
          <RegimePanel regime={analysis.volatility_regime} t={t} />
          <RiskMonitorLinkPanel
            analysis={analysis}
            message={riskMonitorMessage}
            t={t}
            onSend={onSendToRiskMonitor}
          />
        </div>
      </VolatilitySectionCard>

      <div className="risk-monitor-two-column">
        <VolatilitySectionCard
          title={t("volatilityLab.sections.returns")}
          description={t("volatilityLab.sections.returnsDescription")}
        >
          <ReturnMetricGrid returns={analysis.return_summary} t={t} />
        </VolatilitySectionCard>
        <VolatilitySectionCard
          title={t("volatilityLab.sections.volatility")}
          description={t("volatilityLab.sections.volatilityDescription")}
        >
          <VolatilityMetricGrid volatility={analysis.volatility_summary} t={t} />
        </VolatilitySectionCard>
      </div>
    </div>
  );
}

function RollingTab({
  drawdown,
  rolling,
  summary,
  t,
}: {
  drawdown: DrawdownPoint[];
  rolling: RollingVolatilityPoint[];
  summary: VolatilitySummary;
  t: (key: string) => string;
}) {
  const visible = rolling.slice(-30);
  const maxVolatility = Math.max(
    ...visible.map((point) => point.volatility),
    summary.annualized_volatility,
    0.01,
  );

  return (
    <VolatilitySectionCard
      title={t("volatilityLab.sections.rolling")}
      description={t("volatilityLab.sections.rollingDescription")}
    >
      {visible.length ? (
        <>
          <div className="volatility-chart" aria-label="Rolling volatility chart">
            {visible.map((point) => (
              <div className="volatility-chart__column" key={point.date}>
                <span
                  className="volatility-chart__bar"
                  style={{
                    height: `${Math.max(8, (point.volatility / maxVolatility) * 100)}%`,
                  }}
                  title={`${point.date}: ${(point.volatility * 100).toFixed(2)}%`}
                />
              </div>
            ))}
          </div>
          <DrawdownChart drawdown={drawdown} t={t} />
          <div className="risk-monitor-mini-grid">
            <VolatilityMetricCard
              title={t("volatilityLab.table.latest")}
              value={formatNullablePercent(summary.rolling_latest)}
            />
            <VolatilityMetricCard
              title={t("volatilityLab.table.average")}
              value={formatNullablePercent(summary.rolling_average)}
            />
            <VolatilityMetricCard
              title={t("volatilityLab.table.minimum")}
              value={formatNullablePercent(summary.rolling_minimum)}
            />
            <VolatilityMetricCard
              title={t("volatilityLab.table.maximum")}
              value={formatNullablePercent(summary.rolling_maximum)}
            />
          </div>
          <SimpleTable
            headers={[
              t("volatilityLab.table.date"),
              t("volatilityLab.table.volatility"),
            ]}
            rows={visible
              .slice(-12)
              .reverse()
              .map((point) => [
                point.date,
                <PercentValue key={point.date} value={point.volatility} />,
              ])}
          />
        </>
      ) : (
        <EmptyState
          title={t("volatilityLab.empty.noRollingTitle")}
          message={t("volatilityLab.empty.noRollingMessage")}
        />
      )}
    </VolatilitySectionCard>
  );
}

function DrawdownChart({
  drawdown,
  t,
}: {
  drawdown: DrawdownPoint[];
  t: (key: string) => string;
}) {
  const visible = drawdown.slice(-30);
  const maxDrawdown = Math.min(...visible.map((point) => point.drawdown), 0);
  const denominator = Math.abs(maxDrawdown) || 0.01;

  if (!visible.length) {
    return null;
  }

  return (
    <div className="volatility-drawdown-panel">
      <div>
        <span>{t("volatilityLab.sections.drawdown")}</span>
        <strong><PercentValue value={maxDrawdown} /></strong>
      </div>
      <div className="volatility-drawdown-chart" aria-label="Drawdown chart">
        {visible.map((point) => (
          <span
            key={point.date}
            style={{
              height: `${Math.max(6, (Math.abs(point.drawdown) / denominator) * 100)}%`,
            }}
            title={`${point.date}: ${(point.drawdown * 100).toFixed(2)}%`}
          />
        ))}
      </div>
    </div>
  );
}

function DistributionTab({
  distribution,
  t,
}: {
  distribution: DistributionSummary;
  t: (key: string) => string;
}) {
  const maxCount = Math.max(
    ...distribution.histogram.map((bucket) => bucket.count),
    1,
  );

  return (
    <div className="risk-monitor-stack">
      <VolatilitySectionCard
        title={t("volatilityLab.sections.distribution")}
        description={distribution.normality_note}
      >
        <div className="risk-monitor-mini-grid">
          <VolatilityMetricCard
            title={t("volatilityLab.table.mean")}
            value={<PercentValue value={distribution.mean} />}
          />
          <VolatilityMetricCard
            title={t("volatilityLab.table.median")}
            value={<PercentValue value={distribution.median} />}
          />
          <VolatilityMetricCard
            title={t("volatilityLab.table.skewness")}
            value={distribution.skewness.toFixed(3)}
          />
          <VolatilityMetricCard
            title={t("volatilityLab.table.kurtosis")}
            value={distribution.kurtosis.toFixed(3)}
          />
        </div>
        <div className="volatility-histogram" aria-label="Return histogram">
          {distribution.histogram.map((bucket) => (
            <div className="volatility-histogram__row" key={bucket.bucket}>
              <span>
                {formatPercentText(bucket.lower)} / {formatPercentText(bucket.upper)}
              </span>
              <div>
                <span
                  style={{ width: `${(bucket.count / maxCount) * 100}%` }}
                />
              </div>
              <strong>{bucket.count}</strong>
            </div>
          ))}
        </div>
      </VolatilitySectionCard>

      <VolatilitySectionCard
        title={t("volatilityLab.sections.percentiles")}
        description={t("volatilityLab.sections.percentilesDescription")}
      >
        <SimpleTable
          headers={[
            t("volatilityLab.table.percentile"),
            t("volatilityLab.table.value"),
          ]}
          rows={Object.entries(distribution.percentiles).map(([label, value]) => [
            label.toUpperCase(),
            <PercentValue key={label} value={value} />,
          ])}
        />
      </VolatilitySectionCard>
    </div>
  );
}

function DownsideTab({
  analysis,
  selectedVarMethod,
  t,
}: {
  analysis: VolatilityAnalysis;
  selectedVarMethod: VolatilityVarMethod;
  t: (key: string) => string;
}) {
  const downside = analysis.downside_risk;
  const varModels = analysis.var_models;
  const selectedMethodValue = selectedVarMetric(varModels, selectedVarMethod);

  return (
    <div className="risk-monitor-stack">
      <div className="risk-monitor-two-column">
      <VolatilitySectionCard
        title={t("volatilityLab.sections.downside")}
        description={t("volatilityLab.sections.downsideDescription")}
      >
        <div className="risk-monitor-mini-grid">
          <VolatilityMetricCard
            title={t("volatilityLab.table.var")}
            value={<PercentValue value={downside.historical_var} />}
          />
          <VolatilityMetricCard
            title={t("volatilityLab.table.cvar")}
            value={<PercentValue value={downside.historical_cvar} />}
          />
          <VolatilityMetricCard
            title={t("volatilityLab.table.downsideDeviation")}
            value={<PercentValue value={downside.downside_deviation} />}
          />
          <VolatilityMetricCard
            title={t("volatilityLab.table.maxDrawdown")}
            value={<PercentValue value={downside.max_drawdown} />}
            tone="negative"
          />
          <VolatilityMetricCard
            title={t("volatilityLab.table.probabilityNegative")}
            value={<PercentValue value={downside.probability_negative_return} />}
          />
          <VolatilityMetricCard
            title={t("volatilityLab.table.worstReturn")}
            value={<PercentValue value={downside.worst_return} />}
            tone="negative"
          />
        </div>
      </VolatilitySectionCard>

      <VolatilitySectionCard
        title={t("volatilityLab.sections.varMethodology")}
        description={t("volatilityLab.sections.varMethodologyDescription")}
        badges={[
          {
            label: t(`volatilityLab.varMethods.${selectedVarMethod}`),
            variant: "info",
          },
        ]}
      >
        <div className="risk-monitor-mini-grid">
          <VolatilityMetricCard
            title={t("volatilityLab.table.selectedVar")}
            value={<PercentValue value={selectedMethodValue.varValue} />}
          />
          <VolatilityMetricCard
            title={t("volatilityLab.table.selectedCvar")}
            value={<PercentValue value={selectedMethodValue.cvarValue} />}
          />
          <VolatilityMetricCard
            title={t("volatilityLab.table.confidence")}
            value={<PercentValue value={varModels.confidence_level} />}
          />
        </div>
        <SimpleTable
          headers={[
            t("volatilityLab.table.metric"),
            t("volatilityLab.table.value"),
          ]}
          rows={[
            [t("volatilityLab.table.historicalVar"), <PercentValue key="hvar" value={varModels.historical_var} />],
            [t("volatilityLab.table.historicalCvar"), <PercentValue key="hcvar" value={varModels.historical_cvar} />],
            [t("volatilityLab.table.parametricVar"), <PercentValue key="pvar" value={varModels.parametric_var} />],
            [t("volatilityLab.table.parametricCvar"), <PercentValue key="pcvar" value={varModels.parametric_cvar} />],
            [t("volatilityLab.table.monteCarloVar"), formatNullablePercent(varModels.monte_carlo_var)],
            [t("volatilityLab.table.monteCarloCvar"), formatNullablePercent(varModels.monte_carlo_cvar)],
          ]}
        />
        <div className="risk-monitor-note-list">
          <p>{varModels.parametric_assumption}</p>
          <p>{varModels.parametric_horizon_note}</p>
          <p>{varModels.historical_horizon_note}</p>
          <p>{varModels.monte_carlo_status}</p>
        </div>
      </VolatilitySectionCard>
      </div>
      <div className="risk-monitor-two-column">
        <VarBacktestPanel backtest={analysis.var_backtest} t={t} />
        <StressScenarioPanel scenarios={analysis.stress_scenarios} t={t} />
      </div>
    </div>
  );
}

function RiskAdjustedTab({
  riskAdjusted,
  returns,
  t,
}: {
  riskAdjusted: RiskAdjustedSummary;
  returns: ReturnSummary;
  t: (key: string) => string;
}) {
  return (
    <VolatilitySectionCard
      title={t("volatilityLab.sections.riskAdjusted")}
      description={t("volatilityLab.sections.riskAdjustedDescription")}
    >
      <SimpleTable
        headers={[
          t("volatilityLab.table.metric"),
          t("volatilityLab.table.value"),
        ]}
        rows={[
          [t("volatilityLab.table.annualizedReturn"), <PercentValue key="ann" value={returns.annualized_return} />],
          [t("volatilityLab.table.excessReturn"), <PercentValue key="excess" value={returns.excess_return} />],
          [t("volatilityLab.table.activeReturn"), formatNullablePercent(returns.active_return)],
          [t("volatilityLab.table.sharpe"), formatRatio(riskAdjusted.sharpe_ratio)],
          [t("volatilityLab.table.sortino"), formatRatio(riskAdjusted.sortino_ratio)],
          [t("volatilityLab.table.treynor"), formatRatio(riskAdjusted.treynor_ratio)],
          [t("volatilityLab.table.informationRatio"), formatRatio(riskAdjusted.information_ratio)],
          [t("volatilityLab.table.trackingError"), formatNullablePercent(riskAdjusted.tracking_error)],
        ]}
      />
    </VolatilitySectionCard>
  );
}

function DataQualityTab({
  analysis,
  t,
}: {
  analysis: VolatilityAnalysis;
  t: (key: string) => string;
}) {
  return (
    <div className="risk-monitor-two-column">
      <VolatilitySectionCard
        title={t("volatilityLab.sections.dataQuality")}
        description={t("volatilityLab.sections.dataQualityDescription")}
      >
        <DataSourcePanel source={analysis.data_source} t={t} />
      </VolatilitySectionCard>
      <DateFilterPanel dateFilter={analysis.date_filter} t={t} />
      <ReturnQualityPanel quality={analysis.return_quality} t={t} />
      <VolatilitySectionCard
        title={t("volatilityLab.sections.riskMonitorLink")}
        description={t("volatilityLab.sections.riskMonitorLinkDescription")}
      >
        <RiskMonitorPayloadPanel analysis={analysis} t={t} />
      </VolatilitySectionCard>
    </div>
  );
}

function AdvancedModelsTab({
  analysis,
  t,
}: {
  analysis: VolatilityAnalysis;
  t: (key: string) => string;
}) {
  return (
    <div className="risk-monitor-stack">
      <VolatilitySectionCard
        title={t("volatilityLab.sections.advanced")}
        description={t("volatilityLab.sections.advancedDescription")}
      >
        <div className="risk-monitor-mini-grid">
          <VolatilityMetricCard
            title={t("volatilityLab.table.ewmaVolatility")}
            value={formatNullablePercent(analysis.ewma_volatility.latest_volatility)}
            subtitle={analysis.ewma_volatility.explanation}
          />
          <VolatilityMetricCard
            title={t("volatilityLab.table.lambda")}
            value={analysis.ewma_volatility.lambda_decay.toFixed(2)}
            subtitle={analysis.ewma_volatility.badge}
          />
        </div>
        <SimpleTable
          headers={[
            t("volatilityLab.table.model"),
            t("volatilityLab.table.status"),
          ]}
          rows={Object.entries(analysis.advanced_models).map(([model, status]) => [
            model.replace(/_/g, " "),
            <VolatilityStatusBadge
              key={model}
              label={advancedStatusLabel(String(status), t)}
              variant={advancedStatusVariant(String(status))}
            />,
          ])}
        />
      </VolatilitySectionCard>
    </div>
  );
}

function MethodologyTab({
  analysis,
  t,
}: {
  analysis: VolatilityAnalysis;
  t: (key: string) => string;
}) {
  return (
    <div className="risk-monitor-stack">
      <VolatilitySectionCard
        title={t("volatilityLab.sections.methodology")}
        description={t("volatilityLab.sections.methodologyDescription")}
      >
        <SimpleTable
          headers={[t("volatilityLab.table.model"), t("volatilityLab.table.value")]}
          rows={methodologyRows(analysis.methodology, t)}
        />
      </VolatilitySectionCard>
    </div>
  );
}

function BenchmarkTab({
  analysis,
  t,
}: {
  analysis: VolatilityAnalysis;
  t: (key: string) => string;
}) {
  const rows = isPortfolioAnalysis(analysis)
    ? [
        [t("volatilityLab.table.benchmark"), analysis.benchmark_symbol],
        [t("volatilityLab.table.beta"), analysis.portfolio_risk.beta.toFixed(3)],
        [
          t("volatilityLab.table.trackingError"),
          formatNullablePercent(analysis.portfolio_risk.tracking_error),
        ],
        [
          t("volatilityLab.table.largestRiskContributor"),
          analysis.portfolio_risk.largest_risk_contributor ?? "--",
        ],
      ]
    : benchmarkRows(analysis.benchmark_risk, t);

  return (
    <VolatilitySectionCard
      title={t("volatilityLab.sections.benchmark")}
      description={
        isPortfolioAnalysis(analysis)
          ? t("volatilityLab.sections.benchmarkPortfolioDescription")
          : analysis.benchmark_risk.systematic_risk_note
      }
    >
      <SimpleTable
        headers={[t("volatilityLab.table.metric"), t("volatilityLab.table.value")]}
        rows={rows}
      />
      {!isPortfolioAnalysis(analysis) ? (
        <div className="risk-monitor-note-list">
          <p>{analysis.benchmark_risk.diversification_note}</p>
        </div>
      ) : null}
    </VolatilitySectionCard>
  );
}

function PortfolioTab({
  analysis,
  t,
}: {
  analysis: VolatilityAnalysis;
  t: (key: string) => string;
}) {
  if (!isPortfolioAnalysis(analysis)) {
    return (
      <VolatilitySectionCard
        title={t("volatilityLab.sections.portfolio")}
        description={t("volatilityLab.sections.portfolioAssetModeDescription")}
      >
        <EmptyState
          title={t("volatilityLab.empty.assetModeTitle")}
          message={t("volatilityLab.empty.assetModeMessage")}
        />
      </VolatilitySectionCard>
    );
  }

  return (
    <div className="risk-monitor-stack">
      <VolatilitySectionCard
        title={t("volatilityLab.sections.portfolio")}
        description={t("volatilityLab.sections.portfolioDescription")}
        badges={[
          {
            label: `${analysis.holdings_included.length} ${t("volatilityLab.table.holdings")}`,
            variant: "info",
          },
        ]}
      >
        <div className="risk-monitor-mini-grid">
          <VolatilityMetricCard
            title={t("volatilityLab.table.covarianceVol")}
            value={<PercentValue value={analysis.portfolio_risk.covariance_based_volatility} />}
          />
          <VolatilityMetricCard
            title={t("volatilityLab.table.weightedAverageVol")}
            value={<PercentValue value={analysis.portfolio_risk.weighted_average_asset_volatility} />}
          />
          <VolatilityMetricCard
            title={t("volatilityLab.table.diversificationBenefit")}
            value={<PercentValue value={analysis.portfolio_risk.diversification_benefit} />}
            tone="positive"
          />
          <VolatilityMetricCard
            title={t("volatilityLab.table.largestRiskContributor")}
            value={analysis.portfolio_risk.largest_risk_contributor ?? "--"}
          />
        </div>
        <ContributionList contribution={analysis.risk_contribution} t={t} />
      </VolatilitySectionCard>

      <PortfolioCoveragePanel coverage={analysis.portfolio_coverage} t={t} />

      <div className="risk-monitor-two-column">
        <MatrixPanel matrix={analysis.covariance_matrix} t={t} />
        <MatrixPanel matrix={analysis.correlation_matrix} t={t} />
      </div>
    </div>
  );
}

function CommentaryTab({
  aiCommentary,
  commentary,
  t,
}: {
  aiCommentary?: VolatilityAnalysis["athena_ai_commentary"];
  commentary: AthenaVolatilityCommentary;
  t: (key: string) => string;
}) {
  return (
    <div className="risk-monitor-stack">
      <AthenaAICommentaryCard commentary={aiCommentary} />
      <VolatilitySectionCard
        title={t("volatilityLab.sections.commentary")}
        description={commentary.summary}
        badges={[{ label: t("volatilityLab.badges.deterministic"), variant: "info" }]}
      >
        <div className="risk-monitor-commentary-grid volatility-lab-commentary-grid">
          <div className="risk-monitor-driver-list">
            <h3>{t("volatilityLab.sections.keyPoints")}</h3>
            {commentary.key_points.map((point) => (
              <p key={point}>{point}</p>
            ))}
          </div>
          <div className="risk-monitor-driver-list">
            <h3>{t("volatilityLab.sections.cfaNotes")}</h3>
            {commentary.cfa_notes.map((note) => (
              <p key={note}>{note}</p>
            ))}
          </div>
        </div>
      </VolatilitySectionCard>
    </div>
  );
}

function DataSourcePanel({
  source,
  t,
}: {
  source: VolatilityDataSource;
  t: (key: string) => string;
}) {
  return (
    <div className="risk-monitor-data-source">
      <div>
        <span>{t("volatilityLab.dataSource.source")}</span>
        <strong>{sourceLabel(source.metric_source, t)}</strong>
      </div>
      <div>
        <span>{t("volatilityLab.dataSource.observations")}</span>
        <strong>{source.observations.toLocaleString()}</strong>
      </div>
      <div>
        <span>{t("volatilityLab.dataSource.missingSymbols")}</span>
        <strong>
          {source.symbols_missing.length
            ? source.symbols_missing.join(", ")
            : t("volatilityLab.dataSource.none")}
        </strong>
      </div>
      <div>
        <span>{t("volatilityLab.dataSource.fallback")}</span>
        <strong>
          {source.fallback_used
            ? t("volatilityLab.dataSource.yes")
            : t("volatilityLab.dataSource.no")}
        </strong>
      </div>
      <p>{source.fallback_reason ?? t("volatilityLab.dataSource.explanation")}</p>
      {source.warnings.map((warning) => (
        <p key={warning}>{warning}</p>
      ))}
    </div>
  );
}

function DateFilterPanel({
  dateFilter,
  t,
}: {
  dateFilter: DateFilterMetadata;
  t: (key: string) => string;
}) {
  return (
    <VolatilitySectionCard
      title={t("volatilityLab.sections.dateFilter")}
      description={t("volatilityLab.sections.dateFilterDescription")}
    >
      <SimpleTable
        headers={[t("volatilityLab.table.metric"), t("volatilityLab.table.value")]}
        rows={[
          [t("volatilityLab.controls.startDate"), dateFilter.start_date ?? "--"],
          [t("volatilityLab.controls.endDate"), dateFilter.end_date ?? "--"],
          [t("volatilityLab.table.observations"), dateFilter.observations_after_filter.toLocaleString()],
          [t("volatilityLab.table.status"), dateFilter.valid ? t("volatilityLab.dataSource.yes") : t("volatilityLab.dataSource.no")],
        ]}
      />
      <WarningList warnings={dateFilter.warnings} />
    </VolatilitySectionCard>
  );
}

function ReturnQualityPanel({
  quality,
  t,
}: {
  quality: ReturnQualityMetadata;
  t: (key: string) => string;
}) {
  return (
    <VolatilitySectionCard
      title={t("volatilityLab.sections.returnQuality")}
      description={t("volatilityLab.sections.returnQualityDescription")}
      badges={[
        {
          label: quality.has_invalid_prices
            ? t("volatilityLab.sections.invalidPriceObservations")
            : t("volatilityLab.dataSource.none"),
          variant: quality.has_invalid_prices ? "warning" : "success",
        },
      ]}
    >
      <SimpleTable
        headers={[t("volatilityLab.table.metric"), t("volatilityLab.table.value")]}
        rows={[
          [t("volatilityLab.table.priceRows"), quality.total_price_rows.toLocaleString()],
          [t("volatilityLab.table.validReturns"), quality.valid_returns.toLocaleString()],
          [t("volatilityLab.table.skippedReturns"), quality.skipped_returns.toLocaleString()],
          [
            t("volatilityLab.table.skippedReasons"),
            Object.entries(quality.skipped_reason_counts)
              .map(([reason, count]) => `${reason}: ${count}`)
              .join(", ") || "--",
          ],
        ]}
      />
      <WarningList warnings={quality.warnings} />
    </VolatilitySectionCard>
  );
}

function PortfolioCoveragePanel({
  coverage,
  t,
}: {
  coverage: PortfolioCoverageMetadata;
  t: (key: string) => string;
}) {
  return (
    <VolatilitySectionCard
      title={t("volatilityLab.sections.portfolioCoverage")}
      description={t("volatilityLab.sections.portfolioCoverageDescription")}
      badges={[
        {
          label: coverage.coverage_adjusted_risk_warning,
          variant: coverage.missing_weight >= 0.15 ? "danger" : coverage.missing_weight >= 0.05 ? "warning" : "success",
        },
      ]}
    >
      <div className="risk-monitor-mini-grid">
        <VolatilityMetricCard
          title={t("volatilityLab.table.coveredHoldings")}
          value={`${coverage.covered_holdings}/${coverage.total_holdings}`}
        />
        <VolatilityMetricCard
          title={t("volatilityLab.table.missingHoldings")}
          value={coverage.missing_holdings.toLocaleString()}
        />
        <VolatilityMetricCard
          title={t("volatilityLab.table.coverageRatio")}
          value={<PercentValue value={coverage.coverage_ratio} />}
        />
        <VolatilityMetricCard
          title={t("volatilityLab.table.missingWeight")}
          value={<PercentValue value={coverage.missing_weight} />}
          tone={coverage.missing_weight >= 0.05 ? "warning" : "neutral"}
        />
      </div>
      <WarningList
        warnings={[
          coverage.missing_weight_warning,
          coverage.risk_understatement_warning,
        ].filter(Boolean) as string[]}
      />
      {coverage.excluded_holdings.length ? (
        <SimpleTable
          headers={[t("volatilityLab.table.symbol"), t("volatilityLab.table.weight")]}
          rows={coverage.excluded_holdings.map((holding) => [
            holding.symbol,
            <PercentValue key={holding.symbol} value={holding.weight} />,
          ])}
        />
      ) : null}
    </VolatilitySectionCard>
  );
}

function VarBacktestPanel({
  backtest,
  t,
}: {
  backtest: VarBacktestSummary;
  t: (key: string) => string;
}) {
  return (
    <VolatilitySectionCard
      title={t("volatilityLab.sections.varBacktesting")}
      description={backtest.note}
      badges={[{ label: backtest.status, variant: backtest.status === "review" ? "warning" : "info" }]}
    >
      <SimpleTable
        headers={[t("volatilityLab.table.metric"), t("volatilityLab.table.value")]}
        rows={[
          [t("volatilityLab.table.observations"), backtest.observations.toLocaleString()],
          [t("volatilityLab.table.exceptions"), backtest.exceptions.toLocaleString()],
          [t("volatilityLab.table.exceptionRate"), <PercentValue key="exception-rate" value={backtest.exception_rate} />],
          [t("volatilityLab.table.expectedExceptionRate"), <PercentValue key="expected-rate" value={backtest.expected_exception_rate} />],
        ]}
      />
    </VolatilitySectionCard>
  );
}

function StressScenarioPanel({
  scenarios,
  t,
}: {
  scenarios: StressScenarioSummary[];
  t: (key: string) => string;
}) {
  return (
    <VolatilitySectionCard
      title={t("volatilityLab.sections.stressScenarios")}
      description={t("volatilityLab.sections.stressScenariosDescription")}
    >
      <SimpleTable
        headers={[
          t("volatilityLab.table.scenario"),
          t("volatilityLab.table.volatility"),
          t("volatilityLab.table.var"),
          t("volatilityLab.table.status"),
        ]}
        rows={scenarios.map((scenario) => [
          scenario.name,
          <PercentValue key={`${scenario.name}-vol`} value={scenario.stressed_volatility} />,
          <PercentValue key={`${scenario.name}-var`} value={scenario.stressed_var} />,
          scenario.risk_status,
        ])}
      />
    </VolatilitySectionCard>
  );
}

function WarningList({ warnings }: { warnings: string[] }) {
  if (!warnings.length) {
    return null;
  }
  return (
    <div className="risk-monitor-note-list">
      {warnings.map((warning) => (
        <p key={warning}>{warning}</p>
      ))}
    </div>
  );
}

function RiskMonitorLinkPanel({
  analysis,
  message,
  t,
  onSend,
}: {
  analysis: VolatilityAnalysis;
  message: string;
  t: (key: string) => string;
  onSend: () => void;
}) {
  return (
    <div className="risk-monitor-driver-list volatility-lab-link-panel">
      <h3>{t("volatilityLab.sections.riskMonitorLink")}</h3>
      <p>{t("volatilityLab.sections.riskMonitorLinkDescription")}</p>
      <div className="risk-monitor-badge-cluster">
        <VolatilityStatusBadge
          label={t("volatilityLab.badges.riskMonitorReady")}
          variant="success"
        />
        <VolatilityStatusBadge
          label={sourceLabel(analysis.risk_monitor_payload.data_source.metric_source, t)}
          variant={sourceBadgeVariant(
            analysis.risk_monitor_payload.data_source.metric_source,
          )}
        />
      </div>
      <button className="button button--ghost" type="button" onClick={onSend}>
        {t("volatilityLab.sections.sendToRiskMonitor")}
      </button>
      <Link className="button button--primary" to="/risk-monitor">
        {t("volatilityLab.sections.openRiskMonitor")}
      </Link>
      {message ? <p>{message}</p> : null}
    </div>
  );
}

function RiskMonitorPayloadPanel({
  analysis,
  t,
}: {
  analysis: VolatilityAnalysis;
  t: (key: string) => string;
}) {
  const payload = analysis.risk_monitor_payload;
  return (
    <SimpleTable
      headers={[t("volatilityLab.table.metric"), t("volatilityLab.table.value")]}
      rows={[
        [t("volatilityLab.table.sourceModule"), payload.source_module],
        [t("volatilityLab.table.generatedAt"), new Date(payload.generated_at).toLocaleString()],
        [t("volatilityLab.table.annualizedVolatility"), <PercentValue key="vol" value={payload.annualized_volatility} />],
        [t("volatilityLab.table.ewmaVolatility"), formatNullablePercent(payload.ewma_volatility)],
        [t("volatilityLab.table.historicalVar"), <PercentValue key="var" value={payload.historical_var} />],
        [t("volatilityLab.table.historicalCvar"), <PercentValue key="cvar" value={payload.historical_cvar} />],
        [t("volatilityLab.table.parametricVar"), <PercentValue key="pvar" value={payload.parametric_var} />],
        [t("volatilityLab.table.monteCarloVar"), formatNullablePercent(payload.monte_carlo_var)],
        [t("volatilityLab.table.beta"), payload.beta.toFixed(3)],
        [t("volatilityLab.table.correlation"), payload.correlation.toFixed(3)],
        [t("volatilityLab.table.trackingError"), formatNullablePercent(payload.tracking_error)],
        [t("volatilityLab.table.maxDrawdown"), <PercentValue key="dd" value={payload.max_drawdown} />],
        [t("volatilityLab.table.coverageRatio"), formatNullablePercent(payload.coverage_ratio)],
        [t("volatilityLab.dataSource.missingSymbols"), payload.missing_symbols.join(", ") || t("volatilityLab.dataSource.none")],
      ]}
    />
  );
}

function RegimePanel({
  regime,
  t,
}: {
  regime: VolatilityRegimeSummary;
  t: (key: string) => string;
}) {
  return (
    <div className="risk-monitor-driver-list volatility-regime-panel">
      <h3>{t("volatilityLab.sections.regime")}</h3>
      <strong>{regime.regime}</strong>
      <p>{regime.explanation}</p>
      <div className="risk-monitor-mini-grid">
        <VolatilityMetricCard
          title={t("volatilityLab.table.latest")}
          value={formatNullablePercent(regime.latest_volatility)}
        />
        <VolatilityMetricCard
          title={t("volatilityLab.table.referencePercentile")}
          value={formatNullablePercent(regime.reference_percentile)}
        />
      </div>
    </div>
  );
}

function ReturnMetricGrid({
  returns,
  t,
}: {
  returns: ReturnSummary;
  t: (key: string) => string;
}) {
  return (
    <div className="risk-monitor-mini-grid">
      <VolatilityMetricCard
        title={t("volatilityLab.table.observations")}
        value={returns.observations.toLocaleString()}
      />
      <VolatilityMetricCard
        title={t("volatilityLab.table.holdingPeriodReturn")}
        value={<PercentValue value={returns.holding_period_return} />}
      />
      <VolatilityMetricCard
        title={t("volatilityLab.table.annualizedReturn")}
        value={<PercentValue value={returns.annualized_return} />}
      />
      <VolatilityMetricCard
        title={t("volatilityLab.table.activeReturn")}
        value={formatNullablePercent(returns.active_return)}
      />
    </div>
  );
}

function VolatilityMetricGrid({
  volatility,
  t,
}: {
  volatility: VolatilitySummary;
  t: (key: string) => string;
}) {
  return (
    <div className="risk-monitor-mini-grid">
      <VolatilityMetricCard
        title={t("volatilityLab.table.variance")}
        value={volatility.variance.toFixed(6)}
      />
      <VolatilityMetricCard
        title={t("volatilityLab.table.standardDeviation")}
        value={<PercentValue value={volatility.standard_deviation} />}
      />
      <VolatilityMetricCard
        title={t("volatilityLab.table.realizedVol")}
        value={<PercentValue value={volatility.realized_volatility} />}
      />
      <VolatilityMetricCard
        title={t("volatilityLab.table.coefficientVariation")}
        value={formatRatio(volatility.coefficient_of_variation)}
      />
    </div>
  );
}

function MatrixPanel({
  matrix,
  t,
}: {
  matrix: MatrixSummary;
  t: (key: string) => string;
}) {
  return (
    <VolatilitySectionCard
      title={matrix.symbols.length ? matrix.symbols.join(" / ") : t("common.unavailable")}
      description={matrix.interpretation}
    >
      <div className="table-scroll">
        <table className="data-table risk-monitor-table volatility-matrix-table">
          <thead>
            <tr>
              <th>{t("volatilityLab.table.symbol")}</th>
              {matrix.symbols.map((symbol) => (
                <th key={symbol}>{symbol}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {matrix.matrix.map((row, rowIndex) => (
              <tr key={matrix.symbols[rowIndex]}>
                <td className="data-table__symbol">{matrix.symbols[rowIndex]}</td>
                {row.map((value, columnIndex) => (
                  <td
                    className="data-table__numeric"
                    key={`${matrix.symbols[rowIndex]}-${matrix.symbols[columnIndex]}`}
                    style={{ background: matrixCellBackground(value) }}
                  >
                    {value.toFixed(4)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </VolatilitySectionCard>
  );
}

function ContributionList({
  contribution,
  t,
}: {
  contribution: RiskContributionItem[];
  t: (key: string) => string;
}) {
  return (
    <div className="risk-monitor-contribution-list">
      {contribution.map((item) => (
        <div
          key={item.symbol}
          style={{
            "--contribution-width": String(Math.max(0, item.contribution)),
          } as CSSProperties}
        >
          <span>{item.symbol}</span>
          <div>
            <strong><PercentValue value={item.contribution} /></strong>
            <small>
              {t("volatilityLab.table.weight")} <PercentValue value={item.weight} />
            </small>
          </div>
        </div>
      ))}
    </div>
  );
}

function VolatilitySectionCard({
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
              <VolatilityStatusBadge
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

function VolatilityMetricCard({
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
      <table className="data-table risk-monitor-table volatility-lab-table">
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

function benchmarkRows(
  benchmark: BenchmarkRiskSummary,
  t: (key: string) => string,
) {
  return [
    [t("volatilityLab.table.benchmark"), benchmark.benchmark_symbol],
    [t("volatilityLab.table.beta"), benchmark.beta.toFixed(3)],
    [t("volatilityLab.table.correlation"), benchmark.correlation.toFixed(3)],
    [t("volatilityLab.table.covariance"), benchmark.covariance.toFixed(6)],
    [
      t("volatilityLab.table.capmRequiredReturn"),
      <PercentValue key="capm" value={benchmark.capm_required_return} />,
    ],
    [
      t("volatilityLab.table.jensenAlpha"),
      <PercentValue key="jensen" value={benchmark.jensen_alpha} />,
    ],
  ];
}

function methodologyRows(
  methodology: MethodologyMetadata,
  t: (key: string) => string,
) {
  return Object.entries(methodology).map(([family, metadata]) => [
    t(`volatilityLab.methodology.${family}`),
    Object.entries(metadata)
      .map(([key, value]) => `${key}: ${String(value)}`)
      .join(" | "),
  ]);
}

function PrintReport({
  analysis,
  dateRangeLabel,
  mode,
  t,
}: {
  analysis: VolatilityAnalysis;
  dateRangeLabel: string;
  mode: AnalysisMode;
  t: (key: string) => string;
}) {
  return (
    <section className="volatility-print-report">
      <h1>{t("volatilityLab.exports.printTitle")}</h1>
      <p>{t("volatilityLab.exports.disclaimer")}</p>
      <dl>
        <div>
          <dt>{t("volatilityLab.controls.mode")}</dt>
          <dd>
            {mode === "portfolio"
              ? t("volatilityLab.controls.portfolioMode")
              : t("volatilityLab.controls.assetMode")}
          </dd>
        </div>
        <div>
          <dt>{t("volatilityLab.table.metric")}</dt>
          <dd>{analysisTitleFromResponse(analysis)}</dd>
        </div>
        <div>
          <dt>{t("volatilityLab.controls.benchmark")}</dt>
          <dd>{analysis.benchmark_symbol}</dd>
        </div>
        <div>
          <dt>{t("volatilityLab.controls.dateRange")}</dt>
          <dd>{dateRangeLabel}</dd>
        </div>
      </dl>
      <SimpleTable
        headers={[t("volatilityLab.table.metric"), t("volatilityLab.table.value")]}
        rows={[
          [t("volatilityLab.kpis.annualizedVol"), <PercentValue key="print-vol" value={analysis.volatility_summary.annualized_volatility} />],
          [t("volatilityLab.kpis.ewmaVol"), formatNullablePercent(analysis.ewma_volatility.latest_volatility)],
          [t("volatilityLab.table.historicalVar"), <PercentValue key="print-var" value={analysis.var_models.historical_var} />],
          [t("volatilityLab.table.historicalCvar"), <PercentValue key="print-cvar" value={analysis.var_models.historical_cvar} />],
          [t("volatilityLab.table.beta"), analysis.risk_monitor_payload.beta.toFixed(3)],
          [t("volatilityLab.table.sharpe"), formatRatio(analysis.risk_adjusted.sharpe_ratio)],
          [t("volatilityLab.table.maxDrawdown"), <PercentValue key="print-dd" value={analysis.downside_risk.max_drawdown} />],
          [t("volatilityLab.dataSource.source"), sourceLabel(analysis.data_source.metric_source, t)],
        ]}
      />
      <p>{analysis.athena_commentary.summary}</p>
      <ul>
        {analysis.athena_commentary.key_points.map((point) => (
          <li key={point}>{point}</li>
        ))}
      </ul>
    </section>
  );
}

function buildVolatilityCsvRows(analysis: VolatilityAnalysis): CsvRow[] {
  const rows: CsvRow[] = [
    csvRow("summary", "mode", isPortfolioAnalysis(analysis) ? "portfolio" : "asset"),
    csvRow("summary", "name", analysisTitleFromResponse(analysis)),
    csvRow("summary", "benchmark", analysis.benchmark_symbol),
    csvRow("returns", "observations", analysis.return_summary.observations),
    csvRow("returns", "annualized_return", analysis.return_summary.annualized_return),
    csvRow("volatility", "annualized_volatility", analysis.volatility_summary.annualized_volatility),
    csvRow("volatility", "ewma_volatility", analysis.ewma_volatility.latest_volatility),
    csvRow("tail_risk", "historical_var", analysis.var_models.historical_var),
    csvRow("tail_risk", "historical_cvar", analysis.var_models.historical_cvar),
    csvRow("tail_risk", "parametric_var", analysis.var_models.parametric_var),
    csvRow("tail_risk", "parametric_cvar", analysis.var_models.parametric_cvar),
    csvRow("tail_risk", "monte_carlo_var", analysis.var_models.monte_carlo_var),
    csvRow("tail_risk", "monte_carlo_cvar", analysis.var_models.monte_carlo_cvar),
    csvRow("risk_adjusted", "sharpe_ratio", analysis.risk_adjusted.sharpe_ratio),
    csvRow("risk_adjusted", "sortino_ratio", analysis.risk_adjusted.sortino_ratio),
    csvRow("risk_adjusted", "tracking_error", analysis.risk_adjusted.tracking_error),
    csvRow("distribution", "mean", analysis.distribution.mean),
    csvRow("distribution", "median", analysis.distribution.median),
    csvRow("distribution", "skewness", analysis.distribution.skewness),
    csvRow("distribution", "kurtosis", analysis.distribution.kurtosis),
    csvRow("data_source", "metric_source", analysis.data_source.metric_source),
    csvRow("data_source", "fallback_used", analysis.data_source.fallback_used),
    csvRow("data_source", "missing_symbols", analysis.data_source.symbols_missing.join("|")),
  ];

  Object.entries(analysis.distribution.percentiles).forEach(([label, value]) => {
    rows.push(csvRow("distribution_percentiles", label, value));
  });

  if (isPortfolioAnalysis(analysis)) {
    analysis.risk_contribution.forEach((item) => {
      rows.push(csvRow("risk_contribution", item.symbol, item.contribution));
      rows.push(csvRow("risk_contribution_weight", item.symbol, item.weight));
    });
    analysis.correlation_matrix.matrix.forEach((row, rowIndex) => {
      row.forEach((value, columnIndex) => {
        rows.push(
          csvRow(
            "correlation_matrix",
            `${analysis.correlation_matrix.symbols[rowIndex]}_${analysis.correlation_matrix.symbols[columnIndex]}`,
            value,
          ),
        );
      });
    });
  }

  return rows;
}

function buildCsvFilename(analysis: VolatilityAnalysis) {
  const name = analysisTitleFromResponse(analysis)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
  return `athena-volatility-lab-${name || "analysis"}.csv`;
}

function csvRow(section: string, metric: string, value: CsvRow["value"]): CsvRow {
  return { section, metric, value };
}

function analysisTitleFromResponse(analysis: VolatilityAnalysis) {
  return isPortfolioAnalysis(analysis) ? analysis.portfolio_name : analysis.symbol;
}

function selectedVarMetric(
  varModels: VolatilityAnalysis["var_models"],
  method: VolatilityVarMethod,
) {
  if (method === "parametric") {
    return {
      varValue: varModels.parametric_var,
      cvarValue: varModels.parametric_cvar,
    };
  }
  if (method === "monte_carlo") {
    return {
      varValue: varModels.monte_carlo_var ?? 0,
      cvarValue: varModels.monte_carlo_cvar ?? 0,
    };
  }
  return {
    varValue: varModels.historical_var,
    cvarValue: varModels.historical_cvar,
  };
}

function advancedStatusLabel(status: string, t: (key: string) => string) {
  if (status === "available") return t("volatilityLab.advanced.available");
  if (status === "planned") return t("volatilityLab.advanced.planned");
  if (status.includes("options")) return t("volatilityLab.advanced.requiresOptions");
  return status;
}

function advancedStatusVariant(status: string): BadgeVariant {
  if (status === "available") return "success";
  if (status === "planned") return "info";
  return "warning";
}

function matrixCellBackground(value: number) {
  const intensity = Math.min(0.22, Math.abs(value) * 0.18);
  if (value >= 0.65) return `rgba(138, 106, 67, ${intensity + 0.08})`;
  if (value >= 0.3) return `rgba(107, 150, 195, ${intensity + 0.06})`;
  return `rgba(29, 127, 95, ${intensity + 0.04})`;
}

function isPortfolioAnalysis(
  analysis: VolatilityAnalysis,
): analysis is VolatilityPortfolioAnalysisResponse {
  return "portfolio_id" in analysis;
}

function isPositionRead(
  source?: StandaloneSymbolOption | PositionRead,
): source is PositionRead {
  return Boolean(source && "current_price" in source && "portfolio_id" in source);
}

function clampNumber(value: number, minimum: number, maximum: number) {
  if (!Number.isFinite(value)) return minimum;
  return Math.min(maximum, Math.max(minimum, value));
}

function formatRatio(value: number | null) {
  return value === null ? "--" : value.toFixed(3);
}

function formatNullablePercent(value: number | null) {
  return value === null ? "--" : <PercentValue value={value} />;
}

function formatPercentText(value: number) {
  return `${(value * 100).toFixed(2)}%`;
}

function sourceLabel(source: string, t: (key: string) => string) {
  if (source === "realized_market_data") {
    return t("volatilityLab.badges.realized");
  }
  if (source === "partial_data") {
    return t("volatilityLab.badges.partialData");
  }
  if (source === "deterministic_demo") {
    return t("volatilityLab.badges.demo");
  }
  return source;
}

function translateSourceBadge(label: string, t: (key: string) => string) {
  const normalized = label.toLowerCase();
  if (normalized.includes("realized")) return t("volatilityLab.badges.realized");
  if (normalized.includes("partial")) return t("volatilityLab.badges.partialData");
  if (normalized.includes("demo")) return t("volatilityLab.badges.demo");
  if (normalized.includes("requires")) {
    return t("volatilityLab.badges.requiresMarketData");
  }
  return label;
}

function sourceBadgeVariant(label: string): BadgeVariant {
  const normalized = label.toLowerCase();
  if (normalized.includes("realized")) return "success";
  if (
    normalized.includes("demo") ||
    normalized.includes("partial") ||
    normalized.includes("requires")
  ) {
    return "warning";
  }
  return "info";
}

function regimeVariant(regime: string): BadgeVariant {
  const normalized = regime.toLowerCase();
  if (normalized.includes("high") || normalized.includes("stress")) return "danger";
  if (normalized.includes("elevated")) return "warning";
  if (normalized.includes("low")) return "success";
  return "info";
}

function volatilityTone(
  value: number,
): "neutral" | "positive" | "warning" | "negative" {
  if (value >= 0.35) return "negative";
  if (value >= 0.22) return "warning";
  if (value <= 0.12) return "positive";
  return "neutral";
}
