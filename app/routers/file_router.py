from fastapi import File, UploadFile, APIRouter
from app.common.response import Response, Status, Result, convert_exception_to_error
from app.config.resource import Config
from app.services.file_service import FileService

router = APIRouter()

config = Config.load_config()
file_service = FileService()


class FileRouter:

    @router.get("/list-file/")
    async def list_file():
        return file_service.list_file()

    @router.post("/upload/")
    async def upload(file: UploadFile = File(...)):
        result: Result = await file_service.upload(file)
        return result
        # if not result.value:
        #     return Response(
        #         Status(
        #             status=config.STATUS[0],
        #             message=convert_exception_to_error(result.err),
        #         ),
        #         data={},
        #     )
        # return Response(
        #     Status(status=config.STATUS[1]),
        #     data=f"File: {file.filename} successfully uploaded!",
        # )

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
