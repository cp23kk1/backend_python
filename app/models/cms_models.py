from sqlalchemy import (
    Column,
    Index,
    Integer,
    SmallInteger,
    String,
    DateTime,
    Enum,
    ForeignKey,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship
from app.config.database import Base
from app.schemas.cms_schemas import FileCategory


class FileCms(Base):
    __tablename__ = "file_cms"

    id = Column(Integer, primary_key=True)
    filename = Column(String(256), nullable=False)
    extension = Column(String(8), nullable=False)
    path = Column(String(1024), nullable=False)
    category = Column(
        Enum(FileCategory.passage, FileCategory.sentence, FileCategory.vocabulary),
        nullable=False,
    )
    upload_at = Column(DateTime, nullable=False, server_default=func.now())
    process_status = Column(Integer)

    passages = relationship("PassageCms", back_populates="file")
    sentences = relationship("SentenceCms", back_populates="file")
    vocabularies = relationship("VocabularyCms", back_populates="file")


class VocabularyCms(Base):
    __tablename__ = "vocabulary_cms"

    id = Column(String(36), primary_key=True)
    text = Column(String(64), nullable=False)
    meaning = Column(String(128))
    pos = Column(String(256))
    tag = Column(String(256))
    lemma = Column(String(256))
    deb = Column(String(256))
    morph = Column(String(256))
    process_status = Column(SmallInteger, nullable=False, default=0)
    file_cms_id = Column(Integer, ForeignKey("file_cms.id"))

    file = relationship("FileCms", back_populates="vocabularies")
    sentences = relationship("VocabularyRelatedCms", back_populates="vocabulary")
    extra_informations = relationship(
        "ExtraInformationCms", back_populates="vocabulary"
    )

    __table_args__ = (Index("fk_vocabulary_cms_file_cms1_idx", file_cms_id),)


class ProficiencyStandardCms(Base):
    __tablename__ = "proficiency_standard_cms"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    description = Column(String(512))

    levels = relationship("LevelCms", back_populates="proficiency_standard")

    __table_args__ = (UniqueConstraint("id", name="id_UNIQUE"),)


class LevelCms(Base):
    __tablename__ = "level_cms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(16), nullable=False, index=True)
    description = Column(String(256))
    proficiency_standard_cms_id = Column(
        Integer, ForeignKey("proficiency_standard_cms.id"), nullable=False
    )

    proficiency_standard = relationship(
        "ProficiencyStandardCms", back_populates="levels"
    )
    passages = relationship("PassageCms", back_populates="level")


class PassageCms(Base):
    __tablename__ = "passage_cms"

    id = Column(String(36), primary_key=True)
    title = Column(String(256), nullable=False)
    text = Column(String(16384), nullable=False)
    process_status = Column(Integer, nullable=False, default=0)
    level_cms_id = Column(Integer, ForeignKey("level_cms.id"))
    file_cms_id = Column(Integer, ForeignKey("file_cms.id"))

    level = relationship("LevelCms", back_populates="passages")
    file = relationship("FileCms", back_populates="passages")
    sentences = relationship("SentenceCms", back_populates="passage")


class SentenceCms(Base):
    __tablename__ = "sentence_cms"

    id = Column(String(36), primary_key=True)
    text = Column(String(256), nullable=False)
    meaning = Column(String(512))
    sequence = Column(Integer)
    tense = Column(String(256))
    is_sentence = Column(Integer, nullable=False)
    process_status = Column(Integer, nullable=False, default=0)
    file_cms_id = Column(Integer, ForeignKey("file_cms.id"))
    passage_cms_id = Column(String(36), ForeignKey("passage_cms.id"))

    file = relationship("FileCms", back_populates="sentences")
    passage = relationship("PassageCms", back_populates="sentences")
    vocabularies = relationship("VocabularyRelatedCms", back_populates="sentence")


class VocabularyRelatedCms(Base):
    __tablename__ = "vocabulary_related_cms"

    sentence_cms_id = Column(
        String(36), ForeignKey("sentence_cms.id"), primary_key=True
    )
    vocabulary_cms_id = Column(
        String(36), ForeignKey("vocabulary_cms.id"), primary_key=True
    )

    sentence = relationship("SentenceCms", back_populates="vocabularies")
    vocabulary = relationship("VocabularyCms", back_populates="sentences")


class ExtraInformationCms(Base):
    __tablename__ = "extra_information_cms"

    id = Column(Integer, primary_key=True)
    vocabulary_id = Column(String(36), ForeignKey("vocabulary_cms.id"), nullable=False)
    example_usage = Column(String(256))
    meaning = Column(String(512))

    vocabulary = relationship("VocabularyCms", back_populates="extra_informations")
