import http
from fastapi import APIRouter, HTTPException, Depends
from app.config.resource import Config
from app.common.response import VocaverseResponse
from app.exceptions import errors
from sqlalchemy.orm import Session
from app.config.database import get_cms_database_session, get_app_database_session
from app.services import transfer_service

router = APIRouter()

class LanguageRouter:

    @router.post("/passage_transfer", status_code=http.HTTPStatus.OK)
    def passage_transfer(
        cms_db: Session = Depends(get_cms_database_session),
        app_db: Session = Depends(get_app_database_session),
    ):
        return transfer_service.transfer_passage_data(cms_db=cms_db, app_db=app_db)

    @router.post("/sentence_transfer", status_code=http.HTTPStatus.OK)
    def sentence_transfer(
        cms_db: Session = Depends(get_cms_database_session),
        app_db: Session = Depends(get_app_database_session),
    ):
        return transfer_service.transfer_sentence_data(cms_db=cms_db, app_db=app_db)

    @router.post("/vocabulary_transfer", status_code=http.HTTPStatus.OK)
    def vocabulary_transfer(
        cms_db: Session = Depends(get_cms_database_session),
        app_db: Session = Depends(get_app_database_session),
    ):
        return transfer_service.transfer_vocabulary_data(cms_db=cms_db, app_db=app_db)

    @router.post("/vocabulary_related_transfer", status_code=http.HTTPStatus.OK)
    def vocabulary_related_transfer(
        cms_db: Session = Depends(get_cms_database_session),
        app_db: Session = Depends(get_app_database_session),
    ):
        return transfer_service.transfer_vocabulary_related_data(
            cms_db=cms_db, app_db=app_db
        )

    @router.post("/transfer_all", status_code=http.HTTPStatus.OK)
    def vocabulary_related_transfer(
        cms_db: Session = Depends(get_cms_database_session),
        app_db: Session = Depends(get_app_database_session),
    ):
        transfer_service.transfer_passage_data(cms_db=cms_db, app_db=app_db)
        transfer_service.transfer_sentence_data(cms_db=cms_db, app_db=app_db)
        transfer_service.transfer_vocabulary_data(cms_db=cms_db, app_db=app_db)
        transfer_service.transfer_vocabulary_related_data(cms_db=cms_db, app_db=app_db)

        return True
