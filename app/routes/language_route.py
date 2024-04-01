import http
from fastapi import APIRouter, HTTPException, Depends
from app.services import language_service
from app.config.resource import Config
from app.common.response import VocaverseResponse
from app.exceptions import errors
from sqlalchemy.orm import Session
from app.config.database import get_cms_database_session

router = APIRouter()
STATIC = Config.load_config()


class LanguageRouter:

    @router.post("/passage_processing", status_code=http.HTTPStatus.OK)
    def passage_processing(
        passages: list[str], db: Session = Depends(get_cms_database_session)
    ):
        return language_service.passage_processing(db, passages)

    @router.post("/sentence_processing", status_code=http.HTTPStatus.OK)
    def sentence_processing(
        sentences: list[str], db: Session = Depends(get_cms_database_session)
    ):
        return language_service.sentence_processing(db, sentences)

    @router.post("/vocabulary_processing", status_code=http.HTTPStatus.OK)
    def vocabulary_processing(
        vocabularies: list[str], db: Session = Depends(get_cms_database_session)
    ):
        return language_service.vocabulary_processing(db, vocabularies)
