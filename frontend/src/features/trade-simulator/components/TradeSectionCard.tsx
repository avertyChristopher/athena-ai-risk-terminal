import type { ReactNode } from "react";

import {
  TradeStatusBadge,
  TradeStatusBadgeVariant,
} from "./TradeStatusBadge";

type TradeSectionBadge = {
  label: string;
  variant?: TradeStatusBadgeVariant;
};

type TradeSectionCardProps = {
  title: string;
  description?: string;
  badges?: TradeSectionBadge[];
  children: ReactNode;
  className?: string;
};

export function TradeSectionCard({
  title,
  description,
  badges = [],
  children,
  className = "",
}: TradeSectionCardProps) {
  const classes = ["card", "trade-section-card", className]
    .filter(Boolean)
    .join(" ");

  return (
    <section className={classes}>
      <div className="trade-section-card__header">
        <div>
          <h2>{title}</h2>
          {description ? <p>{description}</p> : null}
        </div>
        {badges.length ? (
          <div className="trade-badge-cluster">
            {badges.map((badge) => (
              <TradeStatusBadge
                key={badge.label}
                label={badge.label}
                variant={badge.variant}
              />
            ))}
          </div>
        ) : null}
      </div>
      {children}
    </section>
  );
}
