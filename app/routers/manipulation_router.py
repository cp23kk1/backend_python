import os
from typing import List
from fastapi import APIRouter
from app.services.manipulation_service import ManipulationService
from app.common.response import Response, Status, Result, convert_exception_to_error
from app.config.resource import Config

router = APIRouter()
config = Config.load_config()
manipulation_service = ManipulationService()


class Manipulation:

    @router.post("/extract-passage-from-csv/")
    async def extract_passage_from_csv(source_path: str):
        source_path = os.path.join(config.datasources_path, source_path)
        result = manipulation_service.separate_by_category(source_path)
        if not result.value:
            return Response(
                Status(
                    status=config.STATUS[0],
                    message={
                        str(result.value): f"Have computed this file!: {source_path}"
                    },
                ),
            )
        return Response(
            Status(
                status=config.STATUS[1],
                message={
                    str(result.value): f"Completely process the file: {source_path}"
                },
            )
        )

    @router.post("/import-data-from-csv/")
    async def import_data_from_csv(files_path: List[str]):
        result: Result = manipulation_service.import_data_from_csv(files_path)
        if not result.value:
            return Response(
                Status(status=config.STATUS[0]), convert_exception_to_error(result.err)
            )
        return Response(
            Status(status=config.STATUS[1]),
            data={str(result.value): f"Completely dump the file: {files_path}"},
        )
