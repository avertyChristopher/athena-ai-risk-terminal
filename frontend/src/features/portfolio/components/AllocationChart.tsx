import { MoneyValue } from "../../../components/finance/MoneyValue";
import { PercentValue } from "../../../components/finance/PercentValue";
import { AllocationItem } from "../../../types/portfolio";

type AllocationChartProps = {
  title: string;
  items: AllocationItem[];
  currency: string;
};

export function AllocationChart({ title, items, currency }: AllocationChartProps) {
  return (
    <section className="allocation-panel">
      <h2>{title}</h2>
      <div className="bar-list">
        {items.map((item) => (
          <div className="bar-row" key={item.name}>
            <div className="bar-row__meta">
              <strong>{item.name}</strong>
              <span>
                <MoneyValue value={item.market_value} currency={currency} /> -{" "}
                <PercentValue value={item.weight} />
              </span>
            </div>
            <div className="bar-track">
              <div
                className="bar-fill"
                style={{ width: `${Math.min(item.weight * 100, 100)}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
