import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from pydantic import BaseModel
from app.services.extract_service import ExtractService
from common.response_message import Response
from app.config import constant

router = APIRouter()
extract_service = ExtractService()


class Extraction:

    @router.get("/text-from-csv/")
    async def extract_text_from_csv(source_path: str):
        source_path = os.path.join(constant.datasources_path, source_path)
        result = extract_service.separate_by_category(source_path)
        print(result)
        # if result.error is not None:
        #     raise HTTPException(
        #         status_code=result.error.status_code, detail=result.error.error
        #     )
        # else:
        #     return Response(status="success", data={})
        return os.path.abspath(source_path)
