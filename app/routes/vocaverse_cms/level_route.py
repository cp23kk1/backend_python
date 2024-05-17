from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_cms_database_session
from app.models import cms_models
from app.schemas import cms_schemas
from app.services.vocaverse_cms import level_service

router = APIRouter()


class LevelRouter:

    @router.get("")
    def read_levels(db: Session = Depends(get_cms_database_session)):
        levels = level_service.get_levels(db)
        return levels

    @router.get("/{name}")
    def read_level_by_name(name: str, db: Session = Depends(get_cms_database_session)):
        level = level_service.get_level_by_name(db, name)
        return level
