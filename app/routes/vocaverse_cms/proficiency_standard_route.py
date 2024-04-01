from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_cms_database_session
from app.models import cms_models
from app.schemas import cms_schemas
from app.services.vocaverse_cms import proficiency_standard_service

router = APIRouter()


class ProficiencStandardRouter:

    @router.get("")
    def read_proficienc_standards(db: Session = Depends(get_cms_database_session)):
        proficienc_standards = proficiency_standard_service.get_proficiency_standards(
            db
        )
        return proficienc_standards
