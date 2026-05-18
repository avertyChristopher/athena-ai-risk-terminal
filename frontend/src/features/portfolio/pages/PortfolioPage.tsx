import { useEffect, useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { PageHeader } from "../../../components/layout/PageHeader";
import { apiClient } from "../../../lib/api-client";
import { endpoints } from "../../../lib/endpoints";
import { useTranslation } from "../../../hooks/useTranslation";
import {
  AllocationResponse,
  PortfolioCreate,
  PortfolioListResponse,
  PortfolioRead,
  PortfolioSummary,
  PositionCreate,
  PositionListResponse,
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

      {isLoading ? <p>{t("common.loading")}</p> : null}

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
            currency: t("portfolio.positions.currency"),
            sector: t("portfolio.positions.sector"),
            country: t("portfolio.positions.country"),
            actions: t("portfolio.positions.actions"),
            delete: t("portfolio.positions.delete"),
          }}
        />
      ) : null}

      {summaryQuery.data && sectorAllocationQuery.data ? (
        <AllocationChart
          title={t("portfolio.allocation.sectors")}
          items={sectorAllocationQuery.data.items}
          currency={summaryQuery.data.base_currency}
        />
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
