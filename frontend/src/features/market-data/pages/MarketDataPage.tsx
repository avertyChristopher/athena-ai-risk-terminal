import { ChangeEvent, useEffect, useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { PageHeader } from "../../../components/layout/PageHeader";
import { ErrorBanner } from "../../../components/ui/ErrorBanner";
import { LoadingState } from "../../../components/ui/LoadingState";
import { Card } from "../../../components/ui/Card";
import { PortfolioSelector } from "../../../components/workflow/PortfolioSelector";
import {
  SymbolSelectionMode,
  SymbolSelector,
} from "../../../components/workflow/SymbolSelector";
import { usePortfolioContext } from "../../../context/PortfolioContext";
import { apiClient } from "../../../lib/api-client";
import { endpoints } from "../../../lib/endpoints";
import { useTranslation } from "../../../hooks/useTranslation";
import {
  DataQualityResponse,
  MarketDataImportRequest,
  MarketDataImportResponse,
  MarketAsset,
  MarketDataAnalyticsResponse,
  PortfolioMarketDataCoverageResponse,
  PricePoint,
  ReturnPoint,
  VolatilityResponse,
} from "../../../types/market-data";
import { AssetOverviewSection } from "../components/AssetOverviewSection";
import { AssetSummaryPanel } from "../components/AssetSummaryPanel";
import { BenchmarkAnalysisSection } from "../components/BenchmarkAnalysisSection";
import { DistributionStatsSection } from "../components/DistributionStatsSection";
import { MarketContextSection } from "../components/MarketContextSection";
import { ReturnsAnalyticsSection } from "../components/ReturnsAnalyticsSection";
import { RiskVolatilitySection } from "../components/RiskVolatilitySection";

export function MarketDataPage() {
  const { t } = useTranslation();
  const queryClient = useQueryClient();
  const {
    holdings,
    selectSymbol: selectWorkflowSymbol,
    selectedHolding,
    selectedPortfolioName,
    selectedSymbol: workflowSymbol,
  } = usePortfolioContext();
  const [selectedSymbol, setSelectedSymbol] = useState("");
  const [selectionMode, setSelectionMode] =
    useState<SymbolSelectionMode>("standalone");
  const [importMessage, setImportMessage] = useState("");

  const assetsQuery = useQuery({
    queryKey: ["market-data-assets"],
    queryFn: () => apiClient.get<MarketAsset[]>(endpoints.marketDataAssets),
  });

  const assets = assetsQuery.data ?? [];

  useEffect(() => {
    if (workflowSymbol && workflowSymbol !== selectedSymbol) {
      setSelectedSymbol(workflowSymbol);
    }
  }, [selectedSymbol, workflowSymbol]);

  useEffect(() => {
    if (!selectedSymbol && assets.length > 0) {
      const defaultSymbol = assets[0].symbol;
      setSelectedSymbol(defaultSymbol);
      selectWorkflowSymbol(defaultSymbol);
    }
  }, [assets, selectWorkflowSymbol, selectedSymbol]);

  const standaloneOptions = useMemo(
    () =>
      assets.map((asset) => ({
        symbol: asset.symbol,
        name: asset.name,
      })),
    [assets],
  );
  const portfolioSymbols = useMemo(
    () =>
      Array.from(
        new Set(holdings.map((holding) => holding.symbol.trim().toUpperCase())),
      ).filter(Boolean),
    [holdings],
  );
  const portfolioSymbolsParam = portfolioSymbols.join(",");

  const selectedAsset = useMemo<MarketAsset | undefined>(
    () => {
      const trackedAsset =
        assets.find((asset) => asset.symbol === selectedSymbol) ?? assets[0];

      if (trackedAsset) {
        return trackedAsset;
      }

      if (
        selectedHolding &&
        selectedHolding.symbol.toUpperCase() === selectedSymbol.toUpperCase()
      ) {
        return {
          symbol: selectedHolding.symbol,
          name: selectedHolding.asset_name,
          asset_type: selectedHolding.asset_type,
          currency: selectedHolding.currency,
          sector: selectedHolding.sector,
          country: selectedHolding.country,
        };
      }

      return selectedSymbol
        ? {
            symbol: selectedSymbol,
            name: selectedSymbol,
            asset_type: "unknown",
            currency: "USD",
            sector: "Unknown",
            country: "Unknown",
          }
        : undefined;
    },
    [assets, selectedHolding, selectedSymbol],
  );

  function handleSymbolChange(symbol: string) {
    setSelectedSymbol(symbol);
    selectWorkflowSymbol(symbol);
  }

  const coverageQuery = useQuery({
    queryKey: ["market-data-coverage", portfolioSymbolsParam],
    enabled: portfolioSymbols.length > 0,
    queryFn: () =>
      apiClient.get<PortfolioMarketDataCoverageResponse>(
        endpoints.marketDataCoverage(portfolioSymbolsParam),
      ),
  });

  const importMutation = useMutation({
    mutationFn: (payload: MarketDataImportRequest) =>
      apiClient.post<MarketDataImportResponse>(
        endpoints.marketDataImportPrices,
        payload,
      ),
    onSuccess: async (response) => {
      setImportMessage(
        t("marketData.import.success")
          .replace("{rows}", String(response.imported_rows))
          .replace("{symbols}", response.imported_symbols.join(", ")),
      );
      await Promise.all([
        queryClient.invalidateQueries({ queryKey: ["market-data-assets"] }),
        queryClient.invalidateQueries({ queryKey: ["market-data-coverage"] }),
      ]);

      response.imported_symbols.forEach((symbol) => {
        queryClient.invalidateQueries({
          queryKey: ["market-data-prices", symbol],
        });
        queryClient.invalidateQueries({
          queryKey: ["market-data-returns", symbol],
        });
        queryClient.invalidateQueries({
          queryKey: ["market-data-quality", symbol],
        });
        queryClient.invalidateQueries({
          queryKey: ["market-data-analytics", symbol],
        });
      });
    },
    onError: () => {
      setImportMessage(t("marketData.import.error"));
    },
  });

  async function handleImportFileChange(
    event: ChangeEvent<HTMLInputElement>,
  ) {
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }

    try {
      const rows = parseMarketDataCsv(await file.text());
      importMutation.mutate({ rows });
    } catch {
      setImportMessage(t("marketData.import.parseError"));
    } finally {
      event.target.value = "";
    }
  }

  const pricesQuery = useQuery({
    queryKey: ["market-data-prices", selectedSymbol],
    enabled: Boolean(selectedSymbol),
    queryFn: () =>
      apiClient.get<PricePoint[]>(endpoints.marketDataPrices(selectedSymbol)),
  });

  const returnsQuery = useQuery({
    queryKey: ["market-data-returns", selectedSymbol],
    enabled: Boolean(selectedSymbol),
    queryFn: () =>
      apiClient.get<ReturnPoint[]>(endpoints.marketDataReturns(selectedSymbol)),
  });

  const volatilityQuery = useQuery({
    queryKey: ["market-data-volatility", selectedSymbol],
    enabled: Boolean(selectedSymbol),
    queryFn: () =>
      apiClient.get<VolatilityResponse>(
        endpoints.marketDataVolatility(selectedSymbol),
      ),
  });

  const qualityQuery = useQuery({
    queryKey: ["market-data-quality", selectedSymbol],
    enabled: Boolean(selectedSymbol),
    queryFn: () =>
      apiClient.get<DataQualityResponse>(
        endpoints.marketDataQuality(selectedSymbol),
      ),
  });

  const analyticsQuery = useQuery({
    queryKey: ["market-data-analytics", selectedSymbol],
    enabled: Boolean(selectedSymbol),
    queryFn: () =>
      apiClient.get<MarketDataAnalyticsResponse>(
        endpoints.marketDataAnalytics(selectedSymbol),
      ),
  });

  return (
    <div className="page market-data-page">
      <PageHeader
        title={t("marketData.title")}
        subtitle={t("marketData.subtitle")}
      />

      <div className="workflow-selector-grid">
        <PortfolioSelector compact />
        <SymbolSelector
          mode={selectionMode}
          selectedSymbol={selectedSymbol}
          standaloneOptions={standaloneOptions}
          title={t("marketData.asset")}
          onModeChange={setSelectionMode}
          onSymbolChange={(symbol) => handleSymbolChange(symbol)}
        />
      </div>

      <Card className="market-data-coverage-panel">
        <div className="market-data-coverage-panel__header">
          <div>
            <span className="section-eyebrow">
              {t("marketData.coverage.eyebrow")}
            </span>
            <h2>{t("marketData.coverage.title")}</h2>
            <p>
              {selectedPortfolioName
                ? t("marketData.coverage.description").replace(
                    "{portfolio}",
                    selectedPortfolioName,
                  )
                : t("marketData.coverage.emptyPortfolio")}
            </p>
          </div>
          <label className="button button--primary market-data-import-button">
            {importMutation.isPending
              ? t("marketData.import.loading")
              : t("marketData.import.button")}
            <input
              className="visually-hidden"
              type="file"
              accept=".csv,text/csv"
              disabled={importMutation.isPending}
              onChange={handleImportFileChange}
            />
          </label>
        </div>

        <div className="market-data-coverage-grid">
          <div className="metric-tile">
            <span>{t("marketData.coverage.ratio")}</span>
            <strong>
              {coverageQuery.data
                ? `${Math.round(coverageQuery.data.coverage_ratio * 100)}%`
                : "--"}
            </strong>
            <small>{t("marketData.coverage.ratioHelp")}</small>
          </div>
          <div className="metric-tile">
            <span>{t("marketData.coverage.covered")}</span>
            <strong>{coverageQuery.data?.covered_symbols.length ?? 0}</strong>
            <small>{t("marketData.coverage.coveredHelp")}</small>
          </div>
          <div className="metric-tile">
            <span>{t("marketData.coverage.missing")}</span>
            <strong>{coverageQuery.data?.missing_symbols.length ?? 0}</strong>
            <small>{t("marketData.coverage.missingHelp")}</small>
          </div>
          <div className="metric-tile">
            <span>{t("marketData.import.format")}</span>
            <strong>CSV</strong>
            <small>date,symbol,open,high,low,close,volume</small>
          </div>
        </div>

        <div className="market-data-symbol-list">
          {(coverageQuery.data?.missing_symbols.length ?? 0) > 0 ? (
            coverageQuery.data?.missing_symbols.map((symbol) => (
              <span className="status-pill status-pill--warn" key={symbol}>
                {symbol}
              </span>
            ))
          ) : (
            <span className="status-pill">
              {portfolioSymbols.length
                ? t("marketData.coverage.allCovered")
                : t("marketData.coverage.noSymbols")}
            </span>
          )}
        </div>

        {importMessage ? (
          <p className="status-message">{importMessage}</p>
        ) : null}
        {coverageQuery.isError ? (
          <ErrorBanner title={t("marketData.coverage.title")} message={t("marketData.coverage.error")} />
        ) : null}
      </Card>

      {assetsQuery.isLoading ? <LoadingState label={t("common.loading")} /> : null}
      {assetsQuery.isError ? (
        <ErrorBanner title={t("marketData.title")} message={t("marketData.apiError")} />
      ) : null}

      <AssetSummaryPanel
        asset={selectedAsset}
        analytics={analyticsQuery.data}
        quality={qualityQuery.data}
        labels={{
          asset: t("marketData.summary.asset"),
          latestPrice: t("marketData.summary.latestPrice"),
          latestReturn: t("marketData.summary.latestReturn"),
          annualizedVolatility: t("marketData.summary.annualizedVolatility"),
          maxDrawdown: t("marketData.summary.maxDrawdown"),
          quality: t("marketData.summary.quality"),
          valid: t("marketData.summary.valid"),
          review: t("marketData.summary.review"),
        }}
      />

      <AssetOverviewSection
        asset={selectedAsset}
        analytics={analyticsQuery.data}
        prices={pricesQuery.data ?? []}
        quality={qualityQuery.data}
        labels={{
          title: t("marketData.sections.assetOverview.title"),
          description: t("marketData.sections.assetOverview.description"),
          priceHistory: t("marketData.priceChart"),
          volume: t("marketData.volumeChart"),
          table: t("marketData.table"),
          quality: t("marketData.quality"),
          adjustedClose: t("marketData.planned.adjustedClose"),
          corporateActions: t("marketData.planned.corporateActions"),
          averageVolume20: t("marketData.stats.averageVolume20"),
          latestDollarVolume: t("marketData.stats.latestDollarVolume"),
          liquidityScore: t("marketData.stats.liquidityScore"),
          liquidity: t("marketData.planned.liquidity"),
          highLiquidity: t("marketData.stats.highLiquidity"),
          moderateLiquidity: t("marketData.stats.moderateLiquidity"),
          referenceData: t("marketData.referenceData"),
          date: t("marketData.date"),
          open: t("marketData.open"),
          high: t("marketData.high"),
          low: t("marketData.low"),
          close: t("marketData.close"),
          volumeColumn: t("marketData.volume"),
          rows: t("marketData.rows"),
          missing: t("marketData.missing"),
          duplicates: t("marketData.duplicates"),
          outliers: t("marketData.outliers"),
        }}
      />

      <ReturnsAnalyticsSection
        analytics={analyticsQuery.data}
        returns={returnsQuery.data ?? []}
        labels={{
          title: t("marketData.sections.returns.title"),
          description: t("marketData.sections.returns.description"),
          returnsChart: t("marketData.returnsChart"),
          cumulativeChart: t("marketData.cumulativeReturnsChart"),
          simple: t("marketData.stats.simpleReturn"),
          log: t("marketData.stats.logReturn"),
          holdingPeriod: t("marketData.stats.holdingPeriodReturn"),
          cumulative: t("marketData.stats.cumulativeReturn"),
          arithmetic: t("marketData.stats.arithmeticMeanReturn"),
          geometric: t("marketData.stats.geometricMeanReturn"),
          annualized: t("marketData.stats.annualizedReturn"),
        }}
      />

      <RiskVolatilitySection
        analytics={analyticsQuery.data}
        returns={returnsQuery.data ?? []}
        volatility={volatilityQuery.data}
        labels={{
          title: t("marketData.sections.riskVolatility.title"),
          description: t("marketData.sections.riskVolatility.description"),
          rollingVolatility: t("marketData.volatility"),
          drawdown: t("marketData.drawdownChart"),
          variance: t("marketData.stats.variance"),
          standardDeviation: t("marketData.stats.standardDeviation"),
          dailyVolatility: t("marketData.stats.dailyVolatility"),
          annualizedVolatility: t("marketData.stats.annualizedVolatility"),
          maxDrawdown: t("marketData.stats.maxDrawdown"),
          daily: t("marketData.daily"),
          annualized: t("marketData.annualized"),
        }}
      />

      <DistributionStatsSection
        analytics={analyticsQuery.data}
        returns={returnsQuery.data ?? []}
        labels={{
          title: t("marketData.sections.distribution.title"),
          description: t("marketData.sections.distribution.description"),
          distribution: t("marketData.distributionChart"),
          percentiles: t("marketData.percentiles"),
          outliers: t("marketData.outliers"),
          emptyOutliers: t("marketData.emptyOutliers"),
          skewness: t("marketData.stats.skewness"),
          kurtosis: t("marketData.stats.kurtosis"),
          normalComparison: t("marketData.planned.normalComparison"),
        }}
      />

      <BenchmarkAnalysisSection
        analytics={analyticsQuery.data}
        labels={{
          title: t("marketData.sections.benchmark.title"),
          description: t("marketData.sections.benchmark.description"),
          comparison: t("marketData.benchmarkComparison"),
          stats: t("marketData.benchmarkStats"),
          activeReturn: t("marketData.stats.activeReturn"),
          correlation: t("marketData.stats.correlation"),
          covariance: t("marketData.stats.covariance"),
          beta: t("marketData.stats.beta"),
          sharpe: t("marketData.stats.sharpe"),
          benchmark: t("marketData.stats.benchmark"),
        }}
      />

      <MarketContextSection
        asset={selectedAsset}
        analytics={analyticsQuery.data}
        prices={pricesQuery.data ?? []}
        labels={{
          title: t("marketData.sections.context.title"),
          description: t("marketData.sections.context.description"),
          movingAverages: t("marketData.movingAverages"),
          marketData: t("marketData.marketContext"),
          latest: t("marketData.stats.latest"),
          ma5: t("marketData.stats.ma5"),
          ma20: t("marketData.stats.ma20"),
          momentum5: t("marketData.stats.momentum5"),
          riskFree: t("marketData.stats.riskFree"),
          fxRate: t("marketData.planned.fxRates"),
          currencyConsistency: t("marketData.planned.currencyConsistency"),
          yieldCurve2y: t("marketData.stats.yieldCurve2y"),
          yieldCurve10y: t("marketData.stats.yieldCurve10y"),
          commodityProxy: t("marketData.planned.commodities"),
        }}
      />
    </div>
  );
}

function parseMarketDataCsv(text: string) {
  const [headerLine, ...dataLines] = text
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);

  if (!headerLine) {
    throw new Error("CSV is empty.");
  }

  const headers = headerLine.split(",").map((header) => header.trim().toLowerCase());
  const requiredHeaders = ["date", "symbol", "open", "high", "low", "close", "volume"];
  const hasRequiredHeaders = requiredHeaders.every((header) =>
    headers.includes(header),
  );

  if (!hasRequiredHeaders) {
    throw new Error("CSV headers are incomplete.");
  }

  const rows = dataLines.map((line) => {
    const values = line.split(",").map((value) => value.trim());
    const valueFor = (name: string) => values[headers.indexOf(name)] ?? "";
    const optionalValueFor = (name: string) => {
      const index = headers.indexOf(name);
      return index >= 0 ? values[index] || undefined : undefined;
    };

    return {
      date: valueFor("date"),
      symbol: valueFor("symbol"),
      open: Number(valueFor("open")),
      high: Number(valueFor("high")),
      low: Number(valueFor("low")),
      close: Number(valueFor("close")),
      volume: Number(valueFor("volume")),
      name: optionalValueFor("name"),
      asset_type: optionalValueFor("asset_type") ?? "equity",
      currency: optionalValueFor("currency") ?? "USD",
      sector: optionalValueFor("sector") ?? "Imported",
      country: optionalValueFor("country") ?? "United States",
      exchange: optionalValueFor("exchange"),
      industry: optionalValueFor("industry"),
    };
  });

  const invalidRow = rows.find(
    (row) =>
      !row.date ||
      !row.symbol ||
      !Number.isFinite(row.open) ||
      !Number.isFinite(row.high) ||
      !Number.isFinite(row.low) ||
      !Number.isFinite(row.close) ||
      !Number.isFinite(row.volume),
  );

  if (invalidRow || rows.length === 0) {
    throw new Error("CSV contains invalid rows.");
  }

  return rows;
}
