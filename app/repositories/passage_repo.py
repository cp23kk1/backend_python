from sqlalchemy.orm import Session
from app.config.database.models import Passage


class PassageRepo:

    def get_passage(self, id: int, db: Session):
        return db.query(Passage).filter(Passage.id == id).first()