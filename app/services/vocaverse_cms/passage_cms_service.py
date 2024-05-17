from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload
from app.models import cms_models
from app.schemas import cms_schemas


def get_passages(db: Session):
    return db.query(cms_models.PassageCms).all()


def get_passages_with_children(db: Session, transfer_status: bool):
    return (
        db.query(cms_models.PassageCms)
        .options(
            joinedload(cms_models.PassageCms.sentences)
            .joinedload(cms_models.SentenceCms.vocabularies)
            .joinedload(cms_models.VocabularyRelatedCms.vocabulary)
        )
        .filter(cms_models.PassageCms.process_status == 1)
        .filter(cms_models.PassageCms.transfer_status == transfer_status)
        .all()
    )


def get_passages_filter_transfer_status(db: Session, transfer_status: int):
    return (
        db.query(cms_models.PassageCms)
        .filter(cms_models.PassageCms.transfer_status == transfer_status)
        .all()
    )


def get_passages_filter_process_status(db: Session, process_status: list[bool]):
    return (
        db.query(cms_models.PassageCms)
        .filter(
            or_(
                *(
                    cms_models.PassageCms.process_status == status
                    for status in process_status
                )
            )
        )
        .all()
    )


def get_passage_by_id(db: Session, passage_id: str):
    return (
        db.query(cms_models.PassageCms)
        .filter(cms_models.PassageCms.id == passage_id)
        .first()
    )


def create_passage(db: Session, passage_data: cms_schemas.PassageCmsCreate):
    db_passage = cms_models.PassageCms(**passage_data)
    db.add(db_passage)
    db.commit()
    db.refresh(db_passage)
    return db_passage


def create_or_update_passage(db: Session, passage_data: cms_schemas.PassageCmsCreate):
    # If the passage_id is provided, check if the passage exists in the database
    if passage_data.id:
        existing_passage = get_passage_by_id(db, passage_data.id)
        # If the passage exists, update it
        if existing_passage:
            for key, value in passage_data.__dict__.items():
                setattr(existing_passage, key, value)
            db.commit()
            db.refresh(existing_passage)
            return existing_passage
    # If the passage_id is not provided or if the passage does not exist, create a new passage
    return create_passage(db, passage_data)


def delete_passage(db: Session, passage_id: str):
    passage = get_passage_by_id(db, passage_id)
    if passage:
        db.delete(passage)
        db.commit()
        return True
    return False
