import { formatCurrency } from "../../../lib/formatters";
import { EquityOverviewResponse } from "../../../types/equity";

type CompanyOverviewCardProps = {
  overview?: EquityOverviewResponse;
  labels: {
    title: string;
    company: string;
    ticker: string;
    exchange: string;
    sector: string;
    industry: string;
    country: string;
    currency: string;
    marketCap: string;
    latestPrice: string;
    benchmark: string;
  };
};

export function CompanyOverviewCard({
  overview,
  labels,
}: CompanyOverviewCardProps) {
  if (!overview) {
    return <section className="card equity-card">{labels.title}</section>;
  }

  const rows = [
    [labels.company, overview.company_name],
    [labels.ticker, overview.ticker],
    [labels.exchange, overview.exchange],
    [labels.sector, overview.sector],
    [labels.industry, overview.industry],
    [labels.country, overview.country],
    [labels.currency, overview.currency],
    [labels.marketCap, formatCurrency(overview.market_cap * 1_000_000_000)],
    [labels.latestPrice, formatCurrency(overview.latest_price, overview.currency)],
    [labels.benchmark, overview.benchmark_symbol],
  ];

  return (
    <section className="card equity-card company-overview-card">
      <div>
        <span className="equity-eyebrow">{labels.title}</span>
        <h2>{overview.company_name}</h2>
        <p>
          {overview.exchange} / {overview.sector} / {overview.industry}
        </p>
      </div>
      <dl className="equity-definition-grid">
        {rows.map(([label, value]) => (
          <div key={label}>
            <dt>{label}</dt>
            <dd>{value}</dd>
          </div>
        ))}
      </dl>
    </section>
  );
}
