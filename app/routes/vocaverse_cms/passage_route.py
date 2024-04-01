from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_cms_database_session
from app.schemas import cms_schemas
from app.services.vocaverse_cms import passage_cms_service

router = APIRouter()


class PassageRouter:

    @router.get("")
    def read_passages(db: Session = Depends(get_cms_database_session)):
        return passage_cms_service.get_passages(db)

    @router.get("/{passage_id}")
    def read_passage(passage_id: str, db: Session = Depends(get_cms_database_session)):
        db_passage = passage_cms_service.get_passage_by_id(db, passage_id)
        if db_passage is None:
            raise HTTPException(status_code=404, detail="Passage not found")
        return db_passage

    @router.post("")
    def create_passage(
        passage_data: cms_schemas.PassageCmsCreate,
        db: Session = Depends(get_cms_database_session),
    ):
        return passage_cms_service.create_passage(db, passage_data)

    @router.put("/{passage_id}")
    def update_passage(
        passage_id: str,
        passage_data: cms_schemas.PassageCmsCreate,
        db: Session = Depends(get_cms_database_session),
    ):
        db_passage = passage_cms_service.create_or_update_passage(db, passage_data)
        if db_passage is None:
            raise HTTPException(status_code=404, detail="Passage not found")
        return db_passage

    @router.delete("/{passage_id}")
    def delete_passage(
        passage_id: str, db: Session = Depends(get_cms_database_session)
    ):
        if not passage_cms_service.delete_passage(db, passage_id):
            raise HTTPException(status_code=404, detail="Passage not found")
        return {"message": "Passage deleted successfully"}
