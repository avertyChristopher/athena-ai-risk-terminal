import { EquityDiagnosticsResponse } from "../../../types/equity";

type AnalystDiagnosticsPanelsProps = {
  diagnostics?: EquityDiagnosticsResponse;
  labels: {
    cases: string;
    strengthsWeaknesses: string;
    scorecard: string;
    strengths: string;
    weaknesses: string;
    valuation: string;
    profitability: string;
    balanceSheet: string;
    growth: string;
    dividend: string;
    risk: string;
    disclaimer: string;
  };
};

export function AnalystDiagnosticsPanels({
  diagnostics,
  labels,
}: AnalystDiagnosticsPanelsProps) {
  if (!diagnostics) {
    return <section className="card equity-card">{labels.scorecard}</section>;
  }

  return (
    <div className="section-grid section-grid--three">
      <section className="card equity-card">
        <h3>{labels.scorecard}</h3>
        <dl className="equity-definition-list">
          <Definition label={labels.valuation} value={diagnostics.valuation_profile} />
          <Definition
            label={labels.profitability}
            value={diagnostics.profitability_quality}
          />
          <Definition
            label={labels.balanceSheet}
            value={diagnostics.balance_sheet_quality}
          />
          <Definition label={labels.growth} value={diagnostics.growth_profile} />
          <Definition label={labels.dividend} value={diagnostics.dividend_profile} />
          <Definition label={labels.risk} value={diagnostics.risk_profile} />
        </dl>
      </section>
      <section className="card equity-card">
        <h3>{labels.cases}</h3>
        <dl className="equity-definition-list">
          {Object.entries(diagnostics.bull_base_bear).map(([caseName, text]) => (
            <Definition key={caseName} label={caseName.replace("_", " ")} value={text} />
          ))}
        </dl>
      </section>
      <section className="card equity-card">
        <h3>{labels.strengthsWeaknesses}</h3>
        <h4>{labels.strengths}</h4>
        <ul className="equity-list">
          {diagnostics.strengths.map((strength) => (
            <li key={strength}>{strength}</li>
          ))}
        </ul>
        <h4>{labels.weaknesses}</h4>
        <ul className="equity-list">
          {diagnostics.weaknesses.map((weakness) => (
            <li key={weakness}>{weakness}</li>
          ))}
        </ul>
      </section>
      <section className="card equity-card analyst-summary-panel">
        <h3>{labels.disclaimer}</h3>
        <p>{diagnostics.educational_note}</p>
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
