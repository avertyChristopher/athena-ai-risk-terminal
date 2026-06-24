export const endpoints = {
  health: "/api/health",
  marketDataAssets: "/api/market-data/assets",
  marketDataPrices: (symbol: string) => `/api/market-data/prices/${symbol}`,
  marketDataReturns: (symbol: string) => `/api/market-data/returns/${symbol}`,
  marketDataReturnsPanel: (symbols: string) =>
    `/api/market-data/returns-panel?symbols=${symbols}`,
  marketDataAlignedReturns: (symbols: string) =>
    `/api/market-data/aligned-returns?symbols=${symbols}`,
  marketDataCoverage: (symbols: string) =>
    `/api/market-data/coverage?symbols=${symbols}`,
  marketDataImportPrices: "/api/market-data/import-prices",
  marketDataQualityBatch: (symbols: string, expectedCurrency = "USD") =>
    `/api/market-data/data-quality/batch?symbols=${symbols}&expected_currency=${expectedCurrency}`,
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
  equityCapm: (symbol: string) => `/api/equity/${symbol}/capm`,
  equityDupont: (symbol: string) => `/api/equity/${symbol}/dupont`,
  equityQualityOfEarnings: (symbol: string) =>
    `/api/equity/${symbol}/quality-of-earnings`,
  equityHistoricalFundamentals: (symbol: string) =>
    `/api/equity/${symbol}/historical-fundamentals`,
  equityDcf: (symbol: string) => `/api/equity/${symbol}/dcf`,
  equityDataQuality: (symbol: string) => `/api/equity/${symbol}/data-quality`,
  equitySectorInterpretation: (symbol: string) =>
    `/api/equity/${symbol}/sector-interpretation`,
  equityInstitutionalSignals: (symbol: string) =>
    `/api/equity/${symbol}/institutional-signals`,
  equityGgm: "/api/equity/valuation/ggm",
  equitySensitivity: "/api/equity/valuation/sensitivity",
  equityDcfValuation: "/api/equity/valuation/dcf",
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
  portfolioAssetAllocation: (portfolioId: string) =>
    `/api/portfolios/${portfolioId}/allocation/assets`,
  portfolioCurrencyAllocation: (portfolioId: string) =>
    `/api/portfolios/${portfolioId}/allocation/currencies`,
  portfolioCountryAllocation: (portfolioId: string) =>
    `/api/portfolios/${portfolioId}/allocation/countries`,
  portfolioAssetTypeAllocation: (portfolioId: string) =>
    `/api/portfolios/${portfolioId}/allocation/asset-types`,
  portfolioConcentration: (portfolioId: string) =>
    `/api/portfolios/${portfolioId}/concentration`,
  portfolioDiversification: (portfolioId: string) =>
    `/api/portfolios/${portfolioId}/diversification`,
  portfolioRiskReturn: (portfolioId: string) =>
    `/api/portfolios/${portfolioId}/risk-return`,
  portfolioBenchmark: (portfolioId: string) =>
    `/api/portfolios/${portfolioId}/benchmark`,
  portfolioPolicy: (portfolioId: string) =>
    `/api/portfolios/${portfolioId}/policy`,
  portfolioTargetAllocation: (portfolioId: string) =>
    `/api/portfolios/${portfolioId}/target-allocation`,
  portfolioRebalancingPreview: (portfolioId: string) =>
    `/api/portfolios/${portfolioId}/rebalancing-preview`,
  portfolioPerformanceMeasurement: (portfolioId: string) =>
    `/api/portfolios/${portfolioId}/performance-measurement`,
  portfolioConstraints: (portfolioId: string) =>
    `/api/portfolios/${portfolioId}/constraints`,
  portfolioDiagnostics: (portfolioId: string) =>
    `/api/portfolios/${portfolioId}/diagnostics`,
  portfolioMarketDataIntegration: (portfolioId: string) =>
    `/api/portfolios/${portfolioId}/market-data-integration`,
  portfolioCfaConcepts: (portfolioId: string) =>
    `/api/portfolios/${portfolioId}/cfa-concepts`,
  tradeSimulatorStatus: "/api/trade-simulator/status",
  tradeSimulatorSimulate: "/api/trade-simulator/simulate",
  riskMonitorStatus: "/api/risk-monitor/status",
  riskMonitorAnalyze: "/api/risk-monitor/analyze",
  riskMonitorAnalyzeFromVolatility: "/api/risk-monitor/analyze-from-volatility",
  riskMonitorAnalyzeFromRates: "/api/risk-monitor/analyze-from-rates",
  riskMonitorAnalyzeFromOptions: "/api/risk-monitor/analyze-from-options",
  riskMonitorDemo: "/api/risk-monitor/demo",
  volatilityLabStatus: "/api/volatility-lab/status",
  volatilityLabAnalyzeAsset: "/api/volatility-lab/analyze-asset",
  volatilityLabAnalyzePortfolio: "/api/volatility-lab/analyze-portfolio",
  volatilityLabDemo: "/api/volatility-lab/demo",
  optionsPricingLabStatus: "/api/options-pricing-lab/status",
  optionsPricingLabPrice: "/api/options-pricing-lab/price",
  optionsPricingLabStrategy: "/api/options-pricing-lab/strategy",
  optionsPricingLabImpliedVolatility: "/api/options-pricing-lab/implied-volatility",
  optionsPricingLabDemo: "/api/options-pricing-lab/demo",
  ratesLabStatus: "/api/rates-lab/status",
  ratesLabBondPrice: "/api/rates-lab/bond-price",
  ratesLabYieldAnalysis: "/api/rates-lab/yield-analysis",
  ratesLabDurationConvexity: "/api/rates-lab/duration-convexity",
  ratesLabYieldCurve: "/api/rates-lab/yield-curve",
  ratesLabRateScenarios: "/api/rates-lab/rate-scenarios",
  ratesLabPortfolioExposure: "/api/rates-lab/portfolio-exposure",
  ratesLabDemo: "/api/rates-lab/demo",
  athenaIntelligenceStatus: "/api/athena-intelligence/status",
  athenaIntelligenceCommentary: "/api/athena-intelligence/commentary",
  athenaIntelligenceRiskSynthesis: "/api/athena-intelligence/risk-synthesis",
  athenaIntelligenceExplainMetric: "/api/athena-intelligence/explain-metric",
  athenaIntelligenceDemo: "/api/athena-intelligence/demo",
  stressTestingStatus: "/api/stress-testing/status",
  stressTestingScenarios: "/api/stress-testing/scenarios",
  stressTestingRun: "/api/stress-testing/run",
  stressTestingCustomScenario: "/api/stress-testing/custom-scenario",
  stressTestingDemo: "/api/stress-testing/demo",
  limitCenterStatus: "/api/limit-center/status",
  limitCenterRules: "/api/limit-center/rules",
  limitCenterRule: (ruleId: string) => `/api/limit-center/rules/${ruleId}`,
  limitCenterEvaluate: "/api/limit-center/evaluate",
  limitCenterEvaluateModulePayload: "/api/limit-center/evaluate-module-payload",
  limitCenterBreaches: "/api/limit-center/breaches",
  limitCenterBreach: (breachId: string) => `/api/limit-center/breaches/${breachId}`,
  limitCenterBreachReview: (breachId: string) =>
    `/api/limit-center/breaches/${breachId}/review`,
  limitCenterSourceModules: "/api/limit-center/source-modules",
  limitCenterDemo: "/api/limit-center/demo",
} as const;
