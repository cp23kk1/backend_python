from app.repositories.passage_repo import PassageRepo
from sqlalchemy.orm import Session

passage_repo = PassageRepo()


class PassageService:

    def find_vocabulary_by_id(self, id: int, db: Session):
        return passage_repo.get_passage(id, db)
