import os
from typing import List
from fastapi import APIRouter, HTTPException
from app.models.vocabulary_model import VocabularyModel
from app.services.vocabulary_service import VocabularyService
from common.response_message import Response
from app.config import constant

router = APIRouter()
vocabulary_service = VocabularyService()


class VocabularyRouter:

    @router.get("/{id}")
    async def get_vocabulary(id: int):
        result: VocabularyModel = vocabulary_service.find_vocabulary(id)
        # # if result.error is not None:
        # #     raise HTTPException(
        # #         status_code=result.error.status_code, detail=result.error.error
        # #     )
        # if result is None:
        #     raise HTTPException(
        #         status_code=404, detail=f"Vocabulary ID: {id} not found"
        #     )
        # # else:
        # #     return Response(status="success", data=result)
        # return Response(status="success", data=[result])
        return result
