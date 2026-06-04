import { formatPercent } from "../../../lib/formatters";
import {
  EquityCorporateActionsResponse,
  EquityDiagnosticsResponse,
} from "../../../types/equity";

type CorporateActionsPanelProps = {
  corporateActions?: EquityCorporateActionsResponse;
  labels: {
    dividendTitle: string;
    shareholderReturns: string;
    timeline: string;
    dividendYield: string;
    payout: string;
    retention: string;
    buybackYield: string;
    totalYield: string;
  };
};

type GovernanceRiskPanelProps = {
  diagnostics?: EquityDiagnosticsResponse;
  labels: {
    governance: string;
    esg: string;
    riskFactors: string;
    watchlist: string;
  };
};

export function CorporateActionsPanel({
  corporateActions,
  labels,
}: CorporateActionsPanelProps) {
  if (!corporateActions) {
    return <section className="card equity-card">{labels.dividendTitle}</section>;
  }

  return (
    <div className="section-grid section-grid--three">
      <section className="card equity-card">
        <h3>{labels.dividendTitle}</h3>
        <p>{corporateActions.dividend_profile}</p>
        <dl className="equity-definition-list">
          <Definition
            label={labels.dividendYield}
            value={formatPercent(corporateActions.dividend_yield)}
          />
          <Definition
            label={labels.payout}
            value={
              corporateActions.payout_ratio === null
                ? "--"
                : formatPercent(corporateActions.payout_ratio)
            }
          />
          <Definition
            label={labels.retention}
            value={
              corporateActions.retention_ratio === null
                ? "--"
                : formatPercent(corporateActions.retention_ratio)
            }
          />
        </dl>
      </section>
      <section className="card equity-card">
        <h3>{labels.shareholderReturns}</h3>
        <dl className="equity-definition-list">
          <Definition
            label={labels.buybackYield}
            value={
              corporateActions.buyback_yield === null
                ? "--"
                : formatPercent(corporateActions.buyback_yield)
            }
          />
          <Definition
            label={labels.totalYield}
            value={
              corporateActions.total_shareholder_yield === null
                ? "--"
                : formatPercent(corporateActions.total_shareholder_yield)
            }
          />
        </dl>
        <p>{corporateActions.share_repurchases_summary}</p>
      </section>
      <section className="card equity-card">
        <h3>{labels.timeline}</h3>
        <ul className="equity-list">
          {corporateActions.timeline.map((event) => (
            <li key={event.label}>
              <strong>{event.label}: </strong>
              {event.detail}
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}

export function GovernanceRiskPanel({
  diagnostics,
  labels,
}: GovernanceRiskPanelProps) {
  if (!diagnostics) {
    return <section className="card equity-card">{labels.governance}</section>;
  }

  return (
    <div className="section-grid section-grid--two">
      <section className="card equity-card">
        <h3>{labels.governance}</h3>
        <p>{diagnostics.governance.summary}</p>
      </section>
      <section className="card equity-card">
        <h3>{labels.esg}</h3>
        <p>{diagnostics.esg_considerations.summary}</p>
      </section>
      <section className="card equity-card">
        <h3>{labels.riskFactors}</h3>
        <div className="equity-risk-grid">
          {Object.entries(diagnostics.risk_factors).map(([category, risks]) => (
            <div key={category}>
              <h4>{category}</h4>
              <ul className="equity-list">
                {risks.map((risk) => (
                  <li key={risk}>{risk}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>
      <section className="card equity-card">
        <h3>{labels.watchlist}</h3>
        <ul className="equity-list">
          {diagnostics.watchlist_flags.map((flag) => (
            <li key={flag}>{flag}</li>
          ))}
        </ul>
      </section>
    </div>
  );
}

function Definition({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt>{label}</dt>
      <dd>{value}</dd>
    </div>
  );
}
