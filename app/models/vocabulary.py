from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, BigInteger
from app.core.database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    telegram_id = Column(BigInteger, primary_key=True, index=True) # Telegram ID asosiy kalit [cite: 36]

class Word(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, unique=True, index=True)
    translation = Column(String) # O'zbekcha tarjimasi [cite: 39]
    context = Column(String) # Gap ichida ishlatilishi [cite: 39]

class UserWordProgress(Base):
    __tablename__ = "user_word_progress"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"))
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"))
    
    # SM-2 Anki algoritmi parametrlari 
    interval = Column(Integer, default=1)       # Kunlar soni (keyingi safar qachon chiqishi)
    ease_factor = Column(Float, default=2.5)     # Murakkablik koeffitsiyenti
    repetitions = Column(Integer, default=0)     # Ketma-ket to'g'ri topilganlar soni
    next_review = Column(Date, default=datetime.date.today) # Qachon qaytarilishi kerakligi [cite: 40]