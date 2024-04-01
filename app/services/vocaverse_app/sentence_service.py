from sqlalchemy.orm import Session
from app.models import app_models
from app.schemas import app_schemas


def get_sentences(db: Session):
    return db.query(app_models.Sentence).all()


def get_sentence_by_id(db: Session, sentence_id: str):
    return (
        db.query(app_models.Sentence)
        .filter(app_models.Sentence.id == sentence_id)
        .first()
    )


def create_sentence(db: Session, sentence_data: app_schemas.SentenceCreate):
    db_sentence = app_models.Sentence(**sentence_data)
    db.add(db_sentence)
    db.commit()
    db.refresh(db_sentence)
    return db_sentence


def create_or_update_sentence(db: Session, sentence_data: app_schemas.SentenceCreate):
    # If the sentence_id is provided, check if the sentence exists in the database
    if sentence_data.id:
        existing_sentence = get_sentence_by_id(db, sentence_data.id)
        # If the sentence exists, update it
        if existing_sentence:
            for key, value in sentence_data.__dict__.items():
                setattr(existing_sentence, key, value)
            db.commit()
            db.refresh(existing_sentence)
            return existing_sentence
    # If the sentence_id is not provided or if the sentence does not exist, create a new sentence
    return create_sentence(db, sentence_data)


def delete_sentence(db: Session, sentence_id: str):
    sentence = get_sentence_by_id(db, sentence_id)
    if sentence:
        db.delete(sentence)
        db.commit()
        return True
    return False
