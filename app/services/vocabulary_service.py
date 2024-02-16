from app.repositories.vocabulary_repo import VocabularyRepo

vocabulary_repo = VocabularyRepo()


class VocabularyService:

    def find_vocabulary(self, id: int):
        return vocabulary_repo.read(id)
