from sqlalchemy.orm import Session
from app.models import app_models
from app.schemas import app_schemas


def get_vocabularies(db: Session):
    return db.query(app_models.Vocabulary).all()