from __future__ import annotations

from app.modules.reports_center.schemas import GeneratedReport


class ReportsCenterRepository:
    _reports: dict[str, GeneratedReport] = {}

    def save_report(self, report: GeneratedReport) -> GeneratedReport:
        self._reports[report.report_id] = report
        return report

    def list_reports(self) -> list[GeneratedReport]:
        return sorted(
            self._reports.values(),
            key=lambda report: report.generated_at,
            reverse=True,
        )

    def get_report(self, report_id: str) -> GeneratedReport | None:
        return self._reports.get(report_id)

    def delete_report(self, report_id: str) -> bool:
        return self._reports.pop(report_id, None) is not None

    def clear(self) -> None:
        self._reports.clear()
