import os
import asyncio

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from src.routers import router
import logging
from src.db.queries.orm import AsyncORM


async def main_db():
    await AsyncORM.create_tables()
    # await AsyncORM.get_admin_date()


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    load_dotenv('.env')
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(token=os.getenv('TOKEN'))

    dp.include_routers(router)

    # asyncio.run(syncORM.create_tables())
    await main_db()
    await dp.start_polling(bot)
    await asyncio.sleep(0)


if __name__ == '__main__':
    try:
        asyncio.run(main())

    except(SystemExit, KeyboardInterrupt):
        print('Bot stopped')
