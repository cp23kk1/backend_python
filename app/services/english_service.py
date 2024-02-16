import spacy
import nltk

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    spacy.cli.download("en_core_web_sm")
    nltk.download("punkt")
    nlp = spacy.load("en_core_web_sm")


class EnglishService:

    def check_tenses(self, sentence):
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

    def is_sentence(self, text):
        doc = nlp(text)

        has_verb = any(token.pos_ == "VERB" for token in doc)
        has_subject = any(token.dep_ == "nsubj" for token in doc)
        has_predicate = any(token.dep_ == "ROOT" for token in doc)

        return has_verb and has_subject and has_predicate

    def vocab_info(self, sentence: str):
        vocab_info = {}
        for token in nlp(sentence):
            vocab_info[token.text] = {
                "vocabulary": token.text,
                "pos": token.pos_,
                "tag": token.tag_,
                "lemma": token.lemma_,
                "dep": token.dep_,    
                "is_alpha": token.is_alpha,
                "is_stop": token.is_stop,
                "morph": token.morph.to_json(),
            }
        return vocab_info

    def sentence_info(self, passage: str):
        sentences = nltk.sent_tokenize(passage)
        sentence_info = {}
        for index, sentence in enumerate(sentences):
            is_sentence = self.is_sentence(sentence)
            sentence_info[str(index)] = {
                "sentence": sentence,
                "tense": self.check_tenses(sentence) if is_sentence else [],
                "is_sentence": is_sentence,
            }
        return sentence_info
