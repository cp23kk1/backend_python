from fastapi import APIRouter

from app.routes import vocabulary_route

router = APIRouter()

# Include sub-routers
# router.include_router(
#     manipulation_router.router, tags=["manipulation"], prefix="/manipulation"
# )
# router.include_router(file_router.router, tags=["files"], prefix="/files")
# router.include_router(english_router.router, tags=["language"], prefix="/language")
router.include_router(
    vocabulary_route.router, tags=["vocabulary"], prefix="/vocabulary"
)
