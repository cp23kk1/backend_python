import http
from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from sqlalchemy.orm import Session
from app.common.response import VocaverseResponse
from app.config.database import get_cms_database_session
from app.schemas import cms_schemas
from app.services.vocaverse_cms import sentence_cms_service

router = APIRouter()


class SentenceRouter:

    @router.get("")
    def read_sentences(db: Session = Depends(get_cms_database_session)):
        try:
            result = sentence_cms_service.get_sentences(db)
        except Exception as error:
            raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail=error)
        return VocaverseResponse(data=result)

    @router.get("/with-children")
    def read_sentences_with_children(
        transfer_status: bool,
        db: Session = Depends(get_cms_database_session),
    ):
        try:
            result = sentence_cms_service.get_sentences_with_children(
                db, transfer_status
            )
        except Exception as error:
            raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail=error)
        return VocaverseResponse(data=result)

    @router.get("/{sentence_id}")
    def read_sentence(
        sentence_id: str, db: Session = Depends(get_cms_database_session)
    ):
        db_sentence = sentence_cms_service.get_sentence_by_id(db, sentence_id)
        if db_sentence is None:
            raise HTTPException(status_code=404, detail="Sentence not found")
        return db_sentence

    @router.post("")
    def create_sentence(
        sentence_data: cms_schemas.SentenceCmsCreate,
        db: Session = Depends(get_cms_database_session),
    ):
        return sentence_cms_service.create_sentence(db, sentence_data)

    @router.put("/{sentence_id}")
    def update_sentence(
        sentence_id: str,
        sentence_data: cms_schemas.SentenceCmsCreate,
        db: Session = Depends(get_cms_database_session),
    ):
        db_sentence = sentence_cms_service.create_or_update_sentence(db, sentence_data)
        if db_sentence is None:
            raise HTTPException(status_code=404, detail="Sentence not found")
        return db_sentence

    @router.delete("/{sentence_id}")
    def delete_sentence(
        sentence_id: str, db: Session = Depends(get_cms_database_session)
    ):
        if not sentence_cms_service.delete_sentence(db, sentence_id):
            raise HTTPException(status_code=404, detail="Sentence not found")
        return {"message": "Sentence deleted successfully"}
