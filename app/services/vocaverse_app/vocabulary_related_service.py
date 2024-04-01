from sqlalchemy.orm import Session
from app.models import app_models
from app.schemas import app_schemas


def get_vocabulary_related(db: Session):
    return db.query(app_models.VocabularyRelated).all()


def get_vocabulary_related_by_ids(db: Session, sentence_id: str, vocabulary_id: str):
    return (
        db.query(app_models.VocabularyRelated)
        .filter_by(sentence_id=sentence_id, vocabulary_id=vocabulary_id)
        .first()
    )


def create_vocabulary_related(
    db: Session, vocabulary_related_data: app_schemas.VocabularyRelatedCreate
):
    db_vocabulary_related = app_models.VocabularyRelated(
        sentence_id=vocabulary_related_data.sentence_id,
        vocabulary_id=vocabulary_related_data.vocabulary_id,
    )
    db.add(db_vocabulary_related)
    db.commit()
    db.refresh(db_vocabulary_related)
    return db_vocabulary_related


def delete_vocabulary_related(db: Session, sentence_id: str, vocabulary_id: str):
    vocabulary_related = get_vocabulary_related_by_ids(db, sentence_id, vocabulary_id)
    if vocabulary_related:
        db.delete(vocabulary_related)
        db.commit()
        return True
    return False
