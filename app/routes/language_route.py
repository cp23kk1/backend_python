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

    @router.get("/translate", status_code=http.HTTPStatus.OK)
    def translate(text: str):
        try:
            language_service.is_alpha(text)
            result = language_service.translate_en_to_th(text)
        except errors.InputIsNotAlphabet as error:
            raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail=error)
        return VocaverseResponse(status={"message": STATIC.SUCCESS}, data=result)

    @router.get("/get-word-definitions", status_code=http.HTTPStatus.OK)
    def get_definition(text: str):
        try:
            result = language_service.get_word_definitions(text)
        except errors.InputIsNotAlphabet as error:
            raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail=error)
        return VocaverseResponse(status={"message": STATIC.SUCCESS}, data=result)

    @router.get("/get-dictionary-definitions", status_code=http.HTTPStatus.OK)
    def get_dictionary_definitions(text: str):
        try:
            language_service.is_alpha(text)
            result = language_service.get_dictionary_definitions(text)
            if result is None:
                raise HTTPException(
                    status_code=http.HTTPStatus.NOT_FOUND,
                    detail=errors.NotFound(f"{text} not found!"),
                )
        except errors.TemporarilySuspendService as error:
            raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail=error)
        return VocaverseResponse(status={"message": STATIC.SUCCESS}, data=result[0])

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
