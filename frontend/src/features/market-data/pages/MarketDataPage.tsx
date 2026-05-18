import { useEffect, useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";

import { PageHeader } from "../../../components/layout/PageHeader";
import { apiClient } from "../../../lib/api-client";
import { endpoints } from "../../../lib/endpoints";
import { useTranslation } from "../../../hooks/useTranslation";
import {
  DataQualityResponse,
  MarketAsset,
  PricePoint,
  ReturnPoint,
  VolatilityResponse,
} from "../../../types/market-data";
import { AssetSearch } from "../components/AssetSearch";
import { DataQualityPanel } from "../components/DataQualityPanel";
import { MarketDataTable } from "../components/MarketDataTable";
import { PriceChart } from "../components/PriceChart";
import { ReturnsChart } from "../components/ReturnsChart";
import { RollingVolatilityChart } from "../components/RollingVolatilityChart";

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

      {assetsQuery.isLoading ? <p>{t("common.loading")}</p> : null}
      {assetsQuery.isError ? (
        <p className="status-message status-message--error">
          {t("marketData.apiError")}
        </p>
      ) : null}

      <section className="market-data-grid">
        <PriceChart
          title={t("marketData.priceChart")}
          prices={pricesQuery.data ?? []}
        />
        <ReturnsChart
          title={t("marketData.returnsChart")}
          returns={returnsQuery.data ?? []}
        />
        <RollingVolatilityChart
          title={t("marketData.volatility")}
          volatility={volatilityQuery.data}
          labels={{
            daily: t("marketData.daily"),
            annualized: t("marketData.annualized"),
          }}
        />
        <DataQualityPanel
          title={t("marketData.quality")}
          quality={qualityQuery.data}
          labels={{
            rows: t("marketData.rows"),
            missing: t("marketData.missing"),
            duplicates: t("marketData.duplicates"),
            outliers: t("marketData.outliers"),
          }}
        />
      </section>

      <MarketDataTable
        title={t("marketData.table")}
        prices={pricesQuery.data ?? []}
        currency={selectedAsset?.currency ?? "USD"}
        labels={{
          date: t("marketData.date"),
          open: t("marketData.open"),
          high: t("marketData.high"),
          low: t("marketData.low"),
          close: t("marketData.close"),
          volume: t("marketData.volume"),
        }}
      />
    </div>
  );
}
