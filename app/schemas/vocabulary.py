from pydantic import BaseModel

class WordResponse(BaseModel):
    id: int
    word: str
    translation: str
    context: str

    class Config:
        from_attributes = True

class ReviewRequest(BaseModel):
    telegram_id: int
    word_id: int
    is_correct: bool  # True = Bildim, False = Bilmadim [cite: 46]