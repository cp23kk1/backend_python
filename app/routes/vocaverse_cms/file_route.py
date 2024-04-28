import http
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.common.response import VocaverseResponse
from app.config.database import get_cms_database_session
from app.services.vocaverse_cms import file_service

router = APIRouter()


class FileRouter:

    @router.get("")
    def read_files(db: Session = Depends(get_cms_database_session)):
        try:
            result = file_service.get_files(db)
        except Exception as error:
            raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail=error)
        return VocaverseResponse(data=result)

    @router.post("/upload", status_code=201)
    async def upload(
        category: str,
        file: UploadFile = File(...),
        db: Session = Depends(get_cms_database_session),
    ):
        try:
            result = await file_service.upload(db, category, file)
        except Exception as error:
            raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail=error)
        return VocaverseResponse(data=result)

    @router.post("/retrieve-data", status_code=201)
    def retrieve_data(
        file_id: int,
        db: Session = Depends(get_cms_database_session),
    ):
        try:
            result = file_service.retrieve_passage_from_csv(db, file_id)
        except Exception as error:
            raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail=error)
        return VocaverseResponse(data=result)

    @router.delete("/{file_id}")
    def retrieve_data(
        file_id: int,
        db: Session = Depends(get_cms_database_session),
    ):
        try:
            result = file_service.delete_file(db, file_id)
        except Exception as error:
            raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail=error)
        return VocaverseResponse(data=result)
