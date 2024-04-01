from sqlalchemy import Column, Integer, String, ForeignKey
from app.config.database import Base

class Vocabulary(Base):
    __tablename__ = "vocabulary"

    id = Column(String(36), primary_key=True)
    vocabulary = Column(String(256), nullable=False)
    meaning = Column(String(256), nullable=False)
    definition = Column(String(256), nullable=False)
    difficulty_id = Column(Integer)
    pos = Column(String(256), nullable=False)
    tag = Column(String(256), nullable=False)
    lemma = Column(String(256), nullable=False)
    dep = Column(String(256), nullable=False)
