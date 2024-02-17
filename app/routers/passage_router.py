import os
from typing import List
from fastapi import APIRouter, Depends
from app.config.database.models import Passage
from app.config.database.mysql import get_database_session
from app.services.passage_service import PassageService
from app.common.response import Response, Error
from sqlalchemy.orm import Session
from app.config.resource import Config

router = APIRouter()
passage_service = PassageService()


class PassageRouter:

    @router.get("/{id}")
    async def get_Passage(id: int, db: Session = Depends(get_database_session)):

        result: Passage = passage_service.find_vocabulary_by_id(id, db)
        if result is None:
            return Response(
                status=Config.STATUS[0],
                error=Error(status_code=404, message=f"Passage ID: {id} not found"),
            )
        return Response(status=Config.STATUS[1], data=[result])
