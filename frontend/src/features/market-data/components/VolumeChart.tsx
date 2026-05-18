import { PricePoint } from "../../../types/market-data";

type VolumeChartProps = {
  title: string;
  prices: PricePoint[];
};

export function VolumeChart({ title, prices }: VolumeChartProps) {
  const maxVolume = Math.max(...prices.map((price) => price.volume), 1);

  return (
    <section className="card chart-panel">
      <h3>{title}</h3>
      <div className="volume-bars">
        {prices.map((price) => (
          <div className="volume-bar" key={price.date}>
            <span>{price.date.slice(5)}</span>
            <div className="volume-bar__track">
              <div
                className="volume-bar__fill"
                style={{ height: `${(price.volume / maxVolume) * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
