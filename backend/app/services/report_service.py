from app.repositories.report_repository import ReportRepository
from app.schemas.report_schema import ReportModuleStatus


class ReportService:
    def __init__(self, repository: ReportRepository) -> None:
        self.repository = repository

    def get_module_status(self) -> ReportModuleStatus:
        return ReportModuleStatus(
            module="reports",
            detail="Report generation endpoints are scaffolded. PDF and CSV generation will be added later.",
            formats=self.repository.list_report_formats(),
        )
