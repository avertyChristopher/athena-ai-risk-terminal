from sqlalchemy.orm import Session


class AssetRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_assets(self) -> list[object]:
        return []
