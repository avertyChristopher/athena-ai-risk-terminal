import { ReactNode } from "react";

type ReferenceDataItem = {
  label: string;
  value: ReactNode;
};

type ReferenceDataPanelProps = {
  title: string;
  items: ReferenceDataItem[];
};

export function ReferenceDataPanel({ title, items }: ReferenceDataPanelProps) {
  return (
    <section className="card reference-panel">
      <h3>{title}</h3>
      <dl>
        {items.map((item) => (
          <div key={item.label}>
            <dt>{item.label}</dt>
            <dd>{item.value}</dd>
          </div>
        ))}
      </dl>
    </section>
  );
}
