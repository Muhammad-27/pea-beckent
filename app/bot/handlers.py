from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

# Bu yerga vaqtincha frontend mahalliy urlini qo'yamiz, keyingi qadamda buni internet urliga almashtiramiz
WEB_APP_URL = "https://untimed-esophagus-secluding.ngrok-free.dev" 

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    # Telegram Web App ochadigan tugma yasaymiz
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="🚀 So'z yodlashni boshlash",
            web_app=types.WebAppInfo(url=WEB_APP_URL) # Tugmaga WebApp manzilini beramiz
        )
    )
    
    welcome_text = (
        f"Salom, {message.from_user.full_name}! 👋\n\n"
        f"**Personal English Assistant** botiga xush kelibsiz!\n"
        f"Bu yerda siz ingliz tili so'zlarini xotirada uzoq saqlash "
        f"algoritmi (SRS) orqali juda oson yodlaysiz.\n\n"
        f"Boshlash uchun pastdagi tugmani bosing 👇"
    )
    
    await message.answer(welcome_text, parse_mode="Markdown", reply_markup=builder.as_markup())