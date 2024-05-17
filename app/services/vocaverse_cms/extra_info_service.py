from sqlalchemy.orm import Session
from app.models import cms_models
from app.schemas import cms_schemas
from app.services import language_service
from app.services.vocaverse_cms import vocabulary_cms_service


def get_extra_informations(db: Session):
    return db.query(cms_models.ExtraInformationCms).all()


def get_extra_information_by_id(db: Session, extra_information_id: int):
    return (
        db.query(cms_models.ExtraInformationCms)
        .filter(cms_models.ExtraInformationCms.id == extra_information_id)
        .first()
    )


def create_extra_information(
    db: Session, extra_information_data: cms_schemas.ExtraInformationCmsCreate
):
    db_extra_information = cms_models.ExtraInformationCms(**extra_information_data)
    db.add(db_extra_information)
    db.commit()
    db.refresh(db_extra_information)
    return db_extra_information


def create_or_update_extra_information(
    db: Session, extra_information_data: cms_schemas.ExtraInformationCmsCreate
):
    if extra_information_data.id:
        existing_extra_information = get_extra_information_by_id(
            db, extra_information_data.id
        )
        if existing_extra_information:
            for key, value in extra_information_data.__dict__.items():
                setattr(existing_extra_information, key, value)
            db.commit()
            db.refresh(existing_extra_information)
            return existing_extra_information
    return create_extra_information(db, extra_information_data)


def delete_extra_information(db: Session, extra_information_id: int):
    extra_information = get_extra_information_by_id(db, extra_information_id)
    if extra_information:
        db.delete(extra_information)
        db.commit()
        return True
    return False


def load_extra_information(db: Session, vocab_id: str):
    current_vocab = vocabulary_cms_service.get_vocabulary_by_id(db, vocab_id)
    current_data_dict = language_service.get_dictionary_definitions(current_vocab.text)[
        0
    ]
    vocab_info = {}
    vocab_info["vocabulary"] = current_data_dict["word"]
    extra_info = []
    for meaning in current_data_dict["meanings"]:
        example_content = ""
        if "example" in meaning["definitions"][0]:
            example_content = meaning["definitions"][0]["example"]
        extra_info.append(
            {
                "pos": meaning["partOfSpeech"],
                "definition": meaning["definitions"][0]["definition"],
                "example": example_content if example_content else "",
                "meaning": (
                    language_service.translate_en_to_th(example_content)
                    if example_content
                    else ""
                ),
            }
        )
    vocab_info["info"] = extra_info
    return vocab_info
