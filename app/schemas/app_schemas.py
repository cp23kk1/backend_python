from typing import Optional
from pydantic import BaseModel


class PassageBase(BaseModel):
    id: str
    title: str
    difficulty_id: Optional[int]


class PassageCreate(PassageBase):
    pass


class Passage(PassageBase):

    class Config:
        from_attributes = True


class SentenceBase(BaseModel):
    id: str
    passage_id: Optional[str]
    sequence: Optional[int]
    sentence: str
    meaning: str
    tense: Optional[str]


class SentenceCreate(SentenceBase):
    pass


class Sentence(SentenceBase):

    class Config:
        from_attributes = True


class VocabularyBase(BaseModel):
    id: str
    vocabulary: str
    meaning: str
    definition: str
    difficulty_id: Optional[int]
    pos: str
    tag: str
    lemma: str
    dep: str


class VocabularyCreate(VocabularyBase):
    pass


class Vocabulary(VocabularyBase):

    class Config:
        from_attributes = True


class VocabularyRelatedBase(BaseModel):
    sentence_id: str
    vocabulary_id: str


class VocabularyRelatedCreate(VocabularyRelatedBase):
    pass


class VocabularyRelatedUpdate(VocabularyRelatedBase):
    pass


class VocabularyRelated(VocabularyRelatedBase):
    class Config:
        from_attributes = True


class DifficultyBase(BaseModel):
    standard: str
    level: str
    description: Optional[str] = None


class DifficultyCreate(BaseModel):
    pass


class Difficulty(BaseModel):
    id: int

    class Config:
        from_attributes = True
