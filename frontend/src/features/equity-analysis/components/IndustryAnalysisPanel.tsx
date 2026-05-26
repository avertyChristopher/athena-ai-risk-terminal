import { IndustryAnalysis } from "../../../types/equity";

type IndustryAnalysisPanelProps = {
  analysis?: IndustryAnalysis;
  labels: {
    title: string;
    classification: string;
    porter: string;
    pestle: string;
    position: string;
  };
};

export function IndustryAnalysisPanel({
  analysis,
  labels,
}: IndustryAnalysisPanelProps) {
  if (!analysis) {
    return <section className="card equity-card">{labels.title}</section>;
  }

  return (
    <section className="card equity-card">
      <h3>{labels.title}</h3>
      <p className="equity-kicker">{labels.classification}</p>
      <p>{analysis.classification}</p>
      <div className="section-grid section-grid--two">
        <div>
          <h4>{labels.porter}</h4>
          <ul className="equity-list">
            {analysis.porter_forces.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
        <div>
          <h4>{labels.pestle}</h4>
          <ul className="equity-list">
            {analysis.pestle.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      </div>
      <p className="equity-note">
        <strong>{labels.position}: </strong>
        {analysis.competitive_position}
      </p>
    </section>
  );
}
