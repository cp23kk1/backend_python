# from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
# import datetime


# Base = declarative_base()

# # Define association table
# vocabulary_related = Table(
#     "vocabulary_related",
#     Base.metadata,
#     Column("sentence_id", String(36), ForeignKey("sentence.id")),
#     Column("vocabulary_id", String(36), ForeignKey("vocabulary.id")),
# )


# class File(Base):
#     __tablename__ = "file"

#     id = Column(Integer, primary_key=True)
#     filename = Column(String(256), nullable=False)
#     extension = Column(String(8), nullable=False)
#     category = Column(String(10), nullable=False)
#     uploadAt = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
#     retrievedStatus = Column(Integer)
#     dataQuantity = Column(Integer)


# class Vocabulary(Base):
#     __tablename__ = "vocabulary"

#     id = Column(String(36), primary_key=True)
#     text = Column(String(64), nullable=False)
#     meaning = Column(String(256))
#     pos = Column(String(256))
#     tag = Column(String(256))
#     lemma = Column(String(256))
#     deb = Column(String(256))
#     processStatus = Column(Integer, nullable=False, default=0)
#     file_id = Column(Integer, ForeignKey("file.id"))

#     file = relationship("File", back_populates="vocabulary")


# class Sentence(Base):
#     __tablename__ = "sentence"

#     id = Column(String(36), primary_key=True)
#     text = Column(String(256), nullable=False)
#     meaning = Column(String(512))
#     tense = Column(String(256))
#     file_id = Column(Integer, ForeignKey("file.id"))

#     file = relationship("File", back_populates="sentence")
#     vocabularies = relationship(
#         "Vocabulary", secondary=vocabulary_related, back_populates="sentences"
#     )


# class ProficiencStandard(Base):
#     __tablename__ = "proficienc_standard"

#     id = Column(Integer, primary_key=True)
#     name = Column(String(128), nullable=False)
#     description = Column(String(512))


# class Level(Base):
#     __tablename__ = "level"

#     id = Column(Integer, primary_key=True)
#     name = Column(String(16), nullable=False)
#     description = Column(String(256))
#     proficienc_standard_id = Column(Integer, ForeignKey("proficienc_standard.id"))

#     proficienc_standard = relationship("ProficiencStandard", back_populates="level")


# class Passage(Base):
#     __tablename__ = "passage"

#     id = Column(String(36), primary_key=True)
#     title = Column(String(256), nullable=False)
#     text = Column(String(16384), nullable=False)
#     processStatus = Column(Integer, default=0)
#     level_id = Column(Integer, ForeignKey("level.id"))
#     file_id = Column(Integer, ForeignKey("file.id"))

#     level = relationship("Level", back_populates="passages")
#     file = relationship("File", back_populates="passages")


# class VocabularyRelated(Base):
#     __tablename__ = "vocabulary_related"

#     sentence_id = Column(String(36), ForeignKey("sentence.id"), primary_key=True)
#     vocabulary_id = Column(String(36), ForeignKey("vocabulary.id"), primary_key=True)

#     sentence = relationship("Sentence", back_populates="related_vocabularies")
#     vocabulary = relationship("Vocabulary", back_populates="related_sentences")
