import os
from typing import List
from fastapi import APIRouter
from app.services.manipulation_service import ManipulationService
from app.common.response import Response, Error
from app.config.resource import Config

router = APIRouter()
config = Config.load_config()
manipulation_service = ManipulationService()


class Manipulation:

    @router.post("/extract-text-from-csv/")
    async def extract_text_from_csv(source_path: str):
        source_path = os.path.join(config.datasources_path, source_path)
        if not os.path.exists(source_path):
            return Response(
                status=config.STATUS[0],
                error=Error(
                    status_code=404, message=f"File: {source_path} does not exist!"
                ),
            )
        result = manipulation_service.separate_by_category(source_path)
        if not result:
            return Response(
                status=config.STATUS[0],
                error=Error(
                    status_code=400, message=f"Have computed this file!: {source_path}"
                ),
            )
        return Response(
            status="success", data=f"Completely process the file: {source_path}"
        )

    @router.post("/extract-text-from-csv/")
    async def import_data_from_csv(files_path: List[str]):
        return ""
        # if not result:
        #     return Response(
        #         status=Config.STATUS[0],
        #         error=Error(
        #             status_code=400, message=f"Have computed this file!: {source_path}"
        #         ),
        #     )
        # return Response(
        #     status="success", data=f"Completely process the file: {source_path}"
        # )
