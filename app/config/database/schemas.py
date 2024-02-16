from pydantic import BaseModel


class Vocabulary(BaseModel):
    id: int
    word: str
    meaning: str
    pos: str
    difficulty_cefr: str

    class Config:
        orm_mode = True
