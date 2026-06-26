import { PortfolioRead } from "../../../types/portfolio";

type PortfolioDetailsPanelProps = {
  portfolio: PortfolioRead;
  labels: {
    title: string;
    name: string;
    currency: string;
    benchmark: string;
    strategyType: string;
    investmentObjective: string;
    riskTolerance: string;
    timeHorizon: string;
    targetAllocation: string;
    ipsSummary: string;
    dataSource: string;
    demoProfile: string;
    portfolioProfile: string;
  };
};

export function PortfolioDetailsPanel({
  portfolio,
  labels,
}: PortfolioDetailsPanelProps) {
  return (
    <section className="card details-panel portfolio-profile-panel">
      <div className="section-heading">
        <div>
          <span className="section-eyebrow">
            {portfolio.demo_profile ? labels.demoProfile : labels.portfolioProfile}
          </span>
          <h2>{labels.title}</h2>
        </div>
      </div>
      {portfolio.data_source_badges?.length ? (
        <div className="portfolio-badge-cluster">
          {portfolio.data_source_badges.map((badge) => (
            <span className="status-pill" key={badge}>{badge}</span>
          ))}
        </div>
      ) : null}
      <dl>
        <div>
          <dt>{labels.name}</dt>
          <dd>{portfolio.name}</dd>
        </div>
        <div>
          <dt>{labels.strategyType}</dt>
          <dd>{portfolio.strategy_type ?? "--"}</dd>
        </div>
        <div>
          <dt>{labels.riskTolerance}</dt>
          <dd>{portfolio.risk_tolerance ?? portfolio.risk_profile ?? "--"}</dd>
        </div>
        <div>
          <dt>{labels.timeHorizon}</dt>
          <dd>{portfolio.time_horizon ?? "--"}</dd>
        </div>
        <div>
          <dt>{labels.currency}</dt>
          <dd>{portfolio.base_currency}</dd>
        </div>
        <div>
          <dt>{labels.benchmark}</dt>
          <dd>{portfolio.benchmark}</dd>
        </div>
        <div>
          <dt>{labels.dataSource}</dt>
          <dd>{portfolio.data_source ?? "--"}</dd>
        </div>
      </dl>
      {portfolio.strategy_description ? (
        <p className="portfolio-profile-panel__description">
          {portfolio.strategy_description}
        </p>
      ) : null}
      {portfolio.investment_objective ? (
        <div className="portfolio-profile-panel__note">
          <strong>{labels.investmentObjective}</strong>
          <p>{portfolio.investment_objective}</p>
        </div>
      ) : null}
      {portfolio.ips_summary ? (
        <div className="portfolio-profile-panel__note">
          <strong>{labels.ipsSummary}</strong>
          <p>{portfolio.ips_summary}</p>
        </div>
      ) : null}
      {portfolio.target_allocation?.length ? (
        <div className="portfolio-profile-panel__targets">
          <strong>{labels.targetAllocation}</strong>
          <div>
            {portfolio.target_allocation.map((target) => (
              <span key={target.name}>
                {target.name}: {(target.target_weight * 100).toFixed(0)}%
              </span>
            ))}
          </div>
        </div>
      ) : null}
    </section>
  );
}
