import { formatPercent } from "../../../lib/formatters";
import { EquityValuationResponse } from "../../../types/equity";

type MarginOfSafetyCardProps = {
  valuation?: EquityValuationResponse;
  labels: {
    title: string;
    description: string;
  };
};

export function MarginOfSafetyCard({ valuation, labels }: MarginOfSafetyCardProps) {
  const margin = valuation?.margin_of_safety ?? 0;
  const boundedWidth = Math.max(0, Math.min(100, (margin + 0.5) * 100));

  return (
    <section className="card equity-card margin-card">
      <h3>{labels.title}</h3>
      <strong className={margin >= 0 ? "positive-value" : "negative-value"}>
        {valuation ? formatPercent(margin) : "--"}
      </strong>
      <div className="margin-scale">
        <span style={{ width: `${boundedWidth}%` }} />
      </div>
      <p>{labels.description}</p>
    </section>
  );
}
