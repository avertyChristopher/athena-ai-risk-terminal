export const endpoints = {
  health: "/api/health",
  marketDataAssets: "/api/market-data/assets",
  marketDataPrices: (symbol: string) => `/api/market-data/prices/${symbol}`,
  marketDataReturns: (symbol: string) => `/api/market-data/returns/${symbol}`,
  marketDataVolatility: (symbol: string) =>
    `/api/market-data/volatility/${symbol}`,
  marketDataQuality: (symbol: string) =>
    `/api/market-data/data-quality/${symbol}`,
  portfolios: "/api/portfolios",
  portfolio: (portfolioId: string) => `/api/portfolios/${portfolioId}`,
  portfolioSummary: (portfolioId: string) =>
    `/api/portfolios/${portfolioId}/summary`,
  portfolioPositions: (portfolioId: string) =>
    `/api/portfolios/${portfolioId}/positions`,
  portfolioPosition: (portfolioId: string, positionId: string) =>
    `/api/portfolios/${portfolioId}/positions/${positionId}`,
  portfolioSectorAllocation: (portfolioId: string) =>
    `/api/portfolios/${portfolioId}/allocation/sectors`,
} as const;
