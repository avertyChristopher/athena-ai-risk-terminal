import type { ReactNode } from "react";

import {
  PortfolioStatusBadge,
  PortfolioStatusBadgeVariant,
} from "./PortfolioStatusBadge";

type PortfolioSectionBadge =
  | string
  | {
      label: string;
      variant?: PortfolioStatusBadgeVariant;
    };

type PortfolioSectionCardProps = {
  title: string;
  description?: string;
  eyebrow?: string;
  badges?: PortfolioSectionBadge[];
  actions?: ReactNode;
  children: ReactNode;
  className?: string;
};

export function PortfolioSectionCard({
  title,
  description,
  eyebrow,
  badges = [],
  actions,
  children,
  className = "",
}: PortfolioSectionCardProps) {
  const classes = ["card", "portfolio-section-card", className]
    .filter(Boolean)
    .join(" ");

  return (
    <section className={classes}>
      <div className="portfolio-section-card__header">
        <div>
          {eyebrow ? (
            <span className="portfolio-section-card__eyebrow">{eyebrow}</span>
          ) : null}
          <h2>{title}</h2>
          {description ? <p>{description}</p> : null}
        </div>
        <div className="portfolio-section-card__aside">
          {badges.length ? (
            <div className="portfolio-section-card__badges">
              {badges.map((badge) => {
                const badgeLabel = typeof badge === "string" ? badge : badge.label;
                const badgeVariant =
                  typeof badge === "string" ? "neutral" : badge.variant;

                return (
                  <PortfolioStatusBadge
                    key={badgeLabel}
                    label={badgeLabel}
                    variant={badgeVariant}
                  />
                );
              })}
            </div>
          ) : null}
          {actions}
        </div>
      </div>
      {children}
    </section>
  );
}
