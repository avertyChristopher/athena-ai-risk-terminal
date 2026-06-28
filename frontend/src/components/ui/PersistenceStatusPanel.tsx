import { StatusBadge } from "./StatusBadge";
import type { DemoPersistenceItem, DemoPersistenceStatus } from "../../types/demo-workflow";

type PersistenceStatusPanelProps = {
  title: string;
  description?: string;
  items: DemoPersistenceItem[];
  compact?: boolean;
};

export function PersistenceStatusPanel({
  title,
  description,
  items,
  compact = false,
}: PersistenceStatusPanelProps) {
  return (
    <section className={compact ? "persistence-panel persistence-panel--compact" : "persistence-panel"}>
      <div>
        <span className="equity-kicker">{title}</span>
        {description ? <p>{description}</p> : null}
      </div>
      <div className="persistence-panel__grid">
        {items.map((item) => (
          <article key={`${item.module}-${item.object_name}`}>
            <div>
              <strong>{item.module}</strong>
              <StatusBadge label={statusLabel(item.status)} variant={statusVariant(item.status)} />
            </div>
            <span>{item.object_name}</span>
            {!compact ? <p>{item.notes}</p> : null}
          </article>
        ))}
      </div>
    </section>
  );
}

export function statusLabel(status: DemoPersistenceStatus) {
  const labels: Record<DemoPersistenceStatus, string> = {
    persistent_history: "Persistent history",
    sqlite_demo: "SQLite demo",
    in_memory_fallback: "In-memory fallback",
    not_persisted: "Not persisted",
  };
  return labels[status];
}

function statusVariant(status: DemoPersistenceStatus) {
  if (status === "persistent_history") return "success";
  if (status === "sqlite_demo") return "info";
  if (status === "in_memory_fallback") return "warning";
  return "neutral";
}
