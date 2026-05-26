import { formatCurrency, formatPercent } from "../../../lib/formatters";
import { EquityValuationResponse } from "../../../types/equity";

type IntrinsicValueCardProps = {
  valuation?: EquityValuationResponse;
  labels: {
    title: string;
    marketPrice: string;
    ggm: string;
    ddm: string;
    blended: string;
    requiredReturn: string;
    growth: string;
  };
};

export function IntrinsicValueCard({ valuation, labels }: IntrinsicValueCardProps) {
  return (
    <section className="card equity-card intrinsic-card">
      <h3>{labels.title}</h3>
      <div className="equity-valuation-grid">
        <div>
          <span>{labels.marketPrice}</span>
          <strong>{valuation ? formatCurrency(valuation.market_price) : "--"}</strong>
        </div>
        <div>
          <span>{labels.ggm}</span>
          <strong>
            {valuation ? formatCurrency(valuation.gordon_growth_value) : "--"}
          </strong>
        </div>
        <div>
          <span>{labels.ddm}</span>
          <strong>
            {valuation ? formatCurrency(valuation.dividend_discount_value) : "--"}
          </strong>
        </div>
        <div>
          <span>{labels.blended}</span>
          <strong>{valuation ? formatCurrency(valuation.intrinsic_value) : "--"}</strong>
        </div>
      </div>
      <p className="equity-note">
        {labels.requiredReturn}:{" "}
        {valuation ? formatPercent(valuation.required_return) : "--"} / {labels.growth}:{" "}
        {valuation ? formatPercent(valuation.growth_rate) : "--"}
      </p>
    </section>
  );
}
