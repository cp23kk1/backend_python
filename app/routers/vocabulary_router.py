import os
from typing import List
from fastapi import APIRouter, Depends
from app.config.database.models import Vocabulary
from app.config.database.mysql import get_database_session
from app.services.vocabulary_service import VocabularyService
from app.common.response import Response, Error
from sqlalchemy.orm import Session
from app.config.resource import Config

router = APIRouter()
vocabulary_service = VocabularyService()


class VocabularyRouter:

    @router.get("/{id}")
    async def get_vocabulary(id: int, db: Session = Depends(get_database_session)):
        result: Vocabulary = vocabulary_service.find_vocabulary_by_id(id, db)
        if result is None:
            return Response(
                status=Config.STATUS[0],
                error=Error(status_code=404, message=f"Vocabulary ID: {id} not found"),
            )
        return Response(status=Config.STATUS[1], data=List(result))
