from app.repositories.sentence_repo import SentenceRepo
from sqlalchemy.orm import Session

sentence_repo = SentenceRepo()


class SentenceService:

    def find_sentence_by_id(self, id: int, db: Session):
        return sentence_repo.get_sentence(id, db)
