from sqlalchemy.orm import Session


class PnlRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def attribution_enabled(self) -> bool:
        return False
