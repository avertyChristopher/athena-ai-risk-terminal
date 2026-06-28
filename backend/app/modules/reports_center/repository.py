from __future__ import annotations

from sqlalchemy.orm import Session

from app.modules.reports_center.schemas import GeneratedReport
from app.persistence.repositories import ReportPersistenceRepository


class ReportsCenterRepository:
    _reports: dict[str, GeneratedReport] = {}

    def __init__(self, db: Session | None = None) -> None:
        self.db = db
        self.persistence = ReportPersistenceRepository(db)

    def save_report(self, report: GeneratedReport) -> GeneratedReport:
        self._reports[report.report_id] = report
        self.persistence.save(report)
        return report

    def list_reports(self) -> list[GeneratedReport]:
        persisted = self.persistence.list()
        if persisted:
            return persisted
        return sorted(
            self._reports.values(),
            key=lambda report: report.generated_at,
            reverse=True,
        )

    def get_report(self, report_id: str) -> GeneratedReport | None:
        return self.persistence.get(report_id) or self._reports.get(report_id)

    def delete_report(self, report_id: str) -> bool:
        deleted_from_memory = self._reports.pop(report_id, None) is not None
        return self.persistence.delete(report_id) or deleted_from_memory

    def clear(self) -> None:
        self._reports.clear()
        self.persistence.clear()
