from sqlalchemy.orm import Session


class RiskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_available_metrics(self) -> list[str]:
        return []
