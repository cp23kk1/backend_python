from fastapi import File, UploadFile, APIRouter
from app.common.response import Response, Error
from app.config.resource import Config
from app.services.file_service import FileService

router = APIRouter()

file_service = FileService()


class FileRouter:

    @router.get("/list-file/")
    async def list_file():
        return file_service.list_file()

    @router.post("/upload/")
    async def upload(file: UploadFile = File(...)):
        result: str = await file_service.upload(file)
        if result == "":
            return Response(
                status=Config.STATUS[0],
                error=Error(
                    status_code=400, message=f"File: {file.filename} unsuccessfully uploaded!"
                ),
            )
        return Response(
            status=Config.STATUS[1],
            data={"message": f"File: {file.filename} successfully uploaded!"}
        )

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
