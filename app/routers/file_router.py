from fastapi import Depends, File, UploadFile, APIRouter
from typing import List
from app.services.file_service import FileService

router = APIRouter()

fileService = FileService()


class FileRouter:

    @router.get("/list-file/")
    async def list_file():
        return fileService.list_file()

    @router.post("/upload/")
    async def upload(file: UploadFile = File(...)):
        return await fileService.upload(file)

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
