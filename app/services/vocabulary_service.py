from app.repositories.vocabulary_repo import VocabularyRepo
from sqlalchemy.orm import Session

vocabulary_repo = VocabularyRepo()


class VocabularyService:

    def find_vocabulary_by_id(self, id: int, db: Session):
        return vocabulary_repo.get_vocabulary(id, db)
