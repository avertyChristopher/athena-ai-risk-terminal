import { ReactNode } from "react";

type MetricTileProps = {
  label: string;
  value: ReactNode;
  note?: string;
};

export function MetricTile({ label, value, note }: MetricTileProps) {
  return (
    <div className="metric-tile">
      <span>{label}</span>
      <strong>{value}</strong>
      {note ? <small>{note}</small> : null}
    </div>
  );
}
