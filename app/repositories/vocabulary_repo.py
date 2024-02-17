from sqlalchemy.orm import Session
from app.config.database.models import Vocabulary


class VocabularyRepo:

    def get_vocabulary(self, id: int, db: Session):
        return db.query(Vocabulary).filter(Vocabulary.id == id).first()