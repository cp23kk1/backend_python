from sqlalchemy.orm import Session
from app.models.vocabulary_model import VocabularyModel
from app.config.database.mysql import SessionLocal


class VocabularyRepo:

    def read(self, id: int, db: Session = SessionLocal()):
        return db.query(VocabularyModel).filter(VocabularyModel.id == id).first()
