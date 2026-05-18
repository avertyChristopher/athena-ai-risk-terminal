import { PercentValue } from "../../../components/finance/PercentValue";
import { ReturnPoint } from "../../../types/market-data";

type DrawdownChartProps = {
  title: string;
  returns: ReturnPoint[];
};

export function DrawdownChart({ title, returns }: DrawdownChartProps) {
  return (
    <section className="card chart-panel">
      <h3>{title}</h3>
      <div className="drawdown-bars">
        {returns.map((item) => (
          <div className="drawdown-bar" key={item.date}>
            <span>{item.date.slice(5)}</span>
            <div className="drawdown-bar__track">
              <div
                className="drawdown-bar__fill"
                style={{ width: `${Math.min(Math.abs(item.drawdown) * 500, 100)}%` }}
              />
            </div>
            <strong>
              <PercentValue value={item.drawdown} />
            </strong>
          </div>
        ))}
      </div>
    </section>
  );
}
