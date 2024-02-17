from sqlalchemy import Table, Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .mysql import Base

# Define the association table
vocabulary_related = Table(
    "vocabulary_related",
    Base.metadata,
    Column("sentence_id", Integer, ForeignKey("sentence.id")),
    Column("vocabulary_id", Integer, ForeignKey("vocabulary.id")),
)


class Passage(Base):
    __tablename__ = "passage"

    # id = Column(Integer, primary_key=True, index=True)
    # title = Column(String)
    # level = Column(String)
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)

    sentences = relationship("Sentence", back_populates="passage")


class Sentence(Base):
    __tablename__ = "sentence"

    # id = Column(Integer, primary_key=True, index=True)
    # passage_id = Column(Integer, ForeignKey("passage.id"))
    # sequence = Column(Integer)
    # sentence = Column(String)
    # meaning = Column(String)
    # tense = Column(JSON)
    id = Column(Integer, primary_key=True, index=True)
    passage_id = Column(Integer, ForeignKey("passage.id"))
    sequence = Column(Integer)
    text = Column(String)
    meaning = Column(String)

    passage = relationship("Passage", back_populates="sentences")
    vocabularies = relationship(
        "Vocabulary", secondary=vocabulary_related, back_populates="sentences"
    )


class Vocabulary(Base):
    __tablename__ = "vocabulary"

    # id = Column(Integer, primary_key=True, index=True)
    # # sentence_id = Column(Integer, ForeignKey("sentence.id"))
    # vocabulary = Column(String)
    # meaning = Column(String)
    # difficulty = Column(String)
    # pos = Column(String)
    # tag = Column(String)
    # lemma = Column(String)
    # dep = Column(String)
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String)
    meaning = Column(String)
    pos = Column(String)
    difficulty_cefr = Column(String)

    sentences = relationship(
        "Sentence", secondary=vocabulary_related, back_populates="vocabularies"
    )