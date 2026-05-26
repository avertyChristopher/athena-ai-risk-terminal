import { EquityDiagnosticsResponse } from "../../../types/equity";

type AnalystSummaryPanelProps = {
  diagnostics?: EquityDiagnosticsResponse;
  labels: {
    title: string;
    note: string;
  };
};

export function AnalystSummaryPanel({
  diagnostics,
  labels,
}: AnalystSummaryPanelProps) {
  return (
    <section className="card equity-card analyst-summary-panel">
      <h3>{labels.title}</h3>
      <p>{diagnostics?.analyst_summary ?? "--"}</p>
      <small>{diagnostics?.educational_note ?? labels.note}</small>
    </section>
  );
}
