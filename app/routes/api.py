from fastapi import APIRouter

from app.routes.vocabulary_app import vocabulary_route
from app.routes.vocaverse_cms import (
    file_route,
    level_route,
    proficiency_standard_route,
    passage_route,
    extra_info_route,
)
from app.routes import language_route, transfer_route

router = APIRouter()

# Include sub-routers
router.include_router(file_route.router, tags=["file"], prefix="/file")
router.include_router(language_route.router, tags=["language"], prefix="/language")
router.include_router(passage_route.router, tags=["passage"], prefix="/passage")
router.include_router(transfer_route.router, tags=["transfer"], prefix="/transfer")
router.include_router(
    vocabulary_route.router, tags=["vocabulary"], prefix="/vocabulary"
)
router.include_router(extra_info_route.router, tags=["moreinfo"], prefix="/moreinfo")
router.include_router(
    proficiency_standard_route.router,
    tags=["proficienc-standard"],
    prefix="/proficienc-standard",
)
router.include_router(level_route.router, tags=["level"], prefix="/level")
