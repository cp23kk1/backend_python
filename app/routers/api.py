from fastapi import APIRouter

from app.routers import file_router, manipulation_router, passage_router, sentence_router, vocabulary_router

router = APIRouter()

# Include sub-routers
router.include_router(
    manipulation_router.router, tags=["manipulation"], prefix="/manipulation"
)
router.include_router(file_router.router, tags=["files"], prefix="/files")
router.include_router(
    passage_router.router, tags=["passages"], prefix="/passages"
)
router.include_router(
    sentence_router.router, tags=["sentences"], prefix="/sentences"
)
router.include_router(
    vocabulary_router.router, tags=["vocabularies"], prefix="/vocabularies"
)
