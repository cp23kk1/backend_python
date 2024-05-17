from sqlalchemy.orm import Session
from app.schemas import app_schemas, cms_schemas
from app.services.vocaverse_app import (
    passage_service,
    sentence_service,
    vocabulary_service,
    vocabulary_related_service,
)
from app.services.vocaverse_cms import (
    passage_cms_service,
    sentence_cms_service,
    vocabulary_cms_service,
    vocabulary_related_cms_service,
)


def transfer_passage_data(cms_db: Session, app_db: Session):
    passages_cms = passage_cms_service.get_passages_filter_transfer_status(cms_db, 0)

    for passage_cms in passages_cms:
        passage_data = {
            "id": passage_cms.id,
            "title": passage_cms.title,
            # Assuming you have a mapping between level_cms_id and difficulty_id
            # You may need to adjust this part based on your actual data structure
            "difficulty_id": passage_cms.level_cms_id,
        }
        passage_service.create_passage(app_db, passage_data)
        passage_cms.transfer_status = 1
        passage_cms_service.create_or_update_passage(cms_db, passage_cms)
    return True


def transfer_sentence_data(cms_db: Session, app_db: Session):
    sentences_cms = sentence_cms_service.get_sentences_filter_transfer_status(cms_db, 0)

    for sentence_cms in sentences_cms:
        sentence_data = {
            "id": sentence_cms.id,
            "passage_id": sentence_cms.passage_cms_id,
            "sequence": sentence_cms.sequence,
            "sentence": sentence_cms.text,
            "meaning": sentence_cms.meaning,
            "tense": sentence_cms.tense,
        }
        sentence_service.create_sentence(app_db, sentence_data)
        sentence_cms.transfer_status = 1
        sentence_cms_service.create_or_update_sentence(cms_db, sentence_cms)
    return True


def transfer_vocabulary_data(cms_db: Session, app_db: Session):
    vocabularies_cms = vocabulary_cms_service.get_vocabularies_filter_transfer_status(
        cms_db, 0
    )

    for vocabulary_cms in vocabularies_cms:
        vocabulary_data = {
            "id": vocabulary_cms.id,
            "vocabulary": vocabulary_cms.text,
            "meaning": vocabulary_cms.meaning,
            "definition": "",
            "difficulty_id": vocabulary_cms.level_cms_id,
            "pos": vocabulary_cms.pos,
            "tag": vocabulary_cms.tag,
            "lemma": vocabulary_cms.lemma,
            "dep": vocabulary_cms.dep,
        }
        vocabulary_service.create_vocabulary(app_db, vocabulary_data)
        vocabulary_cms.transfer_status = 1
        vocabulary_cms_service.create_or_update_vocabulary(cms_db, vocabulary_cms)
    return True


def transfer_vocabulary_data(cms_db: Session, app_db: Session):
    vocabularies_cms = vocabulary_cms_service.get_vocabularies_filter_transfer_status(
        cms_db, 0
    )

    for vocabulary_cms in vocabularies_cms:
        vocabulary_data = {
            "id": vocabulary_cms.id,
            "vocabulary": vocabulary_cms.text,
            "meaning": vocabulary_cms.meaning,
            "definition": "",
            "difficulty_id": vocabulary_cms.level_cms_id,
            "pos": vocabulary_cms.pos,
            "tag": vocabulary_cms.tag,
            "lemma": vocabulary_cms.lemma,
            "dep": vocabulary_cms.dep,
        }
        vocabulary_service.create_vocabulary(app_db, vocabulary_data)
        vocabulary_cms.transfer_status = 1
        vocabulary_cms_service.create_or_update_vocabulary(cms_db, vocabulary_cms)
    return True


def transfer_vocabulary_related_data(cms_db: Session, app_db: Session):
    vocabulary_related_cms_list = vocabulary_related_cms_service.get_vocabulary_related_list_filter_transfer_status(
        cms_db, 0
    )

    for vocabulary_related_cms in vocabulary_related_cms_list:
        vocabulary_related_data = {
            "sentence_id": vocabulary_related_cms.sentence_cms_id,
            "vocabulary_id": vocabulary_related_cms.vocabulary_cms_id,
        }
        vocabulary_related_service.create_vocabulary_related(
            app_db,
            app_schemas.VocabularyRelatedCreate(
                sentence_id=vocabulary_related_cms.sentence_cms_id,
                vocabulary_id=vocabulary_related_cms.vocabulary_cms_id,
            ),
        )
        vocabulary_related_cms.transfer_status = 1
        vocabulary_related_cms_service.create_or_update_vocabulary_related(
            cms_db, vocabulary_related_cms
        )
    return True
