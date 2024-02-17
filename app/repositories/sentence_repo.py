from sqlalchemy.orm import Session
from app.config.database.models import Sentence


class SentenceRepo:

    def get_sentence(self, id: int, db: Session):
        return db.query(Sentence).filter(Sentence.id == id).first()