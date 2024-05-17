from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_app_database_session
from app.models import app_models
from app.schemas import app_schemas
from app.services.vocaverse_app import vocabulary_service

router = APIRouter()


class VocabularyRouter:

    @router.get("", response_model=list[app_schemas.Vocabulary])
    def read_vocabularies(db: Session = Depends(get_app_database_session)):
        vocabularies = vocabulary_service.get_vocabularies(db)
        return vocabularies
