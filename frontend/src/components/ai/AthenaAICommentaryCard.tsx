import { EmptyState } from "../ui/EmptyState";
import { LoadingState } from "../ui/LoadingState";
import { StatusBadge } from "../ui/StatusBadge";
import { useTranslation } from "../../hooks/useTranslation";
import type { AthenaAICommentary } from "../../types/athena-intelligence";

type AthenaAICommentaryCardProps = {
  commentary?: AthenaAICommentary | null;
  title?: string;
  isLoading?: boolean;
  className?: string;
};

type CommentarySection = {
  key: string;
  title: string;
  values: string[];
};

export function AthenaAICommentaryCard({
  commentary,
  title,
  isLoading = false,
  className = "",
}: AthenaAICommentaryCardProps) {
  const { t } = useTranslation();

  if (isLoading) {
    return (
      <section className={["athena-ai-card", className].filter(Boolean).join(" ")}>
        <LoadingState label={t("athenaIntelligence.loading")} />
      </section>
    );
  }

  if (!commentary) {
    return (
      <section className={["athena-ai-card", className].filter(Boolean).join(" ")}>
        <EmptyState
          title={t("athenaIntelligence.emptyTitle")}
          message={t("athenaIntelligence.emptyMessage")}
        />
      </section>
    );
  }

  const sections: CommentarySection[] = [
    {
      key: "main_risks",
      title: t("athenaIntelligence.mainRisks"),
      values: commentary.main_risks,
    },
    {
      key: "risk_drivers",
      title: t("athenaIntelligence.riskDrivers"),
      values: commentary.risk_drivers,
    },
    {
      key: "breaches",
      title: t("athenaIntelligence.breaches"),
      values: commentary.breaches,
    },
    {
      key: "suggested_actions",
      title: t("athenaIntelligence.suggestedActions"),
      values: commentary.suggested_actions,
    },
    {
      key: "assumptions",
      title: t("athenaIntelligence.assumptions"),
      values: commentary.assumptions,
    },
    {
      key: "limitations",
      title: t("athenaIntelligence.limitations"),
      values: commentary.limitations,
    },
  ].filter((section) => section.values.length > 0);

  return (
    <section className={["athena-ai-card", className].filter(Boolean).join(" ")}>
      <div className="athena-ai-card__header">
        <div>
          <span className="athena-ai-card__eyebrow">
            {t("athenaIntelligence.eyebrow")}
          </span>
          <h2>{title ?? t("athenaIntelligence.title")}</h2>
          <p>{commentary.summary}</p>
        </div>
        <div className="risk-monitor-badge-cluster">
          <StatusBadge
            label={providerLabel(commentary.generated_by, t)}
            variant={commentary.generated_by.includes("fallback") ? "warning" : "success"}
          />
          <StatusBadge
            label={`${t("athenaIntelligence.confidence")}: ${t(
              `athenaIntelligence.confidenceLevels.${commentary.confidence_level}`,
            )}`}
            variant={confidenceVariant(commentary.confidence_level)}
          />
        </div>
      </div>

      {commentary.source_modules.length ? (
        <div className="athena-ai-source-row" aria-label={t("athenaIntelligence.sources")}>
          <span>{t("athenaIntelligence.sources")}</span>
          <div>
            {commentary.source_modules.map((source) => (
              <strong key={source}>{formatModuleName(source)}</strong>
            ))}
          </div>
        </div>
      ) : null}

      <div className="athena-ai-grid">
        {sections.map((section) => (
          <article className="athena-ai-section" key={section.key}>
            <h3>{section.title}</h3>
            <ul>
              {section.values.map((value) => (
                <li key={value}>{value}</li>
              ))}
            </ul>
          </article>
        ))}
      </div>

      <footer className="athena-ai-card__footer">
        <span>{commentary.disclaimer}</span>
        <time dateTime={commentary.generated_at}>
          {t("common.generatedAt")}: {formatGeneratedAt(commentary.generated_at)}
        </time>
      </footer>
    </section>
  );
}

function providerLabel(provider: string, t: (key: string) => string) {
  if (provider.includes("fallback")) return t("athenaIntelligence.fallbackMode");
  if (provider.includes("openai")) return t("athenaIntelligence.openaiMode");
  return provider;
}

function confidenceVariant(confidence: AthenaAICommentary["confidence_level"]) {
  if (confidence === "high") return "success";
  if (confidence === "medium") return "info";
  return "warning";
}

function formatModuleName(moduleName: string) {
  return moduleName
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

function formatGeneratedAt(value: string) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString();
}
