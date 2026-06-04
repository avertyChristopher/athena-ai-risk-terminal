import { formatCurrency, formatPercent } from "../../../lib/formatters";
import { EquityValuationResponse } from "../../../types/equity";

type MarginOfSafetyCardProps = {
  valuation?: EquityValuationResponse;
  labels: {
    title: string;
    description: string;
    marketPrice: string;
    modelValue: string;
    signal: string;
    extremeWarning: string;
  };
};

export function MarginOfSafetyCard({ valuation, labels }: MarginOfSafetyCardProps) {
  const margin = valuation?.margin_of_safety ?? 0;
  const isExtreme = Math.abs(margin) > 1;
  const boundedMargin = Math.max(-0.5, Math.min(0.5, margin));
  const boundedWidth = (boundedMargin + 0.5) * 100;

  return (
    <section className="card equity-card margin-card">
      <h3>{labels.title}</h3>
      <div className="margin-card__headline">
        <strong className={margin >= 0 ? "positive-value" : "negative-value"}>
          {valuation ? formatPercent(margin) : "--"}
        </strong>
        <span>{valuation?.valuation_status ?? "--"}</span>
      </div>
      <dl className="margin-card__details">
        <div>
          <dt>{labels.marketPrice}</dt>
          <dd>{valuation ? formatCurrency(valuation.market_price) : "--"}</dd>
        </div>
        <div>
          <dt>{labels.modelValue}</dt>
          <dd>{valuation ? formatCurrency(valuation.intrinsic_value) : "--"}</dd>
        </div>
      </dl>
      <div className="margin-scale">
        <span style={{ width: `${boundedWidth}%` }} />
      </div>
      <div className="margin-scale__labels">
        <span>-50%</span>
        <span>{labels.signal}</span>
        <span>+50%</span>
      </div>
      <p>{labels.description}</p>
      {isExtreme ? (
        <p className="model-warning-list__item">{labels.extremeWarning}</p>
      ) : null}
    </section>
  );
}
