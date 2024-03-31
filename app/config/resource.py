import os
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

    # database config
    DB_HOST: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_APP_NAME: str
    DB_CMS_NAME: str
    DB_PORT: str

    # status
    SUCCESS: str = "SUCCESS"
    FAILED: str = "FAILED"

    # extraction processing
    datasources_path = "datasources"
    origin_files_path = os.path.abspath("datasources/origin")
    computed_files_path = os.path.abspath("datasources/computed")
    dumped_files_path = os.path.abspath("datasources/dumped")
    computed_file_path = os.path.join(
        computed_files_path,
        f"computed_file.csv",
    )

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
        cls.ORIGINS = os.getenv("ORIGINS")
        cls.DB_HOST = os.getenv("DB_HOST")
        cls.DB_USERNAME = os.getenv("DB_USERNAME")
        cls.DB_PASSWORD = os.getenv("DB_PASSWORD")
        cls.DB_APP_NAME = os.getenv("DB_APP_NAME")
        cls.DB_CMS_NAME = os.getenv("DB_CMS_NAME")
        cls.DB_PORT = os.getenv("DB_PORT")

        # Return an instance of the Config class
        return cls()

    POS = {
        "ADJ": "Adjective",
        "ADP": "Adposition",
        "ADV": "Adverb",
        "AUX": "Auxiliary verb",
        "CONJ": "Coordinating conjunction",
        "CCONJ": "Coordinating conjunction",
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

    INCLUDED_POS = {
        "ADJ": "Adjective",
        "ADP": "Adposition",
        "ADV": "Adverb",
        "AUX": "Auxiliary verb",
        "CONJ": "Coordinating conjunction",
        "CCONJ": "Coordinating conjunction",
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

    POS_TAGS = {
        "CC": "coordinating conjunction",
        "CD": "cardinal digit",
        "DT": "determiner",
        "EX": "existential there",
        "FW": "foreign word",
        "IN": "preposition/subordinating conjunction",
        "JJ": "adjective",
        "JJR": "adjective, comparative",
        "JJS": "adjective, superlative",
        "LS": "list marker",
        "MD": "modal",
        "NN": "noun, singular or mass",
        "NNS": "noun, plural",
        "NNP": "proper noun, singular",
        "NNPS": "proper noun, plural",
        "PDT": "predeterminer",
        "POS": "possessive ending",
        "PRP": "personal pronoun",
        "PRP$": "possessive pronoun",
        "RB": "adverb",
        "RBR": "adverb, comparative",
        "RBS": "adverb, superlative",
        "RP": "particle",
        "SYM": "symbol",
        "TO": "to",
        "UH": "interjection",
        "VB": "verb, base form",
        "VBD": "verb, past tense",
        "VBG": "verb, gerund/present participle",
        "VBN": "verb, past participle",
        "VBP": "verb, non-3rd person singular present",
        "VBZ": "verb, 3rd person singular present",
        "WDT": "wh-determiner",
        "WP": "wh-pronoun",
        "WP$": "possessive wh-pronoun",
        "WRB": "wh-adverb",
    }

    DEP = {
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
