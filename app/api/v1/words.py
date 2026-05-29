from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.vocabulary import Word, UserWordProgress, User
from app.schemas.vocabulary import WordResponse, ReviewRequest
from app.services.srs_algo import calculate_sm2
import datetime

router = APIRouter(prefix="/words", tags=["Words"])

@router.get("/daily", response_model=list[WordResponse])
def get_daily_words(telegram_id: int, db: Session = Depends(get_db)):
    # 1. Foydalanuvchi bazada bo'lmasa, avtomatik yaratamiz (TWA qulayligi) [cite: 36, 77]
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        user = User(telegram_id=telegram_id)
        db.add(user)
        db.commit()

    today = datetime.date.today()
    
    # 2. Bugun yoki undan oldin qaytarilishi kerak bo'lgan so'zlarni olamiz [cite: 40]
    scheduled_progress = db.query(UserWordProgress).filter(
        UserWordProgress.telegram_id == telegram_id,
        UserWordProgress.next_review <= today
    ).all()
    
    words_to_return = [p.word_id for p in scheduled_progress]
    
    # 3. Agar kunlik dars uchun so'zlar soni 10 tadan kam bo'lsa, yangi so'zlardan qo'shamiz 
    LIMIT = 10
    if len(words_to_return) < LIMIT:
        needed = LIMIT - len(words_to_return)
        
        seen_word_ids = db.query(UserWordProgress.word_id).filter(
            UserWordProgress.telegram_id == telegram_id
        ).subquery()
        
        new_words = db.query(Word).filter(~Word.id.in_(seen_word_ids)).limit(needed).all()
        
        for nw in new_words:
            progress = UserWordProgress(telegram_id=telegram_id, word_id=nw.id, next_review=today)
            db.add(progress)
            words_to_return.append(nw.id)
        db.commit()

    return db.query(Word).filter(Word.id.in_(words_to_return)).all()

@router.post("/review")
def review_word(payload: ReviewRequest, db: Session = Depends(get_db)):
    progress = db.query(UserWordProgress).filter(
        UserWordProgress.telegram_id == payload.telegram_id,
        UserWordProgress.word_id == payload.word_id
    ).first()

    if not progress:
        raise HTTPException(status_code=404, detail="So'z topilmadi")

    # SM-2 orqali yangi muddatlarni hisoblaymiz 
    new_interval, new_reps, new_ef, next_date = calculate_sm2(
        is_correct=payload.is_correct,
        interval=progress.interval,
        repetitions=progress.repetitions,
        ease_factor=progress.ease_factor
    )

    progress.interval = new_interval
    progress.repetitions = new_reps
    progress.ease_factor = new_ef
    progress.next_review = next_date

    db.commit()
    return {"status": "success", "next_review": str(next_date)}