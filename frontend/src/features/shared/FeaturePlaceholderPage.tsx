import { PageHeader } from "../../components/layout/PageHeader";
import { Card } from "../../components/ui/Card";
import { useTranslation } from "../../hooks/useTranslation";

type FeaturePlaceholderPageProps = {
  titleKey: string;
  descriptionKey: string;
};

export function FeaturePlaceholderPage({
  titleKey,
  descriptionKey,
}: FeaturePlaceholderPageProps) {
  const { t } = useTranslation();

  return (
    <div className="page placeholder-page">
      <PageHeader title={t(titleKey)} subtitle={t(descriptionKey)} />
      <Card>
        <div className="placeholder-page__note">
          <p>{t("common.placeholderDescription")}</p>
        </div>
      </Card>
      <Card>
        <PageHeader
          title={t("common.placeholderTitle")}
          subtitle={t("common.comingSoon")}
        />
      </Card>
    </div>
  );
}
