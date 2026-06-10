import { useEffect, useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";

import { PageHeader } from "../../../components/layout/PageHeader";
import { LoadingState } from "../../../components/ui/LoadingState";
import { apiClient } from "../../../lib/api-client";
import { endpoints } from "../../../lib/endpoints";
import { useTranslation } from "../../../hooks/useTranslation";
import {
  DataQualityResponse,
  MarketAsset,
  MarketDataAnalyticsResponse,
  PricePoint,
  ReturnPoint,
  VolatilityResponse,
} from "../../../types/market-data";
import { AssetSearch } from "../components/AssetSearch";
import { AssetOverviewSection } from "../components/AssetOverviewSection";
import { AssetSummaryPanel } from "../components/AssetSummaryPanel";
import { BenchmarkAnalysisSection } from "../components/BenchmarkAnalysisSection";
import { DistributionStatsSection } from "../components/DistributionStatsSection";
import { MarketContextSection } from "../components/MarketContextSection";
import { ReturnsAnalyticsSection } from "../components/ReturnsAnalyticsSection";
import { RiskVolatilitySection } from "../components/RiskVolatilitySection";

export function MarketDataPage() {
  const { t } = useTranslation();
  const [selectedSymbol, setSelectedSymbol] = useState("");

  const assetsQuery = useQuery({
    queryKey: ["market-data-assets"],
    queryFn: () => apiClient.get<MarketAsset[]>(endpoints.marketDataAssets),
  });

  const assets = assetsQuery.data ?? [];

  useEffect(() => {
    if (!selectedSymbol && assets.length > 0) {
      setSelectedSymbol(assets[0].symbol);
    }
  }, [assets, selectedSymbol]);

  const selectedAsset = useMemo(
    () => assets.find((asset) => asset.symbol === selectedSymbol) ?? assets[0],
    [assets, selectedSymbol],
  );

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

      {selectedAsset ? (
        <AssetSearch
          assets={assets}
          selectedSymbol={selectedAsset.symbol}
          onSelect={setSelectedSymbol}
          label={t("marketData.asset")}
        />
      ) : null}

      {assetsQuery.isLoading ? <LoadingState label={t("common.loading")} /> : null}
      {assetsQuery.isError ? (
        <p className="status-message status-message--error">
          {t("marketData.apiError")}
        </p>
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
