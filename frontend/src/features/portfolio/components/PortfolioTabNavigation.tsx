type PortfolioTab = {
  id: string;
  label: string;
  description?: string;
};

type PortfolioTabNavigationProps = {
  tabs: PortfolioTab[];
  activeTab: string;
  onTabChange: (tabId: string) => void;
};

export function PortfolioTabNavigation({
  tabs,
  activeTab,
  onTabChange,
}: PortfolioTabNavigationProps) {
  return (
    <nav className="portfolio-tabs" aria-label="Portfolio Builder sections">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          className={`portfolio-tab ${activeTab === tab.id ? "portfolio-tab--active" : ""}`}
          type="button"
          onClick={() => onTabChange(tab.id)}
        >
          <span>{tab.label}</span>
          {tab.description ? <small>{tab.description}</small> : null}
        </button>
      ))}
    </nav>
  );
}

export type { PortfolioTab };
