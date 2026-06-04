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
  equitySecurityProfile: (symbol: string) =>
    `/api/equity/${symbol}/security-profile`,
  equityIndustry: (symbol: string) => `/api/equity/${symbol}/industry`,
  equityBusinessModel: (symbol: string) =>
    `/api/equity/${symbol}/business-model`,
  equityFundamentals: (symbol: string) => `/api/equity/${symbol}/fundamentals`,
  equityRatios: (symbol: string) => `/api/equity/${symbol}/ratios`,
  equityGrowth: (symbol: string) => `/api/equity/${symbol}/growth`,
  equityValuation: (symbol: string) => `/api/equity/${symbol}/valuation`,
  equityRelativeValuation: (symbol: string) =>
    `/api/equity/${symbol}/relative-valuation`,
  equityPeerComparison: (symbol: string) =>
    `/api/equity/${symbol}/peer-comparison`,
  equityCorporateActions: (symbol: string) =>
    `/api/equity/${symbol}/corporate-actions`,
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
