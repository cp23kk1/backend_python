from fastapi import APIRouter

from app.routes.vocabulary_app import vocabulary_route
from app.routes.vocaverse_cms import (
    file_route as file_cms_route,
    level_route as level_cms_routen,
    proficiency_standard_route as proficiency_standard_cms_route,
    passage_route as passage_cms_route,
    sentence_route as sentence_cms_route,
    vocabulary_route as vocabulary_cms_route,
    extra_info_route as extra_info_cms_route,
)
from app.routes import language_route, transfer_route

router = APIRouter()

# Include sub-routers
router.include_router(file_cms_route.router, tags=["file"], prefix="/file")
router.include_router(language_route.router, tags=["language"], prefix="/language")
router.include_router(
    passage_cms_route.router, tags=["passage-cms"], prefix="/passage-cms"
)
router.include_router(
    sentence_cms_route.router, tags=["sentence-cms"], prefix="/sentence-cms"
)
router.include_router(
    vocabulary_cms_route.router, tags=["vocabulary-cms"], prefix="/vocabulary-cms"
)
router.include_router(transfer_route.router, tags=["transfer"], prefix="/transfer")
router.include_router(
    vocabulary_route.router, tags=["vocabulary"], prefix="/vocabulary"
)
router.include_router(
    extra_info_cms_route.router, tags=["moreinfo"], prefix="/moreinfo"
)
router.include_router(
    proficiency_standard_cms_route.router,
    tags=["proficienc-standard"],
    prefix="/proficienc-standard",
)
router.include_router(level_cms_routen.router, tags=["level"], prefix="/level")
