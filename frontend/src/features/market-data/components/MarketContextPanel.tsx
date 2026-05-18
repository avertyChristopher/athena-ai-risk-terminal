import { MoneyValue } from "../../../components/finance/MoneyValue";
import { PercentValue } from "../../../components/finance/PercentValue";
import { MarketDataAnalyticsResponse } from "../../../types/market-data";
import { ReferenceDataPanel } from "./ReferenceDataPanel";

type MarketContextPanelProps = {
  title: string;
  analytics?: MarketDataAnalyticsResponse;
  labels: {
    fxRate: string;
    currencyConsistency: string;
    yieldCurve2y: string;
    yieldCurve10y: string;
    commodityProxy: string;
  };
};

export function MarketContextPanel({
  title,
  analytics,
  labels,
}: MarketContextPanelProps) {
  return (
    <ReferenceDataPanel
      title={title}
      items={[
        {
          label: labels.fxRate,
          value: analytics?.fx_rate_to_usd.toFixed(4) ?? "--",
        },
        {
          label: labels.currencyConsistency,
          value: analytics?.currency_consistency_status ?? "--",
        },
        {
          label: labels.yieldCurve2y,
          value: analytics ? <PercentValue value={analytics.yield_curve_2y} /> : "--",
        },
        {
          label: labels.yieldCurve10y,
          value: analytics ? <PercentValue value={analytics.yield_curve_10y} /> : "--",
        },
        {
          label: labels.commodityProxy,
          value: analytics ? (
            <>
              {analytics.commodity_proxy_symbol}{" "}
              <MoneyValue
                value={analytics.commodity_proxy_latest_price}
                currency="USD"
              />
            </>
          ) : (
            "--"
          ),
        },
      ]}
    />
  );
}
