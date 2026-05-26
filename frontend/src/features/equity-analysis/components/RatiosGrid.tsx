import { formatPercent } from "../../../lib/formatters";
import { EquityRatiosResponse } from "../../../types/equity";

type RatiosGridProps = {
  ratios?: EquityRatiosResponse;
  labels: {
    title: string;
    profitability: string;
    liquidity: string;
    leverage: string;
    dividend: string;
    grossMargin: string;
    operatingMargin: string;
    netMargin: string;
    roe: string;
    roa: string;
    currentRatio: string;
    quickRatio: string;
    debtToEquity: string;
    interestCoverage: string;
    payout: string;
    retention: string;
    sustainableGrowth: string;
  };
};

export function RatiosGrid({ ratios, labels }: RatiosGridProps) {
  if (!ratios) {
    return <section className="card equity-card">{labels.title}</section>;
  }

  return (
    <section className="card equity-card">
      <h3>{labels.title}</h3>
      <div className="equity-ratio-groups">
        <RatioGroup
          title={labels.profitability}
          rows={[
            [labels.grossMargin, formatPercent(ratios.gross_margin)],
            [labels.operatingMargin, formatPercent(ratios.operating_margin)],
            [labels.netMargin, formatPercent(ratios.net_margin)],
            [labels.roe, formatPercent(ratios.roe)],
            [labels.roa, formatPercent(ratios.roa)],
          ]}
        />
        <RatioGroup
          title={labels.liquidity}
          rows={[
            [labels.currentRatio, ratios.current_ratio.toFixed(2)],
            [labels.quickRatio, ratios.quick_ratio.toFixed(2)],
          ]}
        />
        <RatioGroup
          title={labels.leverage}
          rows={[
            [labels.debtToEquity, ratios.debt_to_equity.toFixed(2)],
            [labels.interestCoverage, `${ratios.interest_coverage.toFixed(1)}x`],
          ]}
        />
        <RatioGroup
          title={labels.dividend}
          rows={[
            [labels.payout, formatPercent(ratios.dividend_payout_ratio)],
            [labels.retention, formatPercent(ratios.retention_ratio)],
            [
              labels.sustainableGrowth,
              formatPercent(ratios.sustainable_growth_rate),
            ],
          ]}
        />
      </div>
    </section>
  );
}

function RatioGroup({
  title,
  rows,
}: {
  title: string;
  rows: Array<[string, string]>;
}) {
  return (
    <div className="equity-ratio-group">
      <h4>{title}</h4>
      {rows.map(([label, value]) => (
        <div key={label}>
          <span>{label}</span>
          <strong>{value}</strong>
        </div>
      ))}
    </div>
  );
}
