import { useLocation } from "react-router-dom";

import { useTranslation } from "../../hooks/useTranslation";
import { navigationItems } from "../../lib/constants";

export function Topbar() {
  const location = useLocation();
  const { i18n, t } = useTranslation();

  const currentItem =
    navigationItems.find((item) => item.path === location.pathname) ??
    navigationItems[0];

  const setLanguage = (language: "en" | "fr") => {
    void i18n.changeLanguage(language);
  };

  return (
    <header className="topbar">
      <div>
        <h2 className="topbar__title">{t(currentItem.labelKey)}</h2>
        <p className="topbar__subtitle">{t("common.environmentValue")}</p>
      </div>

      <div className="topbar__controls">
        <span className="topbar__label">{t("common.language")}</span>
        <div className="topbar__language-group">
          <button
            type="button"
            className={
              i18n.language.startsWith("en")
                ? "language-button language-button--active"
                : "language-button"
            }
            onClick={() => setLanguage("en")}
          >
            {t("common.english")}
          </button>
          <button
            type="button"
            className={
              i18n.language.startsWith("fr")
                ? "language-button language-button--active"
                : "language-button"
            }
            onClick={() => setLanguage("fr")}
          >
            {t("common.french")}
          </button>
        </div>
      </div>
    </header>
  );
}
