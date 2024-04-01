from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_cms_database_session
from app.schemas import cms_schemas
from app.services.vocaverse_cms import vocabulary_cms_service

router = APIRouter()


class VocabularyRouter:

    @router.get("")
    def read_vocabularies(db: Session = Depends(get_cms_database_session)):
        return vocabulary_cms_service.get_vocabularies(db)

    @router.get("/{vocabulary_id}")
    def read_vocabulary(
        vocabulary_id: str, db: Session = Depends(get_cms_database_session)
    ):
        db_vocabulary = vocabulary_cms_service.get_vocabulary_by_id(db, vocabulary_id)
        if db_vocabulary is None:
            raise HTTPException(status_code=404, detail="Vocabulary not found")
        return db_vocabulary

    @router.post("")
    def create_vocabulary(
        vocabulary_data: cms_schemas.VocabularyCmsCreate,
        db: Session = Depends(get_cms_database_session),
    ):
        return vocabulary_cms_service.create_vocabulary(db, vocabulary_data)

    @router.put("/{vocabulary_id}")
    def update_vocabulary(
        vocabulary_id: str,
        vocabulary_data: cms_schemas.VocabularyCmsCreate,
        db: Session = Depends(get_cms_database_session),
    ):
        db_vocabulary = vocabulary_cms_service.create_or_update_vocabulary(
            db, vocabulary_data
        )
        if db_vocabulary is None:
            raise HTTPException(status_code=404, detail="Vocabulary not found")
        return db_vocabulary

    @router.delete("/{vocabulary_id}")
    def delete_vocabulary(
        vocabulary_id: str, db: Session = Depends(get_cms_database_session)
    ):
        if not vocabulary_cms_service.delete_vocabulary(db, vocabulary_id):
            raise HTTPException(status_code=404, detail="Vocabulary not found")
        return {"message": "Vocabulary deleted successfully"}
