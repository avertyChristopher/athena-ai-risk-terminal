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
    currentRatioFormula: string;
    quickRatioFormula: string;
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
            [labels.grossMargin, formatNullablePercent(ratios.gross_margin)],
            [labels.operatingMargin, formatNullablePercent(ratios.operating_margin)],
            [labels.netMargin, formatNullablePercent(ratios.net_margin)],
            [labels.roe, formatNullablePercent(ratios.roe)],
            [labels.roa, formatNullablePercent(ratios.roa)],
          ]}
        />
        <RatioGroup
          title={labels.liquidity}
          rows={[
            [labels.currentRatio, formatNullableNumber(ratios.current_ratio)],
            [labels.quickRatio, formatNullableNumber(ratios.quick_ratio)],
          ]}
          note={`${labels.currentRatioFormula} ${labels.quickRatioFormula}`}
        />
        <RatioGroup
          title={labels.leverage}
          rows={[
            [labels.debtToEquity, formatNullableNumber(ratios.debt_to_equity)],
            [labels.interestCoverage, formatNullableMultiple(ratios.interest_coverage)],
          ]}
        />
        <RatioGroup
          title={labels.dividend}
          rows={[
            [labels.payout, formatNullablePercent(ratios.dividend_payout_ratio)],
            [labels.retention, formatNullablePercent(ratios.retention_ratio)],
            [
              labels.sustainableGrowth,
              formatNullablePercent(ratios.sustainable_growth_rate),
            ],
          ]}
        />
      </div>
    </section>
  );
}

function formatNullablePercent(value: number | null) {
  return value === null ? "--" : formatPercent(value);
}

function formatNullableNumber(value: number | null) {
  return value === null ? "--" : value.toFixed(2);
}

function formatNullableMultiple(value: number | null) {
  return value === null ? "--" : `${value.toFixed(1)}x`;
}

function RatioGroup({
  title,
  rows,
  note,
}: {
  title: string;
  rows: Array<[string, string]>;
  note?: string;
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
      {note ? <p className="equity-note">{note}</p> : null}
    </div>
  );
}
