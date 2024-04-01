from sqlalchemy.orm import Session
from app.models import cms_models
from app.schemas import cms_schemas


def get_vocabulary_related_list(db: Session):
    return db.query(cms_models.VocabularyRelatedCms).all()


def get_vocabulary_related_list_filter_transfer_status(
    db: Session, transfer_status: int
):
    return (
        db.query(cms_models.VocabularyRelatedCms)
        .filter(cms_models.VocabularyRelatedCms.transfer_status == transfer_status)
        .all()
    )


def get_vocabulary_related_by_ids(
    db: Session, sentence_cms_id: str, vocabulary_cms_id: str
):
    return (
        db.query(cms_models.VocabularyRelatedCms)
        .filter_by(sentence_cms_id=sentence_cms_id, vocabulary_cms_id=vocabulary_cms_id)
        .first()
    )


def create_vocabulary_related(
    db: Session, vocabulary_related_data: cms_schemas.VocabularyRelatedCmsCreate
):
    db_vocabulary_related = cms_models.VocabularyRelatedCms(
        sentence_cms_id=vocabulary_related_data.sentence_cms_id,
        vocabulary_cms_id=vocabulary_related_data.vocabulary_cms_id,
    )
    db.add(db_vocabulary_related)
    db.commit()
    db.refresh(db_vocabulary_related)
    return db_vocabulary_related


def create_or_update_vocabulary_related(
    db: Session, vocabulary_related_data: cms_schemas.VocabularyRelatedCmsCreate
):
    if (
        vocabulary_related_data.sentence_cms_id
        and vocabulary_related_data.vocabulary_cms_id
    ):
        existing_vocabulary_related = get_vocabulary_related_by_ids(
            db,
            sentence_cms_id=vocabulary_related_data.sentence_cms_id,
            vocabulary_cms_id=vocabulary_related_data.vocabulary_cms_id,
        )
        if existing_vocabulary_related:
            for key, value in vocabulary_related_data.__dict__.items():
                setattr(existing_vocabulary_related, key, value)
            db.commit()
            db.refresh(existing_vocabulary_related)
            return existing_vocabulary_related
    return create_vocabulary_related(db, vocabulary_related_data)


def delete_vocabulary_related(
    db: Session, sentence_cms_id: str, vocabulary_cms_id: str
):
    vocabulary_related = get_vocabulary_related_by_ids(
        db, sentence_cms_id, vocabulary_cms_id
    )
    if vocabulary_related:
        db.delete(vocabulary_related)
        db.commit()
        return True
    return False
