from sqlalchemy import Column, Index, Integer, SmallInteger, String, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base


class Passage(Base):
    __tablename__ = "passage"

    id = Column(String(36), primary_key=True)
    title = Column(String(256), nullable=False)
    difficulty_id = Column(Integer, ForeignKey("difficulty.id"))

    difficulty = relationship("Difficulty")

    __table_args__ = (Index("fk_passage_difficulty1_idx", difficulty_id),)


class Sentence(Base):
    __tablename__ = "sentence"

    id = Column(String(36), primary_key=True)
    passage_id = Column(String(36), ForeignKey("passage.id"))
    sequence = Column(Integer)
    sentence = Column(String(512), nullable=False)
    meaning = Column(String(1024), nullable=False)
    tense = Column(String(512))

    passage = relationship("Passage")

    __table_args__ = (Index("fk_sentence_passage1_idx", passage_id),)


class Vocabulary(Base):
    __tablename__ = "vocabulary"

    id = Column(String(36), primary_key=True)
    vocabulary = Column(String(256), nullable=False)
    meaning = Column(String(256), nullable=False)
    definition = Column(String(256), nullable=False)
    difficulty_id = Column(Integer, ForeignKey("difficulty.id"))
    pos = Column(String(256), nullable=False)
    tag = Column(String(256), nullable=False)
    lemma = Column(String(256), nullable=False)
    dep = Column(String(256), nullable=False)

    difficulty = relationship("Difficulty")

    __table_args__ = (Index("fk_vocabulary_difficulty1_idx", difficulty_id),)


class VocabularyRelated(Base):
    __tablename__ = "vocabulary_related"

    sentence_id = Column(String(36), ForeignKey("sentence.id"), primary_key=True)
    vocabulary_id = Column(String(36), ForeignKey("vocabulary.id"), primary_key=True)


class Difficulty(Base):
    __tablename__ = "difficulty"

    id = Column(Integer, primary_key=True, autoincrement=True)
    standard = Column(String(16), nullable=False)
    level = Column(String(16), nullable=False)
    description = Column(String(256))
