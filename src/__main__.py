import os
import asyncio

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from src.routers import router
import logging
from src.db.queries.orm import create_tables


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    load_dotenv('.env')
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(token=os.getenv('TOKEN'))

    dp.include_routers(router)
    await create_tables()
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())

    except(SystemExit, KeyboardInterrupt):
        print('Bot stopped')
