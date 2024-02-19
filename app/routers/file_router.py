from fastapi import File, UploadFile, APIRouter, HTTPException
from app.common.response import VocaverseResponse
from app.config.resource import Config
from app.services.file_service import FileService
import http

router = APIRouter()
STATIC = Config.load_config()
file_service = FileService()


class FileRouter:

    @router.get("/list-file", status_code=http.HTTPStatus.OK)
    async def list_file():
        return file_service.list_file()

    @router.post("/upload", status_code=201)
    async def upload(file: UploadFile = File(...)):
        try:
            result = await file_service.upload(file)
        except Exception as error:
            raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail=error)
        return VocaverseResponse(status={"message": STATIC.SUCCESS}, data=result)

    # @router.post("/")
    # async def up_img(file: UploadFile = File(...)):
    #     size = await file.read()
    #     return {"File Name": file.filename, "size": len(size)}

    # @router.post("/multi")
    # async def up_multi_file(files: List[UploadFile] = File(...)):
    #     file = [
    #         {"File Name": file.filename, "Size": len(await file.read())}
    #         for file in files
    #     ]
    #     return file
