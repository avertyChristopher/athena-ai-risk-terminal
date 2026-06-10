import { useTranslation } from "../../hooks/useTranslation";

type PageHeaderProps = {
  title: string;
  subtitle: string;
};

export function PageHeader({ title, subtitle }: PageHeaderProps) {
  const { t } = useTranslation();

  return (
    <header className="page-header">
      <div>
        <span className="page-header__eyebrow">{t("common.workstation")}</span>
        <h1>{title}</h1>
        <p>{subtitle}</p>
      </div>
    </header>
  );
}
