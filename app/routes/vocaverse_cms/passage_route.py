from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_cms_database_session
from app.models import cms_models
from app.schemas import cms_schemas
from app.services.vocaverse_cms import passage_service

router = APIRouter()


class PassageRouter:

    @router.get("")
    def read_Passages(db: Session = Depends(get_cms_database_session)):
        passages = passage_service.get_passages(db)
        return passages

    @router.get("/{passage_id}")
    def read_passage_by_id(
        passage_id: str, db: Session = Depends(get_cms_database_session)
    ):
        passage = passage_service.get_passage_by_name(db, passage_id)
        return passage
