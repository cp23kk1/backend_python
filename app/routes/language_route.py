import http
from fastapi import APIRouter, HTTPException, Depends
from app.services import language_service
from app.config.resource import Config
from app.common.response import VocaverseResponse
from app.exceptions import errors
from sqlalchemy.orm import Session
from app.config.database import get_cms_database_session

router = APIRouter()


class LanguageRouter:

    @router.post("/passage-processing", status_code=http.HTTPStatus.OK)
    def passage_processing(
        passages: list[str], db: Session = Depends(get_cms_database_session)
    ):
        try:
            result = language_service.passage_processing(db, passages)
        except Exception as error:
            raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail=error)
        return VocaverseResponse(data=result)

    @router.post("/sentence-processing", status_code=http.HTTPStatus.OK)
    def sentence_processing(
        sentences: list[str], db: Session = Depends(get_cms_database_session)
    ):
        try:
            result = language_service.sentence_processing(db, sentences)
        except Exception as error:
            raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail=error)
        return VocaverseResponse(data=result)

    @router.post("/vocabulary-processing", status_code=http.HTTPStatus.OK)
    def vocabulary_processing(
        vocabularies: list[str], db: Session = Depends(get_cms_database_session)
    ):
        try:
            result = language_service.vocabulary_processing(db, vocabularies)
        except Exception as error:
            raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail=error)
        return VocaverseResponse(data=result)

    @router.post("/processing", status_code=http.HTTPStatus.OK)
    def processing(category: str, db: Session = Depends(get_cms_database_session)):
        try:
            result = language_service.processing(db, category)
        except Exception as error:
            raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail=error)
        return VocaverseResponse(data=result)
