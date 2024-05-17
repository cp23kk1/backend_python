from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_cms_database_session
from app.models import cms_models
from app.schemas import cms_schemas
from app.services.vocaverse_cms import extra_info_service

router = APIRouter()


class ExtraInformationRouter:

    @router.get("/{vocab_id}")
    def read_extra_info_by_vocab_id(vocab_id: str, db: Session = Depends(get_cms_database_session)):
        extra_info = extra_info_service.load_extra_information(db, vocab_id)
        return extra_info
