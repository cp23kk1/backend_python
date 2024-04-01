from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime
from sqlalchemy import Enum
from app.config.database import Base


# FileCms------------------------------
class FileCategory(str, Enum):
    passage = "passage"
    sentence = "sentence"
    vocabulary = "vocabulary"

    def __get_pydantic_core_schema__(self, handler):
        # Implement schema generation logic here
        return handler.generate_schema(str)


class FileCmsBase(BaseModel):
    filename: str
    extension: str
    path: str
    category: FileCategory
    upload_at: datetime
    process_status: Optional[int]


class FileCmsCreate(FileCmsBase):
    pass


class FileCmsUpdate(FileCmsBase):
    pass


class FileCms(FileCmsBase):
    id: int

    class Config:
        from_attributes = True


# VocabularyCms------------------------------
class VocabularyCmsBase(BaseModel):
    id: str
    text: str
    meaning: Optional[str] = None
    pos: Optional[str] = None
    tag: Optional[str] = None
    lemma: Optional[str] = None
    dep: Optional[str] = None
    morph: Optional[str] = None
    process_status: int = 0
    file_cms_id: int
    level_cms_id: int
    transfer_status: int = 0


class VocabularyCmsCreate(VocabularyCmsBase):
    pass


class VocabularyCmsUpdate(VocabularyCmsBase):
    pass


class VocabularyCms(VocabularyCmsBase):

    class Config:
        from_attributes = True


# ProficiencyStandardCms------------------------------
class ProficiencyStandardCmsBase(BaseModel):
    name: str
    description: Optional[str] = None


class ProficiencyStandardCmsCreate(ProficiencyStandardCmsBase):
    pass


class ProficiencyStandardCmsUpdate(ProficiencyStandardCmsBase):
    pass


class ProficiencyStandardCms(ProficiencyStandardCmsBase):
    id: int

    class Config:
        from_attributes = True


# LevelCms------------------------------
class LevelCmsBase(BaseModel):
    name: str
    description: Optional[str] = None
    proficiency_standard_cms_id: int


class LevelCmsCreate(LevelCmsBase):
    pass


class LevelCmsUpdate(LevelCmsBase):
    pass


class LevelCms(LevelCmsBase):
    id: int

    class Config:
        from_attributes = True


# PassageCms------------------------------
class PassageCmsBase(BaseModel):
    id: str
    title: str
    text: str
    process_status: int
    level_cms_id: int
    file_cms_id: int
    transfer_status: int = 0


class PassageCmsCreate(PassageCmsBase):
    pass


class PassageCmsUpdate(PassageCmsBase):
    pass


class PassageCms(PassageCmsBase):

    class Config:
        from_attributes = True


# SentenceCms------------------------------
class SentenceCmsBase(BaseModel):
    id: str
    text: str
    meaning: Optional[str] = None
    tense: Optional[str] = None
    sequence: int
    is_sentence: int
    process_status: int
    file_cms_id: int
    passage_cms_id: Optional[str] = None
    transfer_status: int = 0


class SentenceCmsCreate(SentenceCmsBase):
    pass


class SentenceCmsUpdate(SentenceCmsBase):
    pass


class SentenceCms(SentenceCmsBase):

    class Config:
        from_attributes = True


# VocabularyRelatedCms------------------------------
class VocabularyRelatedCmsBase(BaseModel):
    sentence_cms_id: str
    vocabulary_cms_id: str
    transfer_status: int = 0


class VocabularyRelatedCmsCreate(VocabularyRelatedCmsBase):
    pass


class VocabularyRelatedCmsUpdate(VocabularyRelatedCmsBase):
    pass


class VocabularyRelatedCms(VocabularyRelatedCmsBase):
    class Config:
        from_attributes = True


# ExtraInformationCms------------------------------
class ExtraInformationCmsBase(BaseModel):
    vocabulary_id: str
    definition: str
    example: str
    meaning: str


class ExtraInformationCmsCreate(ExtraInformationCmsBase):
    pass


class ExtraInformationCmsUpdate(ExtraInformationCmsBase):
    pass


class ExtraInformationCms(ExtraInformationCmsBase):
    id: int

    class Config:
        from_attributes = True
