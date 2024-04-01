from sqlalchemy.orm import Session
from app.models import cms_models
from app.schemas import cms_schemas


def get_sentences(db: Session):
    return db.query(cms_models.SentenceCms).all()


def get_sentence_by_id(db: Session, sentence_id: str):
    return (
        db.query(cms_models.SentenceCms)
        .filter(cms_models.SentenceCms.id == sentence_id)
        .first()
    )


def create_sentence(db: Session, sentence_data: cms_schemas.SentenceCmsCreate):
    db_sentence = cms_models.SentenceCms(**sentence_data)
    db.add(db_sentence)
    db.commit()
    db.refresh(db_sentence)
    return db_sentence


def create_or_update_sentence(
    db: Session, sentence_data: cms_schemas.SentenceCmsCreate
):
    if sentence_data.id:
        existing_sentence = get_sentence_by_id(db, sentence_data.id)
        if existing_sentence:
            for key, value in sentence_data.__dict__.items():
                setattr(existing_sentence, key, value)
            db.commit()
            db.refresh(existing_sentence)
            return existing_sentence
    return create_sentence(db, sentence_data)


def delete_sentence(db: Session, sentence_id: str):
    sentence = get_sentence_by_id(db, sentence_id)
    if sentence:
        db.delete(sentence)
        db.commit()
        return True
    return False
