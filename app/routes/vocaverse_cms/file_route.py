from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from app.config.database import get_cms_database_session
from app.models import cms_models
from app.schemas import cms_schemas
from app.services.vocaverse_cms import file_service

router = APIRouter()


class FileRouter:

    @router.get("", response_model=list[cms_schemas.FileCms])
    def read_files(db: Session = Depends(get_cms_database_session)):
        files = file_service.get_files(db)
        return files

    @router.post("/upload", status_code=201)
    async def upload(
        category: str,
        file: UploadFile = File(...),
        db: Session = Depends(get_cms_database_session),
    ):
        # try:
        #     result = await file_service.upload(file)
        # except Exception as error:
        #     raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail=error)
        # return VocaverseResponse(status={"message": STATIC.SUCCESS}, data=result)
        return await file_service.upload(db, category, file)

    @router.post("/retrieve-data", status_code=201)
    def retrieve_data(
        file_id: int,
        db: Session = Depends(get_cms_database_session),
    ):
        # try:
        #     result = await file_service.upload(file)
        # except Exception as error:
        #     raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail=error)
        # return VocaverseResponse(status={"message": STATIC.SUCCESS}, data=result)
        return file_service.retrieve_passage_from_csv(db, file_id)
