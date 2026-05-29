from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # <-- SHUNI QO'SHING
from app.core.database import engine, Base, SessionLocal
from app.api.v1.words import router as words_router
from app.models.vocabulary import Word

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal English Assistant MVP", version="1.0")

# ---- CORS SOZLAMASI (SHU QISMALARI QO'SHILDI) ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # MVP uchun hamma saytdan ulanishga ruxsat beramiz
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------------------------------------

app.include_router(words_router, prefix="/api/v1")

@app.on_event("startup")
def seed_data():
    db = SessionLocal()
    try:
        if db.query(Word).count() == 0:
            sample_words = [
                Word(word="Abandon", translation="Tark etmoq, tashlab ketmoq", context="He decided to abandon his old car."),
                Word(word="Accurate", translation="Aniq, to'g'ri", context="The weather forecast was accurate."),
                Word(word="Achieve", translation="Erishmoq, muvaffaqiyat qozonmoq", context="She worked hard to achieve her goals."),
                Word(word="Beneficial", translation="Foydali", context="Regular exercise is beneficial for health."),
                Word(word="Challenge", translation="Qiyinchilik, chaqiriq", context="Learning a new language is a great challenge."),
                Word(word="Determine", translation="Aniqlamoq, qaror qilmoq", context="They need to determine the cause of the problem."),
                Word(word="Efficient", translation="Samarali", context="The new system is much more efficient."),
                Word(word="Evaluate", translation="Baholamoq", context="The teacher will evaluate your progress."),
                Word(word="Frequent", translation="Tez-tez bo'lib turadigan", context="He makes frequent trips to London."),
                Word(word="Generous", translation="Saxiy", context="Thank you for your generous donation."),
                Word(word="Inevitable", translation="Muqarrar, qochib bo'lmas", context="Change is an inevitable part of life."),
                Word(word="Maintain", translation="Saqlamoq, ta'minlamoq", context="You must maintain a good speed."),
                Word(word="Objective", translation="Maqsad, xolis", context="Our main objective is to improve quality."),
                Word(word="Permanent", translation="Doimiy", context="This is my permanent address."),
                Word(word="Redundant", translation="Keraksiz, ortiqcha", context="The old data became redundant."),
                Word(word="Significant", translation="Muhim, sezilarli", context="There is a significant difference between them."),
                Word(word="Tolerate", translation="Chidamoq, sabr qilmoq", context="I cannot tolerate this noise anymore."),
                Word(word="Vague", translation="Noaniq, xira", context="He gave a vague answer to the question."),
                Word(word="Wealthy", translation="Boy, badavlat", context="He comes from a wealthy family."),
                Word(word="Yield", translation="Hosildorlik berish, bo'yin egmoq", context="The investment will yield high returns."),
            ]
            db.add_all(sample_words)
            db.commit()
            print("\n>>> Boshlang'ich 20 ta so'z muvaffaqiyatli yuklandi! <<<\n")
    finally:
        db.close()

@app.get("/")
def root():
    return {"status": "running", "project": "PEA-Backend"}