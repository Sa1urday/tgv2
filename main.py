#!/usr/bin/env python3
import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import router
from config import BOT_TOKEN, ADMIN_ID
from aiogram.enums import ParseMode  # Добавьте этот импорт
from aiogram.client.default import DefaultBotProperties  # Новый импорт

# Красивая настройка логов
logging.basicConfig(
    level=logging.INFO,
    format="\033[36m%(asctime)s\033[0m - \033[34m%(name)s\033[0m - \033[32m%(levelname)s\033[0m - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("bot.log", encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

async def on_startup(bot: Bot):
    logger.info("\033[32mБот успешно запущен!\033[0m")
    await bot.send_message(ADMIN_ID, "🤖 Бот запущен и готов к работе!")

async def on_shutdown(bot: Bot):
    logger.info("\033[31mБот остановлен\033[0m")
    await bot.send_message(ADMIN_ID, "🛑 Бот остановлен")

async def main():
    bot = Bot(token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(parse_mode=ParseMode.HTML)
    
    dp.include_router(router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    print("\033[35m" + "="*50)
    print("Starting channel membership bot...")
    print("="*50 + "\033[0m")
    asyncio.run(main())