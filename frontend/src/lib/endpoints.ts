export const endpoints = {
  health: "/api/health",
  marketDataAssets: "/api/market-data/assets",
  marketDataPrices: (symbol: string) => `/api/market-data/prices/${symbol}`,
  marketDataReturns: (symbol: string) => `/api/market-data/returns/${symbol}`,
  marketDataVolatility: (symbol: string) =>
    `/api/market-data/volatility/${symbol}`,
  marketDataQuality: (symbol: string) =>
    `/api/market-data/data-quality/${symbol}`,
  marketDataAnalytics: (symbol: string) =>
    `/api/market-data/analytics/${symbol}`,
  equityOverview: (symbol: string) => `/api/equity/${symbol}/overview`,
  equityFundamentals: (symbol: string) => `/api/equity/${symbol}/fundamentals`,
  equityRatios: (symbol: string) => `/api/equity/${symbol}/ratios`,
  equityValuation: (symbol: string) => `/api/equity/${symbol}/valuation`,
  equityDiagnostics: (symbol: string) => `/api/equity/${symbol}/diagnostics`,
  equityGgm: "/api/equity/valuation/ggm",
  equitySensitivity: "/api/equity/valuation/sensitivity",
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
