import { useState } from "react";
import { useQuery } from "@tanstack/react-query";

import { PageHeader } from "../../../components/layout/PageHeader";
import { apiClient } from "../../../lib/api-client";
import { endpoints } from "../../../lib/endpoints";
import { formatCurrency, formatPercent } from "../../../lib/formatters";
import { useTranslation } from "../../../hooks/useTranslation";
import {
  EquityDiagnosticsResponse,
  EquityFundamentalsResponse,
  EquityOverviewResponse,
  EquityRatiosResponse,
  EquityValuationResponse,
} from "../../../types/equity";
import { AnalystSummaryPanel } from "../components/AnalystSummaryPanel";
import { BusinessModelPanel } from "../components/BusinessModelPanel";
import { CompanyOverviewCard } from "../components/CompanyOverviewCard";
import { EquityDiagnosticsPanel } from "../components/EquityDiagnosticsPanel";
import { EquitySecurityProfileCard } from "../components/EquitySecurityProfileCard";
import { EquitySelector } from "../components/EquitySelector";
import { FundamentalsTable } from "../components/FundamentalsTable";
import { GGMCalculator } from "../components/GGMCalculator";
import { IndustryAnalysisPanel } from "../components/IndustryAnalysisPanel";
import { IntrinsicValueCard } from "../components/IntrinsicValueCard";
import { MarginOfSafetyCard } from "../components/MarginOfSafetyCard";
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

  const overviewQuery = useQuery({
    queryKey: ["equity-overview", selectedSymbol],
    queryFn: () =>
      apiClient.get<EquityOverviewResponse>(
        endpoints.equityOverview(selectedSymbol),
      ),
  });

  const fundamentalsQuery = useQuery({
    queryKey: ["equity-fundamentals", selectedSymbol],
    queryFn: () =>
      apiClient.get<EquityFundamentalsResponse>(
        endpoints.equityFundamentals(selectedSymbol),
      ),
  });

  const ratiosQuery = useQuery({
    queryKey: ["equity-ratios", selectedSymbol],
    queryFn: () =>
      apiClient.get<EquityRatiosResponse>(endpoints.equityRatios(selectedSymbol)),
  });

  const valuationQuery = useQuery({
    queryKey: ["equity-valuation", selectedSymbol],
    queryFn: () =>
      apiClient.get<EquityValuationResponse>(
        endpoints.equityValuation(selectedSymbol),
      ),
  });

  const diagnosticsQuery = useQuery({
    queryKey: ["equity-diagnostics", selectedSymbol],
    queryFn: () =>
      apiClient.get<EquityDiagnosticsResponse>(
        endpoints.equityDiagnostics(selectedSymbol),
      ),
  });

  const hasApiError =
    overviewQuery.isError ||
    fundamentalsQuery.isError ||
    ratiosQuery.isError ||
    valuationQuery.isError ||
    diagnosticsQuery.isError;

  const isLoading =
    overviewQuery.isLoading ||
    fundamentalsQuery.isLoading ||
    ratiosQuery.isLoading ||
    valuationQuery.isLoading ||
    diagnosticsQuery.isLoading;

  return (
    <div className="page equity-analysis-page">
      <PageHeader
        title={t("equityAnalysis.title")}
        subtitle={t("equityAnalysis.subtitle")}
      />

      <EquitySelector
        options={EQUITY_OPTIONS}
        selectedSymbol={selectedSymbol}
        onSelect={setSelectedSymbol}
        label={t("equityAnalysis.selector")}
      />

      {isLoading ? <p>{t("common.loading")}</p> : null}
      {hasApiError ? (
        <p className="status-message status-message--error">
          {t("equityAnalysis.apiError")}
        </p>
      ) : null}

      <section className="equity-summary">
        <div className="equity-summary__identity">
          <span>{t("equityAnalysis.summary.company")}</span>
          <strong>{overviewQuery.data?.company_name ?? selectedSymbol}</strong>
          <small>
            {overviewQuery.data?.exchange ?? "--"} /{" "}
            {overviewQuery.data?.benchmark_symbol ?? "--"}
          </small>
        </div>
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
          value={
            overviewQuery.data
              ? `${formatCurrency(overviewQuery.data.market_cap)}B`
              : "--"
          }
        />
        <SummaryMetric
          label={t("equityAnalysis.summary.intrinsicValue")}
          value={
            valuationQuery.data
              ? formatCurrency(valuationQuery.data.intrinsic_value)
              : "--"
          }
        />
        <SummaryMetric
          label={t("equityAnalysis.summary.marginOfSafety")}
          value={
            valuationQuery.data
              ? formatPercent(valuationQuery.data.margin_of_safety)
              : "--"
          }
        />
        <SummaryMetric
          label={t("equityAnalysis.summary.valuation")}
          value={diagnosticsQuery.data?.valuation_status ?? "--"}
        />
      </section>

      <section className="analytics-section">
        <header className="analytics-section__header">
          <h2>{t("equityAnalysis.sections.overview.title")}</h2>
          <p>{t("equityAnalysis.sections.overview.description")}</p>
        </header>
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
          <EquitySecurityProfileCard
            profile={overviewQuery.data?.security_profile}
            labels={{
              title: t("equityAnalysis.security.title"),
              equityType: t("equityAnalysis.security.equityType"),
              votingRights: t("equityAnalysis.security.votingRights"),
              dividendProfile: t("equityAnalysis.security.dividendProfile"),
              bookValueContext: t("equityAnalysis.security.bookValueContext"),
              riskReturnNotes: t("equityAnalysis.security.riskReturnNotes"),
            }}
          />
        </div>
      </section>

      <section className="analytics-section">
        <header className="analytics-section__header">
          <h2>{t("equityAnalysis.sections.industry.title")}</h2>
          <p>{t("equityAnalysis.sections.industry.description")}</p>
        </header>
        <div className="section-grid section-grid--two">
          <IndustryAnalysisPanel
            analysis={overviewQuery.data?.industry_analysis}
            labels={{
              title: t("equityAnalysis.industry.title"),
              classification: t("equityAnalysis.industry.classification"),
              porter: t("equityAnalysis.industry.porter"),
              pestle: t("equityAnalysis.industry.pestle"),
              position: t("equityAnalysis.industry.position"),
            }}
          />
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
        </div>
      </section>

      <section className="analytics-section">
        <header className="analytics-section__header">
          <h2>{t("equityAnalysis.sections.fundamentals.title")}</h2>
          <p>{t("equityAnalysis.sections.fundamentals.description")}</p>
        </header>
        <div className="section-grid section-grid--two">
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
              bookValuePerShare: t(
                "equityAnalysis.fundamentals.bookValuePerShare",
              ),
              enterpriseValue: t("equityAnalysis.fundamentals.enterpriseValue"),
            }}
          />
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
              debtToEquity: t("equityAnalysis.ratios.debtToEquity"),
              interestCoverage: t("equityAnalysis.ratios.interestCoverage"),
              payout: t("equityAnalysis.ratios.payout"),
              retention: t("equityAnalysis.ratios.retention"),
              sustainableGrowth: t("equityAnalysis.ratios.sustainableGrowth"),
            }}
          />
        </div>
      </section>

      <section className="analytics-section">
        <header className="analytics-section__header">
          <h2>{t("equityAnalysis.sections.valuation.title")}</h2>
          <p>{t("equityAnalysis.sections.valuation.description")}</p>
        </header>
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
            }}
          />
          <MarginOfSafetyCard
            valuation={valuationQuery.data}
            labels={{
              title: t("equityAnalysis.valuation.marginTitle"),
              description: t("equityAnalysis.valuation.marginDescription"),
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
          }}
        />
      </section>

      <section className="analytics-section">
        <header className="analytics-section__header">
          <h2>{t("equityAnalysis.sections.diagnostics.title")}</h2>
          <p>{t("equityAnalysis.sections.diagnostics.description")}</p>
        </header>
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
      </section>
    </div>
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
