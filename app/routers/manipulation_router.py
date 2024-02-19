from fastapi import APIRouter, HTTPException
from app.services.manipulation_service import ManipulationService
from app.common.response import VocaverseResponse
from app.config.resource import Config
from app.exceptions import errors
import http

router = APIRouter()
STATIC = Config.load_config()
manipulation_service = ManipulationService()


class ManipulationRouter:

    @router.post("/extract-passage-from-csv", status_code=http.HTTPStatus.OK)
    async def extract_passage_from_csv(source_path: str):
        # source_path = os.path.join(config.datasources_path, source_path)
        result = manipulation_service.separate_by_category(source_path)
        # if not result.value:
        #     return Response(
        #         ResponseStatus(
        #             status=config.STATUS[0],
        #             message={
        #                 str(result.value): f"Have computed this file!: {source_path}"
        #             },
        #         ),
        #     )
        # return Response(
        #     ResponseStatus(
        #         status=config.STATUS[1],
        #         message={
        #             str(result.value): f"Completely process the file: {source_path}"
        #         },
        #     )
        # )
        return result

    @router.post("/import-data-from-csv", status_code=http.HTTPStatus.OK)
    async def import_data_from_csv(files_path: list[str]):
        try:
            result = manipulation_service.import_data_from_csv(files_path)
        except errors.TemporarilySuspendService as error:
            raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail=error)
        return VocaverseResponse(
            status={"message": STATIC.SUCCESS},
            data={"message": f"Completely dump the file: {files_path}"},
        )
