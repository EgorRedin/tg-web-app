from database_init import Base, str_255
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger
from typing import Annotated

intpk = Annotated[int, mapped_column(autoincrement=True, primary_key=True)]

class User(Base):
    __tablename__ = "users"

    tg_id = mapped_column(BigInteger)
    balance: Mapped[intpk]
    click_size: Mapped[int]
    automainer: Mapped[int]


