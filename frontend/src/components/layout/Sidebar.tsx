import { NavLink, useLocation } from "react-router-dom";

import { useTranslation } from "../../hooks/useTranslation";
import { navigationItems } from "../../lib/constants";

export function Sidebar() {
  const { t } = useTranslation();
  const location = useLocation();

  return (
    <aside className="sidebar">
      <div className="sidebar__brand">
        <span className="sidebar__eyebrow">{t("common.platform")}</span>
        <h1 className="sidebar__title">{t("app.name")}</h1>
        <p className="sidebar__subtitle">{t("app.subtitle")}</p>
      </div>

      <nav className="sidebar__nav" aria-label={t("common.primaryNavigation")}>
        {navigationItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === "/"}
            className={({ isActive }) => {
              const isDashboardAlias =
                item.path === "/" && location.pathname === "/dashboard";
              return isActive || isDashboardAlias
                ? "sidebar__link sidebar__link--active"
                : "sidebar__link";
            }}
          >
            {t(item.labelKey)}
          </NavLink>
        ))}
      </nav>
      <div className="sidebar__footer">
        <span>{t("common.researchMode")}</span>
        <strong>{t("common.demoDataOnline")}</strong>
      </div>
    </aside>
  );
}
