import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router

# Ключи
from dotenv import load_dotenv
import os
load_dotenv()


async def main():
    bot = Bot(os.getenv('API_TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')