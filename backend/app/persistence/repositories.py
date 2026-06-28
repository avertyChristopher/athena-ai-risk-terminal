from __future__ import annotations

from contextlib import contextmanager
from datetime import UTC, date, datetime
from typing import Any, Iterator

from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database.base import Base
from app.database.session import SessionLocal, engine
from app.modules.limit_center.schemas import LimitBreach
from app.modules.pnl_attribution.schemas import PnlAttributionResult
from app.modules.reconciliation.schemas import ReconciliationBreak, ReconciliationRunResult
from app.modules.reports_center.domain.export_formatters import report_to_markdown
from app.modules.reports_center.schemas import GeneratedReport
from app.modules.stress_testing.schemas import StressTestingResponse
from app.persistence.models import (
    AthenaCommentaryModel,
    AnomalyRecordModel,
    LimitBreachModel,
    PnlAnalysisModel,
    PortfolioSnapshotModel,
    ReconciliationBreakModel,
    ReconciliationRunModel,
    ReportModel,
    StressRunModel,
    TradeBlotterEntryModel,
)
from app.persistence.serialization import (
    coerce_datetime,
    from_json,
    model_from_json,
    text_to_value,
    to_json,
    value_to_text,
)

_DB_READY = False


@contextmanager
def managed_session(db: Session | None) -> Iterator[Session]:
    _ensure_persistence_tables()
    if db is not None:
        yield db
        return
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def _ensure_persistence_tables() -> None:
    global _DB_READY
    if _DB_READY:
        return
    try:
        Base.metadata.create_all(bind=engine)
        _DB_READY = True
    except SQLAlchemyError:
        _DB_READY = False


def _commit(session: Session) -> None:
    session.commit()


def _rollback(session: Session) -> None:
    session.rollback()


class PortfolioSnapshotPersistenceRepository:
    def __init__(self, db: Session | None = None) -> None:
        self.db = db

    def save_snapshot(
        self,
        *,
        portfolio_id: str,
        portfolio_name: str | None,
        snapshot_type: str,
        source_module: str,
        payload: Any,
        generated_at: datetime | date | str | None = None,
    ) -> bool:
        try:
            with managed_session(self.db) as session:
                session.add(
                    PortfolioSnapshotModel(
                        portfolio_id=portfolio_id,
                        portfolio_name=portfolio_name,
                        snapshot_type=snapshot_type,
                        payload_json=to_json(payload),
                        source_module=source_module,
                        generated_at=coerce_datetime(generated_at) if generated_at else datetime.now(UTC),
                    ),
                )
                _commit(session)
                return True
        except SQLAlchemyError:
            return False

    def clear(self) -> None:
        _clear_table(self.db, PortfolioSnapshotModel)


class ReportPersistenceRepository:
    def __init__(self, db: Session | None = None) -> None:
        self.db = db

    def save(self, report: GeneratedReport) -> bool:
        try:
            payload = report.model_dump(mode="json")
            with managed_session(self.db) as session:
                model = session.scalar(select(ReportModel).where(ReportModel.report_id == report.report_id))
                if model is None:
                    model = ReportModel(
                        report_id=report.report_id,
                        report_type=report.report_type,
                        portfolio_id=report.portfolio_id,
                        portfolio_name=report.portfolio_name,
                        language=report.language,
                        title=report.title,
                        payload_json=to_json(payload),
                        markdown_content=report_to_markdown(report),
                        source_modules_json=to_json(report.snapshot.source_modules),
                        warnings_json=to_json(report.warnings),
                        generated_by=report.snapshot.generated_by,
                        generated_at=coerce_datetime(report.generated_at),
                    )
                    session.add(model)
                else:
                    model.report_type = report.report_type
                    model.portfolio_id = report.portfolio_id
                    model.portfolio_name = report.portfolio_name
                    model.language = report.language
                    model.title = report.title
                    model.payload_json = to_json(payload)
                    model.markdown_content = report_to_markdown(report)
                    model.source_modules_json = to_json(report.snapshot.source_modules)
                    model.warnings_json = to_json(report.warnings)
                    model.generated_by = report.snapshot.generated_by
                    model.generated_at = coerce_datetime(report.generated_at)
                _commit(session)
                return True
        except SQLAlchemyError:
            return False

    def list(self) -> list[GeneratedReport]:
        try:
            with managed_session(self.db) as session:
                rows = session.scalars(select(ReportModel).order_by(ReportModel.generated_at.desc())).all()
                return [model_from_json(GeneratedReport, row.payload_json) for row in rows]
        except SQLAlchemyError:
            return []

    def get(self, report_id: str) -> GeneratedReport | None:
        try:
            with managed_session(self.db) as session:
                row = session.scalar(select(ReportModel).where(ReportModel.report_id == report_id))
                return model_from_json(GeneratedReport, row.payload_json) if row else None
        except SQLAlchemyError:
            return None

    def delete(self, report_id: str) -> bool:
        try:
            with managed_session(self.db) as session:
                result = session.execute(delete(ReportModel).where(ReportModel.report_id == report_id))
                _commit(session)
                return bool(result.rowcount)
        except SQLAlchemyError:
            return False

    def clear(self) -> None:
        _clear_table(self.db, ReportModel)


class PnlAnalysisPersistenceRepository:
    def __init__(self, db: Session | None = None) -> None:
        self.db = db

    def save(self, analysis: PnlAttributionResult) -> bool:
        try:
            with managed_session(self.db) as session:
                model = session.scalar(select(PnlAnalysisModel).where(PnlAnalysisModel.analysis_id == analysis.analysis_id))
                payload = analysis.model_dump(mode="json")
                start_dt = coerce_datetime(analysis.period.start_date)
                end_dt = coerce_datetime(analysis.period.end_date)
                if model is None:
                    model = PnlAnalysisModel(
                        analysis_id=analysis.analysis_id,
                        portfolio_id=analysis.portfolio_id,
                        portfolio_name=analysis.portfolio_name,
                        start_date=start_dt,
                        end_date=end_dt,
                        benchmark_symbol=analysis.benchmark_comparison.benchmark_symbol,
                        payload_json=to_json(payload),
                        total_pnl=analysis.total_pnl,
                        total_return=analysis.total_pnl_percent,
                        generated_at=coerce_datetime(analysis.generated_at),
                    )
                    session.add(model)
                else:
                    model.portfolio_id = analysis.portfolio_id
                    model.portfolio_name = analysis.portfolio_name
                    model.start_date = start_dt
                    model.end_date = end_dt
                    model.benchmark_symbol = analysis.benchmark_comparison.benchmark_symbol
                    model.payload_json = to_json(payload)
                    model.total_pnl = analysis.total_pnl
                    model.total_return = analysis.total_pnl_percent
                    model.generated_at = coerce_datetime(analysis.generated_at)
                _commit(session)
                return True
        except SQLAlchemyError:
            return False

    def list(self) -> list[PnlAttributionResult]:
        try:
            with managed_session(self.db) as session:
                rows = session.scalars(select(PnlAnalysisModel).order_by(PnlAnalysisModel.generated_at.desc())).all()
                return [model_from_json(PnlAttributionResult, row.payload_json) for row in rows]
        except SQLAlchemyError:
            return []

    def get(self, analysis_id: str) -> PnlAttributionResult | None:
        try:
            with managed_session(self.db) as session:
                row = session.scalar(select(PnlAnalysisModel).where(PnlAnalysisModel.analysis_id == analysis_id))
                return model_from_json(PnlAttributionResult, row.payload_json) if row else None
        except SQLAlchemyError:
            return None

    def delete(self, analysis_id: str) -> bool:
        try:
            with managed_session(self.db) as session:
                result = session.execute(delete(PnlAnalysisModel).where(PnlAnalysisModel.analysis_id == analysis_id))
                _commit(session)
                return bool(result.rowcount)
        except SQLAlchemyError:
            return False

    def clear(self) -> None:
        _clear_table(self.db, PnlAnalysisModel)


class ReconciliationPersistenceRepository:
    def __init__(self, db: Session | None = None) -> None:
        self.db = db

    def save_run(self, run: ReconciliationRunResult) -> bool:
        try:
            with managed_session(self.db) as session:
                model = session.scalar(select(ReconciliationRunModel).where(ReconciliationRunModel.run_id == run.run_id))
                if model is None:
                    model = ReconciliationRunModel(
                        run_id=run.run_id,
                        portfolio_id=run.portfolio_id,
                        portfolio_name=run.portfolio_name,
                        reconciliation_date=coerce_datetime(run.reconciliation_date),
                        external_source=run.external_source,
                        overall_status=run.overall_status,
                        payload_json=to_json(run),
                        generated_at=coerce_datetime(run.generated_at),
                    )
                    session.add(model)
                else:
                    model.portfolio_id = run.portfolio_id
                    model.portfolio_name = run.portfolio_name
                    model.reconciliation_date = coerce_datetime(run.reconciliation_date)
                    model.external_source = run.external_source
                    model.overall_status = run.overall_status
                    model.payload_json = to_json(run)
                    model.generated_at = coerce_datetime(run.generated_at)
                session.execute(delete(ReconciliationBreakModel).where(ReconciliationBreakModel.run_id == run.run_id))
                for item in run.breaks:
                    session.add(self._break_model(item))
                _commit(session)
                return True
        except SQLAlchemyError:
            return False

    def list_runs(self) -> list[ReconciliationRunResult]:
        try:
            with managed_session(self.db) as session:
                rows = session.scalars(select(ReconciliationRunModel).order_by(ReconciliationRunModel.generated_at.desc())).all()
                return [model_from_json(ReconciliationRunResult, row.payload_json) for row in rows]
        except SQLAlchemyError:
            return []

    def get_run(self, run_id: str) -> ReconciliationRunResult | None:
        try:
            with managed_session(self.db) as session:
                row = session.scalar(select(ReconciliationRunModel).where(ReconciliationRunModel.run_id == run_id))
                return model_from_json(ReconciliationRunResult, row.payload_json) if row else None
        except SQLAlchemyError:
            return None

    def delete_run(self, run_id: str) -> bool:
        try:
            with managed_session(self.db) as session:
                session.execute(delete(ReconciliationBreakModel).where(ReconciliationBreakModel.run_id == run_id))
                result = session.execute(delete(ReconciliationRunModel).where(ReconciliationRunModel.run_id == run_id))
                _commit(session)
                return bool(result.rowcount)
        except SQLAlchemyError:
            return False

    def list_breaks(self) -> list[ReconciliationBreak]:
        try:
            with managed_session(self.db) as session:
                rows = session.scalars(select(ReconciliationBreakModel).order_by(ReconciliationBreakModel.created_at.desc())).all()
                return [model_from_json(ReconciliationBreak, row.payload_json) for row in rows]
        except SQLAlchemyError:
            return []

    def get_break(self, break_id: str) -> ReconciliationBreak | None:
        try:
            with managed_session(self.db) as session:
                row = session.scalar(select(ReconciliationBreakModel).where(ReconciliationBreakModel.break_id == break_id))
                return model_from_json(ReconciliationBreak, row.payload_json) if row else None
        except SQLAlchemyError:
            return None

    def save_break(self, item: ReconciliationBreak) -> bool:
        try:
            with managed_session(self.db) as session:
                session.execute(delete(ReconciliationBreakModel).where(ReconciliationBreakModel.break_id == item.break_id))
                session.add(self._break_model(item))
                run_row = session.scalar(select(ReconciliationRunModel).where(ReconciliationRunModel.run_id == item.run_id))
                if run_row is not None:
                    run = model_from_json(ReconciliationRunResult, run_row.payload_json)
                    updated_breaks = [item if row.break_id == item.break_id else row for row in run.breaks]
                    run_row.payload_json = to_json(run.model_copy(update={"breaks": updated_breaks}))
                _commit(session)
                return True
        except SQLAlchemyError:
            return False

    def clear(self) -> None:
        _clear_table(self.db, ReconciliationBreakModel)
        _clear_table(self.db, ReconciliationRunModel)

    def _break_model(self, item: ReconciliationBreak) -> ReconciliationBreakModel:
        return ReconciliationBreakModel(
            break_id=item.break_id,
            run_id=item.run_id,
            portfolio_id=item.portfolio_id,
            break_type=item.break_type,
            severity=item.severity,
            status=item.status,
            symbol=item.symbol,
            metric=item.metric,
            internal_value=value_to_text(item.internal_value),
            external_value=value_to_text(item.external_value),
            difference=value_to_text(item.difference),
            tolerance=value_to_text(item.tolerance),
            source_module=item.source_module,
            explanation=item.explanation,
            suggested_action=item.suggested_action,
            payload_json=to_json(item),
            review_history_json=to_json([event.model_dump(mode="json") for event in item.review_history]),
            created_at=coerce_datetime(item.created_at),
            updated_at=coerce_datetime(item.updated_at),
        )


class LimitBreachPersistenceRepository:
    def __init__(self, db: Session | None = None) -> None:
        self.db = db

    def save_many(self, breaches: list[LimitBreach]) -> bool:
        try:
            with managed_session(self.db) as session:
                for breach in breaches:
                    session.execute(delete(LimitBreachModel).where(LimitBreachModel.breach_id == breach.breach_id))
                    session.add(self._model(breach))
                _commit(session)
                return True
        except SQLAlchemyError:
            return False

    def list(self) -> list[LimitBreach]:
        try:
            with managed_session(self.db) as session:
                rows = session.scalars(select(LimitBreachModel).order_by(LimitBreachModel.created_at.desc())).all()
                return [model_from_json(LimitBreach, row.payload_json) for row in rows]
        except SQLAlchemyError:
            return []

    def get(self, breach_id: str) -> LimitBreach | None:
        try:
            with managed_session(self.db) as session:
                row = session.scalar(select(LimitBreachModel).where(LimitBreachModel.breach_id == breach_id))
                return model_from_json(LimitBreach, row.payload_json) if row else None
        except SQLAlchemyError:
            return None

    def save(self, breach: LimitBreach) -> bool:
        return self.save_many([breach])

    def clear(self) -> None:
        _clear_table(self.db, LimitBreachModel)

    def _model(self, breach: LimitBreach) -> LimitBreachModel:
        return LimitBreachModel(
            breach_id=breach.breach_id,
            portfolio_id=breach.portfolio_id,
            rule_id=breach.rule_id,
            rule_name=breach.rule_name,
            source_module=breach.source_module,
            metric_key=breach.metric_key,
            current_value=value_to_text(breach.current_value) or "",
            limit_value=value_to_text(breach.limit_value) or "",
            severity=breach.severity,
            status=breach.status,
            explanation=breach.explanation,
            suggested_action=breach.suggested_action,
            payload_json=to_json(breach),
            review_history_json=to_json([event.model_dump(mode="json") for event in breach.review_history]),
            created_at=coerce_datetime(breach.created_at),
            updated_at=coerce_datetime(breach.updated_at),
        )


class StressRunPersistenceRepository:
    def __init__(self, db: Session | None = None) -> None:
        self.db = db

    def save(self, run_id: str, response: StressTestingResponse) -> bool:
        try:
            with managed_session(self.db) as session:
                session.execute(delete(StressRunModel).where(StressRunModel.run_id == run_id))
                session.add(
                    StressRunModel(
                        run_id=run_id,
                        portfolio_id=response.selected_portfolio.portfolio_id,
                        portfolio_name=response.selected_portfolio.name,
                        scenario_id=response.selected_scenario.id,
                        scenario_name=response.selected_scenario.name,
                        severity=response.severity.severity,
                        estimated_loss=response.dollar_loss,
                        estimated_loss_percent=response.percent_loss,
                        payload_json=to_json(response),
                        generated_at=coerce_datetime(response.methodology.generated_at),
                    ),
                )
                _commit(session)
                return True
        except SQLAlchemyError:
            return False

    def list(self) -> list[dict[str, Any]]:
        try:
            with managed_session(self.db) as session:
                rows = session.scalars(select(StressRunModel).order_by(StressRunModel.generated_at.desc())).all()
                return [_stress_row(row) for row in rows]
        except SQLAlchemyError:
            return []

    def get(self, run_id: str) -> StressTestingResponse | None:
        try:
            with managed_session(self.db) as session:
                row = session.scalar(select(StressRunModel).where(StressRunModel.run_id == run_id))
                return model_from_json(StressTestingResponse, row.payload_json) if row else None
        except SQLAlchemyError:
            return None

    def delete(self, run_id: str) -> bool:
        try:
            with managed_session(self.db) as session:
                result = session.execute(delete(StressRunModel).where(StressRunModel.run_id == run_id))
                _commit(session)
                return bool(result.rowcount)
        except SQLAlchemyError:
            return False

    def clear(self) -> None:
        _clear_table(self.db, StressRunModel)


class AthenaCommentaryPersistenceRepository:
    def __init__(self, db: Session | None = None) -> None:
        self.db = db

    def save(
        self,
        *,
        commentary_id: str,
        module_name: str,
        language: str,
        generated_by: str,
        payload: dict[str, Any],
        summary: str,
        portfolio_id: str | None = None,
        symbol: str | None = None,
    ) -> bool:
        try:
            with managed_session(self.db) as session:
                session.execute(delete(AthenaCommentaryModel).where(AthenaCommentaryModel.commentary_id == commentary_id))
                session.add(
                    AthenaCommentaryModel(
                        commentary_id=commentary_id,
                        module_name=module_name,
                        portfolio_id=portfolio_id,
                        symbol=symbol,
                        language=language,
                        generated_by=generated_by,
                        payload_json=to_json(payload),
                        summary=summary,
                    ),
                )
                _commit(session)
                return True
        except SQLAlchemyError:
            return False

    def list(self) -> list[dict[str, Any]]:
        try:
            with managed_session(self.db) as session:
                rows = session.scalars(select(AthenaCommentaryModel).order_by(AthenaCommentaryModel.created_at.desc())).all()
                return [
                    {
                        "commentary_id": row.commentary_id,
                        "module_name": row.module_name,
                        "portfolio_id": row.portfolio_id,
                        "symbol": row.symbol,
                        "language": row.language,
                        "generated_by": row.generated_by,
                        "payload": from_json(row.payload_json, {}),
                        "summary": row.summary,
                        "created_at": row.created_at,
                    }
                    for row in rows
                ]
        except SQLAlchemyError:
            return []

    def clear(self) -> None:
        _clear_table(self.db, AthenaCommentaryModel)


class TradeBlotterPersistenceRepository:
    def __init__(self, db: Session | None = None) -> None:
        self.db = db

    def save(self, payload: dict[str, Any]) -> bool:
        try:
            with managed_session(self.db) as session:
                trade_id = str(payload["trade_id"])
                session.execute(delete(TradeBlotterEntryModel).where(TradeBlotterEntryModel.trade_id == trade_id))
                session.add(_trade_model_from_payload(payload))
                _commit(session)
                return True
        except (KeyError, SQLAlchemyError):
            return False

    def list(self) -> list[dict[str, Any]]:
        try:
            with managed_session(self.db) as session:
                rows = session.scalars(select(TradeBlotterEntryModel).order_by(TradeBlotterEntryModel.created_at.desc())).all()
                return [_trade_payload_from_model(row) for row in rows]
        except SQLAlchemyError:
            return []

    def get(self, trade_id: str) -> dict[str, Any] | None:
        try:
            with managed_session(self.db) as session:
                row = session.scalar(select(TradeBlotterEntryModel).where(TradeBlotterEntryModel.trade_id == trade_id))
                return _trade_payload_from_model(row) if row else None
        except SQLAlchemyError:
            return None

    def delete(self, trade_id: str) -> bool:
        try:
            with managed_session(self.db) as session:
                result = session.execute(delete(TradeBlotterEntryModel).where(TradeBlotterEntryModel.trade_id == trade_id))
                _commit(session)
                return bool(result.rowcount)
        except SQLAlchemyError:
            return False

    def clear(self) -> None:
        _clear_table(self.db, TradeBlotterEntryModel)


class AnomalyRecordPersistenceRepository:
    def __init__(self, db: Session | None = None) -> None:
        self.db = db

    def save(self, payload: dict[str, Any]) -> bool:
        try:
            with managed_session(self.db) as session:
                anomaly_id = str(payload["anomaly_id"])
                session.execute(delete(AnomalyRecordModel).where(AnomalyRecordModel.anomaly_id == anomaly_id))
                session.add(_anomaly_model_from_payload(payload))
                _commit(session)
                return True
        except (KeyError, SQLAlchemyError):
            return False

    def save_many(self, payloads: list[dict[str, Any]]) -> list[dict[str, Any]]:
        saved: list[dict[str, Any]] = []
        for payload in payloads:
            if self.save(payload):
                saved.append(payload)
        return saved

    def list(
        self,
        *,
        portfolio_id: str | None = None,
        severity: str | None = None,
        module_name: str | None = None,
        status: str | None = None,
    ) -> list[dict[str, Any]]:
        try:
            with managed_session(self.db) as session:
                statement = select(AnomalyRecordModel)
                if portfolio_id:
                    statement = statement.where(AnomalyRecordModel.portfolio_id == portfolio_id)
                if severity:
                    statement = statement.where(AnomalyRecordModel.severity == severity)
                if module_name:
                    statement = statement.where(AnomalyRecordModel.module_name == module_name)
                if status:
                    statement = statement.where(AnomalyRecordModel.status == status)
                rows = session.scalars(statement.order_by(AnomalyRecordModel.detected_at.desc())).all()
                return [_anomaly_payload_from_model(row) for row in rows]
        except SQLAlchemyError:
            return []

    def recent(self, limit: int = 50) -> list[dict[str, Any]]:
        try:
            with managed_session(self.db) as session:
                rows = session.scalars(
                    select(AnomalyRecordModel).order_by(AnomalyRecordModel.detected_at.desc()).limit(limit),
                ).all()
                return [_anomaly_payload_from_model(row) for row in rows]
        except SQLAlchemyError:
            return []

    def get(self, anomaly_id: str) -> dict[str, Any] | None:
        try:
            with managed_session(self.db) as session:
                row = session.scalar(select(AnomalyRecordModel).where(AnomalyRecordModel.anomaly_id == anomaly_id))
                return _anomaly_payload_from_model(row) if row else None
        except SQLAlchemyError:
            return None

    def delete(self, anomaly_id: str) -> bool:
        try:
            with managed_session(self.db) as session:
                result = session.execute(delete(AnomalyRecordModel).where(AnomalyRecordModel.anomaly_id == anomaly_id))
                _commit(session)
                return bool(result.rowcount)
        except SQLAlchemyError:
            return False

    def clear(self) -> None:
        _clear_table(self.db, AnomalyRecordModel)


def _trade_model_from_payload(payload: dict[str, Any]) -> TradeBlotterEntryModel:
    trade_date = payload.get("trade_date")
    settlement_date = payload.get("settlement_date")
    return TradeBlotterEntryModel(
        trade_id=str(payload["trade_id"]),
        portfolio_id=str(payload.get("portfolio_id") or ""),
        symbol=str(payload.get("symbol") or "").upper(),
        action=str(payload.get("action") or "").lower(),
        quantity=float(payload.get("quantity") or 0.0),
        price=float(payload.get("price") or 0.0),
        estimated_trade_value=float(payload.get("estimated_trade_value") or 0.0),
        currency=str(payload.get("currency") or "USD"),
        status=str(payload.get("status") or "draft"),
        trade_date=coerce_datetime(trade_date) if trade_date else datetime.now(UTC),
        settlement_date=coerce_datetime(settlement_date) if settlement_date else None,
        source_module=str(payload.get("source_module") or "trade_blotter"),
        cost_estimate=float(payload.get("cost_estimate") or 0.0),
        slippage_estimate=float(payload.get("slippage_estimate") or 0.0),
        suitability_status=payload.get("suitability_status"),
        constraint_status=payload.get("constraint_status"),
        risk_summary_json=to_json(payload.get("risk_summary") or {}),
        trade_payload_json=to_json(payload),
        review_history_json=to_json(payload.get("review_history") or []),
        athena_commentary_json=to_json(payload.get("athena_ai_commentary")) if payload.get("athena_ai_commentary") else None,
        created_at=coerce_datetime(payload.get("created_at")) if payload.get("created_at") else datetime.now(UTC),
        updated_at=coerce_datetime(payload.get("updated_at")) if payload.get("updated_at") else datetime.now(UTC),
        reviewed_by=payload.get("reviewed_by"),
        review_note=payload.get("review_note"),
    )


def _trade_payload_from_model(row: TradeBlotterEntryModel) -> dict[str, Any]:
    payload = from_json(row.trade_payload_json, {})
    payload.update(
        {
            "trade_id": row.trade_id,
            "portfolio_id": row.portfolio_id,
            "symbol": row.symbol,
            "action": row.action.upper(),
            "quantity": row.quantity,
            "price": row.price,
            "estimated_trade_value": row.estimated_trade_value,
            "currency": row.currency,
            "status": row.status,
            "trade_date": row.trade_date.date().isoformat() if row.trade_date else None,
            "settlement_date": row.settlement_date.date().isoformat() if row.settlement_date else None,
            "source_module": row.source_module,
            "cost_estimate": row.cost_estimate,
            "slippage_estimate": row.slippage_estimate,
            "suitability_status": row.suitability_status,
            "constraint_status": row.constraint_status,
            "risk_summary": from_json(row.risk_summary_json, {}),
            "review_history": from_json(row.review_history_json, []),
            "created_at": row.created_at.isoformat() if row.created_at else None,
            "updated_at": row.updated_at.isoformat() if row.updated_at else None,
            "reviewed_by": row.reviewed_by,
            "review_note": row.review_note,
            "athena_ai_commentary": from_json(row.athena_commentary_json, None),
        },
    )
    return payload


def _anomaly_model_from_payload(payload: dict[str, Any]) -> AnomalyRecordModel:
    detected_at = payload.get("detected_at")
    updated_at = payload.get("updated_at")
    return AnomalyRecordModel(
        anomaly_id=str(payload["anomaly_id"]),
        portfolio_id=payload.get("portfolio_id"),
        module_name=str(payload.get("module_name") or payload.get("source_module") or "unknown"),
        anomaly_type=str(payload.get("anomaly_type") or "rule_based"),
        category=str(payload.get("category") or "operational"),
        severity=str(payload.get("severity") or "low"),
        status=str(payload.get("status") or "open"),
        title=str(payload.get("title") or "Anomaly detected"),
        description=str(payload.get("description") or ""),
        metric_name=str(payload.get("metric_name") or "metric"),
        observed_value=value_to_text(payload.get("observed_value")),
        expected_value=value_to_text(payload.get("expected_value")) if payload.get("expected_value") is not None else None,
        threshold=value_to_text(payload.get("threshold")) if payload.get("threshold") is not None else None,
        z_score=float(payload["z_score"]) if payload.get("z_score") is not None else None,
        anomaly_score=float(payload.get("anomaly_score") or 0.0),
        confidence=str(payload.get("confidence") or "medium"),
        source_record_id=payload.get("source_record_id"),
        source_module=str(payload.get("source_module") or payload.get("module_name") or "unknown"),
        source_payload_json=to_json(payload.get("source_payload") or {}),
        suggested_action=str(payload.get("suggested_action") or "Review anomaly and source module records."),
        explanation=str(payload.get("explanation") or ""),
        review_history_json=to_json(payload.get("review_history") or []),
        generated_by=str(payload.get("generated_by") or "rule_based_detection"),
        detected_at=coerce_datetime(detected_at) if detected_at else datetime.now(UTC),
        updated_at=coerce_datetime(updated_at) if updated_at else datetime.now(UTC),
    )


def _anomaly_payload_from_model(row: AnomalyRecordModel) -> dict[str, Any]:
    return {
        "anomaly_id": row.anomaly_id,
        "portfolio_id": row.portfolio_id,
        "module_name": row.module_name,
        "anomaly_type": row.anomaly_type,
        "category": row.category,
        "severity": row.severity,
        "status": row.status,
        "title": row.title,
        "description": row.description,
        "metric_name": row.metric_name,
        "observed_value": text_to_value(row.observed_value),
        "expected_value": text_to_value(row.expected_value),
        "threshold": text_to_value(row.threshold),
        "z_score": row.z_score,
        "anomaly_score": row.anomaly_score,
        "confidence": row.confidence,
        "source_record_id": row.source_record_id,
        "source_module": row.source_module,
        "source_payload": from_json(row.source_payload_json, {}),
        "suggested_action": row.suggested_action,
        "explanation": row.explanation,
        "review_history": from_json(row.review_history_json, []),
        "generated_by": row.generated_by,
        "detected_at": row.detected_at.isoformat() if row.detected_at else None,
        "updated_at": row.updated_at.isoformat() if row.updated_at else None,
    }


def _stress_row(row: StressRunModel) -> dict[str, Any]:
    return {
        "run_id": row.run_id,
        "portfolio_id": row.portfolio_id,
        "portfolio_name": row.portfolio_name,
        "scenario_id": row.scenario_id,
        "scenario_name": row.scenario_name,
        "severity": row.severity,
        "estimated_loss": row.estimated_loss,
        "estimated_loss_percent": row.estimated_loss_percent,
        "generated_at": row.generated_at,
    }


def _clear_table(db: Session | None, model: type[BaseModel] | Any) -> None:
    try:
        with managed_session(db) as session:
            session.execute(delete(model))
            _commit(session)
    except SQLAlchemyError:
        if db is not None:
            _rollback(db)
