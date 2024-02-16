from sqlalchemy import Column, Integer, String
from app.config.database.mysql import Base


class VocabularyModel(Base):
    __tablename__ = "vocabulary"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, index=True)
    meaning = Column(String)
    pos = Column(String)
    difficulty_cefr = Column(String)
