from pydantic import BaseModel


class VocabularyBase(BaseModel):
    vocabulary: str
    meaning: str
    definition: str
    pos: str
    tag: str
    lemma: str
    dep: str


class VocabularyCreate(VocabularyBase):
    pass


class VocabularyUpdate(VocabularyBase):
    pass


class Vocabulary(VocabularyBase):
    id: str

    class Config:
        from_attributes = True
