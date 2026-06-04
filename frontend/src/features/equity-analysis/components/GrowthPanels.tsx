import { formatPercent } from "../../../lib/formatters";
import { EquityGrowthResponse } from "../../../types/equity";
import { EquityMetricGrid } from "./EquityMetricGrid";

type GrowthPanelsProps = {
  growth?: EquityGrowthResponse;
  labels: {
    revenueGrowth: string;
    epsGrowth: string;
    operatingIncomeGrowth: string;
    dividendGrowth: string;
    sustainableGrowth: string;
    retention: string;
    roe: string;
    profile: string;
    forecast: string;
  };
};

export function GrowthPanels({ growth, labels }: GrowthPanelsProps) {
  if (!growth) {
    return <section className="card equity-card">{labels.profile}</section>;
  }

  return (
    <div className="section-grid">
      <EquityMetricGrid
        metrics={[
          [labels.revenueGrowth, growth.revenue_growth],
          [labels.epsGrowth, growth.eps_growth],
          [labels.operatingIncomeGrowth, growth.operating_income_growth],
          [labels.dividendGrowth, growth.dividend_growth_rate],
          [labels.sustainableGrowth, growth.sustainable_growth_rate],
          [labels.retention, growth.retention_ratio],
          [labels.roe, growth.roe],
        ].map(([label, value]) => ({
          label: String(label),
          value: value === null ? "--" : formatPercent(Number(value)),
        }))}
      />
      <div className="section-grid section-grid--two">
        <section className="card equity-card">
          <h3>{labels.profile}</h3>
          <strong>{growth.growth_profile}</strong>
        </section>
        <section className="card equity-card">
          <h3>{labels.forecast}</h3>
          <ul className="equity-list">
            {growth.forecast_assumptions.map((assumption) => (
              <li key={assumption}>{assumption}</li>
            ))}
          </ul>
          {growth.warnings.length ? (
            <div className="model-warning-list">
              {growth.warnings.map((warning) => (
                <span key={warning}>{warning}</span>
              ))}
            </div>
          ) : null}
        </section>
      </div>
    </div>
  );
}
