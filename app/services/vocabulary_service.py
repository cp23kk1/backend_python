from sqlalchemy.orm import Session

from app.models import app_models
from app.schemas import app_schemas


def get_vocabulary(db: Session, vocab_id: str):
    return (
        db.query(app_models.Vocabulary)
        .filter(app_models.Vocabulary.id == vocab_id)
        .first()
    )
