from fastapi import APIRouter, HTTPException
from app.services.english_service import EnglishService
from app.config.resource import Config
from app.common.response import VocaverseResponse
from app.exceptions import errors
import http

router = APIRouter()
STATIC = Config.load_config()
english_service = EnglishService()


class EnglishRouter:

    @router.get("/translate", status_code=http.HTTPStatus.OK)
    async def translate(text: str):
        result = english_service.translate_en_to_th(text)
        try:
            english_service.is_alpha(text)
            result = await english_service.get_word_definitions(text)
        except errors.InputIsNotAlphabet as error:
            raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail=error)
        return VocaverseResponse(status={"message": STATIC.SUCCESS}, data=result)

    @router.get("/get-word-definitions", status_code=http.HTTPStatus.OK)
    async def get_definition(text: str):
        try:
            result = await english_service.get_word_definitions(text)
        except errors.InputIsNotAlphabet as error:
            raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail=error)
        return VocaverseResponse(status={"message": STATIC.SUCCESS}, data=result)

    @router.get("/get-dictionary-definitions", status_code=http.HTTPStatus.OK)
    async def get_dictionary_definitions(text: str):
        try:
            english_service.is_alpha(text)
            result = await english_service.get_dictionary_definitions(text)
            if result is None:
                raise HTTPException(
                    status_code=http.HTTPStatus.NOT_FOUND,
                    detail=errors.NotFound(f"{text} not found!"),
                )
        except errors.TemporarilySuspendService as error:
            raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail=error)
        return VocaverseResponse(status={"message": STATIC.SUCCESS}, data=result[0])
