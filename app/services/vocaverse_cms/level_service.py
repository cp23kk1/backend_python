from sqlalchemy.orm import Session, joinedload
from app.models import cms_models
from app.schemas import cms_schemas


def get_levels(db: Session):
    return (
        db.query(cms_models.LevelCms)
        .options(joinedload(cms_models.LevelCms.proficiency_standard))
        .all()
    )


def get_level_by_id(db: Session, level_id: int):
    return (
        db.query(cms_models.LevelCms).filter(cms_models.LevelCms.id == level_id).first()
    )


def get_level_by_name(db: Session, name: str):
    return (
        db.query(cms_models.LevelCms)
        .options(joinedload(cms_models.LevelCms.proficiency_standard))
        .filter(cms_models.LevelCms.name == name)
        .first()
    )


def create_level(db: Session, level_data: cms_schemas.LevelCmsCreate):
    db_level = cms_models.LevelCms(**level_data)
    db.add(db_level)
    db.commit()
    db.refresh(db_level)
    return db_level


def create_or_update_level(db: Session, level_data: cms_schemas.LevelCmsCreate):
    if level_data.id:
        existing_level = get_level_by_id(db, level_data.id)
        if existing_level:
            for key, value in level_data.__dict__.items():
                setattr(existing_level, key, value)
            db.commit()
            db.refresh(existing_level)
            return existing_level
    return create_level(db, level_data)


def delete_level(db: Session, level_id: int):
    level = get_level_by_id(db, level_id)
    if level:
        db.delete(level)
        db.commit()
        return True
    return False
