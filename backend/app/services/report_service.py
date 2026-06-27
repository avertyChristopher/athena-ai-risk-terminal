from app.repositories.report_repository import ReportRepository
from app.schemas.report_schema import ReportModuleStatus


class ReportService:
    def __init__(self, repository: ReportRepository) -> None:
        self.repository = repository

    def get_module_status(self) -> ReportModuleStatus:
        return ReportModuleStatus(
            module="reports",
            status="ready",
            detail=(
                "Reports Center is active at /api/reports-center for snapshot-based "
                "portfolio, risk, stress, limits and trade reporting."
            ),
            formats=self.repository.list_report_formats(),
        )
