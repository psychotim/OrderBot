import os
import asyncio

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import src.utils.database as db
from src.handlers import router
import logging


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    load_dotenv('.env')
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(token=os.getenv('TOKEN'))

    dp.include_router(router)

    await db.db_start()
    await dp.start_polling(bot)
    await asyncio.sleep(0)


if __name__ == '__main__':
    try:
        asyncio.run(main())

    except(SystemExit, KeyboardInterrupt):
        print('Bot stopped')
