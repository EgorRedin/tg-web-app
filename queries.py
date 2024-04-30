from database_init import engine, Base, session_factory
from sqlalchemy import select
from models import User


class AsyncORM:

    @staticmethod
    async def create_table():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)


