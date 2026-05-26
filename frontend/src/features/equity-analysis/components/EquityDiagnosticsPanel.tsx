import { EquityDiagnosticsResponse } from "../../../types/equity";

type EquityDiagnosticsPanelProps = {
  diagnostics?: EquityDiagnosticsResponse;
  labels: {
    title: string;
    valuation: string;
    profitability: string;
    balanceSheet: string;
    strengths: string;
    risks: string;
  };
};

export function EquityDiagnosticsPanel({
  diagnostics,
  labels,
}: EquityDiagnosticsPanelProps) {
  if (!diagnostics) {
    return <section className="card equity-card">{labels.title}</section>;
  }

  return (
    <section className="card equity-card diagnostics-panel">
      <h3>{labels.title}</h3>
      <div className="equity-diagnostic-badges">
        <div>
          <span>{labels.valuation}</span>
          <strong>{diagnostics.valuation_status}</strong>
        </div>
        <div>
          <span>{labels.profitability}</span>
          <strong>{diagnostics.profitability_quality}</strong>
        </div>
        <div>
          <span>{labels.balanceSheet}</span>
          <strong>{diagnostics.balance_sheet_quality}</strong>
        </div>
      </div>
      <div className="section-grid section-grid--two">
        <div>
          <h4>{labels.strengths}</h4>
          <ul className="equity-list">
            {diagnostics.strengths.map((strength) => (
              <li key={strength}>{strength}</li>
            ))}
          </ul>
        </div>
        <div>
          <h4>{labels.risks}</h4>
          <ul className="equity-list">
            {diagnostics.risks.map((risk) => (
              <li key={risk}>{risk}</li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
