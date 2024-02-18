from fastapi import APIRouter

from app.routers import file_router, manipulation_router

router = APIRouter()

# Include sub-routers
router.include_router(
    manipulation_router.router, tags=["manipulation"], prefix="/manipulation"
)
router.include_router(file_router.router, tags=["files"], prefix="/files")
