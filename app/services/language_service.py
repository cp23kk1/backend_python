import spacy
import requests
import nltk
import uuid
from nltk.tokenize import sent_tokenize
from sqlalchemy.orm import Session
from googletrans import Translator
from app.services.vocaverse_cms import (
    passage_cms_service,
    sentence_cms_service,
    vocabulary_cms_service,
    vocabulary_related_cms_service,
)
from app.exceptions.errors import InputIsNotAlphabet, TemporarilySuspendService
from app.schemas import cms_schemas

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    spacy.cli.download("en_core_web_sm")
    nltk.download("punkt", quiet=True)
    nlp = spacy.load("en_core_web_sm")


def check_tenses(sentence):
    doc = nlp(sentence)
    # Initialize variables to track tenses
    tenses = {
        "Simple Present": False,
        "Present Continuous": False,
        "Present Perfect": False,
        "Present Perfect Continuous": False,
        "Simple Past": False,
        "Past Continuous": False,
        "Past Perfect": False,
        "Past Perfect Continuous": False,
        "Simple Future": False,
        "Future Continuous": False,
        "Future Perfect": False,
        "Future Perfect Continuous": False,
    }
    # Iterate over tokens in the sentence
    for token in doc:
        # Check if token is a verb
        if token.pos_ == "VERB":
            # Check morphological features to determine tense
            if "Tense=Pres" in token.morph:
                if "Aspect=Prog" in token.morph:
                    tenses["Present Continuous"] = True
                elif "Aspect=Perf" in token.morph:
                    tenses["Present Perfect"] = True
                elif "Aspect=Perf" in token.morph and "Aspect=Prog" in token.morph:
                    tenses["Present Perfect Continuous"] = True
                else:
                    tenses["Simple Present"] = True
            elif "Tense=Past" in token.morph:
                if "Aspect=Prog" in token.morph:
                    tenses["Past Continuous"] = True
                elif "Aspect=Perf" in token.morph:
                    tenses["Past Perfect"] = True
                elif "Aspect=Perf" in token.morph and "Aspect=Prog" in token.morph:
                    tenses["Past Perfect Continuous"] = True
                else:
                    tenses["Simple Past"] = True
            elif "Tense=Fut" in token.morph:
                if "Aspect=Prog" in token.morph:
                    tenses["Future Continuous"] = True
                elif "Aspect=Perf" in token.morph:
                    tenses["Future Perfect"] = True
                elif "Aspect=Perf" in token.morph and "Aspect=Prog" in token.morph:
                    tenses["Future Perfect Continuous"] = True
                else:
                    tenses["Simple Future"] = True
    # Construct a list of detected tenses
    detected_tenses = [tense for tense, found in tenses.items() if found]
    return detected_tenses


def is_sentence(text) -> bool:
    doc = nlp(text)

    has_verb = any(token.pos_ == "VERB" for token in doc)
    has_subject = any(token.dep_ == "nsubj" for token in doc)
    has_predicate = any(token.dep_ == "ROOT" for token in doc)

    return has_verb and has_subject and has_predicate


def is_alpha(text) -> bool:
    result = all([token.is_alpha for token in nlp(text)])
    if not result:
        raise InputIsNotAlphabet(f"{text} has non-Alphabet!")
    return result


def passage_processing(db: Session, passage_id_list: list[str]):
    sentence_id_list = []
    for passage_id in passage_id_list:
        current_passage = passage_cms_service.get_passage_by_id(db, passage_id)
        sentences = sent_tokenize(current_passage.text)
        for index, sentence in enumerate(sentences):
            save_sentence = sentence_cms_service.create_sentence(
                db,
                {
                    "id": uuid.uuid4(),
                    "text": sentence,
                    "meaning": None,
                    "tense": None,
                    "sequence": index + 1,
                    "is_sentence": is_sentence(sentence),
                    "process_status": 0,
                    "file_cms_id": current_passage.file_cms_id,
                    "passage_cms_id": passage_id,
                    "transfer_status": 0,
                },
            )
            sentence_id_list.append(save_sentence.id)
        current_passage.process_status = 1
        passage_cms_service.create_or_update_passage(db, current_passage)
    sentence_processing(db, sentence_id_list)
    return True


def sentence_processing(db: Session, sentence_id_list: list[str]):
    vocabulary_id_list = []
    for sentence_id in sentence_id_list:
        current_sentence = sentence_cms_service.get_sentence_by_id(db, sentence_id)
        current_sentence.meaning = translate_en_to_th(current_sentence.text)
        current_sentence.tense = (", ".join(check_tenses(current_sentence.text)),)
        for token in nlp(current_sentence.text):
            if token.is_alpha:
                current_vocab = vocabulary_cms_service.get_vocabulary_by_text(
                    db, token.text
                )
                if current_vocab:
                    current_vocabulary_related = (
                        vocabulary_related_cms_service.get_vocabulary_related_by_ids(
                            db, sentence_id, current_vocab.id
                        )
                    )
                    if not current_vocabulary_related:
                        vocabulary_related_cms_service.create_or_update_vocabulary_related(
                            db,
                            cms_schemas.VocabularyRelatedCmsCreate(
                                sentence_cms_id=sentence_id,
                                vocabulary_cms_id=current_vocab.id,
                                transfer_status=0,
                            ),
                        )
                else:
                    save_vocab = vocabulary_cms_service.create_vocabulary(
                        db,
                        {
                            "id": uuid.uuid4(),
                            "text": token.text,
                            "meaning": None,
                            "pos": None,
                            "tag": None,
                            "lemma": None,
                            "dep": None,
                            "morph": None,
                            "process_status": 0,
                            "file_cms_id": current_sentence.file_cms_id,
                            "transfer_status": 0,
                        },
                    )
                    vocabulary_id_list.append(save_vocab.id)
                    vocabulary_related_cms_service.create_or_update_vocabulary_related(
                        db,
                        cms_schemas.VocabularyRelatedCmsCreate(
                            sentence_cms_id=sentence_id,
                            vocabulary_cms_id=save_vocab.id,
                            transfer_status=0,
                        ),
                    )
        current_sentence.process_status = 1
        sentence_cms_service.create_or_update_sentence(db, current_sentence)
    vocabulary_processing(db, vocabulary_id_list)
    return True


def vocabulary_processing(db: Session, vocabulary_id_list: list[str]):
    for vocab_id in vocabulary_id_list:
        current_vocab = vocabulary_cms_service.get_vocabulary_by_id(db, vocab_id)
        for token in nlp(current_vocab.text):
            current_vocab.meaning = translate_en_to_th(token.text)
            current_vocab.pos = (token.pos_,)
            current_vocab.tag = (token.tag_,)
            current_vocab.lemma = (token.lemma_,)
            current_vocab.dep = (token.dep_,)
            current_vocab.morph = token.morph.to_json()
        current_vocab.process_status = 1
        vocabulary_cms_service.create_or_update_vocabulary(db, current_vocab)
    return True


def get_dictionary_definitions(text):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{text}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None
    except requests.exceptions.RequestException as e:
        raise TemporarilySuspendService


def get_word_definitions(text):
    result: dict[str, str] = {}
    translator = Translator(user_agent="Mozilla/5.0")
    translation = translator.translate(text, dest="th")
    is_alpha = [token.is_alpha for token in nlp(text)][0]
    check_length = len(text.split()) == 1
    if is_alpha and check_length:
        if len(translation.extra_data["parsed"]) >= 4:
            result["origin"] = translation.extra_data["parsed"][3][0]
            result["defination"] = (
                translation.extra_data["parsed"][3][1][0][0][1][0][0]
                if translation.extra_data["parsed"][3][1]
                else None
            )
    else:
        result = translate_with_googletrans("th", text)
    return result


def translate_with_googletrans(dest: str, text: str):
    translator = Translator(user_agent="Mozilla/5.0")
    translation = translator.translate(text, dest=dest)
    return translation.text if translation.text else None


def translate_en_to_th(text: str):
    return translate_with_googletrans("th", text)
