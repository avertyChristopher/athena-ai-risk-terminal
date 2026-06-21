import { useMemo, useState } from "react";
import type { ReactNode } from "react";
import { useQuery } from "@tanstack/react-query";

import { MoneyValue } from "../../../components/finance/MoneyValue";
import { PercentValue } from "../../../components/finance/PercentValue";
import { PageHeader } from "../../../components/layout/PageHeader";
import { EmptyState } from "../../../components/ui/EmptyState";
import { LoadingState } from "../../../components/ui/LoadingState";
import { usePortfolioContext } from "../../../context/PortfolioContext";
import { useTranslation } from "../../../hooks/useTranslation";
import { apiClient } from "../../../lib/api-client";
import { endpoints } from "../../../lib/endpoints";
import type {
  BondInputs,
  BondPricingResponse,
  BondType,
  CouponFrequency,
  DurationConvexityResponse,
  PortfolioRatesExposureResponse,
  RateScenarioResponse,
  RateScenarioType,
  RatesLabStatus,
  YieldAnalysisResponse,
  YieldCurveResponse,
} from "../../../types/rates-lab";

type RatesTab =
  | "pricing"
  | "yield"
  | "duration"
  | "curve"
  | "scenarios"
  | "portfolio"
  | "cfa"
  | "commentary"
  | "quality";

const tabs: RatesTab[] = [
  "pricing",
  "yield",
  "duration",
  "curve",
  "scenarios",
  "portfolio",
  "cfa",
  "commentary",
  "quality",
];

const scenarioTypes: RateScenarioType[] = [
  "parallel_up",
  "parallel_down",
  "steepener",
  "flattener",
  "short_rate_up",
  "long_rate_up",
  "short_rate_down",
  "long_rate_down",
];

export function RatesLabPage() {
  const { t, i18n } = useTranslation();
  const { portfolios, selectedPortfolioId, selectPortfolio } = usePortfolioContext();
  const language = i18n.resolvedLanguage?.startsWith("fr") ? "fr" : "en";
  const [activeTab, setActiveTab] = useState<RatesTab>("pricing");
  const [bondType, setBondType] = useState<BondType>("coupon_bond");
  const [faceValue, setFaceValue] = useState(1000);
  const [couponRatePct, setCouponRatePct] = useState(5);
  const [frequency, setFrequency] = useState<CouponFrequency>("semiannual");
  const [yearsToMaturity, setYearsToMaturity] = useState(5);
  const [yieldPct, setYieldPct] = useState(4.5);
  const [marketPrice, setMarketPrice] = useState(1000);
  const [shockBps, setShockBps] = useState(100);
  const [scenarioType, setScenarioType] =
    useState<RateScenarioType>("parallel_up");
  const [settlementDate, setSettlementDate] = useState("");
  const [maturityDate, setMaturityDate] = useState("");

  const bondInputs = useMemo<BondInputs>(
    () => ({
      bond_type: bondType,
      face_value: clamp(faceValue, 1, 100_000_000),
      coupon_rate: bondType === "zero_coupon" ? 0 : clamp(couponRatePct, 0, 100) / 100,
      coupon_frequency: frequency,
      years_to_maturity: clamp(yearsToMaturity, 0.01, 100),
      yield_to_maturity: clamp(yieldPct, -99, 1000) / 100,
      language,
    }),
    [bondType, couponRatePct, faceValue, frequency, language, yearsToMaturity, yieldPct],
  );

  const pricingInputs = useMemo(
    () => ({
      ...bondInputs,
      ...(settlementDate && maturityDate
        ? { settlement_date: settlementDate, maturity_date: maturityDate }
        : {}),
    }),
    [bondInputs, maturityDate, settlementDate],
  );

  const statusQuery = useQuery({
    queryKey: ["rates-lab-status"],
    queryFn: () => apiClient.get<RatesLabStatus>(endpoints.ratesLabStatus),
  });
  const pricingQuery = useQuery({
    queryKey: ["rates-lab-bond-price", pricingInputs],
    queryFn: () =>
      apiClient.post<BondPricingResponse>(endpoints.ratesLabBondPrice, pricingInputs),
  });
  const yieldQuery = useQuery({
    queryKey: ["rates-lab-yield", bondInputs, marketPrice],
    queryFn: () =>
      apiClient.post<YieldAnalysisResponse>(endpoints.ratesLabYieldAnalysis, {
        price: clamp(marketPrice, 0.01, 100_000_000),
        face_value: bondInputs.face_value,
        coupon_rate: bondInputs.coupon_rate,
        coupon_frequency: bondInputs.coupon_frequency,
        years_to_maturity: bondInputs.years_to_maturity,
        language,
      }),
  });
  const durationQuery = useQuery({
    queryKey: ["rates-lab-duration", bondInputs, shockBps],
    queryFn: () =>
      apiClient.post<DurationConvexityResponse>(
        endpoints.ratesLabDurationConvexity,
        { ...bondInputs, rate_shock_bps: clamp(shockBps, -5000, 5000) },
      ),
  });
  const curveQuery = useQuery({
    queryKey: ["rates-lab-curve"],
    queryFn: () =>
      apiClient.post<YieldCurveResponse>(endpoints.ratesLabYieldCurve, {
        curve_type: "treasury_demo",
        interpolation_method: "linear",
        language,
      }),
  });
  const scenarioQuery = useQuery({
    queryKey: ["rates-lab-scenario", bondInputs, scenarioType, shockBps],
    queryFn: () =>
      apiClient.post<RateScenarioResponse>(endpoints.ratesLabRateScenarios, {
        ...bondInputs,
        scenario_type: scenarioType,
        shock_bps: Math.abs(clamp(shockBps, 0, 5000)),
      }),
  });
  const portfolioQuery = useQuery({
    queryKey: ["rates-lab-portfolio", selectedPortfolioId, shockBps],
    enabled: Boolean(selectedPortfolioId),
    queryFn: () =>
      apiClient.post<PortfolioRatesExposureResponse>(
        endpoints.ratesLabPortfolioExposure,
        { portfolio_id: selectedPortfolioId, shock_bps: Math.abs(shockBps) },
      ),
  });

  const pricing = pricingQuery.data;
  const duration = durationQuery.data;
  const hasAnyError = [
    statusQuery,
    pricingQuery,
    yieldQuery,
    durationQuery,
    curveQuery,
    scenarioQuery,
    portfolioQuery,
  ].some((query) => query.isError);
  const statusLabel = hasAnyError
    ? t("ratesLab.status.degraded")
    : statusQuery.data?.status === "ready"
      ? t("ratesLab.status.connected")
      : t("common.loading");

  function reprice() {
    void pricingQuery.refetch();
    void yieldQuery.refetch();
    void durationQuery.refetch();
    void scenarioQuery.refetch();
    if (selectedPortfolioId) void portfolioQuery.refetch();
  }

  function retryAll() {
    void statusQuery.refetch();
    reprice();
    void curveQuery.refetch();
  }

  return (
    <div className="page rates-lab-page risk-monitor-page">
      <PageHeader
        title={t("ratesLab.title")}
        subtitle={t("ratesLab.subtitle")}
      />

      <section className="risk-monitor-command-panel">
        <div>
          <span>{t("ratesLab.workbench.eyebrow")}</span>
          <h2>{t("ratesLab.workbench.title")}</h2>
          <p>{t("ratesLab.workbench.description")}</p>
        </div>
        <div className="risk-monitor-badge-cluster">
          <Badge label={statusLabel} tone={hasAnyError ? "warning" : "success"} />
          <Badge label={t("ratesLab.badges.cfa")} tone="info" />
          <Badge label={t("ratesLab.badges.demoCurve")} tone="warning" />
          <Badge label={t("ratesLab.badges.riskMonitor")} tone="success" />
        </div>
      </section>

      <section className="risk-monitor-controls-panel">
        <div className="risk-monitor-controls-panel__header">
          <div>
            <span>{t("ratesLab.controls.eyebrow")}</span>
            <h2>{t("ratesLab.controls.title")}</h2>
            <p>{t("ratesLab.controls.description")}</p>
          </div>
          <button className="button button--primary" type="button" onClick={reprice}>
            {t("ratesLab.controls.calculate")}
          </button>
        </div>
        <div className="risk-monitor-control-groups">
          <div className="risk-monitor-control-group">
            <h3>{t("ratesLab.controls.bondInputs")}</h3>
            <div className="risk-monitor-control-grid">
              <Field label={t("ratesLab.controls.bondType")}>
                <select value={bondType} onChange={(e) => setBondType(e.target.value as BondType)}>
                  <option value="coupon_bond">{t("ratesLab.labels.couponBond")}</option>
                  <option value="zero_coupon">{t("ratesLab.labels.zeroCoupon")}</option>
                </select>
              </Field>
              <NumberField label={t("ratesLab.controls.faceValue")} min={1} value={faceValue} onChange={setFaceValue} />
              <NumberField label={t("ratesLab.controls.couponRate")} min={0} step={0.1} value={couponRatePct} onChange={setCouponRatePct} />
              <Field label={t("ratesLab.controls.frequency")}>
                <select value={frequency} onChange={(e) => setFrequency(e.target.value as CouponFrequency)}>
                  {(["annual", "semiannual", "quarterly", "monthly"] as CouponFrequency[]).map((item) => (
                    <option key={item} value={item}>{t(`ratesLab.frequency.${item}`)}</option>
                  ))}
                </select>
              </Field>
              <NumberField label={t("ratesLab.controls.maturity")} min={0.01} step={0.25} value={yearsToMaturity} onChange={setYearsToMaturity} />
              <NumberField label={t("ratesLab.controls.ytm")} step={0.1} value={yieldPct} onChange={setYieldPct} />
              <Field label={t("ratesLab.controls.settlementDate")}>
                <input type="date" value={settlementDate} onChange={(event) => setSettlementDate(event.target.value)} />
              </Field>
              <Field label={t("ratesLab.controls.maturityDate")}>
                <input type="date" value={maturityDate} onChange={(event) => setMaturityDate(event.target.value)} />
              </Field>
            </div>
          </div>
          <div className="risk-monitor-control-group">
            <h3>{t("ratesLab.controls.riskInputs")}</h3>
            <div className="risk-monitor-control-grid">
              <NumberField label={t("ratesLab.controls.marketPrice")} min={0.01} value={marketPrice} onChange={setMarketPrice} />
              <NumberField label={t("ratesLab.controls.shockBps")} min={0} step={25} value={shockBps} onChange={setShockBps} />
              <Field label={t("ratesLab.controls.scenarioType")}>
                <select value={scenarioType} onChange={(e) => setScenarioType(e.target.value as RateScenarioType)}>
                  {scenarioTypes.map((item) => (
                    <option key={item} value={item}>{t(`ratesLab.scenarioTypes.${item}`)}</option>
                  ))}
                </select>
              </Field>
              <Field label={t("ratesLab.controls.portfolio")}>
                <select value={selectedPortfolioId} onChange={(e) => selectPortfolio(e.target.value)}>
                  {portfolios.map((portfolio) => (
                    <option key={portfolio.id} value={portfolio.id}>{portfolio.name}</option>
                  ))}
                </select>
              </Field>
            </div>
          </div>
        </div>
      </section>

      {hasAnyError ? (
        <QueryErrorState
          message={t("ratesLab.errors.degradedMessage")}
          onRetry={retryAll}
          t={t}
          title={t("ratesLab.errors.degradedTitle")}
        />
      ) : null}

      {pricing && duration ? (
        <div className="risk-monitor-kpi-grid">
          <Metric title={t("ratesLab.metrics.cleanPrice")} value={<MoneyValue value={pricing.clean_price} />} note={pricing.price_status} />
          <Metric title={t("ratesLab.metrics.ytm")} value={<PercentValue value={bondInputs.yield_to_maturity} />} note={t("ratesLab.notes.inverseRelationship")} />
          <Metric title={t("ratesLab.metrics.modifiedDuration")} value={duration.modified_duration.toFixed(3)} note={t("ratesLab.notes.years")} />
          <Metric title={t("ratesLab.metrics.dv01")} value={<MoneyValue value={duration.dv01} />} note={t("ratesLab.notes.perBasisPoint")} />
        </div>
      ) : null}

      <nav className="risk-monitor-tabs rates-lab-tabs" aria-label={t("ratesLab.tabs.aria")}>
        {tabs.map((tab) => (
          <button
            className={`risk-monitor-tab ${activeTab === tab ? "risk-monitor-tab--active" : ""}`}
            key={tab}
            type="button"
            onClick={() => setActiveTab(tab)}
          >
            <span>{t(`ratesLab.tabs.${tab}`)}</span>
            <small>{t(`ratesLab.tabs.${tab}Short`)}</small>
          </button>
        ))}
      </nav>

      <div className="risk-monitor-panel">
        {activeTab === "pricing" ? <QueryPanel data={pricing} isError={pricingQuery.isError} isLoading={pricingQuery.isLoading} onRetry={() => void pricingQuery.refetch()} render={(data) => <PricingTab pricing={data} t={t} />} t={t} /> : null}
        {activeTab === "yield" ? <QueryPanel data={yieldQuery.data} isError={yieldQuery.isError} isLoading={yieldQuery.isLoading} onRetry={() => void yieldQuery.refetch()} render={(data) => <YieldTab data={data} t={t} />} t={t} /> : null}
        {activeTab === "duration" ? <QueryPanel data={duration} isError={durationQuery.isError} isLoading={durationQuery.isLoading} onRetry={() => void durationQuery.refetch()} render={(data) => <DurationTab data={data} t={t} />} t={t} /> : null}
        {activeTab === "curve" ? <QueryPanel data={curveQuery.data} isError={curveQuery.isError} isLoading={curveQuery.isLoading} onRetry={() => void curveQuery.refetch()} render={(data) => <CurveTab data={data} t={t} />} t={t} /> : null}
        {activeTab === "scenarios" ? <QueryPanel data={scenarioQuery.data} isError={scenarioQuery.isError} isLoading={scenarioQuery.isLoading} onRetry={() => void scenarioQuery.refetch()} render={(data) => <ScenarioTab data={data} t={t} />} t={t} /> : null}
        {activeTab === "portfolio" ? <QueryPanel data={portfolioQuery.data} isError={portfolioQuery.isError} isLoading={portfolioQuery.isLoading} onRetry={() => void portfolioQuery.refetch()} render={(data) => <PortfolioTab data={data} t={t} />} t={t} /> : null}
        {activeTab === "cfa" ? <CfaTab t={t} /> : null}
        {activeTab === "commentary" && pricing && duration ? <CommentaryTab pricing={pricing} duration={duration} t={t} /> : null}
        {activeTab === "commentary" && (!pricing || !duration) ? <EmptyState title={t("ratesLab.empty.title")} message={t("ratesLab.empty.message")} /> : null}
        {activeTab === "quality" && pricing ? <QualityTab pricing={pricing} curve={curveQuery.data} portfolio={portfolioQuery.data} scenario={scenarioQuery.data} t={t} /> : null}
        {activeTab === "quality" && !pricing ? <EmptyState title={t("ratesLab.empty.title")} message={t("ratesLab.empty.message")} /> : null}
      </div>
    </div>
  );
}

function PricingTab({ pricing, t }: { pricing: BondPricingResponse; t: Translator }) {
  return <Section title={t("ratesLab.sections.pricing")} description={pricing.athena_commentary.summary} badges={pricing.data_source.badges}>
    <div className="risk-monitor-mini-grid">
      <Metric title={t("ratesLab.metrics.cleanPrice")} value={<MoneyValue value={pricing.clean_price} />} note={pricing.price_status} />
      <Metric title={t("ratesLab.metrics.dirtyPrice")} value={<MoneyValue value={pricing.dirty_price} />} note={t("ratesLab.notes.includesAccrued")} />
      <Metric title={t("ratesLab.metrics.accruedInterest")} value={<MoneyValue value={pricing.accrued_interest} />} note={t("ratesLab.notes.dayCount")} />
    </div>
    <Table headers={[t("ratesLab.table.period"), t("ratesLab.table.paymentDate"), t("ratesLab.table.time"), t("ratesLab.table.coupon"), t("ratesLab.table.principal"), t("ratesLab.table.presentValue")]} rows={pricing.cash_flow_schedule.map((row) => [row.period, row.payment_date ?? "--", row.time_years.toFixed(2), <MoneyValue value={row.coupon} />, <MoneyValue value={row.principal} />, <MoneyValue value={row.present_value} />])} />
  </Section>;
}

function YieldTab({ data, t }: { data: YieldAnalysisResponse; t: Translator }) {
  return <Section title={t("ratesLab.sections.yield")} description={data.interpretation} badges={[data.convergence_status]}>
    <div className="risk-monitor-mini-grid">
      <Metric title={t("ratesLab.metrics.ytm")} value={data.yield_to_maturity === null ? "--" : <PercentValue value={data.yield_to_maturity} />} note={data.convergence_status} />
      <Metric title={t("ratesLab.metrics.currentYield")} value={<PercentValue value={data.current_yield} />} note={t("ratesLab.notes.annualCouponOverPrice")} />
      <Metric title={t("ratesLab.metrics.hpr")} value={data.holding_period_return === null ? "--" : <PercentValue value={data.holding_period_return} />} note={t("ratesLab.notes.optionalInputs")} />
    </div>
  </Section>;
}

function DurationTab({ data, t }: { data: DurationConvexityResponse; t: Translator }) {
  return <Section title={t("ratesLab.sections.duration")} description={data.risk_interpretation} badges={[t("ratesLab.badges.riskMonitor")] }>
    <div className="risk-monitor-mini-grid">
      <Metric title={t("ratesLab.metrics.macaulayDuration")} value={data.macaulay_duration.toFixed(4)} note={t("ratesLab.notes.years")} />
      <Metric title={t("ratesLab.metrics.modifiedDuration")} value={data.modified_duration.toFixed(4)} note={t("ratesLab.notes.linearSensitivity")} />
      <Metric title={t("ratesLab.metrics.convexity")} value={data.convexity.toFixed(4)} note={t("ratesLab.notes.curvature")} />
      <Metric title={t("ratesLab.metrics.dv01")} value={<MoneyValue value={data.dv01} />} note={t("ratesLab.notes.perBasisPoint")} />
      <Metric title={t("ratesLab.metrics.durationImpact")} value={<MoneyValue value={data.estimated_price_change_duration} />} note={`${data.rate_shock_bps} bps`} />
      <Metric title={t("ratesLab.metrics.convexityImpact")} value={<MoneyValue value={data.estimated_price_change_duration_convexity} />} note={`${data.rate_shock_bps} bps`} />
    </div>
    <div className="risk-monitor-warning-list"><p>{t("ratesLab.notes.durationWarning")}</p></div>
  </Section>;
}

function CurveTab({ data, t }: { data: YieldCurveResponse; t: Translator }) {
  return <Section title={t("ratesLab.sections.curve")} description={data.curve_interpretation} badges={data.data_source.badges}>
    <div className="risk-monitor-mini-grid">
      <Metric title={t("ratesLab.metrics.curveShape")} value={t(`ratesLab.curveShapes.${data.curve_shape}`)} note={t("ratesLab.notes.termStructure")} />
      <Metric title={t("ratesLab.metrics.curveSlope")} value={`${data.curve_slope_bps.toFixed(1)} bps`} note={t("ratesLab.notes.longMinusShort")} />
      <Metric title={t("ratesLab.metrics.forwardPoints")} value={data.forward_rates.length} note={t("ratesLab.notes.impliedNotForecast")} />
    </div>
    <CurveBars points={data.interpolated_curve} />
    <div className="risk-monitor-two-column">
      <Table headers={[t("ratesLab.table.maturity"), t("ratesLab.table.spotRate")]} rows={data.interpolated_curve.map((point) => [`${point.maturity}Y`, <PercentValue value={point.rate} />])} />
      <Table headers={[t("ratesLab.table.interval"), t("ratesLab.table.forwardRate")]} rows={data.forward_rates.map((point) => [`${point.start_maturity}Y - ${point.end_maturity}Y`, <PercentValue value={point.forward_rate} />])} />
    </div>
  </Section>;
}

function ScenarioTab({ data, t }: { data: RateScenarioResponse; t: Translator }) {
  return <Section title={t("ratesLab.sections.scenarios")} description={data.scenario_interpretation} badges={[t(`ratesLab.scenarioTypes.${data.scenario_type}`)]}>
    <div className="risk-monitor-mini-grid">
      <Metric title={t("ratesLab.metrics.basePrice")} value={<MoneyValue value={data.base_price} />} note={t("ratesLab.notes.beforeShock")} />
      <Metric title={t("ratesLab.metrics.stressedPrice")} value={<MoneyValue value={data.stressed_price} />} note={`${data.shock_bps} bps`} />
      <Metric title={t("ratesLab.metrics.priceChange")} value={<MoneyValue value={data.price_change} />} note={<PercentValue value={data.percent_change} />} />
      <Metric title={t("ratesLab.metrics.dv01Impact")} value={<MoneyValue value={data.dv01_impact} />} note={t("ratesLab.notes.durationEstimate")} />
      <Metric title={t("ratesLab.metrics.baseYieldAtMaturity")} value={<PercentValue value={data.base_yield_at_maturity} />} note={t("ratesLab.notes.curveDerived")} />
      <Metric title={t("ratesLab.metrics.shockedYieldAtMaturity")} value={<PercentValue value={data.shocked_yield_at_maturity} />} note={`${data.effective_shock_bps.toFixed(1)} bps`} />
    </div>
    <div className="risk-monitor-warning-list"><p>{data.risk_warning}</p></div>
  </Section>;
}

function PortfolioTab({ data, t }: { data?: PortfolioRatesExposureResponse; t: Translator }) {
  if (!data) return <EmptyState title={t("ratesLab.portfolio.emptyTitle")} message={t("ratesLab.portfolio.emptyMessage")} />;
  return <Section title={t("ratesLab.sections.portfolio")} description={data.portfolio_name} badges={data.data_source.badges}>
    <div className="risk-monitor-mini-grid">
      <Metric title={t("ratesLab.metrics.fixedIncomeValue")} value={<MoneyValue value={data.fixed_income_market_value} />} note={<PercentValue value={data.fixed_income_allocation} />} />
      <Metric title={t("ratesLab.metrics.weightedDuration")} value={data.weighted_average_duration?.toFixed(3) ?? "--"} note={t("ratesLab.notes.requiresMetadata")} />
      <Metric title={t("ratesLab.metrics.portfolioDv01")} value={data.estimated_portfolio_dv01 === null ? "--" : <MoneyValue value={data.estimated_portfolio_dv01} />} note={t("ratesLab.badges.riskMonitor")} />
      <Metric title={t("ratesLab.metrics.shockLoss")} value={data.estimated_rate_shock_loss === null ? "--" : <MoneyValue value={data.estimated_rate_shock_loss} />} note={`${data.shock_bps} bps`} />
    </div>
    <Table headers={[t("ratesLab.table.holding"), t("ratesLab.table.marketValue"), t("ratesLab.table.weight"), t("ratesLab.table.duration"), t("ratesLab.table.dv01"), t("ratesLab.table.source")]} rows={data.fixed_income_holdings.map((holding) => [holding.symbol, <MoneyValue value={holding.market_value} />, <PercentValue value={holding.weight} />, holding.estimated_duration?.toFixed(2) ?? "--", holding.estimated_dv01 === null ? "--" : <MoneyValue value={holding.estimated_dv01} />, holding.metadata_source])} />
    {data.missing_data_warnings.map((warning) => <p className="risk-monitor-table-note" key={warning}>{warning}</p>)}
  </Section>;
}

function CfaTab({ t }: { t: Translator }) {
  const notes = ["inverse", "maturity", "coupon", "convexity", "dv01", "curve", "forward", "reinvestment"];
  return <Section title={t("ratesLab.sections.cfa")} description={t("ratesLab.cfa.description")} badges={[t("ratesLab.badges.cfa")] }>
    <div className="risk-monitor-commentary-grid">{notes.map((note) => <article className="risk-monitor-driver-list" key={note}><h3>{t(`ratesLab.cfa.${note}Title`)}</h3><p>{t(`ratesLab.cfa.${note}`)}</p></article>)}</div>
  </Section>;
}

function CommentaryTab({ pricing, duration, t }: { pricing: BondPricingResponse; duration: DurationConvexityResponse; t: Translator }) {
  return <Section title={t("ratesLab.sections.commentary")} description={pricing.athena_commentary.summary} badges={[t("ratesLab.badges.deterministic")] }>
    <div className="risk-monitor-commentary-grid">
      <div className="risk-monitor-driver-list"><h3>{t("ratesLab.commentary.keyPoints")}</h3>{pricing.athena_commentary.key_points.map((point) => <p key={point}>{point}</p>)}</div>
      <div className="risk-monitor-driver-list"><h3>{t("ratesLab.commentary.risk")}</h3><p>{duration.risk_interpretation}</p>{duration.athena_commentary.cfa_notes.map((note) => <p key={note}>{note}</p>)}</div>
    </div>
  </Section>;
}

function QualityTab({ pricing, curve, portfolio, scenario, t }: { pricing: BondPricingResponse; curve?: YieldCurveResponse; portfolio?: PortfolioRatesExposureResponse; scenario?: RateScenarioResponse; t: Translator }) {
  const source = curve?.data_source ?? pricing.data_source;
  const qualityBlocks = [pricing.data_quality, curve?.data_quality, scenario?.data_quality, portfolio?.data_quality].filter(Boolean);
  const warnings = qualityBlocks.flatMap((quality) => [...(quality?.warnings ?? []), ...(quality?.limitations ?? [])]);
  const pricingMode = String(pricing.methodology.details.pricing_mode ?? "simplified");
  return <Section title={t("ratesLab.sections.quality")} description={t("ratesLab.quality.description")} badges={source.badges}>
    <Table headers={[t("ratesLab.table.field"), t("ratesLab.table.value")]} rows={[[t("ratesLab.quality.pricingMode"), t(`ratesLab.pricingModes.${pricingMode}`)], [t("ratesLab.quality.rateSource"), source.rate_source], [t("ratesLab.quality.curveSource"), source.curve_source], [t("ratesLab.quality.method"), pricing.methodology.method], [t("ratesLab.quality.frequency"), String(pricing.yield_assumptions.coupon_frequency)], [t("ratesLab.quality.datedAvailable"), pricing.data_quality.dated_pricing_available ? t("ratesLab.quality.yes") : t("ratesLab.quality.no")], [t("ratesLab.quality.advice"), t("ratesLab.quality.notAdvice")]]} />
    <p className="risk-monitor-table-note">{t("ratesLab.quality.optionsReuse")}</p>
    {[...new Set([...pricing.methodology.assumptions, ...pricing.methodology.limitations, ...source.warnings, ...warnings])].map((item) => <p className="risk-monitor-table-note" key={item}>{item}</p>)}
  </Section>;
}

function QueryPanel<T>({ data, isError, isLoading, onRetry, render, t }: { data: T | undefined; isError: boolean; isLoading: boolean; onRetry: () => void; render: (data: T) => ReactNode; t: Translator }) {
  if (isLoading) return <LoadingState label={t("common.loading")} />;
  if (isError) return <QueryErrorState title={t("ratesLab.errors.title")} message={t("ratesLab.errors.message")} onRetry={onRetry} t={t} />;
  if (!data) return <EmptyState title={t("ratesLab.empty.title")} message={t("ratesLab.empty.message")} />;
  return <>{render(data)}</>;
}

function QueryErrorState({ title, message, onRetry, t }: { title: string; message: string; onRetry: () => void; t: Translator }) {
  return <div className="empty-state" role="alert"><strong>{title}</strong><p>{message}</p><button className="button button--secondary" type="button" onClick={onRetry}>{t("ratesLab.errors.retry")}</button></div>;
}

type Translator = (key: string) => string;

function Section({ title, description, badges = [], children }: { title: string; description: string; badges?: string[]; children: ReactNode }) {
  return <section className="card risk-monitor-section-card"><div className="risk-monitor-section-card__header"><div><h2>{title}</h2><p>{description}</p></div><div className="risk-monitor-badge-cluster">{badges.map((badge) => <Badge key={badge} label={badge} tone="info" />)}</div></div>{children}</section>;
}

function Metric({ title, value, note }: { title: string; value: ReactNode; note: ReactNode }) {
  return <article className="risk-monitor-metric-card"><span>{title}</span><strong>{value}</strong><p>{note}</p></article>;
}

function Badge({ label, tone }: { label: string; tone: "success" | "info" | "warning" }) {
  return <span className={`risk-monitor-status-badge risk-monitor-status-badge--${tone}`}>{label}</span>;
}

function Field({ label, children }: { label: string; children: ReactNode }) {
  return <label className="form-field"><span>{label}</span>{children}</label>;
}

function NumberField({ label, value, onChange, min, step = 1 }: { label: string; value: number; onChange: (value: number) => void; min?: number; step?: number }) {
  return <Field label={label}><input min={min} step={step} type="number" value={value} onChange={(event) => onChange(Number(event.target.value))} /></Field>;
}

function Table({ headers, rows }: { headers: string[]; rows: ReactNode[][] }) {
  return <div className="risk-monitor-table-wrapper"><table className="risk-monitor-table"><thead><tr>{headers.map((header) => <th key={header}>{header}</th>)}</tr></thead><tbody>{rows.map((row, index) => <tr key={index}>{row.map((cell, cellIndex) => <td key={cellIndex}>{cell}</td>)}</tr>)}</tbody></table></div>;
}

function CurveBars({ points }: { points: { maturity: number; rate: number }[] }) {
  const rates = points.map((point) => point.rate);
  const minimum = Math.min(...rates);
  const maximum = Math.max(...rates);
  const span = Math.max(maximum - minimum, 0.001);
  return <div className="rates-curve-bars" aria-label="Yield curve"><div className="rates-curve-bars__plot">{points.map((point) => <div key={point.maturity}><i style={{ height: `${20 + ((point.rate - minimum) / span) * 75}%` }} /><span>{point.maturity}Y</span><strong>{(point.rate * 100).toFixed(2)}%</strong></div>)}</div></div>;
}

function clamp(value: number, minimum: number, maximum: number) {
  if (!Number.isFinite(value)) return minimum;
  return Math.min(maximum, Math.max(minimum, value));
}
