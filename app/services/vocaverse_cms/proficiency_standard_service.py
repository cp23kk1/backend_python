from sqlalchemy.orm import Session, joinedload
from app.models import cms_models
from app.schemas import cms_schemas


def get_proficiency_standards(db: Session):
    return (
        db.query(cms_models.ProficiencyStandardCms)
        .options(joinedload(cms_models.ProficiencyStandardCms.levels))
        .all()
    )


def get_proficiency_standard_by_id(db: Session, proficiency_standard_id: int):
    return (
        db.query(cms_models.ProficiencyStandardCms)
        .filter(cms_models.ProficiencyStandardCms.id == proficiency_standard_id)
        .first()
    )


def create_proficiency_standard(
    db: Session, proficiency_standard_data: cms_schemas.ProficiencyStandardCmsCreate
):
    db_proficiency_standard = cms_models.ProficiencyStandardCms(
        **proficiency_standard_data
    )
    db.add(db_proficiency_standard)
    db.commit()
    db.refresh(db_proficiency_standard)
    return db_proficiency_standard


def create_or_update_proficiency_standard(
    db: Session, proficiency_standard_data: cms_schemas.ProficiencyStandardCmsCreate
):
    if proficiency_standard_data.id:
        existing_proficiency_standard = get_proficiency_standard_by_id(
            db, proficiency_standard_data.id
        )
        if existing_proficiency_standard:
            for key, value in proficiency_standard_data.__dict__.items():
                setattr(existing_proficiency_standard, key, value)
            db.commit()
            db.refresh(existing_proficiency_standard)
            return existing_proficiency_standard
    return create_proficiency_standard(db, proficiency_standard_data)


def delete_proficiency_standard(db: Session, proficiency_standard_id: int):
    proficiency_standard = get_proficiency_standard_by_id(db, proficiency_standard_id)
    if proficiency_standard:
        db.delete(proficiency_standard)
        db.commit()
        return True
    return False
