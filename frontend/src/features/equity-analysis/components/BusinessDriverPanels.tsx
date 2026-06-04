import { formatLargeCurrency, formatPercent } from "../../../lib/formatters";
import { EquityBusinessModelResponse } from "../../../types/equity";

type BusinessDriverPanelsProps = {
  business?: EquityBusinessModelResponse;
  labels: {
    revenueDrivers: string;
    revenueSegments: string;
    geographicExposure: string;
    operatingLeverage: string;
    cyclicality: string;
    capitalIntensity: string;
    comingSoon: string;
  };
};

export function BusinessDriverPanels({
  business,
  labels,
}: BusinessDriverPanelsProps) {
  if (!business) {
    return <section className="card equity-card">{labels.revenueDrivers}</section>;
  }

  return (
    <div className="section-grid section-grid--three">
      <section className="card equity-card">
        <h3>{labels.revenueDrivers}</h3>
        <ul className="equity-list">
          {business.revenue_drivers.map((driver) => (
            <li key={driver}>{driver}</li>
          ))}
        </ul>
      </section>
      <section className="card equity-card compact-table-card">
        <h3>{labels.revenueSegments}</h3>
        <table className="compact-table">
          <tbody>
            {business.revenue_segments.map((segment) => (
              <tr key={segment.name}>
                <td>{segment.name}</td>
                <td>
                  {segment.revenue ? formatLargeCurrency(segment.revenue) : "--"} /{" "}
                  {formatPercent(segment.weight)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
      <section className="card equity-card compact-table-card">
        <h3>{labels.geographicExposure}</h3>
        <table className="compact-table">
          <tbody>
            {business.geographic_exposure.map((region) => (
              <tr key={region.name}>
                <td>{region.name}</td>
                <td>{formatPercent(region.weight)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
      <section className="card equity-card">
        <h3>{labels.operatingLeverage}</h3>
        <p>{business.operating_leverage}</p>
      </section>
      <section className="card equity-card">
        <h3>{labels.cyclicality}</h3>
        <p>{business.cyclicality}</p>
      </section>
      <section className="card equity-card">
        <h3>{labels.capitalIntensity}</h3>
        <p>{business.capital_intensity}</p>
        <span className="planned-list">
          <span>{labels.comingSoon}</span>
        </span>
      </section>
    </div>
  );
}
