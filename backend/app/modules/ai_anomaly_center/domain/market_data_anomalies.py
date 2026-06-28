from __future__ import annotations

from datetime import date
from statistics import mean
from typing import Any

from app.modules.ai_anomaly_center.domain.anomaly_scoring import build_anomaly, score_anomaly
from app.modules.ai_anomaly_center.schemas import AnomalyRecord


def detect_market_data_anomalies(context: dict[str, Any], portfolio_id: str | None) -> list[AnomalyRecord]:
    records: list[AnomalyRecord] = []
    today = date(2026, 6, 28)
    portfolio = context.get("portfolio") or {}
    positions = context.get("positions") or []
    prices_by_symbol: dict[str, list[dict[str, Any]]] = context.get("prices", {})
    benchmark = str(portfolio.get("benchmark") or "").upper()
    if benchmark and benchmark not in prices_by_symbol:
        records.append(
            build_anomaly(
                portfolio_id=portfolio_id,
                module_name="Market Data",
                category="market_data",
                anomaly_type="benchmark_missing",
                title=f"{benchmark} benchmark data is missing",
                description="Portfolio benchmark was not available in the Market Data scan context.",
                metric_name="benchmark_price_coverage",
                observed_value=0,
                threshold="benchmark price history available",
                score=43,
                suggested_action="Import benchmark prices before relying on active risk and attribution outputs.",
            ),
        )
    base_currency = str(portfolio.get("base_currency") or portfolio.get("currency") or "USD").upper()
    foreign_currencies = {
        str(position.get("currency") or base_currency).upper()
        for position in positions
        if str(position.get("currency") or base_currency).upper() != base_currency
    }
    if foreign_currencies and not context.get("fx_rates"):
        records.append(
            build_anomaly(
                portfolio_id=portfolio_id,
                module_name="Market Data",
                category="market_data",
                anomaly_type="fx_data_unavailable",
                title="FX data unavailable for foreign-currency holdings",
                description="Portfolio contains non-base currency holdings but no FX rates were available.",
                metric_name="fx_rate_coverage",
                observed_value=0,
                threshold="FX rates for foreign currencies",
                score=42,
                suggested_action="Refresh FX data before relying on multi-currency P&L or reconciliation.",
            ),
        )
    for symbol, rows in prices_by_symbol.items():
        sorted_rows = sorted(rows, key=lambda row: str(row.get("date", "")))
        if not sorted_rows:
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id,
                    module_name="Market Data",
                    category="market_data",
                    anomaly_type="missing_latest_price",
                    title=f"{symbol} missing price history",
                    description=f"No price rows were available for {symbol}.",
                    metric_name="price_count",
                    observed_value=0,
                    threshold=">=1",
                    score=45,
                    suggested_action="Review Market Data coverage and import a fresh price series.",
                ),
            )
            continue
        latest = sorted_rows[-1]
        close = _as_float(latest.get("close"))
        if close is None or close <= 0:
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id,
                    module_name="Market Data",
                    category="market_data",
                    anomaly_type="invalid_price",
                    title=f"{symbol} invalid latest price",
                    description="Latest close is missing, zero or negative.",
                    metric_name="latest_close",
                    observed_value=close,
                    threshold=">0",
                    score=70 if close == 0 else 85,
                    suggested_action="Quarantine the price and verify upstream market data.",
                ),
            )
        latest_date = _parse_date(latest.get("date"))
        if latest_date and (today - latest_date).days > 7:
            score, severity, confidence, explanation = score_anomaly(magnitude=min((today - latest_date).days / 30, 1.0), data_quality_penalty=10)
            records.append(
                build_anomaly(
                    portfolio_id=portfolio_id,
                    module_name="Market Data",
                    category="market_data",
                    anomaly_type="stale_price",
                    title=f"{symbol} stale latest price",
                    description=f"Latest Market Data timestamp is {(today - latest_date).days} days old.",
                    metric_name="days_since_latest_price",
                    observed_value=(today - latest_date).days,
                    threshold=7,
                    score=score,
                    severity=severity,
                    confidence=confidence,
                    explanation=explanation,
                    suggested_action="Refresh prices before relying on risk, P&L or reconciliation outputs.",
                ),
            )
        if len(sorted_rows) >= 2:
            previous = _as_float(sorted_rows[-2].get("close"))
            if previous and close:
                daily_return = close / previous - 1.0
                threshold = 0.10 if symbol.endswith(("SPY", "QQQ", "BND", "TLT", "IEF", "VXUS")) else 0.20
                if abs(daily_return) > threshold:
                    records.append(
                        build_anomaly(
                            portfolio_id=portfolio_id,
                            module_name="Market Data",
                            category="market_data",
                            anomaly_type="abnormal_return",
                            title=f"{symbol} abnormal latest return",
                            description=f"Latest one-period return is {daily_return:.2%}.",
                            metric_name="latest_return",
                            observed_value=daily_return,
                            threshold=threshold,
                            score=min(95, abs(daily_return) / threshold * 35),
                            suggested_action="Validate the price move against source data and corporate actions.",
                        ),
                    )
        returns = _returns(sorted_rows)
        if len(returns) >= 8:
            recent = mean(abs(item) for item in returns[-3:])
            baseline = mean(abs(item) for item in returns[:-3]) or 0.0001
            if recent > baseline * 2:
                records.append(
                    build_anomaly(
                        portfolio_id=portfolio_id,
                        module_name="Market Data",
                        category="market_data",
                        anomaly_type="volatility_jump",
                        title=f"{symbol} volatility jump",
                        description="Recent absolute returns are more than twice the baseline.",
                        metric_name="recent_abs_return_vs_baseline",
                        observed_value=recent,
                        expected_value=baseline,
                        threshold="2x",
                        score=min(88, recent / baseline * 18),
                        suggested_action="Review volatility inputs before stress, VaR and option analytics.",
                    ),
                )
    if not prices_by_symbol:
        records.append(
            build_anomaly(
                portfolio_id=portfolio_id,
                module_name="Market Data",
                category="market_data",
                anomaly_type="coverage_drop",
                title="No portfolio Market Data coverage",
                description="No symbols were available for Market Data anomaly scanning.",
                metric_name="symbols_with_prices",
                observed_value=0,
                threshold=">0",
                score=48,
                suggested_action="Select a portfolio with holdings or import Market Data coverage.",
            ),
        )
    return records


def _returns(rows: list[dict[str, Any]]) -> list[float]:
    output: list[float] = []
    previous: float | None = None
    for row in rows:
        close = _as_float(row.get("close"))
        if previous and close:
            output.append(close / previous - 1.0)
        previous = close
    return output


def _parse_date(value: Any) -> date | None:
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def _as_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
