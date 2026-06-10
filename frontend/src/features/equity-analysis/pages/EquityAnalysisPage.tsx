import { ReactNode, useState } from "react";
import { useQuery } from "@tanstack/react-query";

import { PageHeader } from "../../../components/layout/PageHeader";
import { LoadingState } from "../../../components/ui/LoadingState";
import { apiClient } from "../../../lib/api-client";
import { endpoints } from "../../../lib/endpoints";
import {
  formatCurrency,
  formatLargeCurrency,
  formatMultiple,
  formatPercent,
} from "../../../lib/formatters";
import { useTranslation } from "../../../hooks/useTranslation";
import {
  EquityBusinessModelResponse,
  EquityCapmResponse,
  EquityCorporateActionsResponse,
  EquityDataQualityResponse,
  EquityDcfResponse,
  EquityDiagnosticsResponse,
  EquityDupontResponse,
  EquityEarningsQualityResponse,
  EquityFundamentalsResponse,
  EquityGrowthResponse,
  EquityHistoricalFundamentalsResponse,
  EquityInstitutionalSignalsResponse,
  EquityIndustryResponse,
  EquityOverviewResponse,
  EquityPeerComparisonResponse,
  EquityRatiosResponse,
  EquityRelativeValuationResponse,
  EquitySecurityProfileResponse,
  EquitySectorInterpretationResponse,
  EquityValuationResponse,
} from "../../../types/equity";
import { AnalystSummaryPanel } from "../components/AnalystSummaryPanel";
import { AnalystDiagnosticsPanels } from "../components/AnalystDiagnosticsPanels";
import { BusinessDriverPanels } from "../components/BusinessDriverPanels";
import { BusinessModelPanel } from "../components/BusinessModelPanel";
import { CompanyOverviewCard } from "../components/CompanyOverviewCard";
import {
  CorporateActionsPanel,
  GovernanceRiskPanel,
} from "../components/CorporateGovernancePanels";
import { EquityDiagnosticsPanel } from "../components/EquityDiagnosticsPanel";
import { EquityMetricGrid } from "../components/EquityMetricGrid";
import { EquitySelector } from "../components/EquitySelector";
import { EquitySecurityProfileCard } from "../components/EquitySecurityProfileCard";
import { FinancialSnapshotPanels } from "../components/FinancialSnapshotPanels";
import { FundamentalsTable } from "../components/FundamentalsTable";
import { GGMCalculator } from "../components/GGMCalculator";
import { GrowthPanels } from "../components/GrowthPanels";
import { IndustryAnalysisPanel } from "../components/IndustryAnalysisPanel";
import { IntrinsicValueCard } from "../components/IntrinsicValueCard";
import { MarginOfSafetyCard } from "../components/MarginOfSafetyCard";
import { MarketOrganizationPanel } from "../components/MarketOrganizationPanel";
import {
  PeerComparisonTable,
  RelativeValuationCards,
} from "../components/RelativePeerPanels";
import { RatiosGrid } from "../components/RatiosGrid";
import { ValuationMultiplesTable } from "../components/ValuationMultiplesTable";

const EQUITY_OPTIONS = [
  { symbol: "AAPL", name: "Apple Inc." },
  { symbol: "MSFT", name: "Microsoft Corporation" },
  { symbol: "NVDA", name: "NVIDIA Corporation" },
];

export function EquityAnalysisPage() {
  const { t } = useTranslation();
  const [selectedSymbol, setSelectedSymbol] = useState("AAPL");

  const overviewQuery = useEquityQuery<EquityOverviewResponse>(
    "overview",
    selectedSymbol,
    endpoints.equityOverview,
  );
  const securityQuery = useEquityQuery<EquitySecurityProfileResponse>(
    "security-profile",
    selectedSymbol,
    endpoints.equitySecurityProfile,
  );
  const industryQuery = useEquityQuery<EquityIndustryResponse>(
    "industry",
    selectedSymbol,
    endpoints.equityIndustry,
  );
  const businessQuery = useEquityQuery<EquityBusinessModelResponse>(
    "business-model",
    selectedSymbol,
    endpoints.equityBusinessModel,
  );
  const fundamentalsQuery = useEquityQuery<EquityFundamentalsResponse>(
    "fundamentals",
    selectedSymbol,
    endpoints.equityFundamentals,
  );
  const ratiosQuery = useEquityQuery<EquityRatiosResponse>(
    "ratios",
    selectedSymbol,
    endpoints.equityRatios,
  );
  const growthQuery = useEquityQuery<EquityGrowthResponse>(
    "growth",
    selectedSymbol,
    endpoints.equityGrowth,
  );
  const valuationQuery = useEquityQuery<EquityValuationResponse>(
    "valuation",
    selectedSymbol,
    endpoints.equityValuation,
  );
  const relativeQuery = useEquityQuery<EquityRelativeValuationResponse>(
    "relative-valuation",
    selectedSymbol,
    endpoints.equityRelativeValuation,
  );
  const peersQuery = useEquityQuery<EquityPeerComparisonResponse>(
    "peer-comparison",
    selectedSymbol,
    endpoints.equityPeerComparison,
  );
  const corporateActionsQuery = useEquityQuery<EquityCorporateActionsResponse>(
    "corporate-actions",
    selectedSymbol,
    endpoints.equityCorporateActions,
  );
  const diagnosticsQuery = useEquityQuery<EquityDiagnosticsResponse>(
    "diagnostics",
    selectedSymbol,
    endpoints.equityDiagnostics,
  );
  const capmQuery = useEquityQuery<EquityCapmResponse>(
    "capm",
    selectedSymbol,
    endpoints.equityCapm,
  );
  const dupontQuery = useEquityQuery<EquityDupontResponse>(
    "dupont",
    selectedSymbol,
    endpoints.equityDupont,
  );
  const earningsQualityQuery = useEquityQuery<EquityEarningsQualityResponse>(
    "quality-of-earnings",
    selectedSymbol,
    endpoints.equityQualityOfEarnings,
  );
  const historicalQuery = useEquityQuery<EquityHistoricalFundamentalsResponse>(
    "historical-fundamentals",
    selectedSymbol,
    endpoints.equityHistoricalFundamentals,
  );
  const dcfQuery = useEquityQuery<EquityDcfResponse>(
    "dcf",
    selectedSymbol,
    endpoints.equityDcf,
  );
  const dataQualityQuery = useEquityQuery<EquityDataQualityResponse>(
    "data-quality",
    selectedSymbol,
    endpoints.equityDataQuality,
  );
  const sectorInterpretationQuery = useEquityQuery<EquitySectorInterpretationResponse>(
    "sector-interpretation",
    selectedSymbol,
    endpoints.equitySectorInterpretation,
  );
  const institutionalSignalsQuery =
    useEquityQuery<EquityInstitutionalSignalsResponse>(
      "institutional-signals",
      selectedSymbol,
      endpoints.equityInstitutionalSignals,
    );

  const queries = [
    overviewQuery,
    securityQuery,
    industryQuery,
    businessQuery,
    fundamentalsQuery,
    ratiosQuery,
    growthQuery,
    valuationQuery,
    relativeQuery,
    peersQuery,
    corporateActionsQuery,
    diagnosticsQuery,
    capmQuery,
    dupontQuery,
    earningsQualityQuery,
    historicalQuery,
    dcfQuery,
    dataQualityQuery,
    sectorInterpretationQuery,
    institutionalSignalsQuery,
  ];
  const hasApiError = queries.some((query) => query.isError);
  const isLoading = queries.some((query) => query.isLoading);

  return (
    <div className="page equity-analysis-page">
      <PageHeader
        title={t("equityAnalysis.title")}
        subtitle={t("equityAnalysis.subtitle")}
      />

      <div className="equity-controls">
        <EquitySelector
          options={EQUITY_OPTIONS}
          selectedSymbol={selectedSymbol}
          onSelect={setSelectedSymbol}
          label={t("equityAnalysis.selector")}
        />
        <label className="form-field equity-selector">
          <span>{t("equityAnalysis.controls.benchmark")}</span>
          <select value={overviewQuery.data?.benchmark_symbol ?? "SPY"} disabled>
            <option value="SPY">SPY - S&P 500 ETF</option>
          </select>
        </label>
        <div className="equity-demo-badge">
          <span>{overviewQuery.data?.currency ?? "USD"}</span>
          <strong>{t("equityAnalysis.controls.demoData")}</strong>
        </div>
      </div>

      {isLoading ? <LoadingState label={t("common.loading")} /> : null}
      {hasApiError ? (
        <p className="status-message status-message--error">
          {t("equityAnalysis.apiError")}
        </p>
      ) : null}

      <section className="equity-summary equity-summary--wide">
        <div className="equity-summary__identity">
          <span>{t("equityAnalysis.summary.company")}</span>
          <strong>{overviewQuery.data?.company_name ?? selectedSymbol}</strong>
          <small>
            {overviewQuery.data?.sector ?? "--"} / {overviewQuery.data?.industry ?? "--"}
          </small>
        </div>
        <SummaryMetric
          label={t("equityAnalysis.company.exchange")}
          value={overviewQuery.data?.exchange ?? "--"}
        />
        <SummaryMetric
          label={t("equityAnalysis.company.benchmark")}
          value={overviewQuery.data?.benchmark_symbol ?? "--"}
        />
        <SummaryMetric
          label={t("equityAnalysis.summary.latestPrice")}
          value={
            overviewQuery.data
              ? formatCurrency(
                  overviewQuery.data.latest_price,
                  overviewQuery.data.currency,
                )
              : "--"
          }
        />
        <SummaryMetric
          label={t("equityAnalysis.summary.marketCap")}
          value={formatLargeCurrency(overviewQuery.data?.market_cap)}
        />
        <SummaryMetric
          label={t("equityAnalysis.summary.pe")}
          value={formatMultiple(valuationQuery.data?.pe_ratio)}
        />
        <SummaryMetric
          label={t("equityAnalysis.summary.pb")}
          value={formatMultiple(valuationQuery.data?.pb_ratio)}
        />
        <SummaryMetric
          label={t("equityAnalysis.summary.dividendYield")}
          value={
            valuationQuery.data
              ? formatPercent(valuationQuery.data.dividend_yield)
              : "--"
          }
        />
        <SummaryMetric
          label={t("equityAnalysis.summary.roe")}
          value={
            ratiosQuery.data?.roe === null || ratiosQuery.data?.roe === undefined
              ? "--"
              : formatPercent(ratiosQuery.data.roe)
          }
        />
        <SummaryMetric
          label={t("equityAnalysis.summary.revenueGrowth")}
          value={
            growthQuery.data?.revenue_growth === null ||
            growthQuery.data?.revenue_growth === undefined
              ? "--"
              : formatPercent(growthQuery.data.revenue_growth)
          }
        />
        <SummaryMetric
          label={t("equityAnalysis.summary.valuation")}
          value={valuationQuery.data?.valuation_status ?? "--"}
        />
        <SummaryMetric
          label="Price source"
          value={
            overviewQuery.data?.price_timestamp
              ? `${overviewQuery.data.price_source} / ${overviewQuery.data.price_timestamp}`
              : overviewQuery.data?.price_source ?? "--"
          }
        />
      </section>

      <EquitySection
        title="Institutional CFA workstation"
        description="CAPM, DuPont, earnings quality, historical trends, DCF, data quality and portfolio-ready signals."
      >
        <div className="section-grid section-grid--three">
          <InstitutionalPanel
            title="CAPM required return"
            rows={[
              ["Beta", formatNullableMultiple(capmQuery.data?.beta)],
              ["Risk-free rate", formatNullablePercent(capmQuery.data?.risk_free_rate)],
              [
                "Market risk premium",
                formatNullablePercent(capmQuery.data?.market_risk_premium),
              ],
              [
                "CAPM required return",
                formatNullablePercent(capmQuery.data?.capm_required_return),
              ],
              [
                "Expected vs required",
                formatNullablePercent(
                  capmQuery.data?.expected_return_vs_required_return,
                ),
              ],
              ["Signal", capmQuery.data?.capm_signal ?? "--"],
            ]}
            notes={[
              ...(capmQuery.data?.data_source_notes ?? []),
              ...(capmQuery.data?.warnings ?? []),
            ]}
          />
          <InstitutionalPanel
            title="DuPont analysis"
            rows={[
              ["Net margin", formatNullablePercent(dupontQuery.data?.net_margin)],
              [
                "Asset turnover",
                formatNullableMultiple(dupontQuery.data?.asset_turnover),
              ],
              [
                "Financial leverage",
                formatNullableMultiple(dupontQuery.data?.financial_leverage),
              ],
              [
                "3-step ROE",
                formatNullablePercent(dupontQuery.data?.three_step_roe),
              ],
              [
                "Extended ROE",
                formatNullablePercent(dupontQuery.data?.extended_dupont_roe),
              ],
            ]}
            notes={[...(dupontQuery.data?.drivers ?? []), ...(dupontQuery.data?.warnings ?? [])]}
          />
          <InstitutionalPanel
            title="Quality of earnings"
            rows={[
              [
                "Cash conversion",
                formatNullableMultiple(
                  earningsQualityQuery.data?.cash_conversion_ratio,
                ),
              ],
              [
                "Accruals ratio",
                formatNullablePercent(earningsQualityQuery.data?.accruals_ratio),
              ],
              [
                "FCF conversion",
                formatNullableMultiple(
                  earningsQualityQuery.data?.fcf_conversion_ratio,
                ),
              ],
              [
                "Classification",
                earningsQualityQuery.data?.earnings_quality ?? "--",
              ],
            ]}
            notes={[
              earningsQualityQuery.data?.net_income_vs_operating_cash_flow ?? "",
              ...(earningsQualityQuery.data?.warnings ?? []),
            ].filter(Boolean)}
          />
        </div>

        <div className="section-grid section-grid--three">
          <InstitutionalPanel
            title="Historical trend diagnostics"
            rows={[
              ["Revenue CAGR", formatNullablePercent(historicalQuery.data?.revenue_cagr)],
              ["EPS CAGR", formatNullablePercent(historicalQuery.data?.eps_cagr)],
              [
                "Years",
                historicalQuery.data?.rows
                  ? `${historicalQuery.data.rows[0]?.year} - ${
                      historicalQuery.data.rows[historicalQuery.data.rows.length - 1]
                        ?.year
                    }`
                  : "--",
              ],
            ]}
            notes={[
              ...(historicalQuery.data?.trend_diagnostics ?? []),
              ...(historicalQuery.data?.warnings ?? []),
            ]}
          />
          <InstitutionalPanel
            title="DCF FCFF / FCFE foundation"
            rows={[
              [
                "FCFF value/share",
                dcfQuery.data
                  ? formatCurrency(
                      dcfQuery.data.intrinsic_value_per_share_fcff,
                      overviewQuery.data?.currency ?? "USD",
                    )
                  : "--",
              ],
              [
                "FCFE value/share",
                dcfQuery.data
                  ? formatCurrency(
                      dcfQuery.data.intrinsic_value_per_share_fcfe,
                      overviewQuery.data?.currency ?? "USD",
                    )
                  : "--",
              ],
              [
                "FCFF margin of safety",
                formatNullablePercent(dcfQuery.data?.margin_of_safety_fcff),
              ],
              [
                "FCFE margin of safety",
                formatNullablePercent(dcfQuery.data?.margin_of_safety_fcfe),
              ],
            ]}
            notes={dcfQuery.data?.warnings}
          />
          <InstitutionalPanel
            title="Data quality & sector rules"
            rows={[
              [
                "Quality score",
                dataQualityQuery.data
                  ? `${Math.round(dataQualityQuery.data.quality_score * 100)} / 100`
                  : "--",
              ],
              [
                "Market cap check",
                dataQualityQuery.data?.market_cap_consistent ? "Pass" : "Review",
              ],
              [
                "FCF check",
                dataQualityQuery.data?.fcf_consistent ? "Pass" : "Review",
              ],
              [
                "Signal",
                institutionalSignalsQuery.data?.signal ?? "--",
              ],
            ]}
            notes={[
              ...(sectorInterpretationQuery.data?.ratio_emphasis ?? []),
              ...(sectorInterpretationQuery.data?.interpretation_notes ?? []),
              ...(dataQualityQuery.data?.warnings ?? []),
              dataQualityQuery.data?.demo_data_warning ?? "",
            ].filter(Boolean)}
          />
        </div>
      </EquitySection>

      <EquitySection
        title={t("equityAnalysis.sections.marketOrganization.title")}
        description={t("equityAnalysis.sections.marketOrganization.description")}
      >
        <MarketOrganizationPanel
          profile={securityQuery.data}
          labels={{
            instrumentsTitle: t("equityAnalysis.marketOrganization.instruments"),
            marketTitle: t("equityAnalysis.marketOrganization.market"),
            marketVsBookTitle: t("equityAnalysis.marketOrganization.marketVsBook"),
            type: t("equityAnalysis.marketOrganization.type"),
            exchange: t("equityAnalysis.company.exchange"),
            currency: t("equityAnalysis.company.currency"),
            voting: t("equityAnalysis.security.votingRights"),
            liquidity: t("equityAnalysis.marketOrganization.liquidity"),
            marketCap: t("equityAnalysis.company.marketCap"),
            freeFloatMarketCap: t("equityAnalysis.marketOrganization.freeFloat"),
            bookValuePerShare: t(
              "equityAnalysis.fundamentals.bookValuePerShare",
            ),
            marketToBook: t("equityAnalysis.marketOrganization.marketToBook"),
            demoBadge: t("equityAnalysis.controls.demoData"),
          }}
        />
      </EquitySection>

      <EquitySection
        title={t("equityAnalysis.sections.company.title")}
        description={t("equityAnalysis.sections.company.description")}
      >
        <div className="section-grid section-grid--two">
          <CompanyOverviewCard
            overview={overviewQuery.data}
            labels={{
              title: t("equityAnalysis.company.title"),
              company: t("equityAnalysis.company.company"),
              ticker: t("equityAnalysis.company.ticker"),
              exchange: t("equityAnalysis.company.exchange"),
              sector: t("equityAnalysis.company.sector"),
              industry: t("equityAnalysis.company.industry"),
              country: t("equityAnalysis.company.country"),
              currency: t("equityAnalysis.company.currency"),
              marketCap: t("equityAnalysis.company.marketCap"),
              latestPrice: t("equityAnalysis.company.latestPrice"),
              benchmark: t("equityAnalysis.company.benchmark"),
            }}
          />
          <section className="card equity-card">
            <h3>{t("equityAnalysis.company.profile")}</h3>
            <p>{overviewQuery.data?.business_description ?? "--"}</p>
            <span className="status-pill">
              {overviewQuery.data?.sector ?? "--"} / {overviewQuery.data?.industry ?? "--"}
            </span>
          </section>
        </div>
      </EquitySection>

      <EquitySection
        title={t("equityAnalysis.sections.industry.title")}
        description={t("equityAnalysis.sections.industry.description")}
      >
        <div className="section-grid section-grid--two">
          <IndustryAnalysisPanel
            analysis={industryQuery.data ?? overviewQuery.data?.industry_analysis}
            labels={{
              title: t("equityAnalysis.industry.title"),
              classification: t("equityAnalysis.industry.classification"),
              porter: t("equityAnalysis.industry.porter"),
              pestle: t("equityAnalysis.industry.pestle"),
              position: t("equityAnalysis.industry.position"),
            }}
          />
          <section className="card equity-card">
            <h3>{t("equityAnalysis.industry.competitiveDetails")}</h3>
            <dl className="equity-definition-list">
              <Definition
                label={t("equityAnalysis.industry.barriers")}
                value={industryQuery.data?.barriers_to_entry ?? "--"}
              />
              <Definition
                label={t("equityAnalysis.industry.pricingPower")}
                value={industryQuery.data?.pricing_power ?? "--"}
              />
              <Definition
                label={t("equityAnalysis.industry.substitution")}
                value={industryQuery.data?.substitution_risk ?? "--"}
              />
              <Definition
                label={t("equityAnalysis.industry.rivalry")}
                value={industryQuery.data?.competitive_rivalry ?? "--"}
              />
            </dl>
          </section>
        </div>
      </EquitySection>

      <EquitySection
        title={t("equityAnalysis.sections.business.title")}
        description={t("equityAnalysis.sections.business.description")}
      >
        <BusinessModelPanel
          model={overviewQuery.data?.business_model}
          labels={{
            title: t("equityAnalysis.business.title"),
            summary: t("equityAnalysis.business.summary"),
            drivers: t("equityAnalysis.business.drivers"),
            pricingPower: t("equityAnalysis.business.pricingPower"),
            operatingLeverage: t("equityAnalysis.business.operatingLeverage"),
          }}
        />
        <BusinessDriverPanels
          business={businessQuery.data}
          labels={{
            revenueDrivers: t("equityAnalysis.business.drivers"),
            revenueSegments: t("equityAnalysis.business.segments"),
            geographicExposure: t("equityAnalysis.business.geographic"),
            operatingLeverage: t("equityAnalysis.business.operatingLeverage"),
            cyclicality: t("equityAnalysis.business.cyclicality"),
            capitalIntensity: t("equityAnalysis.business.capitalIntensity"),
            comingSoon: t("common.comingSoon"),
          }}
        />
      </EquitySection>

      <EquitySection
        title={t("equityAnalysis.sections.fundamentals.title")}
        description={t("equityAnalysis.sections.fundamentals.description")}
      >
        <FinancialSnapshotPanels
          fundamentals={fundamentalsQuery.data}
          labels={{
            incomeStatement: t("equityAnalysis.fundamentals.incomeStatement"),
            balanceSheet: t("equityAnalysis.fundamentals.balanceSheet"),
            cashFlow: t("equityAnalysis.fundamentals.cashFlow"),
            revenue: t("equityAnalysis.fundamentals.revenue"),
            grossProfit: t("equityAnalysis.fundamentals.grossProfit"),
            operatingIncome: t("equityAnalysis.fundamentals.operatingIncome"),
            ebit: t("equityAnalysis.fundamentals.ebit"),
            ebitda: t("equityAnalysis.fundamentals.ebitda"),
            netIncome: t("equityAnalysis.fundamentals.netIncome"),
            assets: t("equityAnalysis.fundamentals.assets"),
            liabilities: t("equityAnalysis.fundamentals.liabilities"),
            equity: t("equityAnalysis.fundamentals.equity"),
            debt: t("equityAnalysis.fundamentals.debt"),
            cash: t("equityAnalysis.fundamentals.cash"),
            workingCapital: t("equityAnalysis.fundamentals.workingCapital"),
            operatingCashFlow: t("equityAnalysis.fundamentals.operatingCashFlow"),
            capex: t("equityAnalysis.fundamentals.capex"),
            freeCashFlow: t("equityAnalysis.fundamentals.freeCashFlow"),
          }}
        />
        <FundamentalsTable
          fundamentals={fundamentalsQuery.data}
          labels={{
            title: t("equityAnalysis.fundamentals.title"),
            metric: t("equityAnalysis.table.metric"),
            value: t("equityAnalysis.table.value"),
            revenue: t("equityAnalysis.fundamentals.revenue"),
            ebit: t("equityAnalysis.fundamentals.ebit"),
            ebitda: t("equityAnalysis.fundamentals.ebitda"),
            netIncome: t("equityAnalysis.fundamentals.netIncome"),
            eps: t("equityAnalysis.fundamentals.eps"),
            dividends: t("equityAnalysis.fundamentals.dividends"),
            assets: t("equityAnalysis.fundamentals.assets"),
            liabilities: t("equityAnalysis.fundamentals.liabilities"),
            equity: t("equityAnalysis.fundamentals.equity"),
            debt: t("equityAnalysis.fundamentals.debt"),
            cash: t("equityAnalysis.fundamentals.cash"),
            operatingCashFlow: t("equityAnalysis.fundamentals.operatingCashFlow"),
            freeCashFlow: t("equityAnalysis.fundamentals.freeCashFlow"),
            bookValuePerShare: t("equityAnalysis.fundamentals.bookValuePerShare"),
            enterpriseValue: t("equityAnalysis.fundamentals.enterpriseValue"),
          }}
        />
      </EquitySection>

      <EquitySection
        title={t("equityAnalysis.sections.ratios.title")}
        description={t("equityAnalysis.sections.ratios.description")}
      >
        <RatiosGrid
          ratios={ratiosQuery.data}
          labels={{
            title: t("equityAnalysis.ratios.title"),
            profitability: t("equityAnalysis.ratios.profitability"),
            liquidity: t("equityAnalysis.ratios.liquidity"),
            leverage: t("equityAnalysis.ratios.leverage"),
            dividend: t("equityAnalysis.ratios.dividend"),
            grossMargin: t("equityAnalysis.ratios.grossMargin"),
            operatingMargin: t("equityAnalysis.ratios.operatingMargin"),
            netMargin: t("equityAnalysis.ratios.netMargin"),
            roe: t("equityAnalysis.ratios.roe"),
            roa: t("equityAnalysis.ratios.roa"),
            currentRatio: t("equityAnalysis.ratios.currentRatio"),
            quickRatio: t("equityAnalysis.ratios.quickRatio"),
            currentRatioFormula: t("equityAnalysis.ratios.currentRatioFormula"),
            quickRatioFormula: t("equityAnalysis.ratios.quickRatioFormula"),
            debtToEquity: t("equityAnalysis.ratios.debtToEquity"),
            interestCoverage: t("equityAnalysis.ratios.interestCoverage"),
            payout: t("equityAnalysis.ratios.payout"),
            retention: t("equityAnalysis.ratios.retention"),
            sustainableGrowth: t("equityAnalysis.ratios.sustainableGrowth"),
          }}
        />
        <EquityMetricGrid
          metrics={[
            {
              label: t("equityAnalysis.ratios.ebitdaMargin"),
              value:
                ratiosQuery.data?.ebitda_margin === null ||
                ratiosQuery.data?.ebitda_margin === undefined
                  ? "--"
                  : formatPercent(ratiosQuery.data.ebitda_margin),
            },
            {
              label: t("equityAnalysis.ratios.roic"),
              value:
                ratiosQuery.data?.roic === null || ratiosQuery.data?.roic === undefined
                  ? "--"
                  : formatPercent(ratiosQuery.data.roic),
            },
            {
              label: t("equityAnalysis.ratios.debtToAssets"),
              value:
                ratiosQuery.data?.debt_to_assets === null ||
                ratiosQuery.data?.debt_to_assets === undefined
                  ? "--"
                  : formatPercent(ratiosQuery.data.debt_to_assets),
            },
            {
              label: t("equityAnalysis.ratios.netDebtEbitda"),
              value: formatMultiple(ratiosQuery.data?.net_debt_to_ebitda),
            },
            {
              label: t("equityAnalysis.ratios.assetTurnover"),
              value: formatMultiple(ratiosQuery.data?.asset_turnover),
            },
            {
              label: t("equityAnalysis.ratios.fcfMargin"),
              value:
                ratiosQuery.data?.free_cash_flow_margin === null ||
                ratiosQuery.data?.free_cash_flow_margin === undefined
                  ? "--"
                  : formatPercent(ratiosQuery.data.free_cash_flow_margin),
            },
            {
              label: t("equityAnalysis.ratios.qualityScore"),
              value: ratiosQuery.data
                ? `${Math.round(ratiosQuery.data.quality_score * 100)} / 100`
                : "--",
            },
          ]}
        />
      </EquitySection>

      <EquitySection
        title={t("equityAnalysis.sections.growth.title")}
        description={t("equityAnalysis.sections.growth.description")}
      >
        <GrowthPanels
          growth={growthQuery.data}
          labels={{
            revenueGrowth: t("equityAnalysis.growth.revenueGrowth"),
            epsGrowth: t("equityAnalysis.growth.epsGrowth"),
            operatingIncomeGrowth: t("equityAnalysis.growth.operatingIncomeGrowth"),
            dividendGrowth: t("equityAnalysis.growth.dividendGrowth"),
            sustainableGrowth: t("equityAnalysis.ratios.sustainableGrowth"),
            retention: t("equityAnalysis.ratios.retention"),
            roe: t("equityAnalysis.ratios.roe"),
            profile: t("equityAnalysis.growth.profile"),
            forecast: t("equityAnalysis.growth.forecast"),
          }}
        />
      </EquitySection>

      <EquitySection
        title={t("equityAnalysis.sections.valuation.title")}
        description={t("equityAnalysis.sections.valuation.description")}
      >
        <div className="section-grid section-grid--three">
          <IntrinsicValueCard
            valuation={valuationQuery.data}
            labels={{
              title: t("equityAnalysis.valuation.intrinsicTitle"),
              marketPrice: t("equityAnalysis.valuation.marketPrice"),
              ggm: t("equityAnalysis.valuation.ggm"),
              ddm: t("equityAnalysis.valuation.ddm"),
              blended: t("equityAnalysis.valuation.blended"),
              requiredReturn: t("equityAnalysis.valuation.requiredReturn"),
              growth: t("equityAnalysis.valuation.growth"),
              limitation: t("equityAnalysis.valuation.modelLimitation"),
            }}
          />
          <MarginOfSafetyCard
            valuation={valuationQuery.data}
            labels={{
              title: t("equityAnalysis.valuation.marginTitle"),
              description: t("equityAnalysis.valuation.marginDescription"),
              marketPrice: t("equityAnalysis.valuation.marketPrice"),
              modelValue: t("equityAnalysis.valuation.blended"),
              signal: t("equityAnalysis.valuation.modelSignal"),
              extremeWarning: t("equityAnalysis.valuation.extremeMarginWarning"),
            }}
          />
          <ValuationMultiplesTable
            valuation={valuationQuery.data}
            labels={{
              title: t("equityAnalysis.valuation.multiplesTitle"),
              metric: t("equityAnalysis.table.metric"),
              value: t("equityAnalysis.table.value"),
              pe: t("equityAnalysis.valuation.pe"),
              pb: t("equityAnalysis.valuation.pb"),
              ps: t("equityAnalysis.valuation.ps"),
              evEbitda: t("equityAnalysis.valuation.evEbitda"),
              dividendYield: t("equityAnalysis.valuation.dividendYield"),
              earningsYield: t("equityAnalysis.valuation.earningsYield"),
              fcfYield: t("equityAnalysis.valuation.fcfYield"),
              impliedCost: t("equityAnalysis.valuation.impliedCost"),
              impliedGrowth: t("equityAnalysis.valuation.impliedGrowth"),
            }}
          />
        </div>
        <GGMCalculator
          valuation={valuationQuery.data}
          labels={{
            title: t("equityAnalysis.ggm.title"),
            dividend: t("equityAnalysis.ggm.dividend"),
            requiredReturn: t("equityAnalysis.ggm.requiredReturn"),
            growth: t("equityAnalysis.ggm.growth"),
            calculate: t("equityAnalysis.ggm.calculate"),
            intrinsicValue: t("equityAnalysis.ggm.intrinsicValue"),
            spread: t("equityAnalysis.ggm.spread"),
            sensitivity: t("equityAnalysis.ggm.sensitivity"),
            invalid: t("equityAnalysis.ggm.invalid"),
            invalidCell: t("equityAnalysis.ggm.invalidCell"),
            limitation: t("equityAnalysis.ggm.limitation"),
          }}
        />
      </EquitySection>

      <EquitySection
        title={t("equityAnalysis.sections.relative.title")}
        description={t("equityAnalysis.sections.relative.description")}
      >
        <RelativeValuationCards
          relative={relativeQuery.data}
          labels={{
            relativeTitle: t("equityAnalysis.relative.title"),
            multiple: t("equityAnalysis.relative.multiple"),
            company: t("equityAnalysis.relative.company"),
            peerMedian: t("equityAnalysis.relative.peerMedian"),
            status: t("equityAnalysis.relative.status"),
            premiumDiscount: t("equityAnalysis.relative.premiumDiscount"),
          }}
        />
      </EquitySection>

      <EquitySection
        title={t("equityAnalysis.sections.peers.title")}
        description={t("equityAnalysis.sections.peers.description")}
      >
        <PeerComparisonTable
          peers={peersQuery.data}
          labels={{
            peerTitle: t("equityAnalysis.peers.title"),
            symbol: t("equityAnalysis.peers.symbol"),
            pe: t("equityAnalysis.valuation.pe"),
            pb: t("equityAnalysis.valuation.pb"),
            roe: t("equityAnalysis.ratios.roe"),
            growth: t("equityAnalysis.growth.revenueGrowth"),
            valuation: t("equityAnalysis.diagnostics.valuation"),
            benchmark: t("equityAnalysis.peers.benchmark"),
            relativePerformance: t("equityAnalysis.peers.relativePerformance"),
            summary: t("equityAnalysis.peers.summary"),
          }}
        />
      </EquitySection>

      <EquitySection
        title={t("equityAnalysis.sections.corporateActions.title")}
        description={t("equityAnalysis.sections.corporateActions.description")}
      >
        <CorporateActionsPanel
          corporateActions={corporateActionsQuery.data}
          labels={{
            dividendTitle: t("equityAnalysis.corporateActions.dividend"),
            shareholderReturns: t("equityAnalysis.corporateActions.shareholderReturns"),
            timeline: t("equityAnalysis.corporateActions.timeline"),
            dividendYield: t("equityAnalysis.valuation.dividendYield"),
            payout: t("equityAnalysis.ratios.payout"),
            retention: t("equityAnalysis.ratios.retention"),
            buybackYield: t("equityAnalysis.corporateActions.buybackYield"),
            totalYield: t("equityAnalysis.corporateActions.totalYield"),
          }}
        />
      </EquitySection>

      <EquitySection
        title={t("equityAnalysis.sections.governance.title")}
        description={t("equityAnalysis.sections.governance.description")}
      >
        <GovernanceRiskPanel
          diagnostics={diagnosticsQuery.data}
          labels={{
            governance: t("equityAnalysis.governance.governance"),
            esg: t("equityAnalysis.governance.esg"),
            riskFactors: t("equityAnalysis.governance.riskFactors"),
            watchlist: t("equityAnalysis.governance.watchlist"),
          }}
        />
      </EquitySection>

      <EquitySection
        title={t("equityAnalysis.sections.diagnostics.title")}
        description={t("equityAnalysis.sections.diagnostics.description")}
      >
        <div className="section-grid section-grid--two">
          <EquityDiagnosticsPanel
            diagnostics={diagnosticsQuery.data}
            labels={{
              title: t("equityAnalysis.diagnostics.title"),
              valuation: t("equityAnalysis.diagnostics.valuation"),
              profitability: t("equityAnalysis.diagnostics.profitability"),
              balanceSheet: t("equityAnalysis.diagnostics.balanceSheet"),
              strengths: t("equityAnalysis.diagnostics.strengths"),
              risks: t("equityAnalysis.diagnostics.risks"),
            }}
          />
          <AnalystSummaryPanel
            diagnostics={diagnosticsQuery.data}
            labels={{
              title: t("equityAnalysis.summaryPanel.title"),
              note: t("equityAnalysis.summaryPanel.note"),
            }}
          />
        </div>
        <AnalystDiagnosticsPanels
          diagnostics={diagnosticsQuery.data}
          labels={{
            cases: t("equityAnalysis.diagnostics.cases"),
            strengthsWeaknesses: t("equityAnalysis.diagnostics.strengthsWeaknesses"),
            scorecard: t("equityAnalysis.diagnostics.scorecard"),
            strengths: t("equityAnalysis.diagnostics.strengths"),
            weaknesses: t("equityAnalysis.diagnostics.weaknesses"),
            valuation: t("equityAnalysis.diagnostics.valuation"),
            profitability: t("equityAnalysis.diagnostics.profitability"),
            balanceSheet: t("equityAnalysis.diagnostics.balanceSheet"),
            growth: t("equityAnalysis.growth.profile"),
            dividend: t("equityAnalysis.diagnostics.dividend"),
            risk: t("equityAnalysis.diagnostics.risk"),
            disclaimer: t("equityAnalysis.diagnostics.disclaimer"),
          }}
        />
      </EquitySection>
    </div>
  );
}

function useEquityQuery<T>(
  key: string,
  symbol: string,
  endpoint: (symbol: string) => string,
) {
  return useQuery({
    queryKey: ["equity", key, symbol],
    queryFn: () => apiClient.get<T>(endpoint(symbol)),
  });
}

function InstitutionalPanel({
  title,
  rows,
  notes,
}: {
  title: string;
  rows: Array<[string, string]>;
  notes?: string[];
}) {
  return (
    <section className="card equity-card compact-table-card">
      <h3>{title}</h3>
      <table className="compact-table">
        <tbody>
          {rows.map(([label, value]) => (
            <tr key={label}>
              <td>{label}</td>
              <td>{value}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {notes?.length ? (
        <ul>
          {notes.map((note) => (
            <li key={note}>{note}</li>
          ))}
        </ul>
      ) : null}
    </section>
  );
}

function formatNullablePercent(value: number | null | undefined) {
  return value === null || value === undefined ? "--" : formatPercent(value);
}

function formatNullableMultiple(value: number | null | undefined) {
  return value === null || value === undefined ? "--" : formatMultiple(value);
}

function EquitySection({
  title,
  description,
  children,
}: {
  title: string;
  description: string;
  children: ReactNode;
}) {
  return (
    <section className="analytics-section">
      <header className="analytics-section__header">
        <h2>{title}</h2>
        <p>{description}</p>
      </header>
      {children}
    </section>
  );
}

function SummaryMetric({ label, value }: { label: string; value: string }) {
  return (
    <div className="equity-summary__metric">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function Definition({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt>{label}</dt>
      <dd>{value}</dd>
    </div>
  );
}
