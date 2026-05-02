import { MetricCard } from "../../../components/finance/MetricCard";
import { MoneyValue } from "../../../components/finance/MoneyValue";
import { PercentValue } from "../../../components/finance/PercentValue";
import { RiskBadge } from "../../../components/finance/RiskBadge";
import { PageHeader } from "../../../components/layout/PageHeader";
import { Card } from "../../../components/ui/Card";
import { useHealth } from "../../../hooks/useHealth";
import { useTranslation } from "../../../hooks/useTranslation";

export function DashboardPage() {
  const { t } = useTranslation();
  const healthQuery = useHealth();

  const healthValue = healthQuery.isLoading
    ? t("common.loading")
    : healthQuery.isError
      ? t("common.unavailable")
      : healthQuery.data?.status ?? t("common.unavailable");

  return (
    <div className="page">
      <PageHeader
        title={t("dashboard.title")}
        subtitle={t("dashboard.subtitle")}
      />

      <section className="hero">
        <h2>{t("dashboard.heroTitle")}</h2>
        <p>{t("dashboard.heroSubtitle")}</p>
      </section>

      <section className="grid">
        <MetricCard
          title={t("dashboard.cards.platformHealth")}
          value={healthValue}
          subtitle={t("dashboard.descriptions.platformHealth")}
          meta={<RiskBadge level={healthQuery.isError ? "high" : "low"} />}
        />
        <MetricCard
          title={t("dashboard.cards.samplePnl")}
          value={<MoneyValue value={1250000} />}
          subtitle={t("dashboard.descriptions.samplePnl")}
          meta={<RiskBadge level="low" />}
        />
        <MetricCard
          title={t("dashboard.cards.sampleVar")}
          value={<PercentValue value={0.0234} />}
          subtitle={t("dashboard.descriptions.sampleVar")}
          meta={<RiskBadge level="medium" />}
        />
        <MetricCard
          title={t("dashboard.cards.riskDna")}
          value={<RiskBadge level="medium" />}
          subtitle={t("dashboard.descriptions.riskDna")}
        />
      </section>

      <Card>
        <PageHeader
          title={t("dashboard.contentTitle")}
          subtitle={t("dashboard.contentBody")}
        />
        {!healthQuery.isError && healthQuery.data ? (
          <p>
            {healthQuery.data.service}: {healthQuery.data.status}
          </p>
        ) : null}
      </Card>
    </div>
  );
}
