import asyncio
import logging
import telebot

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

import config
from handlers import router

async def main():
    # НАСТРОЙКА БОТА (исправленная версия)
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2)
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Подключаем роутер с обработчиками
    dp.include_router(router)

    # Запускаем бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
