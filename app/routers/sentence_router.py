import os
from typing import List
from fastapi import APIRouter, Depends
from app.config.database.models import Sentence
from app.config.database.mysql import get_database_session
from app.services.sentence_service import SentenceService
from app.common.response import Response, Error
from sqlalchemy.orm import Session
from app.config.resource import Config

router = APIRouter()
sentence_service = SentenceService()


class SentenceRouter:

    @router.get("/{id}")
    async def get_Sentence(id: int, db: Session = Depends(get_database_session)):

        result: Sentence = sentence_service.find_sentence_by_id(id, db)
        if result is None:
            return Response(
                status=Config.STATUS[0],
                error=Error(status_code=404, message=f"Sentence ID: {id} not found"),
            )
        return Response(status=Config.STATUS[1], data=[result])
