from fastapi import APIRouter

from app.routers import extract_router, file_router, vocabulary_router

router = APIRouter()
router.include_router(extract_router.router, tags=["extraction"], prefix="/extract")
router.include_router(file_router.router, tags=["files"], prefix="/files")
router.include_router(
    vocabulary_router.router, tags=["vocabularies"], prefix="/vocabularies"
)
