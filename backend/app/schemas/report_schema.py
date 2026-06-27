from app.schemas.common_schema import ModuleStatus


class ReportModuleStatus(ModuleStatus):
    formats: list[str] = ["json", "markdown", "csv"]
