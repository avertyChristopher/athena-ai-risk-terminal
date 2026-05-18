import { PortfolioRead } from "../../../types/portfolio";

type PortfolioDetailsPanelProps = {
  portfolio: PortfolioRead;
  labels: {
    title: string;
    name: string;
    currency: string;
    benchmark: string;
  };
};

export function PortfolioDetailsPanel({
  portfolio,
  labels,
}: PortfolioDetailsPanelProps) {
  return (
    <section className="card details-panel">
      <h2>{labels.title}</h2>
      <dl>
        <div>
          <dt>{labels.name}</dt>
          <dd>{portfolio.name}</dd>
        </div>
        <div>
          <dt>{labels.currency}</dt>
          <dd>{portfolio.base_currency}</dd>
        </div>
        <div>
          <dt>{labels.benchmark}</dt>
          <dd>{portfolio.benchmark}</dd>
        </div>
      </dl>
    </section>
  );
}
