import os
from typing import Dict
from dotenv import load_dotenv

dotenv_path = (
    ".env" if os.getenv("ENVIRONMENT") in ["prod", "sit", "dev"] else ".env.local"
)

# Load environment variables from .env file
try:
    load_dotenv(dotenv_path)
except Exception as e:
    raise Exception(f"Error loading {dotenv_path} file: {e}")


class Config:

    # initial
    API_PREFIX: str
    PROJECT_NAME: str
    VERSION: str
    ORIGINS: str
    # API_PREFIX: str = "/api"
    # PROJECT_NAME: str = "VOCAVERSE"
    # VERSION: str = "R2.0.1"
    # ORIGINS: str = [
    #     "http://localhost:8080",
    #     "http://localhost:3000",
    #     "https://stackpython.co",
    # ]

    # database config
    DB_HOST: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_PORT: str

    # extraction processing
    origin_files_location_path = os.path.abspath("datasources/origin")
    computed_files_location_path = os.path.abspath("datasources/computed")
    computed_file_path = os.path.join(
        computed_files_location_path,
        f"computed_file.csv",
    )

    # response
    STATUS: Dict[int, str] = {1: "success", 0: "failed"}

    @classmethod
    def load_config(cls):
        # Load .env.local if available, otherwise fallback to .env
        dotenv_path = (
            ".env"
            if os.getenv("ENVIRONMENT") in ["prod", "sit", "dev"]
            else ".env.local"
        )

        # Load environment variables from .env file
        try:
            from dotenv import load_dotenv

            load_dotenv(dotenv_path)
        except Exception as e:
            raise Exception(f"Error loading {dotenv_path} file: {e}")

        # Assign environment variables to class attributes
        cls.API_PREFIX = os.getenv("API_PREFIX")
        cls.PROJECT_NAME = os.getenv("PROJECT_NAME")
        cls.VERSION = os.getenv("VERSION")
        cls.ORIGINS = os.getenv("ORIGINS").split(",")
        cls.DB_HOST = os.getenv("DB_HOST")
        cls.DB_USERNAME = os.getenv("DB_USERNAME")
        cls.DB_PASSWORD = os.getenv("DB_PASSWORD")
        cls.DB_NAME = os.getenv("DB_NAME")
        cls.DB_PORT = os.getenv("DB_PORT")

        # Return an instance of the Config class
        return cls()


tables_name = {"vocabulary": "vocabulary"}


pos = {
    "ADJ": "Adjective",
    "ADP": "Adposition",
    "ADV": "Adverb",
    "AUX": "Auxiliary verb",
    "CONJ": "Coordinating conjunction",
    "DET": "Determiner",
    "INTJ": "Interjection",
    "NOUN": "Noun",
    "NUM": "Numeral",
    "PART": "Particle",
    "PRON": "Pronoun",
    "PROPN": "Proper noun",
    "PUNCT": "Punctuation",
    "SCONJ": "Subordinating conjunction",
    "SYM": "Symbol",
    "VERB": "Verb",
    "X": "Other",
}

included_pos = {
    "ADJ": "Adjective",
    "ADP": "Adposition",
    "ADV": "Adverb",
    "AUX": "Auxiliary verb",
    "CONJ": "Coordinating conjunction",
    "DET": "Determiner",
    # 'INTJ': 'Interjection',
    "NOUN": "Noun",
    # 'NUM': 'Numeral',
    # 'PART': 'Particle',
    "PRON": "Pronoun",
    "PROPN": "Proper noun",
    "PUNCT": "Punctuation",
    "SCONJ": "Subordinating conjunction",
    "SYM": "Symbol",
    "VERB": "Verb",
    # 'X': 'Other'
}

pos_more_tags = {
    "NN": "Noun, singular or mass",
    "NNS": "Noun, plural",
    "NNP": "Proper noun, singular",
    "NNPS": "Proper noun, plural",
    "VB": "Verb, base form",
    "VBD": "Verb, past tense",
    "VBG": "Verb, gerund or present participle",
    "VBN": "Verb, past participle",
    "VBP": "Verb, non-3rd person singular present",
    "VBZ": "Verb, 3rd person singular present",
    "JJ": "Adjective",
    "JJR": "Adjective, comparative",
    "JJS": "Adjective, superlative",
    "RB": "Adverb",
    "RBR": "Adverb, comparative",
    "RBS": "Adverb, superlative",
    "PRP": "Personal pronoun",
    "PRP$": "Possessive pronoun",
    "DT": "Determiner",
    "IN": "Preposition or subordinating conjunction",
    "CC": "Coordinating conjunction",
    "CD": "Cardinal number",
    "MD": "Modal",
}

dependency_relations = {
    "ROOT": "The root of the sentence, typically the main verb.",
    "acl": "A clausal modifier of a noun, adjective, or adverb.",
    "acomp": "Adjectival complement.",
    "advcl": "Adverbial clause modifier.",
    "advmod": "Adverbial modifier.",
    "agent": "Agent of passive verb.",
    "amod": "Adjectival modifier.",
    "appos": "Appositional modifier.",
    "attr": "Attribute.",
    "aux": "Auxiliary.",
    "auxpass": "Auxiliary (passive).",
    "case": "Case marker.",
    "cc": "Coordinating conjunction.",
    "ccomp": "Clausal complement.",
    "compound": "Compound.",
    "conj": "Conjunct.",
    "csubj": "Clausal subject.",
    "csubjpass": "Clausal subject (passive).",
    "dative": "Dative.",
    "dep": "Unclassified dependent.",
    "det": "Determiner.",
    "dobj": "Direct object.",
    "expl": "Expletive.",
    "intj": "Interjection.",
    "mark": "Marker.",
    "meta": "Meta modifier.",
    "neg": "Negation modifier.",
    "nmod": "Nominal modifier.",
    "npadvmod": "Noun phrase adverbial modifier.",
    "nsubj": "Nominal subject.",
    "nsubjpass": "Nominal subject (passive).",
    "nummod": "Numeric modifier.",
    "oprd": "Object predicate.",
    "parataxis": "Parataxis.",
    "pcomp": "Prepositional complement.",
    "pobj": "Object of a preposition.",
    "poss": "Possession modifier.",
    "preconj": "Pre-correlative conjunction.",
    "predet": "Predeterminer.",
    "prep": "Prepositional modifier.",
    "prt": "Particle.",
    "punct": "Punctuation.",
    "quantmod": "Quantifier modifier.",
    "relcl": "Relative clause modifier.",
    "xcomp": "Open clausal complement.",
}
