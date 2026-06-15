import {
  PortfolioDiagnosticsResponse,
  PortfolioMarketDataIntegrationResponse,
} from "../../../types/portfolio";
import { PortfolioSectionCard } from "./PortfolioSectionCard";
import { PortfolioStatusBadge } from "./PortfolioStatusBadge";
import { PortfolioWarningCard } from "./PortfolioWarningCard";

type PortfolioDiagnosticsPanelProps = {
  diagnostics: PortfolioDiagnosticsResponse;
  marketDataIntegration?: PortfolioMarketDataIntegrationResponse;
  labels: {
    title: string;
    description: string;
    allocation: string;
    diversification: string;
    concentration: string;
    cash: string;
    benchmark: string;
    policy: string;
    rebalancing: string;
    limitations: string;
    nextSteps: string;
    assumptions: string;
    plannedAnalytics: string;
    readiness: string;
  };
};

export function PortfolioDiagnosticsPanel({
  diagnostics,
  marketDataIntegration,
  labels,
}: PortfolioDiagnosticsPanelProps) {
  const statusRows = [
    { label: labels.allocation, value: diagnostics.allocation_quality },
    { label: labels.diversification, value: diagnostics.diversification_quality },
    { label: labels.concentration, value: diagnostics.concentration_risk },
    { label: labels.cash, value: diagnostics.cash_level },
    { label: labels.benchmark, value: diagnostics.benchmark_alignment },
    { label: labels.policy, value: diagnostics.policy_alignment },
    { label: labels.rebalancing, value: diagnostics.rebalancing_need },
  ];

  return (
    <PortfolioSectionCard
      title={labels.title}
      description={labels.description}
      badges={marketDataIntegration?.readiness_badges.slice(0, 4).map((label) => ({
        label,
        variant: label.includes("Requires") ? "warning" : "info",
      }))}
    >
      <div className="portfolio-diagnostics-grid">
        {statusRows.map((row) => (
          <div className="portfolio-diagnostic-tile" key={row.label}>
            <span>{row.label}</span>
            <strong>{row.value}</strong>
          </div>
        ))}
      </div>

      <div className="portfolio-analyst-note">
        <strong>{diagnostics.summary}</strong>
      </div>

      <div className="portfolio-warning-grid">
        {diagnostics.data_quality_limitations.map((limitation) => (
          <PortfolioWarningCard
            key={limitation}
            title={labels.limitations}
            message={limitation}
            badge="Demo"
          />
        ))}
      </div>

      <div className="portfolio-diagnostics-columns">
        <div>
          <h3>{labels.nextSteps}</h3>
          <ul className="portfolio-note-list">
            {diagnostics.next_analytical_steps.map((step) => (
              <li key={step}>{step}</li>
            ))}
          </ul>
        </div>

        {marketDataIntegration ? (
          <div>
            <h3>{labels.readiness}</h3>
            <div className="portfolio-badge-cluster">
              {marketDataIntegration.readiness_badges.map((badge) => (
                <PortfolioStatusBadge
                  key={badge}
                  label={badge}
                  variant={badge.includes("No") ? "warning" : "info"}
                />
              ))}
            </div>
          </div>
        ) : null}
      </div>

      {marketDataIntegration ? (
        <div className="portfolio-diagnostics-columns">
          <div>
            <h3>{labels.assumptions}</h3>
            <ul className="portfolio-note-list">
              {marketDataIntegration.current_assumptions.map((assumption) => (
                <li key={assumption}>{assumption}</li>
              ))}
            </ul>
          </div>
          <div>
            <h3>{labels.plannedAnalytics}</h3>
            <ul className="portfolio-note-list">
              {marketDataIntegration.planned_analytics.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        </div>
      ) : null}
    </PortfolioSectionCard>
  );
}
