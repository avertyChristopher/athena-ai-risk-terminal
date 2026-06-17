import {
  PropsWithChildren,
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";

import { apiClient } from "../lib/api-client";
import { endpoints } from "../lib/endpoints";
import {
  PortfolioListResponse,
  PortfolioRead,
  PositionListResponse,
  PositionRead,
} from "../types/portfolio";

type PortfolioContextValue = {
  selectedPortfolioId: string;
  selectedPortfolioName: string;
  selectedPortfolio: PortfolioRead | null;
  selectedSymbol: string;
  selectedHolding: PositionRead | null;
  portfolios: PortfolioRead[];
  holdings: PositionRead[];
  isLoading: boolean;
  error: Error | null;
  selectPortfolio: (portfolioId: string) => void;
  selectSymbol: (symbol: string) => void;
  clearSelection: () => void;
  refreshPortfolios: () => Promise<void>;
  getSymbolsFromSelectedPortfolio: () => string[];
};

const PortfolioContext = createContext<PortfolioContextValue | undefined>(
  undefined,
);

export function PortfolioProvider({ children }: PropsWithChildren) {
  const queryClient = useQueryClient();
  const [selectedPortfolioId, setSelectedPortfolioId] = useState("");
  const [selectedSymbol, setSelectedSymbol] = useState("");

  const portfoliosQuery = useQuery({
    queryKey: ["portfolios"],
    queryFn: () => apiClient.get<PortfolioListResponse>(endpoints.portfolios),
  });

  const portfolios = useMemo(
    () => portfoliosQuery.data?.items ?? [],
    [portfoliosQuery.data?.items],
  );

  useEffect(() => {
    if (!portfolios.length) {
      if (selectedPortfolioId) {
        setSelectedPortfolioId("");
      }
      return;
    }

    const hasSelectedPortfolio = portfolios.some(
      (portfolio) => portfolio.id === selectedPortfolioId,
    );

    if (!selectedPortfolioId || !hasSelectedPortfolio) {
      setSelectedPortfolioId(portfolios[0].id);
    }
  }, [portfolios, selectedPortfolioId]);

  const selectedPortfolio = useMemo(
    () =>
      portfolios.find((portfolio) => portfolio.id === selectedPortfolioId) ??
      null,
    [portfolios, selectedPortfolioId],
  );

  const positionsQuery = useQuery({
    queryKey: ["portfolio-positions", selectedPortfolioId],
    enabled: Boolean(selectedPortfolioId),
    queryFn: () =>
      apiClient.get<PositionListResponse>(
        endpoints.portfolioPositions(selectedPortfolioId),
      ),
  });

  const holdings = useMemo(
    () => positionsQuery.data?.items ?? [],
    [positionsQuery.data?.items],
  );

  useEffect(() => {
    if (!selectedSymbol && holdings.length > 0) {
      setSelectedSymbol(holdings[0].symbol);
    }
  }, [holdings, selectedSymbol]);

  const selectedHolding = useMemo(() => {
    const normalizedSymbol = selectedSymbol.toUpperCase();
    return (
      holdings.find(
        (holding) => holding.symbol.toUpperCase() === normalizedSymbol,
      ) ?? null
    );
  }, [holdings, selectedSymbol]);

  const selectPortfolio = useCallback((portfolioId: string) => {
    setSelectedPortfolioId(portfolioId);
  }, []);

  const selectSymbol = useCallback((symbol: string) => {
    setSelectedSymbol(symbol.trim().toUpperCase());
  }, []);

  const clearSelection = useCallback(() => {
    setSelectedPortfolioId("");
    setSelectedSymbol("");
  }, []);

  const refreshPortfolios = useCallback(async () => {
    await queryClient.invalidateQueries({ queryKey: ["portfolios"] });

    if (selectedPortfolioId) {
      await queryClient.invalidateQueries({
        queryKey: ["portfolio-positions", selectedPortfolioId],
      });
    }
  }, [queryClient, selectedPortfolioId]);

  const getSymbolsFromSelectedPortfolio = useCallback(
    () => holdings.map((holding) => holding.symbol),
    [holdings],
  );

  const error =
    portfoliosQuery.error instanceof Error
      ? portfoliosQuery.error
      : positionsQuery.error instanceof Error
        ? positionsQuery.error
        : null;

  const value = useMemo(
    () => ({
      selectedPortfolioId,
      selectedPortfolioName: selectedPortfolio?.name ?? "",
      selectedPortfolio,
      selectedSymbol,
      selectedHolding,
      portfolios,
      holdings,
      isLoading: portfoliosQuery.isLoading || positionsQuery.isLoading,
      error,
      selectPortfolio,
      selectSymbol,
      clearSelection,
      refreshPortfolios,
      getSymbolsFromSelectedPortfolio,
    }),
    [
      clearSelection,
      error,
      getSymbolsFromSelectedPortfolio,
      holdings,
      portfolios,
      portfoliosQuery.isLoading,
      positionsQuery.isLoading,
      refreshPortfolios,
      selectPortfolio,
      selectSymbol,
      selectedHolding,
      selectedPortfolio,
      selectedPortfolioId,
      selectedSymbol,
    ],
  );

  return (
    <PortfolioContext.Provider value={value}>
      {children}
    </PortfolioContext.Provider>
  );
}

export function usePortfolioContext() {
  const context = useContext(PortfolioContext);

  if (!context) {
    throw new Error("usePortfolioContext must be used inside PortfolioProvider");
  }

  return context;
}
