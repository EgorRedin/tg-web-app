from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import config

engine = create_async_engine(
    url=config.database_url,
    echo=False,
)

session_factory = async_sessionmaker(engine)


class Base(DeclarativeBase):
    pass

