import { PropsWithChildren } from "react";

type AnalyticsSectionProps = PropsWithChildren<{
  title: string;
  description: string;
}>;

export function AnalyticsSection({
  title,
  description,
  children,
}: AnalyticsSectionProps) {
  return (
    <section className="analytics-section">
      <header className="analytics-section__header">
        <h2>{title}</h2>
        <p>{description}</p>
      </header>
      {children}
    </section>
  );
}
