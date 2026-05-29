import datetime

def calculate_sm2(is_correct: bool, interval: int, repetitions: int, ease_factor: float):
    """
    Anki SM-2 algoritmiga asoslangan takrorlash tizimi.
    is_correct: True (Bildim) yoki False (Bilmadim) [cite: 46]
    """
    # Bildim desa 4 (yaxshi), Bilmadim desa 1 (yomon) baho beramiz
    quality = 4 if is_correct else 1

    if quality >= 3:
        if repetitions == 0:
            new_interval = 1
        elif repetitions == 1:
            new_interval = 6
        else:
            new_interval = int(round(interval * ease_factor))
        new_repetitions = repetitions + 1
    else:
        new_repetitions = 0
        new_interval = 1

    # Ease Factor (Murakkablik faktori) yangilanishi
    new_ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    if new_ease_factor < 1.3:
        new_ease_factor = 1.3

    next_review_date = datetime.date.today() + datetime.timedelta(days=new_interval)
    
    return new_interval, new_repetitions, new_ease_factor, next_review_date