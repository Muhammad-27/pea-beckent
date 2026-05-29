import asyncio
import logging
from aiogram import Bot, Dispatcher
from app.core.config import settings
from app.bot.handlers import router

async def start_bot():
    # Loggingni sozlash (Bot xatolarini terminalda ko'rish uchun)
    logging.basicConfig(level=logging.INFO)
    
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    
    # Routerni ulash
    dp.include_router(router)
    
    print("\n>>> Telegram Bot muvaffaqiyatli ishga tushdi! <<<\n")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(start_bot())