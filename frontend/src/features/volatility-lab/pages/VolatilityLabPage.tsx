import { useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";
import { useQuery } from "@tanstack/react-query";

import { MoneyValue } from "../../../components/finance/MoneyValue";
import { PercentValue } from "../../../components/finance/PercentValue";
import { PageHeader } from "../../../components/layout/PageHeader";
import { EmptyState } from "../../../components/ui/EmptyState";
import { LoadingState } from "../../../components/ui/LoadingState";
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
  DistributionSummary,
  DownsideRiskSummary,
  MatrixSummary,
  ReturnSummary,
  RiskAdjustedSummary,
  RiskContributionItem,
  RollingVolatilityPoint,
  VolatilityAnalysis,
  VolatilityAssetAnalysisResponse,
  VolatilityDataSource,
  VolatilityLabStatus,
  VolatilityPortfolioAnalysisResponse,
  VolatilityRegimeSummary,
  VolatilitySummary,
} from "../../../types/volatility";

type AnalysisMode = "asset" | "portfolio";
type VolatilityTab =
  | "overview"
  | "rolling"
  | "distribution"
  | "downside"
  | "benchmark"
  | "portfolio"
  | "commentary";

type BadgeVariant = "neutral" | "info" | "success" | "warning" | "danger";

const volatilityTabs: VolatilityTab[] = [
  "overview",
  "rolling",
  "distribution",
  "downside",
  "benchmark",
  "portfolio",
  "commentary",
];

export function VolatilityLabPage() {
  const { t } = useTranslation();
  const {
    holdings,
    selectedHolding,
    selectedPortfolio,
    selectedPortfolioId,
    selectedSymbol: workflowSymbol,
    selectPortfolio,
    selectSymbol,
  } = usePortfolioContext();
  const [analysisMode, setAnalysisMode] = useState<AnalysisMode>("portfolio");
  const [symbolSelectionMode, setSymbolSelectionMode] =
    useState<SymbolSelectionMode>("portfolio");
  const [selectedSymbol, setSelectedSymbol] = useState(workflowSymbol || "AAPL");
  const [benchmarkSymbol, setBenchmarkSymbol] = useState(
    selectedPortfolio?.benchmark || "SPY",
  );
  const [rollingWindow, setRollingWindow] = useState(20);
  const [confidenceLevel, setConfidenceLevel] = useState(0.95);
  const [riskFreeRate, setRiskFreeRate] = useState(0.02);
  const [activeTab, setActiveTab] = useState<VolatilityTab>("overview");

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
      holdingsSignature,
    ],
    enabled:
      analysisMode === "asset"
        ? Boolean(selectedSymbol.trim())
        : Boolean(selectedPortfolio?.id),
    queryFn: () => {
      const sharedPayload = {
        benchmark_symbol: benchmarkSymbol.trim().toUpperCase() || "SPY",
        rolling_window: rollingWindow,
        confidence_level: confidenceLevel,
        risk_free_rate: riskFreeRate,
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
        <div className="risk-monitor-badge-cluster">
          <VolatilityStatusBadge
            label={statusQuery.data?.status ?? t("common.loading")}
            variant={statusQuery.data?.status === "ready" ? "success" : "warning"}
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
              <OverviewTab analysis={analysis} t={t} />
            ) : null}
            {activeTab === "rolling" ? (
              <RollingTab
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
                downside={analysis.downside_risk}
                riskAdjusted={analysis.risk_adjusted}
                returns={analysis.return_summary}
                t={t}
              />
            ) : null}
            {activeTab === "benchmark" ? (
              <BenchmarkTab analysis={analysis} t={t} />
            ) : null}
            {activeTab === "portfolio" ? (
              <PortfolioTab analysis={analysis} t={t} />
            ) : null}
            {activeTab === "commentary" ? (
              <CommentaryTab commentary={analysis.athena_commentary} t={t} />
            ) : null}
          </div>
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
  t,
}: {
  analysis: VolatilityAnalysis;
  t: (key: string) => string;
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
  rolling,
  summary,
  t,
}: {
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
  downside,
  riskAdjusted,
  returns,
  t,
}: {
  downside: DownsideRiskSummary;
  riskAdjusted: RiskAdjustedSummary;
  returns: ReturnSummary;
  t: (key: string) => string;
}) {
  return (
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

      <div className="risk-monitor-two-column">
        <MatrixPanel matrix={analysis.covariance_matrix} t={t} />
        <MatrixPanel matrix={analysis.correlation_matrix} t={t} />
      </div>
    </div>
  );
}

function CommentaryTab({
  commentary,
  t,
}: {
  commentary: AthenaVolatilityCommentary;
  t: (key: string) => string;
}) {
  return (
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
        <div key={item.symbol}>
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

function VolatilityStatusBadge({
  label,
  variant = "neutral",
}: {
  label: string;
  variant?: BadgeVariant;
}) {
  return (
    <span className={`risk-monitor-status-badge risk-monitor-status-badge--${variant}`}>
      {label}
    </span>
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
