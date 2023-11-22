from sqlalchemy import Integer, and_, cast, func, insert, inspect, or_, select, text, delete
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload
from aiogram.fsm.context import FSMContext

from src.db.database import Base, async_engine, async_session_factory
from src.db.models.client import AccountsData, Dates, AdminsData


class AsyncORM:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def add_item(state: FSMContext):
        async with async_session_factory() as session:
            data = await state.get_data()

            insert_data = insert(AccountsData).values(data)
            await session.execute(insert_data)
            await session.commit()

    @staticmethod
    async def write_date(state: FSMContext):
        async with async_session_factory() as session:
            data = await state.get_data()

            insert_data = insert(Dates).values(data)
            await session.execute(insert_data)
            await session.commit()

    @staticmethod
    async def get_admin_date():
        async with async_session_factory() as session:

            get_dates = select(Dates).union_all()

            res = await session.execute(get_dates)
            res_date = res.all()
            # print(f'{res_date=}')
            return res_date

    @staticmethod
    async def get_all_clients():
        async with async_session_factory() as session:
            get_clients = select(AccountsData).union_all()

            res = await session.execute(get_clients)
            res_data = res.all()
            return res_data

    @staticmethod
    async def get_all_dates():
        async with async_session_factory as session:
            get_dates = select(Dates).union_all()

            res = await session.execute(get_dates)
            res_date = res.all()
            return res_date

    @staticmethod
    async def delete_user(user_id: str):
        async with async_session_factory() as session:
            del_user = delete(AccountsData).where(AccountsData.user_id == int(user_id))
            await session.execute(del_user)
            await session.commit()

    @staticmethod
    async def delete_date(user_id: str):
        async with async_session_factory() as session:
            del_user = delete(Dates).where(Dates.user_id == int(user_id))
            await session.execute(del_user)
            await session.commit()