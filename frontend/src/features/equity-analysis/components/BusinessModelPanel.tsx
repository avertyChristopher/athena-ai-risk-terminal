import { BusinessModel } from "../../../types/equity";

type BusinessModelPanelProps = {
  model?: BusinessModel;
  labels: {
    title: string;
    summary: string;
    drivers: string;
    pricingPower: string;
    operatingLeverage: string;
  };
};

export function BusinessModelPanel({ model, labels }: BusinessModelPanelProps) {
  if (!model) {
    return <section className="card equity-card">{labels.title}</section>;
  }

  return (
    <section className="card equity-card">
      <h3>{labels.title}</h3>
      <p className="equity-kicker">{labels.summary}</p>
      <p>{model.summary}</p>
      <div className="section-grid section-grid--three">
        <div>
          <h4>{labels.drivers}</h4>
          <ul className="equity-list">
            {model.revenue_drivers.map((driver) => (
              <li key={driver}>{driver}</li>
            ))}
          </ul>
        </div>
        <div>
          <h4>{labels.pricingPower}</h4>
          <p>{model.pricing_power}</p>
        </div>
        <div>
          <h4>{labels.operatingLeverage}</h4>
          <p>{model.operating_leverage}</p>
        </div>
      </div>
    </section>
  );
}
