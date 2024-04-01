from sqlalchemy.orm import Session
from app.models import cms_models
from app.schemas import cms_schemas


def get_vocabularies(db: Session):
    return db.query(cms_models.VocabularyCms).all()


def get_vocabularies_filter_transfer_status(db: Session, transfer_status: int):
    return (
        db.query(cms_models.VocabularyCms)
        .filter(cms_models.VocabularyCms.transfer_status == transfer_status)
        .all()
    )


def get_vocabularies_filter_process_status(db: Session, process_status: int):
    return (
        db.query(cms_models.VocabularyCms)
        .filter(cms_models.VocabularyCms.process_status == process_status)
        .all()
    )


def get_vocabulary_by_id(db: Session, vocabulary_id: str):
    return (
        db.query(cms_models.VocabularyCms)
        .filter(cms_models.VocabularyCms.id == vocabulary_id)
        .first()
    )


def get_vocabulary_by_text(db: Session, vocabulary_text: str):
    return (
        db.query(cms_models.VocabularyCms)
        .filter(cms_models.VocabularyCms.text == vocabulary_text)
        .first()
    )


def create_vocabulary(db: Session, vocabulary_data: cms_schemas.VocabularyCmsCreate):
    db_vocabulary = cms_models.VocabularyCms(**vocabulary_data)
    db.add(db_vocabulary)
    db.commit()
    db.refresh(db_vocabulary)
    return db_vocabulary


def create_or_update_vocabulary(
    db: Session, vocabulary_data: cms_schemas.VocabularyCmsCreate
):
    if vocabulary_data.id:
        existing_vocabulary = get_vocabulary_by_id(db, vocabulary_data.id)
        if existing_vocabulary:
            for key, value in vocabulary_data.__dict__.items():
                setattr(existing_vocabulary, key, value)
            db.commit()
            db.refresh(existing_vocabulary)
            return existing_vocabulary
    return create_vocabulary(db, vocabulary_data)


def delete_vocabulary(db: Session, vocabulary_id: str):
    vocabulary = get_vocabulary_by_id(db, vocabulary_id)
    if vocabulary:
        db.delete(vocabulary)
        db.commit()
        return True
    return False
