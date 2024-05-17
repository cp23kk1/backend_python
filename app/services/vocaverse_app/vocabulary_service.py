from sqlalchemy.orm import Session
from app.models import app_models
from app.schemas import app_schemas


def get_vocabularies(db: Session):
    return db.query(app_models.Vocabulary).all()


def get_vocabulary_by_id(db: Session, vocabulary_id: str):
    return (
        db.query(app_models.Vocabulary)
        .filter(app_models.Vocabulary.id == vocabulary_id)
        .first()
    )


def create_vocabulary(db: Session, vocabulary_data: app_schemas.VocabularyCreate):
    db_vocabulary = app_models.Vocabulary(**vocabulary_data)
    db.add(db_vocabulary)
    db.commit()
    db.refresh(db_vocabulary)
    return db_vocabulary


def create_or_update_vocabulary(
    db: Session, vocabulary_data: app_schemas.VocabularyCreate
):
    # If the vocabulary_id is provided, check if the vocabulary exists in the database
    if vocabulary_data.id:
        existing_vocabulary = get_vocabulary_by_id(db, vocabulary_data.id)
        # If the vocabulary exists, update it
        if existing_vocabulary:
            for key, value in vocabulary_data.__dict__.items():
                setattr(existing_vocabulary, key, value)
            db.commit()
            db.refresh(existing_vocabulary)
            return existing_vocabulary
    # If the vocabulary_id is not provided or if the vocabulary does not exist, create a new vocabulary
    return create_vocabulary(db, vocabulary_data)


def delete_vocabulary(db: Session, vocabulary_id: str):
    vocabulary = get_vocabulary_by_id(db, vocabulary_id)
    if vocabulary:
        db.delete(vocabulary)
        db.commit()
        return True
    return False
