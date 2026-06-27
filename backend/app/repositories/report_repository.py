from sqlalchemy.orm import Session


class ReportRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_report_formats(self) -> list[str]:
        return ["json", "markdown", "csv"]
